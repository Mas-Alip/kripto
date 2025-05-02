def embed_file(image_path, file_path, output_image_path, key):
    from PIL import Image
    import os
    from encryption.aes import AESCipher

    # Check if the image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found.")

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError("File to embed not found.")

    # Encrypt the file
    cipher = AESCipher(key)
    encrypted_file = cipher.encrypt_file(file_path)

    # Open the image
    image = Image.open(image_path)
    encoded_image = image.copy()

    # Convert the encrypted file to bytes
    encrypted_bytes = bytearray(encrypted_file)

    # Embed the encrypted bytes into the image
    width, height = encoded_image.size
    pixel_index = 0

    for byte in encrypted_bytes:
        for bit in range(8):
            x = pixel_index % width
            y = pixel_index // width
            if y >= height:
                raise ValueError("Image is too small to hold the file.")
            pixel = list(encoded_image.getpixel((x, y)))
            pixel[0] = (pixel[0] & ~1) | ((byte >> (7 - bit)) & 1)  # Modify the least significant bit
            encoded_image.putpixel((x, y), tuple(pixel))
            pixel_index += 1

    # Save the modified image
    encoded_image.save(output_image_path)
    return output_image_path