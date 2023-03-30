## AI21 Miner
AI21 Language Model Serving with BitTensor
This code is for running a language model powered by AI21 through the BitTensor framework. 

# Example Usage
```
python3 -m pip install -r neurons/text/prompting/miners/AI21/requirements.txt 
python3 neurons/text/prompting/miners/AI21/miner.py --neuron.api_key <your AI21 api_key>
```

# Full Usage
```
usage: miner.py [-h] [--netuid NETUID] [--config CONFIG] [--neuron.model_name NEURON.MODEL_NAME] [--neuron.name NEURON.NAME] [--neuron.temperature NEURON.TEMPERATURE] [--neuron.max_tokens NEURON.MAX_TOKENS]
                [--neuron.min_tokens NEURON.MIN_TOKENS] [--neuron.top_p NEURON.TOP_P] [--neuron.presence_penalty NEURON.PRESENCE_PENALTY] [--neuron.count_penalty NEURON.COUNT_PENALTY] [--neuron.frequency_penalty NEURON.FREQUENCY_PENALTY]
                [--neuron.num_results NEURON.NUM_RESULTS] [--neuron.logit_bias NEURON.LOGIT_BIAS] [--neuron.stop NEURON.STOP] [--neuron.base_url NEURON.BASE_URL] [--neuron.api_key NEURON.API_KEY] [--wallet.name WALLET.NAME]
                [--wallet.hotkey WALLET.HOTKEY] [--wallet.path WALLET.PATH] [--wallet._mock] [--wallet.reregister WALLET.REREGISTER] [--axon.priority.max_workers AXON.PRIORITY.MAX_WORKERS] [--axon.priority.maxsize AXON.PRIORITY.MAXSIZE]
                [--axon.port AXON.PORT] [--axon.ip AXON.IP] [--axon.external_port AXON.EXTERNAL_PORT] [--axon.external_ip AXON.EXTERNAL_IP] [--axon.max_workers AXON.MAX_WORKERS]
                [--axon.maximum_concurrent_rpcs AXON.MAXIMUM_CONCURRENT_RPCS] [--subtensor.network SUBTENSOR.NETWORK] [--subtensor.chain_endpoint SUBTENSOR.CHAIN_ENDPOINT] [--subtensor._mock]
                [--subtensor.register.num_processes SUBTENSOR.REGISTER.NUM_PROCESSES] [--subtensor.register.update_interval SUBTENSOR.REGISTER.UPDATE_INTERVAL] [--subtensor.register.no_output_in_place] [--subtensor.register.verbose]
                [--subtensor.register.cuda.use_cuda] [--subtensor.register.cuda.no_cuda] [--subtensor.register.cuda.dev_id SUBTENSOR.REGISTER.CUDA.DEV_ID [SUBTENSOR.REGISTER.CUDA.DEV_ID ...]]
                [--subtensor.register.cuda.TPB SUBTENSOR.REGISTER.CUDA.TPB] [--logging.debug] [--logging.trace] [--logging.record_log] [--logging.logging_dir LOGGING.LOGGING_DIR] [--metagraph._mock] [--strict]

optional arguments:
  -h, --help            show this help message and exit
  --netuid NETUID       Subnet netuid
  --config CONFIG       If set, defaults are overridden by passed file.
  --neuron.model_name NEURON.MODEL_NAME
                        Name of the model.
  --neuron.name NEURON.NAME
                        Name of the neuron.
  --neuron.temperature NEURON.TEMPERATURE
                        Sampling temperature.
  --neuron.max_tokens NEURON.MAX_TOKENS
                        Maximum number of tokens to generate.
  --neuron.min_tokens NEURON.MIN_TOKENS
                        Minimum number of tokens to generate.
  --neuron.top_p NEURON.TOP_P
                        Total probability mass of tokens to consider at each step.
  --neuron.presence_penalty NEURON.PRESENCE_PENALTY
                        Penalizes repeated tokens.
  --neuron.count_penalty NEURON.COUNT_PENALTY
                        Penalizes repeated tokens according to count.
  --neuron.frequency_penalty NEURON.FREQUENCY_PENALTY
                        Penalizes repeated tokens according to frequency.
  --neuron.num_results NEURON.NUM_RESULTS
                        How many completions to generate for each prompt.
  --neuron.logit_bias NEURON.LOGIT_BIAS
                        Adjust the probability of specific tokens being generated.
  --neuron.stop NEURON.STOP
                        Stop tokens.
  --neuron.base_url NEURON.BASE_URL
                        Base url to use, if None decides based on model name.
  --neuron.api_key NEURON.API_KEY
                        AI21 API key.
  --wallet.name WALLET.NAME
                        The name of the wallet to unlock for running bittensor (name mock is reserved for mocking this wallet)
  --wallet.hotkey WALLET.HOTKEY
                        The name of wallet's hotkey.
  --wallet.path WALLET.PATH
                        The path to your bittensor wallets
  --wallet._mock        To turn on wallet mocking for testing purposes.
  --wallet.reregister WALLET.REREGISTER
                        Whether to reregister the wallet if it is not already registered.
  --axon.priority.max_workers AXON.PRIORITY.MAX_WORKERS
                        maximum number of threads in thread pool
  --axon.priority.maxsize AXON.PRIORITY.MAXSIZE
                        maximum size of tasks in priority queue
  --axon.port AXON.PORT
                        The local port this axon endpoint is bound to. i.e. 8091
  --axon.ip AXON.IP     The local ip this axon binds to. ie. [::]
  --axon.external_port AXON.EXTERNAL_PORT
                        The public port this axon broadcasts to the network. i.e. 8091
  --axon.external_ip AXON.EXTERNAL_IP
                        The external ip this axon broadcasts to the network to. ie. [::]
  --axon.max_workers AXON.MAX_WORKERS
                        The maximum number connection handler threads working simultaneously on this endpoint. The grpc server distributes new worker threads to service requests up to this number.
  --axon.maximum_concurrent_rpcs AXON.MAXIMUM_CONCURRENT_RPCS
                        Maximum number of allowed active connections
  --subtensor.network SUBTENSOR.NETWORK
                        The subtensor network flag. The likely choices are: -- finney (main network) -- local (local running network) -- mock (creates a mock connection (for testing)) If this option is set it overloads
                        subtensor.chain_endpoint with an entry point node from that network.
  --subtensor.chain_endpoint SUBTENSOR.CHAIN_ENDPOINT
                        The subtensor endpoint flag. If set, overrides the --network flag.
  --subtensor._mock     To turn on subtensor mocking for testing purposes.
  --subtensor.register.num_processes SUBTENSOR.REGISTER.NUM_PROCESSES, -n SUBTENSOR.REGISTER.NUM_PROCESSES
                        Number of processors to use for registration
  --subtensor.register.update_interval SUBTENSOR.REGISTER.UPDATE_INTERVAL, --subtensor.register.cuda.update_interval SUBTENSOR.REGISTER.UPDATE_INTERVAL, --cuda.update_interval SUBTENSOR.REGISTER.UPDATE_INTERVAL, -u SUBTENSOR.REGISTER.UPDATE_INTERVAL
                        The number of nonces to process before checking for next block during registration
  --subtensor.register.no_output_in_place, --no_output_in_place
                        Whether to not ouput the registration statistics in-place. Set flag to disable output in-place.
  --subtensor.register.verbose
                        Whether to ouput the registration statistics verbosely.
  --subtensor.register.cuda.use_cuda, --cuda, --cuda.use_cuda
                        Set flag to use CUDA to register.
  --subtensor.register.cuda.no_cuda, --no_cuda, --cuda.no_cuda
                        Set flag to not use CUDA for registration
  --subtensor.register.cuda.dev_id SUBTENSOR.REGISTER.CUDA.DEV_ID [SUBTENSOR.REGISTER.CUDA.DEV_ID ...], --cuda.dev_id SUBTENSOR.REGISTER.CUDA.DEV_ID [SUBTENSOR.REGISTER.CUDA.DEV_ID ...]
                        Set the CUDA device id(s). Goes by the order of speed. (i.e. 0 is the fastest).
  --subtensor.register.cuda.TPB SUBTENSOR.REGISTER.CUDA.TPB, --cuda.TPB SUBTENSOR.REGISTER.CUDA.TPB
                        Set the number of Threads Per Block for CUDA.
  --logging.debug       Turn on bittensor debugging information
  --logging.trace       Turn on bittensor trace level information
  --logging.record_log  Turns on logging to file.
  --logging.logging_dir LOGGING.LOGGING_DIR
                        Logging default root directory.
  --metagraph._mock     To turn on metagraph mocking for testing purposes.
  --strict              If flagged, config will check that only exact arguemnts have been set.
```