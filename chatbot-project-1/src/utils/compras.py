from load_data import load_data

def showCategories():
    productos = load_data('chatbot-project-1/src/data/productos.csv')
    categorias = productos['categoria'].unique()
    print("Categorías disponibles:")
    for categoria in categorias:
        print(f"🔹 {categoria}")
