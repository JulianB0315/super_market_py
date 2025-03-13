import re
import random
import pandas as pd
from utils.compras import show_categories, products_by_categorie, show_all_products
from model.recommendations import RecommendationModel

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
        self.recommendation_model = RecommendationModel('chatbot-project-1/src/data/ventas.csv', 'chatbot-project-1/src/data/productos.csv')
        self.ventas = pd.read_csv('chatbot-project-1/src/data/ventas.csv')

    def handle_message(self, message):
        if not self.user_logged_in:
            return self.login(message)
        
        cleaned_message = self._clean_message(message)
        if "compras" in cleaned_message:
            return self.handle_compras(cleaned_message)
        elif "recomendaciones" in cleaned_message:
            return self.handle_recommendations()
        elif "historial" in cleaned_message:
            return self.handle_historial_compras()
        elif "todos los productos" in cleaned_message:
            return self.handle_all_products()
        
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

    def handle_compras(self, message):
        category = message.split("compras", 1)[1].strip()
        if not category:
            return "Por favor, especifica una categoría. Ejemplo: compras alimentos"
        
        productos_categoria = products_by_categorie(category)
        if productos_categoria is None or productos_categoria.empty:
            return f"No se encontraron productos en la categoría {category}."
        
        response = f"Productos en la categoría {category}:\n"
        for i, row in productos_categoria.iterrows():
            response += f"🔸 {row['nombre']} | 💰 {row['precio']} | ⭐ {row['puntuacion']}/5\n"
        return response

    def handle_recommendations(self):
        recomendaciones = self.recommendation_model.recommend(n=5)
        response = "Te recomiendo los siguientes productos:\n"
        for _, row in recomendaciones.iterrows():
            response += f"🔸 {row['nombre']} | 💰 {row['precio']} | {row['etiqueta']}\n"
        return response

    def handle_historial_compras(self):
        user_id = self.current_user['id']
        historial = self.ventas[self.ventas['id_user'] == user_id]
        if historial.empty:
            return "No tienes compras registradas."
        
        response = "Aquí está tu historial de compras:\n"
        for i, row in historial.iterrows():
            response += f"🔸 Producto ID: {row['id_producto']} | Cantidad: {row['cantidad']} | Fecha: {row['fecha']} | Total: {row['total']}\n"
        return response

    def handle_all_products(self):
        productos = show_all_products()
        response = "Aquí están todos los productos:\n"
        for i, row in productos.iterrows():
            response += f"🔸 {row['nombre']} | 💰 {row['precio']} | ⭐ {row['puntuacion']}/5\n"
        return response