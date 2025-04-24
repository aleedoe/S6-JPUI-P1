import os

# Path yang benar relatif dari lokasi file ini
base_path = "../../dataset/kelas-1/ainaya"

# Ambil semua file gambar
image_files = [
    f for f in os.listdir(base_path)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
]

# Tampilkan semua file gambar
if not image_files:
    print("Tidak ada file gambar ditemukan.")
else:
    print("Daftar gambar:")
    for img in image_files:
        print("-", img)
