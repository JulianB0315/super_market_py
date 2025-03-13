import pandas as pd

class RecommendationModel:
    def __init__(self, compras_path, productos_path):
        self.compras = pd.read_csv(compras_path)
        self.productos = pd.read_csv(productos_path)
        self.calcular_popularidad()
    
    def calcular_popularidad(self):
        ventas_por_producto = self.compras.groupby('id_producto')['cantidad'].sum().reset_index()
        ventas_por_producto.columns = ['id', 'total_ventas']
        self.productos = self.productos.merge(ventas_por_producto, on='id', how='left')
        self.productos['total_ventas'] = self.productos['total_ventas'].fillna(0)
        self.productos['popularidad'] = (0.5 * self.productos['puntuacion'] + 
                                       0.3 * (self.productos['total_ventas'] / self.productos['total_ventas'].max()) +
                                       0.2 * (self.productos['personas'] / self.productos['personas'].max()))
    
    def recommend(self, user_id=None, n=5, categoria=None):
        try:
            recomendaciones = self.productos.copy()
            
            if categoria:
                recomendaciones = recomendaciones[recomendaciones['categoria'].str.lower() == categoria.lower()]
            recomendaciones = recomendaciones.sort_values(
                by=['popularidad', 'puntuacion'], 
                ascending=[False, False]
            ).head(n)
            recomendaciones['etiqueta'] = recomendaciones.apply(
                lambda x: f"⭐ {x['puntuacion']}/5 | 👥 {x['personas']} opiniones | 🛒 {int(x['total_ventas'])} ventas", 
                axis=1
            )
            return recomendaciones[['id', 'nombre', 'precio', 'categoria', 'puntuacion', 'etiqueta']]
        except Exception as e:
            print(f"❌ Error en la recomendación: {e}")
            return pd.DataFrame()
compras_path = 'chatbot-project-1/src/data/ventas.csv'
productos_path = 'chatbot-project-1/src/data/productos.csv'
modelo = RecommendationModel(compras_path, productos_path)
recomendaciones = modelo.recommend(n=5)