import tkinter as tk
from tkinter import filedialog, messagebox
from main import embed, extract  # Impor fungsi dari main.py
import os

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB dalam bytes

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
        if self.file_path and os.path.getsize(self.file_path) > MAX_FILE_SIZE:
            messagebox.showerror("Error", "Ukuran file terlalu besar! Maksimal 5MB.")
            self.file_path = ""
            self.label_file.config(text="📄 Tidak ada file yang dipilih")
        else:
            self.label_file.config(text=f"📄 File: {os.path.basename(self.file_path)}")

    def choose_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Images", "*.png")])
        if self.image_path and os.path.getsize(self.image_path) > MAX_FILE_SIZE:
            messagebox.showerror("Error", "Ukuran gambar terlalu besar! Maksimal 5MB.")
            self.image_path = ""
            self.label_image.config(text="🖼️ Tidak ada gambar yang dipilih")
        else:
            self.label_image.config(text=f"🖼️ Gambar: {os.path.basename(self.image_path)}")

    def embed(self):
        if not self.file_path or not self.image_path:
            messagebox.showerror("Error", "Pilih file dan gambar terlebih dahulu.")
            return

        self.password = self.entry_password.get()
        if not self.password:
            messagebox.showerror("Error", "Masukkan password.")
            return

        output_image = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("Images", "*.png")])
        if not output_image:
            return

        try:
            embed(self.file_path, self.image_path, self.password, output_image)
            messagebox.showinfo("Sukses", f"File berhasil disembunyikan dalam gambar:\n{output_image}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyembunyikan file: {e}")

    def extract(self):
        if not self.image_path:
            messagebox.showerror("Error", "Pilih gambar yang mengandung file.")
            return

        self.password = self.entry_password.get()
        if not self.password:
            messagebox.showerror("Error", "Masukkan password.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".docx",
                                                   filetypes=[("Dokumen", "*.docx *.pdf")])
        if not output_file:
            return

        try:
            # Panggil fungsi extract dari main.py
            extract(self.image_path, self.password, output_file)

            # Periksa apakah file hasil ekstraksi benar-benar ada dan tidak kosong
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                messagebox.showinfo("Sukses", f"File berhasil diekstrak:\n{output_file}")
            else:
                # Jika file tidak valid, hapus file kosong dan tampilkan pesan error
                if os.path.exists(output_file):
                    os.remove(output_file)
                messagebox.showerror("Error", "Gagal mengekstrak file. Password salah atau data rusak.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekstrak file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoVaultApp(root)
    root.mainloop()
