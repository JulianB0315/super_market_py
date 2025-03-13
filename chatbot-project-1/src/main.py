import tkinter as tk
from tkinter import scrolledtext
from bot.handlers import MessageHandler

class ChatBotApp:
    def __init__(self, root):
        self.handler = MessageHandler()
        self.root = root
        self.root.title("ChatBot")
        self.root.configure(bg="#2C2F33")
        
        self.chat_frame = tk.Frame(root, bg="#2C2F33")
        self.chat_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.chat_log = scrolledtext.ScrolledText(self.chat_frame, state='disabled', width=50, height=20, bg="#23272A", fg="#FFFFFF", font=("Helvetica", 14), wrap=tk.WORD)
        self.chat_log.pack(padx=10, pady=10)
        
        self.entry_box = tk.Entry(root, width=40, bg="#23272A", fg="#FFFFFF", font=("Helvetica", 14))
        self.entry_box.grid(row=1, column=0, padx=10, pady=10)
        self.entry_box.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(root, text="Enviar", command=self.send_message, bg="#7289DA", fg="white", font=("Helvetica", 14))
        self.send_button.grid(row=1, column=1, padx=10, pady=10)
        
    def send_message(self, event=None):
        user_input = self.entry_box.get()
        if user_input.lower() in ["salir", "adiós"]:
            self.root.quit()
            return
        
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, "Tú: " + user_input + "\n", "user")
        self.entry_box.delete(0, tk.END)
        
        response = self.handler.handle_message(user_input)
        self.chat_log.insert(tk.END, "Bot: " + response + "\n", "bot")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()