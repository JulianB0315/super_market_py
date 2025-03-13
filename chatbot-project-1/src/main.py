import customtkinter as ctk
from bot.handlers import MessageHandler

class LoginWindow(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.title("Login")
        self.geometry("400x300")
        self.configure(fg_color="#2C2F33")

        self.label_email = ctk.CTkLabel(self, text="Correo:", text_color="#FFFFFF", font=("Helvetica", 14))
        self.label_email.pack(pady=10)
        self.entry_email = ctk.CTkEntry(self, width=300, fg_color="#23272A", text_color="#FFFFFF", font=("Helvetica", 14))
        self.entry_email.pack(pady=10)

        self.label_password = ctk.CTkLabel(self, text="Contraseña:", text_color="#FFFFFF", font=("Helvetica", 14))
        self.label_password.pack(pady=10)
        self.entry_password = ctk.CTkEntry(self, width=300, show="*", fg_color="#23272A", text_color="#FFFFFF", font=("Helvetica", 14))
        self.entry_password.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Iniciar Sesión", command=self.login, fg_color="#7289DA", text_color="white", font=("Helvetica", 14))
        self.login_button.pack(pady=20)

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        handler = MessageHandler()
        response = handler.login(f"{email},{password}")
        if handler.user_logged_in:
            self.on_login_success(handler)
            self.after(100, self.withdraw) 
        else:
            ctk.CTkLabel(self, text=response, text_color="#FF0000", font=("Helvetica", 12)).pack(pady=5)

class ChatBotApp(ctk.CTk):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.title("ChatBot")
        self.geometry("600x500")
        self.configure(fg_color="#2C2F33")

        self.chat_frame = ctk.CTkFrame(self, fg_color="#2C2F33")
        self.chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.chat_log = ctk.CTkTextbox(self.chat_frame, state='disabled', width=50, height=20, fg_color="#23272A", text_color="#FFFFFF", font=("Helvetica", 14), wrap="word")
        self.chat_log.pack(padx=10, pady=10, fill="both", expand=True)

        self.entry_box = ctk.CTkEntry(self, width=400, fg_color="#23272A", text_color="#FFFFFF", font=("Helvetica", 14))
        self.entry_box.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.entry_box.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self, text="Enviar", command=self.send_message, fg_color="#7289DA", text_color="white", font=("Helvetica", 14))
        self.send_button.pack(side="right", padx=10, pady=10)

    def send_message(self, event=None):
        user_input = self.entry_box.get()
        if user_input.lower() in ["salir", "adiós"]:
            self.quit()
            return

        self.chat_log.configure(state='normal')
        self.chat_log.insert("end", "Tú: " + user_input + "\n", "user")
        self.entry_box.delete(0, "end")

        response = self.handler.handle_message(user_input)
        self.chat_log.insert("end", "Bot: " + response + "\n", "bot")
        self.chat_log.configure(state='disabled')
        self.chat_log.yview("end")

def on_login_success(handler):
    app = ChatBotApp(handler)
    app.mainloop()

if __name__ == "__main__":
    login_window = LoginWindow(on_login_success)
    login_window.mainloop()