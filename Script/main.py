import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from models.recommendations import RecommendationModel 

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
            user_row = df_user[(df_user['nombres'] == user)]
            
            if not user_row.empty:
                if user_row.iloc[0]['contraseña'] == password:
                    user_id = user_row.iloc[0]['id']
                    self.root.destroy()
                    open_menu(user_id)
                    messagebox.showerror("Error", "Contraseña incorrecta")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")
        except FileNotFoundError:
            messagebox.showerror("Error", "No hay usuarios registrados")

class MenuApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("📢 Supermercado 📢")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.frame, text="Bienvenido al Supermercado", font=("Arial", 16)).pack(pady=10)

        opciones = ["Recomendaciones", "Salir"]
        for opcion in opciones:
            button = ctk.CTkButton(self.frame, text=opcion, command=lambda opt=opcion: self.opcion_seleccionada(opt))
            button.pack(pady=5)

    def opcion_seleccionada(self, opcion):
        if opcion == "Recomendaciones":
            self.mostrar_recomendaciones()
        elif opcion == "Salir":
            self.root.destroy()
        else:
            messagebox.showinfo("Opción seleccionada", f"Has seleccionado {opcion}")


def open_menu(user_id):
    menu_root = ctk.CTk()
    MenuApp(menu_root, user_id)
    menu_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    LoginApp(root)
    root.mainloop()