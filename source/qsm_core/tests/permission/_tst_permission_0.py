# coding:utf-8
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# 生成一个随机秘钥
key = os.urandom(32)  # 256位秘钥，适用于AES-256


# 加密函数
def encrypt(data, key):
    # 使用PKCS7填充
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode())+padder.finalize()

    # 随机生成IV
    iv = os.urandom(16)

    # 创建AES加密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # 加密数据
    encrypted_data = encryptor.update(padded_data)+encryptor.finalize()

    return iv+encrypted_data  # 返回IV和加密后的数据


# 解密函数
def decrypt(encrypted_data, key):
    iv = encrypted_data[:16]  # 提取IV
    encrypted_data = encrypted_data[16:]  # 提取加密数据

    # 创建AES解密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # 解密数据
    decrypted_data = decryptor.update(encrypted_data)+decryptor.finalize()

    # 去除填充
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data)+unpadder.finalize()

    return unpadded_data.decode()


# 示例使用
original_data = "Hello, this is a secret message!"
encrypted = encrypt(original_data, key)
print("Encrypted data:", encrypted)

decrypted = decrypt(encrypted, key)
print("Decrypted data:", decrypted)
