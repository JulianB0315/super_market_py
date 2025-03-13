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
        self.modelo_svd = None
        self.matriz_svd = None
        self.mae = None
    
    def train(self):
        try:
            matriz_usuarios_productos = self.compras.pivot_table(index='id_user', columns='id_producto', values='cantidad', fill_value=0)
            imputer = SimpleImputer(strategy="mean")
            matriz_imputed = imputer.fit_transform(matriz_usuarios_productos)
            
            train_data, test_data = train_test_split(matriz_imputed, test_size=0.2, random_state=42)
            
            n_components = min(50, train_data.shape[1])
            self.modelo_svd = TruncatedSVD(n_components=n_components, random_state=42)
            self.modelo_svd.fit(train_data)
            
            test_pred = self.modelo_svd.transform(test_data) @ self.modelo_svd.components_
            self.mae = mean_absolute_error(test_data, test_pred)
            print(f"📊 Margen de error (MAE): {self.mae:.4f}")
        except Exception as e:
            print(f"❌ Error en entrenamiento: {e}")
    
    def recommend(self, user_id, n=5):
        try:
            if user_id not in self.compras['id_user'].values:
                return self.productos.sort_values(by=['puntuacion', 'personas'], ascending=[False, False]).head(n)
            
            matriz_usuarios_productos = self.compras.pivot_table(index='id_user', columns='id_producto', values='cantidad', fill_value=0)
            user_idx = matriz_usuarios_productos.index.get_loc(user_id)
            user_vector = self.modelo_svd.transform([matriz_usuarios_productos.iloc[user_idx]])
            similitudes = cosine_similarity(user_vector, self.modelo_svd.transform(matriz_usuarios_productos))[0]
            productos_ordenados = np.argsort(similitudes)[-n:][::-1]
            
            return self.productos[self.productos['id'].isin(matriz_usuarios_productos.columns[productos_ordenados])]
        except Exception as e:
            print(f"❌ Error en la recomendación: {e}")
            return pd.DataFrame()

compras_path = 'Script/data/ventas.csv'
productos_path = 'Script/data/productos.csv'

# Crear una instancia del modelo de recomendación
modelo = RecommendationModel(compras_path, productos_path)

# Entrenar el modelo
modelo.train()

# Obtener recomendaciones para un usuario específico
user_id = 1  # Cambia esto por el ID del usuario que deseas probar
recomendaciones = modelo.recommend(user_id, n=5)

# Mostrar las recomendaciones
print(recomendaciones)