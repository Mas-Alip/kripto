class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt_file(self, file_path):
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        import os

        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv

        with open(file_path, 'rb') as file:
            plaintext = file.read()

        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as file:
            file.write(iv + ciphertext)

        return encrypted_file_path

    def decrypt_file(self, encrypted_file_path):
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad

        with open(encrypted_file_path, 'rb') as file:
            iv = file.read(16)
            ciphertext = file.read()

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        decrypted_file_path = encrypted_file_path.replace('.enc', '')
        with open(decrypted_file_path, 'wb') as file:
            file.write(plaintext)

        return decrypted_file_path