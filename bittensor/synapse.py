from typing import List, Tuple, Dict, Optional

import torch
import torch.nn as nn
import torch.optim as optim

import bittensor
from bittensor import bittensor_pb2
    
class Synapse(nn.Module):
    """
    """
    def __init__(self, config: bittensor.Config):
        super().__init__()
        self._config = config
        self._synapse_key = bittensor.Crypto.public_key_to_string(bittensor.Crypto.generate_private_ed25519().public_key())
        self.optimizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def to_proto(self):
        synapse_proto = bittensor_pb2.Synapse(
            version = bittensor.__version__, 
            neuron_key = self._config.neuron_key, 
            synapse_key = self.synapse_key(), 
            address = self._config.remote_ip, 
            port = self._config.axon_port, 
        )
        return synapse_proto
    
    def synapse_key(self) -> str:
        return self._synapse_key
    
    def setup_optimizer(self):
        if not self.optimizer:
            self.optimizer = optim.SGD(self.parameters(),
                          lr=0.1,
                          momentum=0.9)

    def encode_tensor(self, inputs: torch.Tensor) -> torch.Tensor:
        return NotImplementedError    
 
    def encode_image(self, inputs: torch.Tensor) -> torch.Tensor:
        return NotImplementedError    
    
    def encode_text(self, inputs: List[str]) -> torch.Tensor:
        return NotImplementedError       
    
    def call_encode(self, inputs: object, modality: bittensor_pb2.Modality) -> torch.Tensor:
        """
        Apply modality encoders.
        """
        # TODO (const catch not implemented error.)
        if modality == bittensor_pb2.Modality.TEXT:
            return self.encode_text(inputs)
        
        elif modality == bittensor_pb2.Modality.IMAGE:
            return self.encode_image(inputs)
        
        elif modality == bittensor_pb2.Modality.TENSOR:
            return self.encode_tensor(inputs)
                
        else:
            raise NotImplementedError

    
    def call_forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """
        Apply forward pass to the nn.module given inputs.
        """
        # TODO(const): check schema (inputs, input_schema)
        with torch.no_grad():
            outputs = self.forward(inputs)
        return outputs
    
    def call_backward(self, inputs: object, grads: torch.Tensor)-> torch.Tensor:
        """
        Apply a backward pass to the nn.module given grads and inputs.
        """
        # NOTE(const): removing gradient application here, needs to be replaced with gradient queueing.
        # with torch.enable_grad():
        #    outputs = self.forward(inputs)
        #    torch.autograd.backward(outputs, grad_tensors=grads.to(self.device), create_graph=False, retain_graph=False)
        #    self.apply_gradients()
        # TODO(const): check instance type.
        return torch.zeros((1,1))

    def apply_gradients(self) -> None:
        """
        Train the expert for one step.
        """
        pass
        #self.optimizer.step()
        #self.optimizer.zero_grad()
