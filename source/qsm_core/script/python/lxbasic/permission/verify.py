# coding:utf-8
import os

import json

import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import padding, hashes


class Encrypt:
    @classmethod
    def generate_key_from_string(cls, secret_string):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(secret_string.encode())
        return digest.finalize()

    @classmethod
    def encrypt(cls, key, data_dict):
        data_string = json.dumps(data_dict)

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data_string.encode())+padder.finalize()

        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        encrypted_data = encryptor.update(padded_data)+encryptor.finalize()
        return iv, encrypted_data

    @staticmethod
    def encrypt_():
        pass

    @classmethod
    def decrypt(cls, key, iv, encrypted_data):
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_data)+decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_data)+unpadder.finalize()

        data_string = unpadded_data.decode()
        return json.loads(data_string)

    @classmethod
    def save_encrypted_data_to_json(cls, json_path, iv, encrypted_data):
        directory_path = os.path.dirname(json_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        data_to_save = {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'data': base64.b64encode(encrypted_data).decode('utf-8')
        }
        with open(json_path, 'w') as json_file:
            json.dump(data_to_save, json_file)

    @classmethod
    def load_encrypted_data_from_json(cls, json_path):
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
            iv = base64.b64decode(data['iv'])
            encrypted_data = base64.b64decode(data['data'])
            return iv, encrypted_data

