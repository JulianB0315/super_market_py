import customtkinter as ctk
from tkinter import messagebox
import pandas as pd

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        # Frame principal
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.frame, text="Usuario:", font=("Arial", 14)).pack(pady=5)
        self.entry_user = ctk.CTkEntry(self.frame, width=250)
        self.entry_user.pack(pady=5)

        ctk.CTkLabel(self.frame, text="Contraseña:", font=("Arial", 14)).pack(pady=5)
        self.entry_pass = ctk.CTkEntry(self.frame, width=250, show="*")
        self.entry_pass.pack(pady=5)

        self.login_button = ctk.CTkButton(self.frame, text="Iniciar Sesión", command=self.check_login)
        self.login_button.pack(pady=15)
        
    def check_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        try:
            df_user = pd.read_csv('Script/data/usuarios.csv')
            print(df_user)
            if ((df_user['nombres'] == user) & (df_user['contraseña'] == password)).any():
                self.root.destroy()
                open_menu()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        except FileNotFoundError:
            messagebox.showerror("Error", "No hay usuarios registrados")

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📢 Supermercado 📢")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Frame principal
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(expand=True, padx=20, pady=20)

        self.text_area = ctk.CTkTextbox(self.frame, height=200, width=350, font=("Arial", 12))
        self.text_area.pack(pady=10)

        self.print_to_menu("Bienvenido al Supermercado")
        opciones = ["1️⃣. Opción 1", "2️⃣. Opción 2", "3️⃣. Opción 3", 
                    "4️⃣. Opción 4", "5️⃣. Opción 5", "6️⃣. Opción 6"]
        for opcion in opciones:
            self.print_to_menu(opcion)

    def print_to_menu(self, text):
        self.text_area.insert("end", text + '\n')

def open_menu():
    menu_root = ctk.CTk()
    MenuApp(menu_root)
    menu_root.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    LoginApp(root)
    root.mainloop()