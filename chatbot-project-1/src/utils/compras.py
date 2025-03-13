from .load_data import load_data

productos = load_data('chatbot-project-1/src/data/productos.csv')
categorias = productos['categoria'].unique()

def show_categories():
    print("Categorías disponibles:")
    for categoria in categorias:
        print(f"🔹 {categoria}")

def products_by_categorie(categoria):
    productos_categoria = productos[productos['categoria'].str.lower() == categoria.lower()]
    if productos_categoria.empty:
        return None
    return productos_categoria

def show_all_products():
    return productos
