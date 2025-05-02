def extract_file(image_path, output_file_path, aes_key):
    from PIL import Image
    import numpy as np
    from encryption.aes import AESCipher

    # Load the image
    image = Image.open(image_path)
    image_data = np.array(image)

    # Extract the hidden data from the image
    hidden_data = []
    for row in image_data:
        for pixel in row:
            hidden_data.append(pixel[0] & 1)  # Extract the least significant bit

    # Convert the hidden data to bytes
    hidden_bytes = bytearray()
    for i in range(0, len(hidden_data), 8):
        byte = 0
        for bit in hidden_data[i:i + 8]:
            byte = (byte << 1) | bit
        hidden_bytes.append(byte)

    # Decrypt the hidden file using AES
    aes_cipher = AESCipher(aes_key)
    decrypted_file = aes_cipher.decrypt_file(hidden_bytes)

    # Save the extracted file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decrypted_file)