# 📜 Kisskh Subtitle Decryption Tools

Alat ini digunakan untuk mendekripsi subtitle berformat `.srt` atau `.txt` dari situs Kisskh, yang dienkripsi menggunakan algoritma **AES-128 CBC + Base64**.

---

## 📥 Requirement (Prasyarat)

Agar tool ini dapat berjalan, pastikan sistem kamu sudah terpasang:

### Untuk Versi GUI dan CLI (Python Script)

- Python 3.10 atau lebih baru
- Paket Python berikut:
  ```
  pip install pycryptodome
  pip install customtkinter
  ```

### Untuk Versi EXE (Standalone)

- Tidak membutuhkan Python (EXE sudah termasuk semua dependency)

---

## 🚀 Cara Penggunaan

### 1️⃣ Mode GUI (Tampilan Grafis)

#### Jalankan:

- **Jika menggunakan Python script:**
  ```bash
  python gui.py
  ```
- **Jika menggunakan EXE:**
  - Double klik file `SubtitleDecryptor.exe`.

#### Fitur:

- Pilih file atau folder subtitle.
- Pilih preset key/IV atau input manual.
- Tampilkan progress bar selama proses.
- Log hasil ditampilkan dalam jendela GUI.
- Dukungan drag & drop file/folder.

---

### 2️⃣ Mode CLI (Command Line Interface)

#### Jalankan:

- **Jika menggunakan Python script:**
  ```bash
  python decrypt_cli.py
  ```
- **Jika menggunakan EXE CLI (jika ada):**
  ```bash
  SubtitleDecryptor_CLI.exe
  ```

#### Fitur:

- Interaktif di terminal.
- Pilih file atau folder subtitle.
- Pilih preset key/IV atau input manual.
- Tampilkan progress dan hasil langsung di terminal.
- Dukungan drag & drop file/folder.
- Setelah proses selesai, otomatis kembali ke menu utama.

---

## 🔗 Cara Drag & Drop (CLI)

- Jalankan program CLI.
- Ketika diminta input file/folder, cukup seret file/folder ke terminal dan tekan **Enter**.
- Bisa juga tekan **Enter** langsung untuk membuka file explorer.

---

## 🔑 Konfigurasi Key & IV

### Lokasi:

`config.json`

### Contoh Isi:

```json
{
  "presets": {
    "default1": {
      "key": "1234567890123456",
      "iv": "abcdefghijklmnop"
    },
    "default2": {
      "key": "6543210987654321",
      "iv": "ponmlkjihgfedcba"
    }
  }
}
```
