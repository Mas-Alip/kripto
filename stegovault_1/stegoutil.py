from PIL import Image
import numpy as np

def hide_data(image_path, data: bytes, output_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    arr = np.array(img)

    flat = arr.flatten()
    total_available_bits = len(flat)  # total piksel * 3 kanal warna
    total_data_bits = (len(data) * 8) + 16  # 8 bit per byte + 16 bit EOF

    if total_data_bits > total_available_bits:
        raise ValueError(
            f"Data terlalu besar untuk gambar ini.\n"
            f"Maksimum: {total_available_bits // 8} bytes, "
            f"File terenkripsi: {len(data)} bytes."
        )

    bin_data = ''.join(f'{byte:08b}' for byte in data)
    bin_data += '1111111111111110'  # EOF marker

    for i in range(len(bin_data)):
        flat[i] = (flat[i] & 0b11111110) | int(bin_data[i])

    arr = flat.reshape(arr.shape)
    Image.fromarray(arr).save(output_path)

def estimate_capacity(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    width, height = img.size
    total_pixels = width * height
    total_bits = total_pixels * 3  # RGB = 3 channel
    max_bytes = (total_bits - 16) // 8  # 16 bit disisakan untuk EOF
    return max_bytes


def extract_data(image_path):
    print(f"📂 Membuka gambar: {image_path}")
    img = Image.open(image_path)
    img = img.convert("RGB")
    arr = np.array(img)
    flat = arr.flatten()

    bits = []
    for val in flat:
        bits.append(str(val & 1))

    all_bits = ''.join(bits)
    eof = all_bits.find('1111111111111110')
    if eof == -1:
        raise ValueError("Tidak ditemukan data dalam gambar!")

    print(f"📥 Data ditemukan hingga EOF pada bit ke-{eof}.")
    byte_data = [int(all_bits[i:i+8], 2) for i in range(0, eof, 8)]
    print(f"📦 Ukuran data yang diekstrak: {len(byte_data)} bytes.")
    return bytes(byte_data)
