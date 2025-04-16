# 📜 Kisskh Subtitle Decryption Tools

Program ini berfungsi untuk mendekripsi file subtitle berformat `.srt` atau `.txt` dari situs Kisskh. Contohnya seperti berikut:

Sebelum :
```
1
00:00:29,820 --> 00:00:33,980
8SDXM2phcW+GaQEKsHBS27mj06iChhZpsf30cM3i3UR+KjvMrpyCfKZLhlnXD2Ta

2
00:00:34,150 --> 00:00:38,720
OsxqBrHkWykRfifpPOLtmh4YkLV5wIbyyPHSa/P3gZ5Yr0W207yaZ1rTqWt/2f2X

3
00:00:38,820 --> 00:00:43,920
gYyJh+kvoq2OcSg7JJGeyabFIQ7xS+BeIZYaSHoHiDY4rH+2vo3yxWPZZ41nhsO5

4
00:00:44,080 --> 00:00:47,520
qiXVSA9qKu7bv6d+bJ68fU1qrVAj9AvitI5Ddi1w/8CXJwdcsAHfg3vNWajX5AFM

5
00:00:47,920 --> 00:00:52,720
0ijd7MSpcDImJVdy+X+7fRcuNawb3l8BRnq3zQfZHnZKM3JtSXCi1vDhEGqk58TYfKj9NZl+kwr170kzkfXLkMuE9+8XyArOWxd5sBlKDpw=

```

Sesudah :
```
1
00:00:29,820 --> 00:00:33,980
♪A beautiful place full of smiles♪

2
00:00:34,150 --> 00:00:38,720
♪Where imaginations about you grow wildly♪

3
00:00:38,820 --> 00:00:43,920
♪The winter sun is like your white teeth♪

4
00:00:44,080 --> 00:00:47,520
♪Expecting your visit all day long♪

5
00:00:47,920 --> 00:00:52,720
♪Like the light breeze and

```

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
---

## 🚀 Cara Penggunaan

### 1️⃣ Mode GUI

#### Jalankan:

- **Jika menggunakan Python script:**
  ```bash
  python gui.py
  ```
- **Jika menggunakan EXE:**
  - Double klik file `SubtitleDecryptor.exe`.

#### Fitur:

- Pilih file atau folder subtitle.
- Pilih preset Key/IV atau input manual.
- Tampilkan progress bar selama proses.
- Log hasil ditampilkan dalam jendela GUI.
- Dukungan drag & drop file/folder.

---

### 2️⃣ Mode CLI

#### Jalankan:

- **Jika menggunakan Python script:**
  ```bash
  python cli.py
  ```

#### Fitur:

- Interaktif di terminal.
- Pilih file atau folder subtitle.
- Pilih preset Key/IV atau input manual.
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
