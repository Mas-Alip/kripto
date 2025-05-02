import tkinter as tk
from tkinter import filedialog, messagebox
from cryptoutil import encrypt_file, decrypt_file
from stegoutil import hide_data, extract_data, estimate_capacity
import os

class StegoVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StegoVault - File Hider with AES & Steganography")
        self.root.geometry("500x400")

        self.file_path = ""
        self.image_path = ""
        self.output_path = ""
        self.password = ""

        # === UI ELEMENTS ===
        tk.Label(root, text="StegoVault", font=("Helvetica", 20, "bold")).pack(pady=10)

        self.label_file = tk.Label(root, text="📄 Tidak ada file yang dipilih")
        self.label_file.pack()
        tk.Button(root, text="Pilih File (PDF/DOCX)", command=self.choose_file).pack(pady=5)

        self.label_image = tk.Label(root, text="🖼️ Tidak ada gambar yang dipilih")
        self.label_image.pack()
        tk.Button(root, text="Pilih Gambar (PNG)", command=self.choose_image).pack(pady=5)

        tk.Label(root, text="🔑 Password:").pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(pady=5)

        tk.Button(root, text="🔐 Embed File", command=self.embed).pack(pady=10)
        tk.Button(root, text="📤 Extract File", command=self.extract).pack()

    def choose_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx")])
        self.label_file.config(text=f"📄 File: {os.path.basename(self.file_path)}")

    def choose_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Images", "*.png")])
        self.label_image.config(text=f"🖼️ Gambar: {os.path.basename(self.image_path)}")

    def embed(self):
        if not self.file_path or not self.image_path:
            messagebox.showerror("Error", "Pilih file dan gambar terlebih dahulu.")
            return

        self.password = self.entry_password.get()
        if not self.password:
            messagebox.showerror("Error", "Masukkan password.")
            return

        with open(self.file_path, "rb") as f:
            file_data = f.read()
        enc_data = encrypt_file(file_data, self.password)

        try:
            max_bytes = estimate_capacity(self.image_path)
            if len(enc_data) > max_bytes:
                messagebox.showerror("Gagal", f"File terenkripsi terlalu besar.\nMax kapasitas gambar: {max_bytes} bytes")
                return

            # Ganti nama output jika tidak ingin menimpa
            output_path = self.image_path  # ditimpa
            hide_data(self.image_path, enc_data, output_path)
            messagebox.showinfo("Sukses", f"File berhasil disembunyikan dalam gambar:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract(self):
        if not self.image_path:
            messagebox.showerror("Error", "Pilih gambar yang mengandung file.")
            return

        self.password = self.entry_password.get()
        if not self.password:
            messagebox.showerror("Error", "Masukkan password.")
            return

        try:
            enc_data = extract_data(self.image_path)
            data = decrypt_file(enc_data, self.password)

            output_file = filedialog.asksaveasfilename(defaultextension=".docx",
                                                       filetypes=[("Dokumen", "*.docx *.pdf")])
            if output_file:
                with open(output_file, "wb") as f:
                    f.write(data)
                messagebox.showinfo("Sukses", f"File berhasil diekstrak:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Gagal", f"Tidak dapat mendekripsi file.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoVaultApp(root)
    root.mainloop()
