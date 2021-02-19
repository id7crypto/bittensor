import bittensor
import pytest
from munch import Munch

def test_create():
    subtensor = bittensor.subtensor.Subtensor()

def test_defaults_to_akira( ):
    subtensor = bittensor.subtensor.Subtensor()
    assert subtensor.endpoint_for_network() in bittensor.__akira_entrypoints__

def test_endpoint_overides():
    subtensor = bittensor.subtensor.Subtensor()
    subtensor.config.subtensor.chain_endpoint = "this is the endpoint"
    assert subtensor.endpoint_for_network() == "this is the endpoint"

def test_networks():
    subtensor = bittensor.subtensor.Subtensor()
    subtensor.config.subtensor.network = 'akira'
    assert subtensor.endpoint_for_network()  in bittensor.__akira_entrypoints__
    subtensor.config.subtensor.network = 'boltzmann'
    assert subtensor.endpoint_for_network()  in bittensor.__boltzmann_entrypoints__
    subtensor.config.subtensor.network = 'kusanagi'
    assert subtensor.endpoint_for_network() in bittensor.__kusanagi_entrypoints__

def test_connect_failure( ):
    subtensor = bittensor.subtensor.Subtensor()
    subtensor.config.subtensor.chain_endpoint = "this is the endpoint"
    with pytest.raises(RuntimeError):
        subtensor.connect(timeout = 1)

def test_connect_no_failure( ):
    subtensor = bittensor.subtensor.Subtensor()
    subtensor.config.subtensor.chain_endpoint = "this is the endpoint"
    subtensor.connect(timeout = 1, failure=False)

config = bittensor.subtensor.Subtensor.build_config()
config.network = 'boltzmann'
subtensor = bittensor.subtensor.Subtensor( config )

def test_connect_success( ):
    subtensor.connect()

def test_neurons( ):
    neurons = subtensor.neurons()
    assert len(neurons) > 0
    assert type(neurons[0][0]) == int
    assert type(neurons[0][1]['ip']) == int
    assert type(neurons[0][1]['port']) == int
    assert type(neurons[0][1]['ip_type']) == int
    assert type(neurons[0][1]['uid']) == int
    assert type(neurons[0][1]['modality']) == int
    assert type(neurons[0][1]['hotkey']) == str
    assert type(neurons[0][1]['coldkey']) == str

    neuron = subtensor.get_neuron_for_uid( 0 )
    assert neurons[0][1]['ip'] == neuron['ip']
    assert neurons[0][1]['port'] == neuron['port']
    assert neurons[0][1]['ip_type'] == neuron['ip_type']
    assert neurons[0][1]['uid'] == neuron['uid']
    assert neurons[0][1]['modality'] == neuron['modality']
    assert neurons[0][1]['hotkey'] == neuron['hotkey']
    assert neurons[0][1]['coldkey'] == neuron['coldkey']

def test_uid_for_public_key( ):
    assert subtensor.get_uid_for_pubkey("0x2ebbc6812171f4cff93927319ccda80cc3101fb5dbc283821d1ff9cede03893d") == 0

def test_stake( ):
    assert(type(subtensor.get_stake_for_uid(0)) == bittensor.utils.balance.Balance)

def test_weight_uids( ):
    weight_uids = subtensor.weight_uids_for_uid(0)
    assert(type(weight_uids) == list)
    assert(type(weight_uids[0]) == int)

def test_weight_vals( ):
    weight_vals = subtensor.weight_vals_for_uid(0)
    assert(type(weight_vals) == list)
    assert(type(weight_vals[0]) == int)

def test_last_emit( ):
    last_emit = subtensor.get_last_emit_data_for_uid(0)
    assert(type(last_emit) == int)