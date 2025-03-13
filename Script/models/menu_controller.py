import pandas as pd 
import datetime as dt
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


productos = pd.read_csv('Script/data/productos.csv')
compras = pd.read_csv('Script/data/ventas.csv')
df_users = pd.read_csv('Script/data/usuarios.csv')

if compras.empty:
    print("📢 No hay compras registradas. Se recomendarán los productos más populares.")
    productos_populares = productos.sort_values(by=["puntuacion", "personas"], ascending=[False, False]).head(5)
    print(productos_populares[["nombre", "categoria", "precio", "puntuacion"]])
else:
    # Crear matriz usuario-producto
    matriz_usuarios_productos = compras.pivot_table(index='id_user', columns='id_producto', values='cantidad', fill_value=0)
    
    # Manejo de valores faltantes
    imputer = SimpleImputer(strategy="mean")
    matriz_usuarios_productos_imputed = imputer.fit_transform(matriz_usuarios_productos)
    
    # Dividir en conjunto de entrenamiento y prueba
    train_data, test_data = train_test_split(matriz_usuarios_productos_imputed, test_size=0.2, random_state=42)
    
    # Aplicar SVD para entrenamiento
    n_components = min(50, train_data.shape[1])  # Ajustar el número de componentes según los datos
    modelo_svd = TruncatedSVD(n_components=n_components, random_state=42)
    modelo_svd.fit(train_data)
    
    # Evaluar el margen de error con MAE
    test_pred = modelo_svd.transform(test_data)
    mae = mean_absolute_error(test_data, test_pred @ modelo_svd.components_)
    print(f"📊 Margen de error (MAE): {mae:.4f}")
    
    # Función para recomendar productos a un usuario
    def recomendar_productos(user_id, n=5):
        if user_id not in matriz_usuarios_productos.index:
            print("📢 Usuario nuevo. Se mostrarán los productos más comprados y mejor calificados.")
            return productos.sort_values(by=["puntuacion", "num_calificaciones"], ascending=[False, False]).head(n)[['nombre', 'categoria', 'precio', 'puntuacion']]
        
        user_idx = matriz_usuarios_productos.index.get_loc(user_id)
        user_vector = modelo_svd.transform([matriz_usuarios_productos_imputed[user_idx]])
        similitudes = cosine_similarity(user_vector, modelo_svd.transform(matriz_usuarios_productos_imputed))[0]
        productos_ordenados = np.argsort(similitudes)[-n:][::-1]
        return productos[productos['producto_id'].isin(matriz_usuarios_productos.columns[productos_ordenados])][['nombre', 'categoria', 'precio', 'puntuacion']]
    
    # Prueba con un usuario
    usuario_prueba = 1
    recomendaciones = recomendar_productos(usuario_prueba, 5)
    print("🎯 Recomendaciones personalizadas para el usuario:")
    print(recomendaciones)
