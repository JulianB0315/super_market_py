import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler

def calculate_category_averages():
    data = pd.read_csv('chatbot-project-1/src/data/productos.csv')
    category_analysis = data.groupby('categoria').agg({
        'precio': 'mean',
        'descuento': 'mean',
        'personas': 'mean'
    }).reset_index()

    category_analysis.rename(columns={
        'precio': 'Precio Promedio',
        'descuento': 'Descuento Promedio',
        'personas': 'Popularidad Promedio'
    }, inplace=True)

    return category_analysis

def display_dendrogram():
    data = pd.read_csv('chatbot-project-1/src/data/productos.csv')

    category_analysis = data.groupby('categoria').agg({
        'precio': 'mean',
        'descuento': 'mean',
        'personas': 'mean'
    }).reset_index()

    category_analysis.rename(columns={
        'precio': 'Precio Promedio',
        'descuento': 'Descuento Promedio',
        'personas': 'Popularidad Promedio'
    }, inplace=True)

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(category_analysis[['Precio Promedio', 'Descuento Promedio', 'Popularidad Promedio']])

    linked = linkage(features_scaled, method='ward')

    plt.figure(figsize=(10, 7))
    plt.title("Dendrograma de Clustering Jerárquico (Categorías)")
    dendrogram(linked, labels=category_analysis['categoria'].values, leaf_rotation=90, leaf_font_size=10)
    plt.xlabel("Categorías")
    plt.ylabel("Distancia")
    plt.show()