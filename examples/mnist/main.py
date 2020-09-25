from loguru import logger

import argparse
import math
import time
import torch
import torchvision
from typing import List, Tuple, Dict, Optional

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.tensorboard import SummaryWriter
import torch.nn.functional as F

import bittensor
from bittensor import bittensor_pb2

class MnistSynapse(bittensor.Synapse):
    """ Bittensor endpoint trained on 28, 28 pixel images to detect handwritten characters.
    """
    def __init__(self, config: bittensor.Config):
        super(MnistSynapse, self).__init__(config)
        # Image encoder
        self._adaptive_pool = nn.AdaptiveAvgPool2d((28, 28))
        
        # Forward Network
        self.forward_layer1 = nn.Linear((784 + 1024), 1024)
        self.forward_layer2 = nn.Linear(1024, 1024)
        
        # Distillation Network
        self.dist_layer1 = nn.Linear(784, 1024)
        self.dist_layer2 = nn.Linear(1024, 1024)
        
        # Logit Network 
        self.logit_layer1 = nn.Linear(1024, 512)
        self.logit_layer2 = nn.Linear(512, 256)
        self.logit_layer3 = nn.Linear(256, 10)

    def distill(self, x):
        x = F.relu(self.dist_layer1 (x))
        x = F.relu(self.dist_layer2 (x))
        return x
    
    def logits (self, x):
        x = F.relu(self.logit_layer1 (x))
        x = F.relu(self.logit_layer2 (x))
        x = F.log_softmax(x)
        return x
        
    def forward (self, x, y = None):
        y = self.distill(x) if y == None else y
        x = torch.cat((x, y), dim=1)
        x = F.relu(self.forward_layer1 (x))
        x = F.relu(self.forward_layer2 (x))
        x = x # + y
        return x  
    
    def encode_image(self, inputs: List [object]) -> torch.Tensor:
        transform = torchvision.transforms.Compose([
                               torchvision.transforms.ToTensor(),
                               torchvision.transforms.Normalize(
                                 (0.1307,), (0.3081,))
                             ])
        # Apply our image transform and an adaptive pool to take all images
        # into the correct [batch_size, 784] size tensor shape. 
        image_batch = [transform(image) for image in inputs]
        image_batch = torch.cat(image_batch, dim=0)
        image_batch = self._adaptive_pool(image_batch)
        return torch.flatten(image_batch, start_dim = 1)

def main(hparams):
     
    # Load bittensor config from hparams.
    config = bittensor.Config( hparams )

    # Additional training params.
    batch_size_train = 64
    batch_size_test = 64
    learning_rate = 0.1
    momentum = 0.9
    log_interval = 10
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Log/data/model paths.
    trial_id =  'mnist-' + str(time.time()).split('.')[0]
    data_path = "data/datasets/"
    log_dir = 'data/' + trial_id + '/logs/'
    model_path = 'data/' + trial_id + '/model.torch'

    # Load (Train, Test) datasets into memory.
    training_data = torchvision.datasets.MNIST(root=data_path, train=True, download=True)
    testing_data = torchvision.datasets.MNIST(root=data_path, train=False, download=True)
    
    # Build summary writer for tensorboard.
    writer = SummaryWriter(log_dir=log_dir)
    
    # Build local synapse to serve on the network.
    model = MnistSynapse(config) # Synapses take a config object.
    model.to( device ) # Set model to device.
    
    # Build and start the metagraph background object.
    # The metagraph is responsible for connecting to the blockchain
    # and finding the other neurons on the network.
    metagraph = bittensor.Metagraph( config )
    metagraph.subscribe( model ) # Adds the synapse to the metagraph.
    metagraph.start() # Starts the metagraph gossip threads.
    
    # Build and start the Axon server.
    # The axon server serves synapse objects (models) 
    # allowing other neurons to make queries through a dendrite.
    axon = bittensor.Axon( config )
    axon.serve( model )
    axon.start() # Starts the server background threads. Must be paired with axon.stop().
    
    # Build the dendrite and router. 
    # The dendrite is a torch object which makes calls to synapses across the network
    # The router is responsible for learning which synapses to call.
    dendrite = bittensor.Dendrite( config )
    router = bittensor.Router(x_dim = 784, key_dim = 100, topk = 10)
        
    # Build the optimizer.
    params = list(router.parameters()) + list(model.parameters())
    optimizer = optim.SGD(params, lr=learning_rate, momentum=momentum)

    # Train loop: Single threaded training of MNIST.
    # 1. Makes calls to the network using the bittensor.dendrite
    # 2. Trains the local model using inputs from network + raw_features.
    # 3. Trains the distillation model to emulate network inputs.
    # 4. Trains the local model and passes gradients through the network.
    def train(model, epoch, global_step):
        # Turn on Dropoutlayers BatchNorm etc.
        model.train()
        correct = 0
        n = len(training_data)
        for batch_idx in range( int(n / batch_size_train)):
            
            # Batch the mnist dataset.
            raw_inputs = []
            targets = []
            for i in range(batch_size_train):
                idx = batch_idx * batch_size_test + i
                input_i = training_data [idx][0]
                target_i = training_data [idx][1]
                raw_inputs.append(input_i)
                targets.append(target_i)
            targets = torch.LongTensor(targets)
            
            # Clear gradients on model parameters.
            optimizer.zero_grad()
            
            # Encode PIL images to tensors.
            encoded_inputs = model.encode_image(raw_inputs).to(device)
            
            # Query the remote network.
            # Flatten mnist inputs for routing.
            synapses = metagraph.get_synapses( 1000 ) # Returns a list of synapses on the network (max 1000).
            requests, scores = router.route( synapses, encoded_inputs, raw_inputs ) # routes inputs to network.
            responses = dendrite ( synapses, requests ) # Makes network calls.
            network_input = router.join( responses ) # Joins responses based on scores..
            
            # Run distilled model.
            dist_output = model.distill(encoded_inputs.detach())
            dist_loss = F.mse_loss(dist_output, network_input.detach())
            
            # Query the local network.
            local_embedding = model.forward(encoded_inputs, network_input)
            local_logits = model.logits(local_embedding)
            target_loss = F.nll_loss(local_logits, targets)
            
            loss = (target_loss + dist_loss)
            loss.backward()
            optimizer.step()
            global_step += 1
            
            # Set network weights.
            weights = metagraph.getweights(synapses).to(device)
            weights = (0.99) * weights + 0.01 * torch.mean(scores, dim=0)
            metagraph.setweights(synapses, weights)
                
            # Logs:
            if batch_idx % log_interval == 0:
                n_peers = len(metagraph.peers)
                n_synapses = len(metagraph.synapses)
                writer.add_scalar('n_peers', n_peers, global_step)
                writer.add_scalar('n_synapses', n_synapses, global_step)
                writer.add_scalar('train_loss', float(loss.item()), global_step)
            
                n = len(training_data)
                logger.info('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\tDistill Loss: {:.6f}'.format(
                    epoch, (batch_idx * batch_size_train), n, (100. * batch_idx * batch_size_train)/n, target_loss.item(), dist_loss.item()))

    # Test loop.
    # Evaluates the local model on the hold-out set.
    # Returns the test_accuracy and test_loss.
    def test( model: bittensor.Synapse ):
        
        # Turns off Dropoutlayers, BatchNorm etc.
        model.eval()
        
        # Turns off gradient computation for inference speed up.
        with torch.no_grad():
            
            loss = 0.0
            correct = 0.0
            n = len(testing_data)
            for batch_idx in range( int(n / batch_size_train)):
            
                # we do our own batchig
                raw_inputs = []
                targets = []
                for i in range(batch_size_test):
                    idx = batch_idx * batch_size_test + i
                    input_i = testing_data [idx][0]
                    target_i = testing_data [idx][1]
                    raw_inputs.append(input_i)
                    targets.append(target_i)
                targets = torch.LongTensor(targets)
            
                # Measure loss.
                encoded_inputs = model.encode_image(raw_inputs) 
                embedding = model.forward( encoded_inputs, model.distill( encoded_inputs ))
                logits = model.logits(embedding)
                loss += F.nll_loss(logits, targets, size_average=False).item()
                
                # Count accurate predictions.
                max_logit = logits.data.max(1, keepdim=True)[1]
                correct += max_logit.eq( targets.data.view_as(max_logit) ).sum()
                
        # Log results.
        loss /= n
        accuracy = (100. * correct) / n
        logger.info('Test set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(loss, correct, n, accuracy))        
        return loss, accuracy
    
    epoch = 0
    global_step = 0
    best_test_loss = math.inf
    try:
        while True:
            # Train model
            train( model, epoch, global_step )
            
            # Test model.
            test_loss, test_accuracy = test( model )
       
            # Save best model. 
            if test_loss < best_test_loss:
                # Update best_loss.
                best_test_loss = test_loss
                
                # Save the best local model.
                logger.info('Saving model: epoch: {}, loss: {}, path: {}', model_path, epoch, test_loss)
                torch.save({'epoch': epoch, 'model': model.state_dict(), 'test_loss': test_loss}, model_path)
                
            epoch += 1
            
    except Exception as e:
        logger.error(e)
        metagraph.stop()
        axon.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    hparams = bittensor.Config.add_args(parser)
    hparams = parser.parse_args()
    main(hparams)
