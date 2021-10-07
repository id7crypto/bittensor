""" Functions for wallets, including key extraction, storage, and user interface,
other then 
"""
import os
import sys
import stat
import base64
import getpass

from termcolor import colored
from password_strength import PasswordPolicy
from loguru import logger
from substrateinterface import Keypair

from cryptography.exceptions import InvalidSignature, InvalidKey
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from loguru import logger
from ansible_vault import Vault

import json
from substrateinterface import Keypair


class CryptoKeyError(Exception):
    """ Exception for invalid signature, key, token, password, etc 
        Overwrite the built-in CryptoKeyError
    """

class KeyFileError(Exception):
    """ Overwrite the built-in CryptoKeyError
    """

__SALT = b"Iguesscyborgslikemyselfhaveatendencytobeparanoidaboutourorigins"

class _user_interface:
    """ Stores functions for the interactions with user
    including asking and validating password, permission for overwrite and displaying messages
    """
    @staticmethod
    def ask_password_to_encrypt():
        """ Ask user to input a password
        """
        valid = False
        while not valid:
            password = getpass.getpass("Specify password for key encryption: ")
            valid = wallet_utils.validate_password(password)

        return password

    @staticmethod
    def ask_password_to_decrypt():
        """ Ask user to input a password
        """
        password = getpass.getpass("Enter password to unlock key: ")
        return password
    
    @staticmethod
    def validate_password(password):
        """ The policy to validate the strength of password
        """
        policy = PasswordPolicy.from_names(
            strength=0.20,
            entropybits=10,
            length=6,
        )
        if not password:
            return False

        tested_pass = policy.password(password)
        result = tested_pass.test()
        if len(result) > 0:
            print(colored('Password not strong enough. Try increasing the length of the password or the password complexity'))
            return False

        password_verification = getpass.getpass("Retype your password: ")
        if password != password_verification:
            print("Passwords do not match")
            return False

        return True

    @staticmethod
    def may_overwrite( file:str ):
        choice = input("File %s already exists. Overwrite ? (y/N) " % file)
        return choice == 'y'
      
    @staticmethod
    def display_mnemonic_msg( kepair : Keypair ):
        """ Displaying the mnemonic and warning message to keep mnemonic safe
        """
        mnemonic = kepair.mnemonic
        mnemonic_green = colored(mnemonic, 'green')
        print (colored("\nIMPORTANT: Store this mnemonic in a secure (preferable offline place), as anyone " \
                    "who has possesion of this mnemonic can use it to regenerate the key and access your tokens. \n", "red"))
        print ("The mnemonic to the new key is:\n\n%s\n" % mnemonic_green)
        print ("You can use the mnemonic to recreate the key in case it gets lost. The command to use to regenerate the key using this mnemonic is:")
        print("bittensor-cli regen --mnemonic %s" % mnemonic)
        print('')

