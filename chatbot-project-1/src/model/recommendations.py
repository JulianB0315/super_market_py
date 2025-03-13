import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.impute import SimpleImputer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

class RecommendationModel:
    def __init__(self, compras_path, productos_path):
        self.compras = pd.read_csv(compras_path)
        self.productos = pd.read_csv(productos_path)
        # Calcular la popularidad de los productos al inicializar
        self.calcular_popularidad()
    
    def calcular_popularidad(self):
        # Agregar total de ventas por producto
        ventas_por_producto = self.compras.groupby('id_producto')['cantidad'].sum().reset_index()
        ventas_por_producto.columns = ['id', 'total_ventas']
        
        # Combinar con información de productos
        self.productos = self.productos.merge(ventas_por_producto, on='id', how='left')
        self.productos['total_ventas'] = self.productos['total_ventas'].fillna(0)
        
        # Calcular score de popularidad
        self.productos['popularidad'] = (0.5 * self.productos['puntuacion'] + 
                                       0.3 * (self.productos['total_ventas'] / self.productos['total_ventas'].max()) +
                                       0.2 * (self.productos['personas'] / self.productos['personas'].max()))
    
    def recommend(self, user_id=None, n=5, categoria=None):
        try:
            recomendaciones = self.productos.copy()
            
            if categoria:
                recomendaciones = recomendaciones[recomendaciones['categoria'].str.lower() == categoria.lower()]
            
            # Ordenar por popularidad y seleccionar top N
            recomendaciones = recomendaciones.sort_values(
                by=['popularidad', 'puntuacion'], 
                ascending=[False, False]
            ).head(n)
            
            # Agregar etiquetas descriptivas
            recomendaciones['etiqueta'] = recomendaciones.apply(
                lambda x: f"⭐ {x['puntuacion']}/5 | 👥 {x['personas']} opiniones | 🛒 {int(x['total_ventas'])} ventas", 
                axis=1
            )
            
            return recomendaciones[['id', 'nombre', 'precio', 'categoria', 'puntuacion', 'etiqueta']]
            
        except Exception as e:
            print(f"❌ Error en la recomendación: {e}")
            return pd.DataFrame()

    def train(self):
        # Ya no necesitamos entrenar un modelo
        print("ℹ️ Sistema de recomendaciones basado en popularidad iniciado")
        print("✅ Listo para mostrar recomendaciones")

compras_path = 'Script/data/ventas.csv'
productos_path = 'Script/data/productos.csv'

# Crear una instancia del modelo de recomendación
modelo = RecommendationModel(compras_path, productos_path)

recomendaciones = modelo.recommend(n=5)
print("📊 Productos más populares:")
print(recomendaciones)