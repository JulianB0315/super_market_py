import sys
from pathlib import Path

# Agregar el directorio Script al path
script_dir = Path(__file__).parent.parent
sys.path.append(str(script_dir))
from utils.load_data import load_data
from models import recommendations

def showProducts (id_user):
    productos = load_data('Script/data/productos.csv')
    recomendaciones = recommendations.modelo.recommend(id_user, 5)
    print(recomendaciones)

if __name__ == "__main__":
    showProducts(1)