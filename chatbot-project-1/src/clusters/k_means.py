import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import seaborn as sns

def cargar_datos(path):
    df = pd.read_csv(path)
    print(f'Dataset cargado: {df.shape[0]} productos con {df.shape[1]} características')
    return df

def preprocess_data(df, caracteristicas=None):
    if caracteristicas is None:
        caracteristicas = ['precio', 'descuento', 'puntuacion', 'personas']
    X = df[caracteristicas].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, caracteristicas

def find_optimal_clusters(X_scaled, max_clusters = 10):
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans_model = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans_model.fit(X_scaled)
        inertias.append(kmeans_model.inertia_)

    cambios = np.diff(inertias, 2)  
    k_optimo = np.argmin(cambios) + 2 
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_clusters + 1), inertias, marker='o')
    plt.axvline(x=k_optimo, color='red', linestyle='--', label=f'Clusters óptimos: {k_optimo}')
    plt.title('Método del Codo para Número Óptimo de Clusters')
    plt.xlabel('Número de Clusters')
    plt.ylabel('Inercia')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(f'🔹 Número óptimo de clusters seleccionado automáticamente: {k_optimo}')
    return k_optimo

def apply_kmeans(X_scaled, n_clusters):  
    kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans_model.fit_predict(X_scaled)  
    return cluster_labels, kmeans_model

def view_clusters(X_scaled, cluster_labels, df, kmeans_model): 
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    df_plot = pd.DataFrame({
        'PC1': X_pca[:, 0],
        'PC2': X_pca[:, 1],
        'Cluster': cluster_labels, 
        'Producto': df['nombre'],
        'Categoria': df['categoria']
    })
    centroids_pca = pca.transform(kmeans_model.cluster_centers_)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df_plot,
        x='PC1', y='PC2', 
        hue='Cluster',
        palette='tab10',
        s=100,
        alpha=0.7,
        edgecolor='black'
    )
    plt.scatter(centroids_pca[:, 0], centroids_pca[:,1],
                marker='x', s=200, c='red', edgecolors='black', label='Centroides')

    for i, row in df_plot.iterrows():
        plt.plot(
            [row['PC1'], centroids_pca[row['Cluster'], 0]],
            [row['PC2'], centroids_pca[row['Cluster'], 1]],
            linestyle='dotted', color='grey', alpha=0.5
        )
    for i, row in df_plot.iterrows():
        plt.annotate(
            row['Producto'],
            (row['PC1'], row['PC2']),
            alpha=0.7,
            ha='center',
            fontsize=8
        )
    
    plt.title('Clusters de Productos')
    plt.legend()
    plt.tight_layout()
    plt.show()
    return df_plot

def analizar_clusters(df, cluster_labels): 
    df['Cluster'] = cluster_labels  

    resumen_clusters = df.groupby('Cluster').agg({
        'precio': ['mean', 'min', 'max', 'std'],
        'descuento': ['mean', 'min', 'max'],
        'puntuacion': ['mean', 'min', 'max'],
        'personas': ['mean', 'min', 'max']
    })

    categorias_per_cluster = df.groupby(['Cluster', 'categoria']).size().unstack().fillna(0)
    return resumen_clusters, categorias_per_cluster

def main(path, n_clusters=None):
    df = cargar_datos(path)
    X_scaled, caracteristicas = preprocess_data(df)

    if n_clusters is None:
        n_clusters = find_optimal_clusters(X_scaled) 
    
    cluster_labels, kmeans_model = apply_kmeans(X_scaled, n_clusters)  
    df_plot = view_clusters(X_scaled, cluster_labels, df, kmeans_model)  
    resumen, categorias_dist = analizar_clusters(df, cluster_labels)  

    print('Resumen de los Clusters:')
    print(resumen)
    print('\nDistribución de Categorías por Cluster:')
    print(categorias_dist)

    df_clusters = df.copy()
    df_clusters['Cluster'] = cluster_labels 
    df_clusters.to_csv('clusters.csv', index=False)

    return df_clusters, kmeans_model

def run_kmeans_analysis(path, n_clusters):
    pass  
if __name__ == '__main__':
    main('chatbot-project-1/src/data/productos.csv')