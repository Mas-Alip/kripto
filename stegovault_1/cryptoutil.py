from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib

def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(data: bytes, password: str) -> bytes:
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))  # Tambahkan padding
    return iv + encrypted_data

def decrypt_file(enc_data: bytes, password: str) -> bytes:
    key = derive_key(password)
    iv = enc_data[:16]
    encrypted_data = enc_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)  # Hapus padding
    return decrypted_data
