import base64
import json
import time
import os
from pathlib import Path
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import tkinter as tk
from tkinter import filedialog

# Warna ANSI untuk terminal
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
BLUE = "\033[94m"

SUPPORTED_EXTENSIONS = [".srt", ".txt"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_presets():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)["presets"]
    except Exception as e:
        print(f"{RED}Error loading config: {e}{RESET}")
        return {"Default": {"key": "AmSmZVcH93UQUezi", "iv": "ReBKWW8cqdjPEnF6"}}


def is_valid_base64(s: str) -> bool:
    try:
        return base64.b64encode(base64.b64decode(s)) == s.encode()
    except:
        return False


def decrypt_content(content: str, secret_key: bytes, iv: bytes) -> str:
    """
    Decrypt AES-128 CBC content with better error handling
    """
    if not content or not is_valid_base64(content):
        return content

    try:
        encrypted_bytes = base64.b64decode(content)
        if len(encrypted_bytes) % 16 != 0:
            return content

        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted_bytes), 16).decode(
            "utf-8", errors="ignore"
        )
        return decrypted
    except Exception as e:
        return content


def test_key_iv_on_file(file_path: Path, secret_key: bytes, iv: bytes) -> bool:
    """
    Test key/iv validity with multiple sample checks
    """
    sample_lines_checked = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if (
                line
                and not line.isdigit()
                and "-->" not in line
                and is_valid_base64(line)
            ):
                try:
                    encrypted_bytes = base64.b64decode(line)
                    if len(encrypted_bytes) % 16 == 0:
                        decrypted = decrypt_content(line, secret_key, iv)
                        if decrypted != line:  # Verify actual decryption happened
                            sample_lines_checked += 1
                            if sample_lines_checked >= 3:
                                return True
                except:
                    continue
    return sample_lines_checked > 0


