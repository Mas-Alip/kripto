from cryptoutil import encrypt_file
from stegoutil import hide_data, estimate_capacity,  extract_data, hide_data
from cryptoutil import decrypt_file

import os

def embed(file_path, image_path, password, output_image):
    print("🔐 Mengenkripsi file...")
    with open(file_path, 'rb') as f:
        file_data = f.read()
    enc_data = encrypt_file(file_data, password)

    # Hitung kapasitas gambar
    max_bytes = estimate_capacity(image_path)
    enc_size = len(enc_data)

    print(f"📦 Ukuran file terenkripsi: {enc_size} bytes")
    print(f"🖼️  Kapasitas maksimum gambar: {max_bytes} bytes")

    # Validasi kapasitas
    if enc_size > max_bytes:
        print("❌ Gagal: File terlalu besar untuk disisipkan ke gambar.")
        print("💡 Tips: Gunakan gambar dengan resolusi lebih tinggi atau kompres file.")
        return

    print("📥 Menyisipkan data ke dalam gambar...")
    try:
        hide_data(image_path, enc_data, output_image)
        print(f"✅ Berhasil! File telah disembunyikan dalam '{output_image}'")
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat menyisipkan data: {e}")


def extract(image_path, password, output_file):
    try:
        # Ekstrak data terenkripsi dari gambar
        enc_data = extract_data(image_path)

        # Validasi data yang diekstrak
        if not enc_data or len(enc_data) < 16:
            raise ValueError("Data yang diekstrak tidak valid atau rusak.")

        # Dekripsi data menggunakan password
        data = decrypt_file(enc_data, password)

        # Simpan data hasil dekripsi ke file output
        with open(output_file, 'wb') as f:
            f.write(data)
        print("✅ File berhasil diekstrak dan didekripsi.")
    except Exception as e:
        print(f"❌ Gagal mendekripsi data: {e}")
        raise e  # Lempar error agar ditangani oleh GUI

if __name__ == "__main__":
    embed("Draft.docx", "berbi.png", "rahasia123", "berbi.png")
    # Setelah embed, kamu bisa ganti dengan baris di bawah ini untuk ekstraksi:
    extract("berbi.png", "rahasia123", "Draft.docx")
