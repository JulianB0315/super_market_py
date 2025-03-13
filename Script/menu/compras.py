import sys
from pathlib import Path
script_dir = Path(__file__).parent.parent
sys.path.append(str(script_dir))
from utils.load_data import load_data
from models import recommendations

def showProducts (id_user):
    productos = load_data('Script/data/productos.csv')
    recomendaciones = recommendations.modelo.recommend(id_user, 5)
    print("🎯 Recomendaciones personalizadas para el usuario:")
    print("🎯 Recomendaciones personalizadas para el usuario:")
    for idx, producto in recomendaciones.iterrows():
        print(f"Producto: {producto['nombre']}, Categoría: {producto['categoria']}, Precio: ${producto['precio']:.2f}")

    print("\n📜 Categorías:")
    for categoria in productos['categoria'].unique():
        print(f"• {categoria}")
    opcion = input("\n🔍 ¿Deseas ver más acerca de alguna categoría? (s/n): ")
    if opcion == 's':
        categoria = input("🔍 Ingresa la categoría que deseas ver: ")
        ver_categoria(id_user,categoria)
    else:
        print("👋 ¡Hasta luego!")
        menu(id_user)
    
if __name__ == "__main__":
    showProducts(1)