def process_file(file_path: Path, output_folder: Path, secret_key: bytes, iv: bytes):
    """
    Process file with detailed decryption tracking
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    decryption_fail_count = 0
    total_encrypted_lines = 0
    decrypted_lines = []
    line_details = []

    for line_num, line in enumerate(lines, 1):
        original_line = line.strip("\n")
        if (
            original_line
            and not original_line.strip().isdigit()
            and "-->" not in original_line
        ):
            total_encrypted_lines += 1
            decrypted = decrypt_content(original_line.strip(), secret_key, iv)
            if decrypted == original_line:
                decryption_fail_count += 1
                line_details.append(f"Line {line_num}: Failed to decrypt")
            decrypted_lines.append(decrypted)
        else:
            decrypted_lines.append(original_line)

    # Prepare output
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / (file_path.stem + "_decrypted.srt")

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(decrypted_lines))

    # Print detailed results
    success_count = total_encrypted_lines - decryption_fail_count
    print(f"\n{BLUE}=== Hasil Dekripsi ==={RESET}")
    print(
        f"{GREEN}✔ Berhasil didekripsi: {success_count}/{total_encrypted_lines} baris{RESET}"
    )

    if decryption_fail_count > 0:
        print(f"{YELLOW}⚠ Gagal didekripsi: {decryption_fail_count} baris{RESET}")
        if len(line_details) > 0:
            print(f"{YELLOW}Detail baris gagal (5 pertama):{RESET}")
            for detail in line_details[:5]:
                print(f" - {detail}")
            if len(line_details) > 5:
                print(f" - ...dan {len(line_details)-5} baris lainnya")

    print(f"{CYAN}File output: {output_path}{RESET}")
    time.sleep(0.5)


def get_source_path(source_type):
    if source_type == "1":
        print(
            f"{CYAN}Seret file ke terminal atau tekan Enter untuk membuka File Explorer.{RESET}"
        )
        path = input("File Path: ").strip('"')

        if not path:
            root = tk.Tk()
            root.withdraw()
            path = filedialog.askopenfilename(
                filetypes=[("Subtitle Files", "*.srt *.txt")]
            )

        return Path(path) if path else None

    elif source_type == "2":
        print(
            f"{CYAN}Seret folder ke terminal atau tekan Enter untuk membuka File Explorer.{RESET}"
        )
        path = input("Folder Path: ").strip('"')

        if not path:
            root = tk.Tk()
            root.withdraw()
            path = filedialog.askdirectory()

        return Path(path) if path else None

    return None


def select_key_iv(presets):
    while True:
        clear_screen()
        print(f"{CYAN}Pilih Preset Key/IV:{RESET}")
        for idx, preset in enumerate(presets.keys(), 1):
            print(f"{idx}. {preset}")
        print(f"{len(presets) + 1}. Manual Input")
        print(f"0. Kembali")

        choice = input(f"{YELLOW}Pilihan: {RESET}").strip()

        if choice == "0":
            return None, None

        try:
            choice = int(choice)
        except ValueError:
            print(f"{RED}Pilihan harus berupa angka!{RESET}")
            time.sleep(1)
            continue

        if 1 <= choice <= len(presets):
            selected_preset = list(presets.keys())[choice - 1]
            return presets[selected_preset]["key"].encode("utf-8"), presets[
                selected_preset
            ]["iv"].encode("utf-8")
        elif choice == len(presets) + 1:
            key = input("Masukkan Secret Key (16 karakter): ").encode("utf-8")
            iv = input("Masukkan IV (16 karakter): ").encode("utf-8")
            if len(key) == 16 and len(iv) == 16:
                return key, iv
            print(f"{RED}Key dan IV harus tepat 16 karakter!{RESET}")
            time.sleep(1)
        else:
            print(f"{RED}Pilihan tidak valid!{RESET}")
            time.sleep(1)


def main_menu():
    presets = load_presets()

    while True:
        clear_screen()
        print(f"{BOLD}{YELLOW}KISSKH SUBTITLE DECRYPTOR (CLI Version){RESET}")
        print(f"{CYAN}Algoritma: AES-128 CBC + BASE64{RESET}\n")

        print("Pilih metode input:")
        print("1. File Tunggal")
        print("2. Seluruh Folder")
        print("0. Keluar")
        source_type = input(f"{YELLOW}Pilihan (1/2/0): {RESET}").strip()

        if source_type == "0":
            print(f"{GREEN}Terima kasih!{RESET}")
            break

        source_path = get_source_path(source_type)

        if not source_path or not source_path.exists():
            print(f"{RED}File/Folder tidak ditemukan!{RESET}")
            input("Tekan Enter untuk kembali...")
            continue

        if source_type == "1":
            if source_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                print(f"{RED}Format file tidak didukung!{RESET}")
                input("Tekan Enter untuk kembali...")
                continue
            files = [source_path]
            output_folder = source_path.parent / "decrypted"
        else:
            files = [
                f
                for f in source_path.glob("*")
                if f.suffix.lower() in SUPPORTED_EXTENSIONS
            ]
            if not files:
                print(f"{RED}Tidak ada file SRT/TXT yang ditemukan!{RESET}")
                input("Tekan Enter untuk kembali...")
                continue
            output_folder = source_path / "decrypted"

        secret_key, iv = select_key_iv(presets)
        if not secret_key or not iv:
            continue

        success_files = []
        fail_files = []

        for file in files:
            if test_key_iv_on_file(file, secret_key, iv):
                process_file(file, output_folder, secret_key, iv)
                success_files.append(file.name)
            else:
                print(f"{RED}❌ Key/IV tidak cocok untuk: {file.name}{RESET}")
                fail_files.append(file.name)

        print(f"\n{BOLD}{BLUE}=== Ringkasan Akhir ==={RESET}")
        print(f"{GREEN}✔ Berhasil diproses: {len(success_files)} file{RESET}")
        if fail_files:
            print(f"{RED}❌ Gagal diproses: {len(fail_files)} file{RESET}")
            for fail in fail_files[:5]:
                print(f" - {fail}")
            if len(fail_files) > 5:
                print(f" - ...dan {len(fail_files)-5} file lainnya")

        print(f"\n{CYAN}Semua file output disimpan di: {output_folder}{RESET}")
        input("\nTekan Enter untuk kembali ke menu utama...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{RED}Program dihentikan oleh pengguna.{RESET}")
    except Exception as e:
        print(f"\n{RED}Error tidak terduga: {e}{RESET}")
