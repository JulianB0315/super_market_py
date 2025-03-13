import re
import random
import pandas as pd

class MessageHandler:
    def __init__(self, csv_file='chatbot-project-1/src/bot/responses.csv'):
        self.responses = pd.read_csv(csv_file)
        self.positive_responses = [
            "¡Genial! Me alegra escuchar eso.",
            "¡Qué bien! ¿En qué más puedo ayudarte?",
            "¡Excelente! ¿Algo más que necesites?"
        ]
        self.negative_responses = [
            "Lo siento, no entiendo tu pregunta.",
            "No estoy seguro de cómo responder a eso.",
            "Podrías intentar preguntar de otra manera."
        ]
        self.user_logged_in = False
        self.current_user = None

    def handle_message(self, message):
        if not self.user_logged_in:
            return self.login(message)
        
        cleaned_message = self._clean_message(message)
        for _, response in self.responses.iterrows():
            if self._message_matches(cleaned_message, response):
                return response["response"]
        return self.response_negative()

    def _clean_message(self, message):
        return re.sub(r'[^\w\s]', '', message).lower()

    def _message_matches(self, message, response):
        message_words = message.split()
        keywords = response["keywords"].split() if pd.notna(response["keywords"]) else []
        required_words = response["required_words"].split() if pd.notna(response["required_words"]) else []
        if response.get("single_response"):
            return any(word in message_words for word in keywords)
        if required_words:
            return all(word in message_words for word in required_words) and any(word in message_words for word in keywords)
        return False

    def response_negative(self):
        return random.choice(self.negative_responses)

    def response_positive(self):
        return random.choice(self.positive_responses)

    def login(self, message):
        users = pd.read_csv('chatbot-project-1/src/data/usuarios.csv')
        email, password = message.split(',')
        user = users[(users['correo'] == email.strip()) & (users['contraseña'] == password.strip())]
        if not user.empty:
            self.user_logged_in = True
            self.current_user = user.iloc[0]
            return f"Bienvenido {self.current_user['nombres']} {self.current_user['apellidos']}!"
        else:
            return "Credenciales incorrectas. Por favor, intente de nuevo."