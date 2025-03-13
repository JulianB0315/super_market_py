# Chatbot Project

Este proyecto es un chatbot simple desarrollado en Python. El chatbot está diseñado para recibir mensajes y responder de manera adecuada utilizando un conjunto de respuestas predefinidas.

## Estructura del Proyecto

```
chatbot-project
├── src
│   ├── main.py          # Punto de entrada de la aplicación
│   ├── bot
│   │   ├── __init__.py  # Paquete del bot
│   │   ├── handlers.py   # Manejo de mensajes
│   │   └── responses.py  # Respuestas predefinidas
│   └── utils
│       └── __init__.py  # Paquete de utilidades
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación del proyecto
```

## Requisitos

Asegúrate de tener Python instalado en tu sistema. Este proyecto utiliza las siguientes dependencias:

- flask
- requests

Puedes instalar las dependencias ejecutando:

```
pip install -r requirements.txt
```

## Ejecución

Para ejecutar el chatbot, utiliza el siguiente comando:

```
python src/main.py
```

Esto iniciará el chatbot y comenzará a recibir mensajes.