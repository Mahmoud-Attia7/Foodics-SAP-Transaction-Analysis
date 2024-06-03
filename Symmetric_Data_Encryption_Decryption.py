#!/usr/bin/env python
# coding: utf-8

# In[25]:


import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


# In[27]:


class SymmetricDataED:
    
    def generate_key(salt: bytes) -> bytes:
        password = "strong_password"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return key

    def encrypt(plaintext: str) -> bytes:
        salt = os.urandom(16)
        key = SymmetricDataED.generate_key(salt)
        iv = os.urandom(16)

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return salt + iv + ciphertext

    def decrypt(ciphertext: bytes) -> str:
        salt = ciphertext[:16]
        iv = ciphertext[16:32]
        encrypted_data = ciphertext[32:]

        key = SymmetricDataED.generate_key(salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()

        return plaintext.decode()


# In[ ]:





# In[ ]:




