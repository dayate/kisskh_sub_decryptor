import base64
import json
import time
from pathlib import Path
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar

SUPPORTED_EXTENSIONS = [".srt", ".txt"]


class SubtitleDecryptorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kisskh Subtitle Decryptor")
        self.geometry("700x800")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.source_path = None
        self.secret_key = None
        self.iv = None
        self.presets = self.load_config()

        self.create_widgets()

    def load_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)["presets"]
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat config.json: {e}")
            return {"Default": {"key": "AmSmZVcH93UQUezi", "iv": "ReBKWW8cqdjPEnF6"}}

    def create_widgets(self):
        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header Section
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="KISSKH SUBTITLE DECRYPTOR",
            font=("Helvetica", 20, "bold"),
        ).pack(pady=5)
        ctk.CTkLabel(header_frame, text="Algoritma: AES-128 CBC + BASE64").pack()

        # Key/IV Section
        key_iv_frame = ctk.CTkFrame(main_frame)
        key_iv_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(key_iv_frame, text="Preset Secret Key+IV").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.key_iv_option = StringVar(value="Pilih Preset")
        self.option_menu = ctk.CTkOptionMenu(
            key_iv_frame,
            variable=self.key_iv_option,
            values=list(self.presets.keys()) + ["Manual Input"],
            command=self.update_key_iv,
        )
        self.option_menu.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(key_iv_frame, text="Secret Key (16 karakter)").grid(
            row=1, column=0, sticky="w", padx=5
        )
        self.key_entry = ctk.CTkEntry(key_iv_frame, width=300)
        self.key_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(key_iv_frame, text="IV (16 karakter)").grid(
            row=2, column=0, sticky="w", padx=5
        )
        self.iv_entry = ctk.CTkEntry(key_iv_frame, width=300)
        self.iv_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Button Section
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)

        self.select_file_btn = ctk.CTkButton(
            button_frame, text="Pilih File", command=self.select_file
        )
        self.select_file_btn.pack(side="left", padx=5, expand=True)

        self.select_folder_btn = ctk.CTkButton(
            button_frame, text="Pilih Folder", command=self.select_folder
        )
        self.select_folder_btn.pack(side="left", padx=5, expand=True)

        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Mulai Dekripsi",
            command=self.start_process,
            state="disabled",
            fg_color="green",
            hover_color="dark green",
        )
        self.start_btn.pack(side="left", padx=5, expand=True)

        # Progress Section
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", pady=10)

        self.progress_label = ctk.CTkLabel(progress_frame, text="Progres: 0%")
        self.progress_label.pack()

        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=5)

        # Log Section
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            log_frame,
            height=15,
            wrap="word",
            bg="#f0f0f0",
            fg="black",
            font=("Consolas", 10),
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure text tags
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("info", foreground="blue")

        self.log("Silakan pilih file atau folder subtitle.", "info")
        self.update_key_iv()

    def update_key_iv(self, _=None):
        choice = self.key_iv_option.get()
        self.key_entry.configure(state="normal")
        self.iv_entry.configure(state="normal")

        self.key_entry.delete(0, "end")
        self.iv_entry.delete(0, "end")

        if choice in self.presets:
            self.key_entry.insert(0, self.presets[choice]["key"])
            self.iv_entry.insert(0, self.presets[choice]["iv"])
            self.key_entry.configure(state="disabled")
            self.iv_entry.configure(state="disabled")

    def validate_key_iv(self):
        self.secret_key = self.key_entry.get().encode("utf-8")
        self.iv = self.iv_entry.get().encode("utf-8")

        if len(self.secret_key) != 16 or len(self.iv) != 16:
            messagebox.showerror("Error", "Secret Key dan IV harus tepat 16 karakter!")
            return False
        return True

    def is_valid_base64(self, s: str) -> bool:
        try:
            return base64.b64encode(base64.b64decode(s)) == s.encode()
        except:
            return False

    def test_key_iv_on_file(self, file_path: Path) -> bool:
        sample_lines_checked = 0
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if (
                    line
                    and not line.isdigit()
                    and "-->" not in line
                    and self.is_valid_base64(line)
                ):
                    try:
                        encrypted_bytes = base64.b64decode(line)
                        if len(encrypted_bytes) % 16 == 0:
                            decrypted = self.decrypt_content(line)
                            if decrypted != line:  # Verify actual decryption
                                sample_lines_checked += 1
                                if sample_lines_checked >= 3:
                                    return True
                    except:
                        continue
        return sample_lines_checked > 0

    def decrypt_content(self, encrypted_content: str) -> str:
        if not encrypted_content or not self.is_valid_base64(encrypted_content):
            return encrypted_content

        try:
            encrypted_bytes = base64.b64decode(encrypted_content)
            if len(encrypted_bytes) % 16 != 0:
                return encrypted_content

            cipher = AES.new(self.secret_key, AES.MODE_CBC, self.iv)
            decrypted = unpad(cipher.decrypt(encrypted_bytes), 16).decode(
                "utf-8", errors="ignore"
            )
            return decrypted
        except Exception as e:
            return encrypted_content

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Subtitle Files", "*.srt *.txt")]
        )
        if file_path:
            self.source_path = Path(file_path)
            self.log(f"File terpilih: {file_path}", "info")
            self.start_btn.configure(state="normal")

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.source_path = Path(folder_path)
            files = [
                f
                for f in self.source_path.glob("*")
                if f.suffix.lower() in SUPPORTED_EXTENSIONS
            ]
            self.log(f"Folder terpilih: {folder_path}", "info")
            self.log(f"Ditemukan {len(files)} file subtitle", "info")
            self.start_btn.configure(state="normal")

    def log(self, message, tag=None):
        self.log_text.insert("end", message + "\n", tag)
        self.log_text.see("end")
        self.update_idletasks()

    def process_file(self, file_path: Path, output_folder: Path):
        decryption_fail_count = 0
        total_encrypted_lines = 0

        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        decrypted_lines = []
        for line in lines:
            original_line = line.strip("\n")
            if (
                original_line
                and not original_line.strip().isdigit()
                and "-->" not in original_line
            ):
                total_encrypted_lines += 1
                decrypted = self.decrypt_content(original_line.strip())
                if decrypted == original_line:
                    decryption_fail_count += 1
                decrypted_lines.append(decrypted)
            else:
                decrypted_lines.append(original_line)

        output_folder.mkdir(parents=True, exist_ok=True)
        output_path = output_folder / (file_path.stem + "_decrypted.srt")

        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write("\n".join(decrypted_lines))

        success_count = total_encrypted_lines - decryption_fail_count
        self.log(
            f"✔ {file_path.name}: {success_count}/{total_encrypted_lines} baris berhasil",
            "success",
        )
        if decryption_fail_count > 0:
            self.log(f"⚠ {decryption_fail_count} baris gagal didekripsi", "warning")

    def start_process(self):
        if not self.validate_key_iv():
            return

        if not self.source_path:
            messagebox.showerror(
                "Error", "Silakan pilih file atau folder terlebih dahulu!"
            )
            return

        output_folder = (
            self.source_path.parent / "decrypted"
            if self.source_path.is_file()
            else self.source_path / "decrypted"
        )

        files = (
            [self.source_path]
            if self.source_path.is_file()
            else [
                f
                for f in self.source_path.glob("*")
                if f.suffix.lower() in SUPPORTED_EXTENSIONS
            ]
        )

        if not files:
            messagebox.showerror("Error", "Tidak ada file SRT/TXT yang ditemukan!")
            return

        self.log("\nMemulai proses dekripsi...", "info")
        self.progress_bar.set(0)
        self.update_idletasks()

        success_files = []
        fail_files = []

        for idx, file in enumerate(files):
            try:
                if self.test_key_iv_on_file(file):
                    self.process_file(file, output_folder)
                    success_files.append(file.name)
                else:
                    self.log(f"❌ Key/IV tidak cocok untuk: {file.name}", "error")
                    fail_files.append(file.name)
            except Exception as e:
                self.log(f"❌ Error memproses {file.name}: {str(e)}", "error")
                fail_files.append(file.name)

            # Update progress
            progress = (idx + 1) / len(files)
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"Progres: {int(progress * 100)}%")
            self.update_idletasks()

        # Show summary
        summary = (
            f"=== Hasil Dekripsi ===\n"
            f"✔ File berhasil: {len(success_files)}\n"
            f"❌ File gagal: {len(fail_files)}\n"
            f"📁 Output folder: {output_folder}"
        )

        self.log("\n" + summary, "info")
        messagebox.showinfo("Proses Selesai", summary)


if __name__ == "__main__":
    try:
        app = SubtitleDecryptorApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror(
            "Error Fatal", f"Aplikasi tidak dapat dijalankan: {str(e)}"
        )
