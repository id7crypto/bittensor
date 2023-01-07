# The MIT License (MIT)
# Copyright © 2021 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

import os
import sys
from typing import List, Union, Optional, Dict, Tuple

from cachetools import Cache

import bittensor
from bittensor.utils.balance import Balance
from fuzzywuzzy import fuzz
from rich import print
from rich.prompt import Confirm
from rich.table import Table
from rich.tree import Tree
from rich.align import Align
from tqdm import tqdm


class CLI:
    """
    Implementation of the CLI class, which handles the coldkey, hotkey and money transfer 
    """
    def __init__(self, config: 'bittensor.Config' ):
        r""" Initialized a bittensor.CLI object.
            Args:
                config (:obj:`bittensor.Config`, `required`): 
                    bittensor.cli.config()
        """
        # (d)efaults to True if config.no_version_checking is not set.
        if not config.get("no_version_checking", d=True):
            try:
                bittensor.utils.version_checking()
            except:
                raise RuntimeError("To avoid internet based version checking pass --no_version_checking while running the CLI.")
        self.config = config

    def run ( self ):
        """ Execute the command from config 
        """
        if self.config.command == "run":
            self.run_miner ()
        elif self.config.command == "transfer":
            self.transfer ()
        elif self.config.command == "register":
            self.register()
        elif self.config.command == "unstake":
            self.unstake()
        elif self.config.command == "stake":
            self.stake()
        elif self.config.command == "overview":
            self.overview()
        elif self.config.command == "list":
            self.list()
        elif self.config.command == "new_coldkey":
            self.create_new_coldkey()
        elif self.config.command == "new_hotkey":
            self.create_new_hotkey()
        elif self.config.command == "regen_coldkey":
            self.regen_coldkey()
        elif self.config.command == "regen_coldkeypub":
            self.regen_coldkeypub()
        elif self.config.command == "regen_hotkey":
            self.regen_hotkey()
        elif self.config.command == "metagraph":
            self.metagraph()
        elif self.config.command == "weights":
            self.weights()
        elif self.config.command == "set_weights":
            self.set_weights()
        elif self.config.command == "inspect":
            self.inspect()
        elif self.config.command == "query":
            self.query()
        elif self.config.command == "help":
            self.help()
        elif self.config.command == 'update':
            self.update()
        elif self.config.command == 'become_delegate':
            self.become_delegate()
        elif self.config.command == 'list_delegates':
            self.list_delegates()
        elif self.config.command == 'list_subnets':
            self.list_subnets()


    def list_delegates( self ) -> None:
        r"""
        List all delegates on the network.
        """
        subtensor = bittensor.subtensor( config = self.config )
        delegates: bittensor.DelegateInfo = subtensor.get_delegates()

        table = Table(show_footer=True, width=self.config.get('width', None), pad_edge=False, box=None)
        table.add_column("[overline white]DELEGATE",  str(len(delegates)), footer_style = "overline white", style='bold white')
        table.add_column("[overline white]TAKE", style='white')
        table.add_column("[overline white]OWNER", style='yellow')
        table.add_column("[overline white]NOMINATORS", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]TOTAL STAKE(\u03C4)", justify='right', style='green', no_wrap=True)

        for delegate in delegates:
            table.add_row(
                str(delegate.hotkey_ss58),
                str(delegate.take),
                str(delegate.owner_ss58),
                str(len(delegate.nominators)),
                str(delegate.total_stake),
            )
        bittensor.__console__.print(table)

    def become_delegate( self ) -> None:
        r""" Become a delegate.
        """
        wallet = bittensor.wallet(config = self.config)
        subtensor = bittensor.subtensor( config = self.config )

        # Unlock the wallet.
        wallet.hotkey
        wallet.coldkey

        result: bool = subtensor.become_delegate( wallet )

        if not result:
            bittensor.__console__.print("Could not became a delegate on [white]{}[/white]".format(subtensor.network))
        else:
            # Check if we are a delegate.
            is_delegate: bool = subtensor.is_hotkey_delegate( wallet.hotkey.ss58_address )
            if not is_delegate:
                bittensor.__console__.print("Could not became a delegate on [white]{}[/white]".format(subtensor.network))
                return

            bittensor.__console__.print("Successfully became a delegate on [white]{}[/white]".format(subtensor.network))


    def create_new_coldkey ( self ):
        r""" Creates a new coldkey under this wallet.
        """
        wallet = bittensor.wallet(config = self.config)
        wallet.create_new_coldkey( n_words = self.config.n_words, use_password = self.config.use_password, overwrite = self.config.overwrite_coldkey)   

    def create_new_hotkey ( self ):
        r""" Creates a new hotke under this wallet.
        """
        wallet = bittensor.wallet(config = self.config)
        wallet.create_new_hotkey( n_words = self.config.n_words, use_password = self.config.use_password, overwrite = self.config.overwrite_hotkey)   

    def regen_coldkey ( self ):
        r""" Creates a new coldkey under this wallet.
        """
        wallet = bittensor.wallet(config = self.config)
        wallet.regenerate_coldkey( mnemonic = self.config.mnemonic, seed = self.config.seed, use_password = self.config.use_password, overwrite = self.config.overwrite_coldkey )

    def regen_coldkeypub ( self ):
        r""" Creates a new coldkeypub under this wallet.
        """
        wallet = bittensor.wallet(config = self.config)
        wallet.regenerate_coldkeypub( ss58_address=self.config.get('ss58_address'), public_key=self.config.get('public_key_hex'), overwrite = self.config.overwrite_coldkeypub )

    def regen_hotkey ( self ):
        r""" Creates a new coldkey under this wallet.
        """
        wallet = bittensor.wallet(config = self.config)
        wallet.regenerate_hotkey( mnemonic = self.config.mnemonic, seed=self.config.seed, use_password = self.config.use_password, overwrite = self.config.overwrite_hotkey)

    def query ( self ):
        r""" Query an endpoint and get query time.
        """
        wallet = bittensor.wallet(config = self.config)
        subtensor = bittensor.subtensor( config = self.config )

        # Verify subnet exists
        if not subtensor.subnet_exists( netuid = self.config.netuid ):
            bittensor.__console__.print(f"[red]Subnet {self.config.netuid} does not exist[/red]")
            sys.exit(1)

        dendrite = bittensor.dendrite( wallet = wallet )
        stats = {}
        for uid in self.config.uids:
            neuron = subtensor.neuron_for_uid( uid = uid, netuid = self.config.netuid )
            endpoint = bittensor.endpoint.from_neuron( neuron )
            _, c, t = dendrite.forward_text( endpoints = endpoint, inputs = 'hello world')
            latency = "{}".format(t.tolist()[0]) if c.tolist()[0] == 1 else 'N/A'
            bittensor.__console__.print("\tUid: [bold white]{}[/bold white]\n\tLatency: [bold white]{}[/bold white]\n\tCode: [bold {}]{}[/bold {}]\n\n".format(uid, latency, bittensor.utils.codes.code_to_loguru_color( c.item() ), bittensor.utils.codes.code_to_string( c.item() ), bittensor.utils.codes.code_to_loguru_color( c.item() )), highlight=True)
            stats[uid] = latency
        print (stats)

    def inspect ( self ):
        r""" Inspect a cold, hot pair.
        """
        wallet = bittensor.wallet(config = self.config)
        subtensor = bittensor.subtensor( config = self.config )

        if self.config.netuid != None:
            # Verify subnet exists
            if not subtensor.subnet_exists( netuid = self.config.netuid ):
                bittensor.__console__.print(f"[red]Subnet {self.config.netuid} does not exist[/red]")
                sys.exit(1)

            
        with bittensor.__console__.status(":satellite: Looking up account on: [white]{}[/white] ...".format(self.config.subtensor.get('network', bittensor.defaults.subtensor.network))):
            
            if self.config.wallet.get('hotkey', bittensor.defaults.wallet.hotkey) is None:
                # If no hotkey is provided, inspect just the coldkey
                wallet.coldkeypub
                cold_balance = wallet.get_balance( subtensor = subtensor )
                bittensor.__console__.print("\n[bold white]{}[/bold white]:\n  {}[bold white]{}[/bold white]\n {} {}\n".format( wallet, "coldkey:".ljust(15), wallet.coldkeypub.ss58_address, " balance:".ljust(15), cold_balance.__rich__()), highlight=True)

            else:
                wallet.hotkey
                wallet.coldkeypub

                if self.config.netuid != None:
                    # If a netuid is provided, inspect the hotkey and the neuron
                    dendrite = bittensor.dendrite( wallet = wallet )
                    neuron = subtensor.neuron_for_pubkey( ss58_hotkey = wallet.hotkey.ss58_address, netuid = self.config.netuid )
                    endpoint = bittensor.endpoint.from_neuron( neuron )
                    if neuron.is_null:
                        registered = '[bold white]No[/bold white]'
                        stake = bittensor.Balance.from_tao( 0 )
                        emission = bittensor.Balance.from_rao( 0 )
                        latency = 'N/A'
                    else:
                        registered = '[bold white]Yes[/bold white]'
                        stake = bittensor.Balance.from_tao( neuron.stake )
                        emission = bittensor.Balance.from_rao( neuron.emission * 1000000000 )
                        synapses = [bittensor.synapse.TextLastHiddenState()]
                        _, c, t = dendrite.text( endpoints = endpoint, inputs = 'hello world', synapses=synapses)
                        latency = "{}".format((t[0]).tolist()[0]) if (c[0]).tolist()[0] == 1 else 'N/A'

                    cold_balance = wallet.get_balance( subtensor = subtensor )
                    bittensor.__console__.print((
                        "\n[bold white]{}[/bold white]:\n  [bold grey]{}[bold white]{}[/bold white]\n" + \
                        "  {}[bold white]{}[/bold white]\n  {}{}\n  {}{}\n  {}{}\n  {}{}\n  {}{}[/bold grey]"
                    )
                    .format(
                        wallet,
                        "coldkey:".ljust(15),
                        wallet.coldkeypub.ss58_address,
                        "hotkey:".ljust(15),
                        wallet.hotkey.ss58_address,
                        "registered:".ljust(15),
                        registered,
                        "balance:".ljust(15),
                        cold_balance.__rich__(),
                        "stake:".ljust(15),
                        stake.__rich__(),
                        "emission:".ljust(15),
                        emission.__rich_rao__(),
                        "latency:".ljust(15),
                        latency 
                    ), highlight=True)
                else:
                    # Otherwise, print all subnets the hotkey is registered on.
                    # If a netuid is provided, inspect the hotkey and the neuron
                    stake = subtensor.get_stake_for_coldkey_and_hotkey( hotkey_ss58 = wallet.hotkey.ss58_address, coldkey_ss58 = wallet.coldkeypub.ss58_address )
                    if stake == None:
                        # Not registered on any subnets
                        subnets = "[bold white][][/bold white]"
                        stake = bittensor.Balance.from_tao( 0 )
                    else:
                        # Registered on subnets
                        subnets_registered = subtensor.get_netuids_for_hotkey( ss58_hotkey = wallet.hotkey.ss58_address )
                        subnets = f'[bold white]{subnets_registered}[/bold white]'
                        
                        emission = bittensor.Balance.from_rao( 0 )
                        for netuid in subnets_registered:
                            neuron = subtensor.neuron_for_pubkey( ss58_hotkey = wallet.hotkey.ss58_address, netuid = netuid )
                            emission += bittensor.Balance.from_rao( neuron.emission * 1000000000 )

                    cold_balance = wallet.get_balance( subtensor = subtensor )
                    bittensor.__console__.print((
                        "\n[bold white]{}[/bold white]:\n  [bold grey]{}[bold white]{}[/bold white]\n" + \
                        "  {}[bold white]{}[/bold white]\n  {}{}\n  {}{}\n  {}{}\n  {}{}\n  {}{}[/bold grey]"
                    )
                    .format(
                        wallet,
                        "coldkey:".ljust(15),
                        wallet.coldkeypub.ss58_address,
                        "hotkey:".ljust(15),
                        wallet.hotkey.ss58_address,
                        "subnets:".ljust(15),
                        subnets,
                        "balance:".ljust(15),
                        cold_balance.__rich__(),
                        "stake:".ljust(15),
                        stake.__rich__(),
                        "emission:".ljust(15),
                        emission.__rich_rao__(),
                    ), highlight=True)


    def run_miner ( self ):
        self.config.to_defaults()

        subtensor = bittensor.subtensor( config = self.config )

        # Verify subnet exists
        if not subtensor.subnet_exists( netuid = self.config.netuid ):
            bittensor.__console__.print(f"[red]Subnet {self.config.netuid} does not exist[/red]")
            sys.exit(1)

        # Check coldkey.
        wallet = bittensor.wallet( config = self.config )
        if not wallet.coldkeypub_file.exists_on_device():
            if Confirm.ask("Coldkey: [bold]'{}'[/bold] does not exist, do you want to create it".format(self.config.wallet.get('name', bittensor.defaults.wallet.name))):
                wallet.create_new_coldkey()
            else:
                sys.exit()

        # Check hotkey.
        if not wallet.hotkey_file.exists_on_device():
            if Confirm.ask("Hotkey: [bold]'{}'[/bold] does not exist, do you want to create it".format(self.config.wallet.hotkey)):
                wallet.create_new_hotkey()
            else:
                sys.exit()

        if wallet.hotkey_file.is_encrypted():
            bittensor.__console__.print("Decrypting hotkey ... ")
        wallet.hotkey

        if wallet.coldkeypub_file.is_encrypted():
            bittensor.__console__.print("Decrypting coldkeypub ... ")
        wallet.coldkeypub

        # Check registration
        ## Will exit if --wallet.reregister is False
        wallet.reregister( netuid = self.config.netuid )

        # Run miner.
        if self.config.model == 'core_server':
            
            if self.config.synapse == 'TextLastHiddenState':
                bittensor.neurons.core_server.neuron(lasthidden=True, causallm=False, seq2seq = False).run()
            elif self.config.synapse == 'TextCausalLM':
                bittensor.neurons.core_server.neuron(lasthidden=False, causallm=True, seq2seq = False).run()
            elif self.config.synapse == 'TextSeq2Seq':
                bittensor.neurons.core_server.neuron(lasthidden=False, causallm=False, seq2seq = True).run()
            else:
                bittensor.neurons.core_server.neuron().run()

        elif self.config.model == 'core_validator':
            bittensor.neurons.core_validator.neuron().run()
        elif self.config.model == 'multitron_server':
            bittensor.neurons.multitron_server.neuron().run()

    def help ( self ):
        self.config.to_defaults()

        sys.argv = [sys.argv[0], '--help']

        # Run miner.
        if self.config.model == 'core_server':
            bittensor.neurons.core_server.neuron().run()
        elif self.config.model == 'core_validator':
            bittensor.neurons.core_validator.neuron().run()
        elif self.config.model == 'multitron_server':
            bittensor.neurons.multitron_server.neuron().run()


    def update ( self ):
        if self.config.no_prompt or self.config.answer == 'Y':
            os.system(' (cd ~/.bittensor/bittensor/ ; git checkout master ; git pull --ff-only )')
            os.system('pip install -e ~/.bittensor/bittensor/')

    def register( self ):
        r""" Register neuron.
        """
        wallet = bittensor.wallet( config = self.config )
        subtensor = bittensor.subtensor( config = self.config )

        # Verify subnet exists
        if not subtensor.subnet_exists( netuid = self.config.netuid ):
            bittensor.__console__.print(f"[red]Subnet {self.config.netuid} does not exist[/red]")
            sys.exit(1)

        subtensor.register(
            wallet = wallet,
            netuid = self.config.netuid,
            prompt = not self.config.no_prompt,
            TPB = self.config.subtensor.register.cuda.get('TPB', None),
            update_interval = self.config.subtensor.register.get('update_interval', None),
            num_processes = self.config.subtensor.register.get('num_processes', None),
            cuda = self.config.subtensor.register.cuda.get('use_cuda', bittensor.defaults.subtensor.register.cuda.use_cuda),
            dev_id = self.config.subtensor.register.cuda.get('dev_id', None),
            output_in_place = self.config.subtensor.register.get('output_in_place', bittensor.defaults.subtensor.register.output_in_place),
            log_verbose = self.config.subtensor.register.get('verbose', bittensor.defaults.subtensor.register.verbose),
        )

    def transfer( self ):
        r""" Transfer token of amount to destination.
        """
        wallet = bittensor.wallet( config = self.config )
        subtensor = bittensor.subtensor( config = self.config )
        subtensor.transfer( wallet = wallet, dest = self.config.dest, amount = self.config.amount, wait_for_inclusion = True, prompt = not self.config.no_prompt )

    def unstake( self ):
        r""" Unstake token of amount from hotkey(s).
        """        
        # TODO: allow delegate unstake
        config = self.config.copy()
        config.hotkey = None
        wallet = bittensor.wallet( config = self.config )

        subtensor: bittensor.subtensor = bittensor.subtensor( config = self.config )

        wallets_to_unstake_from: List[bittensor.wallet]
        if self.config.wallet.get('all_hotkeys'):
            # Unstake from all hotkeys.
            all_hotkeys: List[bittensor.wallet] = self._get_hotkey_wallets_for_wallet( wallet = wallet )
            # Exclude hotkeys that are specified.
            wallets_to_unstake_from = [
                wallet for wallet in all_hotkeys if wallet.hotkey_str not in self.config.wallet.get('hotkeys', [])
            ]

        elif self.config.wallet.get('hotkeys'):
            # Unstake from specific hotkeys.
            wallets_to_unstake_from = [
                bittensor.wallet( config = self.config, hotkey = hotkey ) for hotkey in self.config.wallet.get('hotkeys')
            ]
        else:
            # Do regular unstake
            subtensor.unstake( wallet, amount = None if self.config.get('unstake_all') else self.config.get('amount'), wait_for_inclusion = True, prompt = not self.config.no_prompt )
            return None

        

        final_wallets: List['bittensor.wallet'] = [] 
        final_amounts: List[Union[float, Balance]] = []
        for wallet in tqdm(wallets_to_unstake_from):
            wallet: bittensor.wallet
            if not wallet.is_registered(): # must be registered on any subnet.
                # Skip unregistered hotkeys.
                continue

            unstake_amount_tao: float = self.config.get('amount')
            if self.config.get('max_stake'):
                wallet_stake: Balance = wallet.get_stake()
                unstake_amount_tao: float = wallet_stake.tao - self.config.get('max_stake')   
                self.config.amount = unstake_amount_tao  
                if unstake_amount_tao < 0:
                    # Skip if max_stake is greater than current stake.
                    continue
                    
            final_wallets.append(wallet)
            final_amounts.append(unstake_amount_tao)

        # Ask to unstake
        if not self.config.no_prompt:
            if not Confirm.ask("Do you want to unstake from the following keys:\n" + \
                    "".join([
                        f"    [bold white]- {wallet.hotkey_str}: {amount}𝜏[/bold white]\n" for wallet, amount in zip(final_wallets, final_amounts)
                    ])
                ):
                return None
                
        subtensor.unstake_multiple( wallet = final_wallets[0], hotkey_ss58s=[wallet.hotkey.ss58_address for wallet in final_wallets], amounts = None if self.config.get('unstake_all') else final_amounts, wait_for_inclusion = True, prompt = False )


    def stake( self ):
        r""" Stake token of amount to hotkey(s).
        """
        # TODO: allow delegate stake
        config = self.config.copy()
        config.hotkey = None
        wallet = bittensor.wallet( config = config )

        subtensor: bittensor.subtensor = bittensor.subtensor( config = self.config )

        wallets_to_stake_to: List[bittensor.wallet]
        if self.config.wallet.get('all_hotkeys'):
            # Stake to all hotkeys.
            all_hotkeys: List[bittensor.wallet] = self._get_hotkey_wallets_for_wallet( wallet = wallet )
            # Exclude hotkeys that are specified.
            wallets_to_stake_to = [
                wallet for wallet in all_hotkeys if wallet.hotkey_str not in self.config.wallet.get('hotkeys', [])
            ]

        elif self.config.wallet.get('hotkeys'):
            # Stake to specific hotkeys.
            wallets_to_stake_to = [
                bittensor.wallet( config = self.config, hotkey = hotkey ) for hotkey in self.config.wallet.get('hotkeys')
            ]
        else:
            # Only self.config.wallet.hotkey is specified.
            #  so we stake to that single hotkey.
            assert self.config.wallet.hotkey is not None
            wallets_to_stake_to = [ bittensor.wallet( config = self.config ) ]
           
        # Otherwise we stake to multiple wallets

        wallet_0: 'bittensor.wallet' = wallets_to_stake_to[0]
        # Decrypt coldkey for all wallet(s) to use
        wallet_0.coldkey

        # Get coldkey balance
        wallet_balance: Balance = wallet_0.get_balance()
        final_wallets: List['bittensor.wallet'] = [] 
        final_amounts: List[Union[float, Balance]] = []
        for wallet in tqdm(wallets_to_stake_to):
            wallet: bittensor.wallet            
            if not wallet.is_registered(): # must be registered on any subnet.
                # Skip unregistered hotkeys.
                continue
            
            # Assign decrypted coldkey from wallet_0
            #  so we don't have to decrypt again
            wallet._coldkey = wallet_0._coldkey

            stake_amount_tao: float = self.config.get('amount')
            if self.config.get('max_stake'):
                wallet_stake: Balance = wallet.get_stake()
                stake_amount_tao: float = self.config.get('max_stake') - wallet_stake.tao

                # If the max_stake is greater than the current wallet balance, stake the entire balance.
                stake_amount_tao: float = min(stake_amount_tao, wallet_balance.tao)
                if stake_amount_tao <= 0.00001: # Threshold because of fees, might create a loop otherwise
                    # Skip hotkey if max_stake is less than current stake.
                    continue
                wallet_balance = Balance.from_tao(wallet_balance.tao - stake_amount_tao)
            final_amounts.append(stake_amount_tao)
            final_wallets.append(wallet)

        if len(final_wallets) == 0:
            # No wallets to stake to.
            bittensor.__console__.print("Not enough balance to stake to any hotkeys or max_stake is less than current stake.")
            return None

        # Ask to stake
        if not self.config.no_prompt:
            if not Confirm.ask(f"Do you want to stake to the following keys from {wallet_0.name}:\n" + \
                    "".join([
                        f"    [bold white]- {wallet.hotkey_str}: {amount}𝜏[/bold white]\n" for wallet, amount in zip(final_wallets, final_amounts)
                    ])
                ):
                return None
        
        if len(final_wallets) == 1:
            # do regular stake
            return subtensor.add_stake( wallet=final_wallets[0], amount = None if self.config.get('stake_all') else final_amounts[0], wait_for_inclusion = True, prompt = not self.config.no_prompt )

        subtensor.add_stake_multiple( wallet = final_wallets[0], hotkey_ss58s=[wallet.hotkey.ss58_address for wallet in final_wallets], amounts =  None if self.config.get('stake_all') else final_amounts, wait_for_inclusion = True, prompt = False )


    def set_weights( self ):
        r""" Set weights and uids on chain.
        """
        wallet = bittensor.wallet( config = self.config )
        subtensor = bittensor.subtensor( config = self.config )

        # Verify subnet exists
        if not subtensor.subnet_exists( netuid = self.config.netuid ):
            bittensor.__console__.print(f"[red]Subnet {self.config.netuid} does not exist[/red]")
            sys.exit(1)

        # Get version key TODO
        version_key: int = bittensor.__version_as_int__
        
        subtensor.set_weights( 
            wallet, 
            uids = self.config.uids,
            netuid = self.config.netuid,
            weights = self.config.weights,
            version_key = version_key,
            wait_for_inclusion = True, 
            prompt = not self.config.no_prompt 
        )

    @staticmethod
    def _get_hotkey_wallets_for_wallet( wallet ) -> List['bittensor.wallet']:
        hotkey_wallets = []
        hotkeys_path = wallet.path + '/' + wallet.name + '/hotkeys'
        try:
            hotkey_files = next(os.walk(os.path.expanduser(hotkeys_path)))[2]
        except StopIteration:
            hotkey_files = []
        for hotkey_file_name in hotkey_files:
            try:
                hotkey_for_name = bittensor.wallet( path = wallet.path, name = wallet.name, hotkey = hotkey_file_name )
                if hotkey_for_name.hotkey_file.exists_on_device() and not hotkey_for_name.hotkey_file.is_encrypted():
                    hotkey_wallets.append( hotkey_for_name )
            except Exception:
                pass
        return hotkey_wallets

    @staticmethod
    def _get_coldkey_wallets_for_path( path: str ) -> List['bittensor.wallet']:
        try:
            wallet_names = next(os.walk(os.path.expanduser(path)))[1]
            return [ bittensor.wallet( path= path, name=name ) for name in wallet_names ]
        except StopIteration:
            # No wallet files found.
            wallets = []
        return wallets

    @staticmethod
    def _get_all_wallets_for_path( path:str ) -> List['bittensor.wallet']:
        all_wallets = []
        cold_wallets = CLI._get_coldkey_wallets_for_path(path)
        for cold_wallet in cold_wallets:
            if cold_wallet.coldkeypub_file.exists_on_device() and not cold_wallet.coldkeypub_file.is_encrypted():
                all_wallets.extend( CLI._get_hotkey_wallets_for_wallet(cold_wallet) )
        return all_wallets

    def list(self):
        r""" Lists wallets.
        """
        try:
            wallets = next(os.walk(os.path.expanduser(self.config.wallet.path)))[1]
        except StopIteration:
            # No wallet files found.
            wallets = []

        root = Tree("Wallets")
        for w_name in wallets:
            wallet_for_name = bittensor.wallet( path = self.config.wallet.path, name = w_name)
            try:
                if wallet_for_name.coldkeypub_file.exists_on_device() and not wallet_for_name.coldkeypub_file.is_encrypted():
                    coldkeypub_str = wallet_for_name.coldkeypub.ss58_address
                else:
                    coldkeypub_str = '?'
            except:
                coldkeypub_str = '?'

            wallet_tree = root.add("\n[bold white]{} ({})".format(w_name, coldkeypub_str))
            hotkeys_path = os.path.join(self.config.wallet.path, w_name, 'hotkeys')
            try:
                hotkeys = next(os.walk(os.path.expanduser(hotkeys_path)))
                if len( hotkeys ) > 1:
                    for h_name in hotkeys[2]:
                        hotkey_for_name = bittensor.wallet( path = self.config.wallet.path, name = w_name, hotkey = h_name)
                        try:
                            if hotkey_for_name.hotkey_file.exists_on_device() and not hotkey_for_name.hotkey_file.is_encrypted():
                                hotkey_str = hotkey_for_name.hotkey.ss58_address
                            else:
                                hotkey_str = '?'
                        except:
                            hotkey_str = '?'
                        wallet_tree.add("[bold grey]{} ({})".format(h_name, hotkey_str))
            except:
                continue

        if len(wallets) == 0:
            root.add("[bold red]No wallets found.")
        print(root)

    def metagraph(self):
        r""" Prints an entire metagraph.
        """
        console = bittensor.__console__
        subtensor = bittensor.subtensor( config = self.config )
        console.print(":satellite: Syncing with chain: [white]{}[/white] ...".format(self.config.subtensor.network))
        metagraph = subtensor.metagraph( netuid = self.config.netuid )
        metagraph.save()
        issuance = subtensor.total_issuance
        difficulty = subtensor.difficulty

        TABLE_DATA = [] 
        total_stake = 0.0
        total_rank = 0.0
        total_trust = 0.0
        total_consensus = 0.0
        total_incentive = 0.0
        total_dividends = 0.0
        total_emission = 0  
        for uid in metagraph.uids:
            ep = metagraph.endpoint_objs[uid]
            row = [
                str(ep.uid), 
                '{:.5f}'.format( metagraph.stake[uid]),
                '{:.5f}'.format( metagraph.ranks[uid]), 
                '{:.5f}'.format( metagraph.trust[uid]), 
                '{:.5f}'.format( metagraph.consensus[uid]), 
                '{:.5f}'.format( metagraph.incentive[uid]),
                '{:.5f}'.format( metagraph.dividends[uid]),
                '{}'.format( int(metagraph.emission[uid] * 1000000000)),
                str((metagraph.block.item() - metagraph.last_update[uid].item())),
                str( metagraph.active[uid].item() ), 
                ep.ip + ':' + str(ep.port) if ep.is_serving else '[yellow]none[/yellow]', 
                ep.hotkey[:10],
                ep.coldkey[:10]
            ]
            total_stake += metagraph.stake[uid]
            total_rank += metagraph.ranks[uid]
            total_trust += metagraph.trust[uid]
            total_consensus += metagraph.consensus[uid]
            total_incentive += metagraph.incentive[uid]
            total_dividends += metagraph.dividends[uid]
            total_emission += int(metagraph.emission[uid] * 1000000000)
            TABLE_DATA.append(row)
        total_neurons = len(metagraph.uids)                
        table = Table(show_footer=False)
        table.title = (
            "[white]Metagraph: net: {}:{}, block: {}, N: {}/{}, tau: {}/block, stake: {}, issuance: {}, difficulty: {}".format(subtensor.network, metagraph.netuid, metagraph.block.item(), sum(metagraph.active.tolist()), metagraph.n.item(), bittensor.Balance.from_tao(metagraph.tau.item()), bittensor.Balance.from_tao(total_stake), issuance, difficulty )
        )
        table.add_column("[overline white]UID",  str(total_neurons), footer_style = "overline white", style='yellow')
        table.add_column("[overline white]STAKE(\u03C4)", '\u03C4{:.5f}'.format(total_stake), footer_style = "overline white", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]RANK", '{:.5f}'.format(total_rank), footer_style = "overline white", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]TRUST", '{:.5f}'.format(total_trust), footer_style = "overline white", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]CONSENSUS", '{:.5f}'.format(total_consensus), footer_style = "overline white", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]INCENTIVE", '{:.5f}'.format(total_incentive), footer_style = "overline white", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]DIVIDENDS", '{:.5f}'.format(total_dividends), footer_style = "overline white", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]EMISSION(\u03C1)", '\u03C1{}'.format(int(total_emission)), footer_style = "overline white", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]UPDATED", justify='right', no_wrap=True)
        table.add_column("[overline white]ACTIVE", justify='right', style='green', no_wrap=True)
        table.add_column("[overline white]AXON", justify='left', style='dim blue', no_wrap=True) 
        table.add_column("[overline white]HOTKEY", style='dim blue', no_wrap=False)
        table.add_column("[overline white]COLDKEY", style='dim purple', no_wrap=False)
        table.show_footer = True

        for row in TABLE_DATA:
            table.add_row(*row)
        table.box = None
        table.pad_edge = False
        table.width = None
        console.print(table)

    def weights(self):
        r""" Prints an weights to screen.
        """
        console = bittensor.__console__
        subtensor = bittensor.subtensor( config = self.config )
        wallet = bittensor.wallet( config = self.config )
        with console.status(":satellite: Syncing with chain: [white]{}[/white] ...".format(self.config.subtensor.get('network', bittensor.defaults.subtensor.network))):
            metagraph = subtensor.metagraph( netuid = self.config('netuid') )
            metagraph.save()

        table = Table()
        rows = []
        table.add_column("[bold white]uid", style='white', no_wrap=False)
        for uid in metagraph.uids.tolist():
            table.add_column("[bold white]{}".format(uid), style='white', no_wrap=False)
            if self.config.all_weights:
                rows.append(["[bold white]{}".format(uid) ] + ['{:.3f}'.format(v) for v in metagraph.W[uid].tolist()])
            else:
                if metagraph.coldkeys[uid] == wallet.coldkeypub.ss58_address:
                    if not self.config.all_hotkeys:
                        if metagraph.hotkeys[uid] == wallet.hotkey.ss58_address:
                            rows.append(["[bold white]{}".format(uid) ] + ['{:.3f}'.format(v) for v in metagraph.W[uid].tolist()])
                    else:
                        rows.append(["[bold white]{}".format(uid) ] + ['{:.3f}'.format(v) for v in metagraph.W[uid].tolist()])

        for row in rows:
            table.add_row(*row)
        table.box = None
        table.pad_edge = False
        table.width = None
        with console.pager():
            console.print(table)

    def overview(self):
        r""" Prints an overview for the wallet's colkey.
        """
        console = bittensor.__console__
        subtensor: 'bittensor.Subtensor' = bittensor.subtensor( config = self.config )

        all_hotkeys = []
        total_balance = bittensor.Balance(0)
        
        # We are printing for every coldkey.
        if self.config.all:
            cold_wallets = CLI._get_coldkey_wallets_for_path(self.config.wallet.path)
            for cold_wallet in tqdm(cold_wallets, desc="Pulling balances"):
                if cold_wallet.coldkeypub_file.exists_on_device() and not cold_wallet.coldkeypub_file.is_encrypted():
                    total_balance = total_balance + subtensor.get_balance( cold_wallet.coldkeypub.ss58_address )
            all_hotkeys = CLI._get_all_wallets_for_path( self.config.wallet.path )
        else:
            # We are only printing keys for a single coldkey
            coldkey_wallet = bittensor.wallet( config = self.config )
            if coldkey_wallet.coldkeypub_file.exists_on_device() and not coldkey_wallet.coldkeypub_file.is_encrypted():
                total_balance = subtensor.get_balance( coldkey_wallet.coldkeypub.ss58_address )
            if not coldkey_wallet.coldkeypub_file.exists_on_device():
                console.print("[bold red]No wallets found.")
                return
            all_hotkeys = CLI._get_hotkey_wallets_for_wallet( coldkey_wallet )

        # We are printing for a select number of hotkeys from all_hotkeys.

        if self.config.wallet.get('hotkeys', []):
            if not self.config.get('all_hotkeys', False):
                # We are only showing hotkeys that are specified.
                all_hotkeys = [hotkey for hotkey in all_hotkeys if hotkey.hotkey_str in self.config.wallet.hotkeys]
            else:
                # We are excluding the specified hotkeys from all_hotkeys.
                all_hotkeys = [hotkey for hotkey in all_hotkeys if hotkey.hotkey_str not in self.config.wallet.hotkeys]

        # Check we have keys to display.
        if len(all_hotkeys) == 0:
            console.print("[red]No wallets found.[/red]")
            return

        # Pull neuron info for all keys.            
        neurons: Dict[str, List[bittensor.NeuronInfo, bittensor.Wallet]] = {}
        block = subtensor.block

        netuids = set()
        for hotkey in all_hotkeys:
            netuids_for_hotkey = subtensor.get_netuids_for_hotkey( ss58_hotkey = hotkey.hotkey.ss58_address )
            netuids = netuids.union( netuids_for_hotkey )
        for netuid in netuids:
            neurons[str(netuid)] = []

        with console.status(":satellite: Syncing with chain: [white]{}[/white] ...".format(self.config.subtensor.get('network', bittensor.defaults.subtensor.network))):
            for netuid in netuids:
                all_neurons = subtensor.neurons( netuid = netuid )
                # Map the hotkeys to uids
                hotkey_to_neurons = {n.hotkey: n.uid for n in all_neurons}
                for wallet in tqdm(all_hotkeys):
                    uid = hotkey_to_neurons.get(wallet.hotkey.ss58_address)
                    if uid is not None:
                        nn = all_neurons[uid]
                        neurons[str(netuid)].append( (nn, wallet) )

        # Setup outer table.
        grid = Table.grid(pad_edge=False)

        title: str = ""
        if not self.config.all:
            title = ( "[bold white italic]Wallet - {}:{}".format(self.config.wallet.name, wallet.coldkeypub.ss58_address) )
        else:
            title = ( "[bold whit italic]All Wallets:" )

        # Add title
        grid.add_row(Align(title, vertical="middle", align="center"))

        # Generate rows per netuid
        for netuid in netuids:
            TABLE_DATA = []  
            total_stake = 0.0
            total_rank = 0.0
            total_trust = 0.0
            total_consensus = 0.0
            total_incentive = 0.0
            total_dividends = 0.0
            total_emission = 0   

            for nn, hotwallet in tqdm(neurons[str(netuid)]):
                nn: bittensor.NeuronInfo
                uid = nn.uid
                active = nn.active
                stake = sum([el[1] for el in nn.stake]).tao
                rank = nn.rank
                trust = nn.trust
                consensus = nn.consensus
                incentive = nn.incentive
                dividends = nn.dividends
                emission = int(nn.emission * 1000000000)
                last_update = int(block -  nn.last_update)
                row = [
                    hotwallet.name,
                    hotwallet.hotkey_str,
                    str(uid), 
                    str(active), 
                    '{:.5f}'.format(stake),
                    '{:.5f}'.format(rank), 
                    '{:.5f}'.format(trust), 
                    '{:.5f}'.format(consensus), 
                    '{:.5f}'.format(incentive),
                    '{:.5f}'.format(dividends),
                    '{}'.format(emission),
                    str(last_update),
                    bittensor.utils.networking.int_to_ip( nn.axon_info.ip) + ':' + str(nn.axon_info.port) if nn.axon_info.port != 0 else '[yellow]none[/yellow]', 
                    nn.hotkey
                ]
                total_stake += stake
                total_rank += rank
                total_trust += trust
                total_consensus += consensus
                total_incentive += incentive
                total_dividends += dividends
                total_emission += emission
                TABLE_DATA.append(row)
                
            total_neurons = len(neurons)

            # Add subnet header
            grid.add_row(f"Subnet: [bold white]{1}[/bold white]")

            table = Table(show_footer=False, width=self.config.get('width', None), pad_edge=False, box=None)
            table.add_column("[overline white]COLDKEY",  str(total_neurons), footer_style = "overline white", style='bold white')
            table.add_column("[overline white]HOTKEY",  str(total_neurons), footer_style = "overline white", style='white')
            table.add_column("[overline white]UID",  str(total_neurons), footer_style = "overline white", style='yellow')
            table.add_column("[overline white]ACTIVE", justify='right', style='green', no_wrap=True)
            table.add_column("[overline white]STAKE(\u03C4)", '\u03C4{:.5f}'.format(total_stake), footer_style = "overline white", justify='right', style='green', no_wrap=True)
            table.add_column("[overline white]RANK", '{:.5f}'.format(total_rank), footer_style = "overline white", justify='right', style='green', no_wrap=True)
            table.add_column("[overline white]TRUST", '{:.5f}'.format(total_trust), footer_style = "overline white", justify='right', style='green', no_wrap=True)
            table.add_column("[overline white]CONSENSUS", '{:.5f}'.format(total_consensus), footer_style = "overline white", justify='right', style='green', no_wrap=True)
            table.add_column("[overline white]INCENTIVE", '{:.5f}'.format(total_incentive), footer_style = "overline white", justify='right', style='green', no_wrap=True)
            table.add_column("[overline white]DIVIDENDS", '{:.5f}'.format(total_dividends), footer_style = "overline white", justify='right', style='green', no_wrap=True)
            table.add_column("[overline white]EMISSION(\u03C1)", '\u03C1{}'.format(int(total_emission)), footer_style = "overline white", justify='right', style='green', no_wrap=True)
            table.add_column("[overline white]UPDATED", justify='right', no_wrap=True)
            table.add_column("[overline white]AXON", justify='left', style='dim blue', no_wrap=True) 
            table.add_column("[overline white]HOTKEY_SS58", style='dim blue', no_wrap=False)
            table.show_footer = True

            sort_by: Optional[str] = self.config.get('sort_by', None)
            sort_order: Optional[str] = self.config.get('sort_order', None)

            if sort_by is not None and sort_by != "":
                column_to_sort_by: int = 0
                highest_matching_ratio: int = 0
                sort_descending: bool = False # Default sort_order to ascending

                for index, column in zip(range(len(table.columns)), table.columns):
                    # Fuzzy match the column name. Default to the first column.
                    column_name = column.header.lower().replace('[overline white]', '')
                    match_ratio = fuzz.ratio(sort_by.lower(), column_name)
                    # Finds the best matching column
                    if  match_ratio > highest_matching_ratio:
                        highest_matching_ratio = match_ratio
                        column_to_sort_by = index
                
                if sort_order.lower() in { 'desc', 'descending', 'reverse'}:
                    # Sort descending if the sort_order matches desc, descending, or reverse
                    sort_descending = True
                
                def overview_sort_function(row):
                    data = row[column_to_sort_by]
                    # Try to convert to number if possible
                    try:
                        data = float(data)
                    except ValueError:
                        pass
                    return data

                TABLE_DATA.sort(key=overview_sort_function, reverse=sort_descending)

            for row in TABLE_DATA:
                table.add_row(*row)

            grid.add_row(table)


        console.clear()

        caption = "[italic][dim][white]Wallet balance: [green]\u03C4" + str(total_balance.tao)
        grid.add_row(Align(caption, vertical="middle", align="center"))

        # Print the entire table/grid
        console.print(grid, width=self.config.get('width', None))

    def full(self):
        r""" Prints an overview for the wallet's colkey.
        """
        # Set the config to output all wallets.
        self.config.all = True
        # Print the overview.
        self.overview()

    def list_subnets( self ) -> None:
        r"""
        List all subnet netuids in the network.
        """
        subtensor = bittensor.subtensor( config = self.config )
        subnets: List[bittensor.SubnetInfo] = subtensor.get_subnets_info()

        rows = []
        total_neurons = 0
        
        for subnet in subnets:
            total_neurons += subnet.max_n
            rows.append((
                str(subnet.netuid),
                str(subnet.max_n),
                str(subnet.max_n),
                str(bittensor.utils.registration.millify(subnet.difficulty)),
                str(subnet.immunity_period),
                str(subnet.validator_batch_size),
                str(subnet.validator_sequence_length),
                str(subnet.tempo),
                str(subnet.modality),
                str(list(subnet.connection_requirements.keys())),
                str(subnet.emission_value),
            ))

        table = Table(show_footer=True, width=self.config.get('width', None), pad_edge=False, box=None)
        table.title = (
            "[white]Subnets - {}".format(subtensor.network)
        )
        table.add_column("[overline white]NETUID",  str(len(subnets)), footer_style = "overline white", style='bold white')
        table.add_column("[overline white]N", str(total_neurons), footer_style = "overline white", style='white')
        table.add_column("[overline white]MAX_N", style='white')
        table.add_column("[overline white]DIFFICULTY", style='white')
        table.add_column("[overline white]IMMUNITY", style='white')
        table.add_column("[overline white]BATCH SIZE", style='white')
        table.add_column("[overline white]SEQ_LEN", style='white')
        table.add_column("[overline white]TEMPO", style='white')
        table.add_column("[overline white]MODALITY", style='white')
        table.add_column("[overline white]CON_REQ", style='white')
        table.add_column("[overline white]EMISSION", "1.0", style='white', footer_style="overline white") # sums to 1.0
        
        for row in rows:
            table.add_row(*row)

        bittensor.__console__.print(table)
        