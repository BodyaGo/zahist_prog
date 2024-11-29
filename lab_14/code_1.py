import itertools 
import time      
import threading 
import tkinter as tk

class BruteForceApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторна робота №14") 

        self.password_var = tk.StringVar()  
        self.charset = ""  
        self.is_running = False
        self.found_password = None
        self.time_taken = None  
        self.total_combinations = 0

        self.setup_layout()

    def setup_layout(self):
        tk.Label(self.root, text="Введіть пароль для пошуку:", bg="#f0f0f0", fg="#333333").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.root, textvariable=self.password_var, width=30, bg="#ffffff", fg="#000000").grid(row=1, column=0, padx=5, pady=5)

        tk.Label(self.root, text="Оберіть символи для перебору:", bg="#f0f0f0", fg="#333333").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.lowercase_var = tk.BooleanVar()
        self.uppercase_var = tk.BooleanVar()
        self.digits_var = tk.BooleanVar()
        self.special_var = tk.BooleanVar()
        self.space_var = tk.BooleanVar()

        tk.Checkbutton(self.root, text="Малі латинські літери (a-z)", variable=self.lowercase_var, bg="#f0f0f0").grid(row=3, column=0, sticky="w")
        tk.Checkbutton(self.root, text="Великі латинські літери (A-Z)", variable=self.uppercase_var, bg="#f0f0f0").grid(row=4, column=0, sticky="w")
        tk.Checkbutton(self.root, text="Цифри (0-9)", variable=self.digits_var, bg="#f0f0f0").grid(row=5, column=0, sticky="w")
        tk.Checkbutton(self.root, text="Спеціальні символи (!@#...)", variable=self.special_var, bg="#f0f0f0").grid(row=6, column=0, sticky="w")
        tk.Checkbutton(self.root, text="Пробіли", variable=self.space_var, bg="#f0f0f0").grid(row=7, column=0, sticky="w")

        self.start_button = tk.Button(self.root, text="Здійснити пошук", command=self.start_brute_force)
        self.start_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)


    def update_charset(self):
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        special = "!@#$%^&*()-_=+[]{}|;:',.<>/?"
        space = " "

        self.charset = ""
        if self.lowercase_var.get():
            self.charset += lowercase
        if self.uppercase_var.get():
            self.charset += uppercase
        if self.digits_var.get():
            self.charset += digits
        if self.special_var.get():
            self.charset += special
        if self.space_var.get():
            self.charset += space

    def calculate_total_combinations(self, password_length):
        charset_length = len(self.charset)
        self.total_combinations = sum(charset_length ** i for i in range(1, password_length + 1))

    def start_brute_force(self):
        self.update_charset()
        self.is_running = True
        self.start_button.config(state="disabled") 
        print("Початок атаки")

        self.thread = threading.Thread(target=self.brute_force)
        self.thread.start()

    def brute_force(self):
        password = self.password_var.get() 
        start_time = time.time()
        length = len(password)
        self.calculate_total_combinations(length) 
        attempt_count = 0

        for guess_length in range(1, length + 1):
            if not self.is_running:
                break
            for guess in itertools.product(self.charset, repeat=guess_length):
                if not self.is_running:
                    break
                guess_str = ''.join(guess)
                attempt_count += 1

                print(f"Спроба {attempt_count}: {guess_str}")

                if guess_str == password:
                    self.is_running = False
                    self.found_password = guess_str
                    self.time_taken = time.time() - start_time
                    print(f"Пароль '{self.found_password}' знайдено на спробі {attempt_count} за {self.time_taken:.2f} секунд.")
                    self.start_button.config(state="normal")
                    return

        if not self.found_password:
            print("Пароль не знайдено")
        self.start_button.config(state="normal")
if __name__ == "__main__":
    root = tk.Tk()
    app = BruteForceApp(root)
    root.mainloop()