class _keyfile_manager:
    """ Stores functions for managing keyfiles,
    including encryption and decryption, writing keys to files and setting file permissions
    """

    @staticmethod
    def validate_create_path(keyfile_path, overwrite: bool = False ):
        """ Check if we can overwrite the keyfile with the os and the user
        """
        full_path = os.path.expanduser(keyfile_path)
        if os.path.isfile(full_path):
            if os.access(full_path, os.W_OK):
                if overwrite:
                    return full_path

                elif _user_interface.may_overwrite( full_path ):
                    return full_path

                else:
                    quit()
            else:
                print(colored("No write access for  %s" % full_path, 'red'))
                quit()
        else:
            pdir = os.path.dirname(full_path)
            if os.access(pdir, os.W_OK):
                return full_path
            else:
                print(colored("No write access for  %s" % full_path, 'red'))
                quit()

    @staticmethod
    def encrypt_to_file(data, password, full_path):
        """ Encrypt the data with password
        """
        vault = Vault(password)
        vault.dump( data, open( full_path, 'w') )
        return 

    @staticmethod
    def decrypt_file(password, full_path):
        """ Decrypt the data with password
        """
        @staticmethod
        def __generate_key(password):
            """ Get key from password
            """
            kdf = PBKDF1HMAC(algorithm=hashes.SHA256(), salt=__SALT, length=32, iterations=10000000, backend=default_backend())
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return key
    
        try:
            with open( full_path , 'rb') as f:
                data = f.read()
                
                if  data[:14] == b'$ANSIBLE_VAULT':
                    vault = Vault(password)
                    data = vault.load(open(full_path).read())
                    return data

                elif data[:5] == b"gAAAAA":
                    key = __generate_key(password)
                    cipher_suite = Fernet(key)
                    data = cipher_suite.decrypt(data)
                    wallet_utils.encrypt_to_file(data, password, full_path)
                
                else:
                    raise KeyFileError("Keyfile corrupt")
        
        except (InvalidSignature, InvalidKey, InvalidToken) as key_error:
            raise CryptoKeyError from key_error

    @staticmethod
    def is_encrypted(full_path):
        """ Check if data was encrypted
        """
        with open( full_path , 'rb') as f:
            data = f.read()
            return (data[:14] == b'$ANSIBLE_VAULT') or (data[:6] == b"gAAAAA")
    
    @staticmethod
    def write_pubkey_to_file( keyfile_path, pubkey_str:str ):
        """ Write  public key to text file
        """
        full_path = os.path.expanduser(keyfile_path)
        with open(full_path + "pub.txt", "w") as pubfile:
            pubfile.write(pubkey_str.strip())

    @staticmethod
    def write_key_to_file(full_path, key_str):
        """ Write the key(data) to path
        """
        print("Writing key to %s" % full_path)
        with open(full_path, "wb") as keyfile:
            keyfile.write(key_str)
    
    @staticmethod
    def set_file_permissions(full_path):
        """ Set permission to be read and write by owner
        """
        os.chmod(full_path, stat.S_IRUSR | stat.S_IWUSR)

class _key_obtainer:
    """ Stores functions for getting keypair from different ways
    including generating a new key, from an existing mnemonic and loading from data 
    """
    @staticmethod
    def gen_new_key(n_words):
        """ Generate new public/privete keypair 
        1. gen mnemonic 
        2. gen keypair from mnemonic
        """
        mnemonic = Keypair.generate_mnemonic( n_words)
        keypair = Keypair.create_from_mnemonic(mnemonic)
        return keypair

    @staticmethod
    def get_key_from_mnemonic(mnemonic):
        """ Create keypair from mnemonic, a list of words
        """
        if len(mnemonic) not in [12,15,18,21,24]:
            print(colored("Mnemonic has invalid size. This should be 12,15,18,21 or 24 words", 'red'))
            quit()

        try:
            keypair = Keypair.create_from_mnemonic(" ".join(mnemonic))
            return keypair
        except ValueError as e:
            print(colored(str(e), "red"))
            quit()

    @staticmethod
    def load_keypair_from_data(data) -> Keypair:
        """ Get keypair from data seed
        """
        try:
            data = json.loads(data.decode())
            if "secretSeed" not in data:
                raise KeyFileError("Keyfile corrupt")

            return Keypair.create_from_seed(data['secretSeed'])

        except BaseException as e:
            logger.debug(e)
            raise KeyFileError("Keyfile corrupt") from e

class wallet_utils:
    """ Wrap up all functions for user_interface, keyfile_manager and key_obtainer
    """
    ask_password_to_encrypt = _user_interface.ask_password_to_encrypt
    ask_password_to_decrypt = _user_interface.ask_password_to_decrypt
    validate_password = _user_interface.validate_password
    may_overwrite = _user_interface.may_overwrite
    display_mnemonic_msg = _user_interface.display_mnemonic_msg

    validate_create_path = _keyfile_manager.validate_create_path
    encrypt_to_file = _keyfile_manager.encrypt_to_file
    decrypt_file = _keyfile_manager.decrypt_file
    is_encrypted = _keyfile_manager.is_encrypted
    write_pubkey_to_file = _keyfile_manager.write_pubkey_to_file
    write_key_to_file = _keyfile_manager.write_key_to_file
    set_file_permissions  = _keyfile_manager.set_file_permissions

    load_keypair_from_data = _key_obtainer.load_keypair_from_data
    get_key_from_mnemonic = _key_obtainer.get_key_from_mnemonic
    gen_new_key = _key_obtainer.gen_new_key
