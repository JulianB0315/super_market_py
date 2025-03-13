from load_data import load_data

productos = load_data('chatbot-project-1/src/data/productos.csv')
categorias = productos['categoria'].unique()
def show_categories():
    print("Categorías disponibles:")
    for categoria in categorias:
        print(f"🔹 {categoria}")
def products_by_categorie(categoria):
    print(f"Productos en la categoría {categoria}:")
    productos_categoria = productos[productos['categoria'] == categoria]
    if productos_categoria.empty:
        print("❌ No se encontraron productos en esta categoría")
        return
    for i, row in productos_categoria.iterrows():
        print(f"🔸 {row['nombre']} | 💰 {row['precio']} | ⭐ {row['puntuacion']}/5")
products_by_categorie('tec')