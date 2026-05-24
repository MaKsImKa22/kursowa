import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from cryptography.fernet import Fernet
import datetime

class FileEncryptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 FILE ENCRYPTOR PRO - Шифрування файлів")
        self.root.geometry("850x650")
        self.root.resizable(True, True)
        
        # Змінні
        self.key = None
        self.fernet = None
        self.current_file = None
        self.theme_color = "#2c3e50"
        self.accent_color = "#3498db"
        
        # Налаштування стилю
        self.setup_styles()
        
        # Створення інтерфейсу
        self.create_widgets()
        
        # Центруємо вікно
        self.center_window()
        
    def center_window(self):
        """Центрує вікно на екрані"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Налаштування стилів"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Кольорова схема
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground=self.theme_color)
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground=self.theme_color)
        style.configure('Status.TLabel', font=('Arial', 10))
        style.configure('Action.TButton', font=('Arial', 10, 'bold'), padding=10)
        style.configure('Browse.TButton', font=('Arial', 9), padding=5)
        
    def create_widgets(self):
        """Створення всіх віджетів"""
        
        # Головний контейнер
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame, 
            text="🔐 FILE ENCRYPTOR PRO", 
            style='Title.TLabel'
        )
        title_label.pack(side=tk.LEFT)
        
        # Статус ключа
        self.key_status_label = ttk.Label(
            title_frame,
            text="⚫ Ключ не завантажено",
            style='Status.TLabel',
            foreground="red"
        )
        self.key_status_label.pack(side=tk.RIGHT)
        
        # Ноутбук для вкладок
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Вкладка 1: Управління ключами
        self.create_key_tab()
        
        # Вкладка 2: Шифрування
        self.create_encrypt_tab()
        
        # Вкладка 3: Дешифрування
        self.create_decrypt_tab()
        
        # Вкладка 4: Інформація
        self.create_info_tab()
        
        # Статус бар
        self.create_status_bar(main_frame)
    
    def create_key_tab(self):
        """Вкладка управління ключами"""
        key_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(key_frame, text="🔑 Ключі")
        
        # Заголовок
        ttk.Label(
            key_frame, 
            text="Управління ключами шифрування",
            style='Header.TLabel'
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Фрейм для генерації ключа
        gen_frame = ttk.LabelFrame(key_frame, text="Генерація ключа", padding="15")
        gen_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            gen_frame, 
            text="Згенерувати новий випадковий ключ:"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        gen_btn = ttk.Button(
            gen_frame,
            text="🔄 Згенерувати новий ключ",
            command=self.generate_key,
            style='Action.TButton'
        )
        gen_btn.pack(anchor=tk.W, pady=5)
        
        # Фрейм для збереження ключа
        save_frame = ttk.LabelFrame(key_frame, text="Збереження ключа", padding="15")
        save_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            save_frame, 
            text="Зберегти поточний ключ у файл:"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        save_btn = ttk.Button(
            save_frame,
            text="💾 Зберегти ключ",
            command=self.save_key,
            style='Action.TButton'
        )
        save_btn.pack(anchor=tk.W, pady=5)
        
        # Фрейм для завантаження ключа (з вибором файлу)
        load_frame = ttk.LabelFrame(key_frame, text="Завантаження ключа", padding="15")
        load_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            load_frame, 
            text="Завантажити існуючий ключ з файлу:"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Фрейм для вибору файлу
        file_select_frame = ttk.Frame(load_frame)
        file_select_frame.pack(fill=tk.X, pady=5)
        
        self.key_file_path = tk.StringVar()
        key_file_entry = ttk.Entry(
            file_select_frame,
            textvariable=self.key_file_path,
            font=('Arial', 10),
            state='readonly'
        )
        key_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(
            file_select_frame,
            text="🔍 Огляд",
            command=self.browse_key_file,
            style='Browse.TButton',
            width=10
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Кнопка завантаження вибраного ключа
        load_btn = ttk.Button(
            load_frame,
            text="📂 Завантажити вибраний ключ",
            command=self.load_selected_key,
            style='Action.TButton'
        )
        load_btn.pack(anchor=tk.W, pady=10)
        
        # Фрейм для відображення ключа
        display_frame = ttk.LabelFrame(key_frame, text="Поточний ключ", padding="15")
        display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.key_display = scrolledtext.ScrolledText(
            display_frame,
            height=4,
            font=('Courier', 10),
            wrap=tk.WORD,
            bg='#f8f9fa'
        )
        self.key_display.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка копіювання ключа
        copy_btn = ttk.Button(
            display_frame,
            text="📋 Копіювати ключ",
            command=self.copy_key_to_clipboard,
            style='Browse.TButton'
        )
        copy_btn.pack(anchor=tk.E, pady=5)
    
    def create_encrypt_tab(self):
        """Вкладка шифрування"""
        encrypt_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(encrypt_frame, text="🔒 Шифрування")
        
        # Заголовок
        ttk.Label(
            encrypt_frame, 
            text="Шифрування файлів",
            style='Header.TLabel'
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Фрейм вибору файлу
        file_frame = ttk.LabelFrame(encrypt_frame, text="Вибір файлу", padding="15")
        file_frame.pack(fill=tk.X, pady=10)
        
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill=tk.X, pady=5)
        
        self.encrypt_file_path = tk.StringVar()
        file_entry = ttk.Entry(
            file_select_frame,
            textvariable=self.encrypt_file_path,
            font=('Arial', 10),
            state='readonly'
        )
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(
            file_select_frame,
            text="📁 Огляд",
            command=self.browse_encrypt_file,
            style='Browse.TButton',
            width=10
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Фрейм налаштувань
        options_frame = ttk.LabelFrame(encrypt_frame, text="Налаштування", padding="15")
        options_frame.pack(fill=tk.X, pady=10)
        
        self.delete_original = tk.BooleanVar(value=False)
        delete_check = ttk.Checkbutton(
            options_frame,
            text="🗑️ Видалити оригінальний файл після шифрування",
            variable=self.delete_original
        )
        delete_check.pack(anchor=tk.W, pady=5)
        
        # Кнопка шифрування
        encrypt_btn = ttk.Button(
            encrypt_frame,
            text="🔐 ЗАШИФРУВАТИ ФАЙЛ",
            command=self.encrypt_file,
            style='Action.TButton'
        )
        encrypt_btn.pack(pady=20)
        
        # Інформація
        info_text = """
        ℹ️ Інформація:
        • Підтримуються файли будь-якого розширення
        • Зашифрований файл отримає розширення .encrypted
        • Для розшифрування потрібен той самий ключ
        """
        info_label = ttk.Label(
            encrypt_frame,
            text=info_text,
            justify=tk.LEFT,
            foreground="#666"
        )
        info_label.pack(anchor=tk.W, pady=10)
    
    def create_decrypt_tab(self):
        """Вкладка дешифрування"""
        decrypt_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(decrypt_frame, text="🔓 Дешифрування")
        
        # Заголовок
        ttk.Label(
            decrypt_frame, 
            text="Дешифрування файлів",
            style='Header.TLabel'
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Фрейм вибору файлу
        file_frame = ttk.LabelFrame(decrypt_frame, text="Вибір файлу", padding="15")
        file_frame.pack(fill=tk.X, pady=10)
        
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill=tk.X, pady=5)
        
        self.decrypt_file_path = tk.StringVar()
        file_entry = ttk.Entry(
            file_select_frame,
            textvariable=self.decrypt_file_path,
            font=('Arial', 10),
            state='readonly'
        )
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(
            file_select_frame,
            text="📁 Огляд",
            command=self.browse_decrypt_file,
            style='Browse.TButton',
            width=10
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Кнопка дешифрування
        decrypt_btn = ttk.Button(
            decrypt_frame,
            text="🔓 ДЕШИФРУВАТИ ФАЙЛ",
            command=self.decrypt_file,
            style='Action.TButton'
        )
        decrypt_btn.pack(pady=20)
        
        # Інформація
        info_text = """
        ℹ️ Інформація:
        • Виберіть зашифрований файл (.encrypted)
        • Ключ для дешифрування завантажте на вкладці 🔑 Ключі
        • Розшифрований файл збережеться в тій же папці
        """
        info_label = ttk.Label(
            decrypt_frame,
            text=info_text,
            justify=tk.LEFT,
            foreground="#666"
        )
        info_label.pack(anchor=tk.W, pady=10)
    
    def create_info_tab(self):
        """Вкладка інформації"""
        info_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(info_frame, text="ℹ️ Інформація")
        
        # Заголовок
        ttk.Label(
            info_frame, 
            text="Про програму",
            style='Header.TLabel'
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Інформація
        info_text = """
        🔐 FILE ENCRYPTOR PRO v1.0
        
        Програма для безпечного шифрування та дешифрування 
        файлів будь-якого розширення.
        
        ⚙️ Як це працює:
        • Використовується алгоритм AES-256
        • Ключі генеруються випадковим чином
        • Кожен файл шифрується індивідуально
        
        📋 Інструкція:
        1. 🔑 На вкладці "Ключі":
           - Згенеруйте новий ключ АБО
           - Виберіть файл з ключем та завантажте його
        2. 🔒 На вкладці "Шифрування":
           - Виберіть файл та зашифруйте його
        3. 🔓 На вкладці "Дешифрування":
           - Виберіть зашифрований файл та дешифруйте
        
        ⚠️ Важливо:
        • Зберігайте ключі в безпечному місці
        • Без ключа неможливо розшифрувати файли
        • Не видаляйте ключ після шифрування
        • Різні ключі для різних файлів
        
        👨‍💻 Розробник: Lagsi
        📅 Версія: 1.0 (2026)
        """
        
        info_display = scrolledtext.ScrolledText(
            info_frame,
            height=20,
            font=('Arial', 11),
            wrap=tk.WORD,
            bg='#f8f9fa'
        )
        info_display.pack(fill=tk.BOTH, expand=True)
        info_display.insert(tk.END, info_text)
        info_display.config(state=tk.DISABLED)
    
    def create_status_bar(self, parent):
        """Створення статус бару"""
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN, padding="5")
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="✅ Готовий до роботи",
            style='Status.TLabel'
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Таймер
        self.time_label = ttk.Label(
            status_frame,
            text=datetime.datetime.now().strftime("%H:%M:%S"),
            style='Status.TLabel'
        )
        self.time_label.pack(side=tk.RIGHT)
        
        # Оновлення часу
        self.update_time()
    
    def update_time(self):
        """Оновлення часу в статус барі"""
        self.time_label.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def update_key_status(self):
        """Оновлення статусу ключа"""
        if self.fernet:
            self.key_status_label.config(
                text="🟢 Ключ завантажено",
                foreground="green"
            )
            if self.key:
                self.key_display.delete(1.0, tk.END)
                self.key_display.insert(tk.END, self.key.decode())
                self.key_display.see(1.0)
        else:
            self.key_status_label.config(
                text="⚫ Ключ не завантажено",
                foreground="red"
            )
            self.key_display.delete(1.0, tk.END)
    
    def browse_key_file(self):
        """Вибір файлу з ключем"""
        filename = filedialog.askopenfilename(
            title="Виберіть файл з ключем",
            filetypes=[
                ("Key files", "*.key"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.key_file_path.set(filename)
            self.status_label.config(text=f"📁 Вибрано ключ: {os.path.basename(filename)}")
    
    def load_selected_key(self):
        """Завантаження вибраного ключа"""
        key_file = self.key_file_path.get()
        if not key_file:
            messagebox.showwarning("Увага", "Спочатку виберіть файл з ключем!")
            return
        
        try:
            with open(key_file, 'rb') as f:
                self.key = f.read()
            self.fernet = Fernet(self.key)
            self.update_key_status()
            self.status_label.config(text=f"✅ Ключ завантажено: {os.path.basename(key_file)}")
            messagebox.showinfo("Успіх", f"Ключ успішно завантажено з файлу:\n{key_file}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити ключ: {e}")
    
    def generate_key(self):
        """Генерація нового ключа"""
        try:
            self.key = Fernet.generate_key()
            self.fernet = Fernet(self.key)
            self.update_key_status()
            self.status_label.config(text="✅ Новий ключ згенеровано")
            messagebox.showinfo("Успіх", "Новий ключ успішно згенеровано!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося згенерувати ключ: {e}")
    
    def save_key(self):
        """Збереження ключа у файл"""
        if not self.key:
            messagebox.showwarning("Увага", "Спочатку згенеруйте або завантажте ключ!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Зберегти ключ",
            defaultextension=".key",
            filetypes=[("Key files", "*.key"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'wb') as f:
                    f.write(self.key)
                self.status_label.config(text=f"✅ Ключ збережено: {os.path.basename(filename)}")
                messagebox.showinfo("Успіх", f"Ключ збережено у файл:\n{filename}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти ключ: {e}")
    
    def copy_key_to_clipboard(self):
        """Копіювання ключа в буфер обміну"""
        if not self.key:
            messagebox.showwarning("Увага", "Немає ключа для копіювання!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(self.key.decode())
        self.status_label.config(text="📋 Ключ скопійовано в буфер обміну")
        messagebox.showinfo("Інформація", "Ключ скопійовано в буфер обміну!")
    
    def browse_encrypt_file(self):
        """Вибір файлу для шифрування"""
        filename = filedialog.askopenfilename(
            title="Виберіть файл для шифрування"
        )
        if filename:
            self.encrypt_file_path.set(filename)
            self.status_label.config(text=f"📁 Вибрано файл: {os.path.basename(filename)}")
    
    def browse_decrypt_file(self):
        """Вибір файлу для дешифрування"""
        filename = filedialog.askopenfilename(
            title="Виберіть файл для дешифрування",
            filetypes=[
                ("Encrypted files", "*.encrypted"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.decrypt_file_path.set(filename)
            self.status_label.config(text=f"📁 Вибрано файл: {os.path.basename(filename)}")
    
    def encrypt_file(self):
        """Шифрування файлу"""
        if not self.fernet:
            messagebox.showwarning(
                "Увага", 
                "Спочатку завантажте або згенеруйте ключ!\n\n"
                "Перейдіть на вкладку 🔑 Ключі та:\n"
                "1. Згенеруйте новий ключ АБО\n"
                "2. Виберіть файл з ключем та натисніть 'Завантажити вибраний ключ'"
            )
            self.notebook.select(0)  # Перемикаємо на вкладку ключів
            return
        
        file_path = self.encrypt_file_path.get()
        if not file_path:
            messagebox.showwarning("Увага", "Виберіть файл для шифрування!")
            return
        
        # Запускаємо в окремому потоці
        threading.Thread(target=self._encrypt_thread, args=(file_path,), daemon=True).start()
    
    def _encrypt_thread(self, file_path):
        """Потік для шифрування"""
        try:
            self.root.after(0, lambda: self.status_label.config(text="🔄 Шифрування..."))
            
            # Читаємо файл
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Шифруємо
            encrypted_data = self.fernet.encrypt(file_data)
            
            # Зберігаємо
            output_file = file_path + '.encrypted'
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Видаляємо оригінал якщо потрібно
            if self.delete_original.get():
                os.remove(file_path)
                status_msg = f"✅ Файл зашифровано, оригінал видалено"
            else:
                status_msg = f"✅ Файл зашифровано"
            
            self.root.after(0, lambda: self.status_label.config(text=status_msg))
            self.root.after(0, lambda: messagebox.showinfo(
                "Успіх", 
                f"✅ Файл успішно зашифровано!\n\n"
                f"📁 Оригінал: {os.path.basename(file_path)}\n"
                f"🔐 Зашифрований: {os.path.basename(output_file)}"
            ))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Помилка", 
                f"❌ Помилка шифрування:\n{e}"
            ))
            self.root.after(0, lambda: self.status_label.config(text="❌ Помилка шифрування"))
    
    def decrypt_file(self):
        """Дешифрування файлу"""
        if not self.fernet:
            messagebox.showwarning(
                "Увага", 
                "Спочатку завантажте ключ для дешифрування!\n\n"
                "Перейдіть на вкладку 🔑 Ключі та:\n"
                "1. Виберіть файл з ключем (кнопка 'Огляд')\n"
                "2. Натисніть 'Завантажити вибраний ключ'"
            )
            self.notebook.select(0)  # Перемикаємо на вкладку ключів
            return
        
        file_path = self.decrypt_file_path.get()
        if not file_path:
            messagebox.showwarning("Увага", "Виберіть файл для дешифрування!")
            return
        
        # Запускаємо в окремому потоці
        threading.Thread(target=self._decrypt_thread, args=(file_path,), daemon=True).start()
    
    def _decrypt_thread(self, file_path):
        """Потік для дешифрування"""
        try:
            self.root.after(0, lambda: self.status_label.config(text="🔄 Дешифрування..."))
            
            # Читаємо файл
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Дешифруємо
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Визначаємо назву вихідного файлу
            if file_path.endswith('.encrypted'):
                output_file = file_path[:-10]
            else:
                output_file = file_path + '.decrypted'
            
            # Зберігаємо
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            self.root.after(0, lambda: self.status_label.config(text="✅ Файл дешифровано"))
            self.root.after(0, lambda: messagebox.showinfo(
                "Успіх", 
                f"✅ Файл успішно дешифровано!\n\n"
                f"🔐 Зашифрований: {os.path.basename(file_path)}\n"
                f"📁 Дешифрований: {os.path.basename(output_file)}"
            ))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Помилка", 
                f"❌ Помилка дешифрування:\n{e}\n\n"
                f"Можливо, ви використовуєте неправильний ключ?"
            ))
            self.root.after(0, lambda: self.status_label.config(text="❌ Помилка дешифрування"))

def main():
    root = tk.Tk()
    app = FileEncryptorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()