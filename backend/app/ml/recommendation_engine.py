import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib

def train_knn_model(data: pd.DataFrame):
    """
    data: DataFrame con columnas ['user_id', 'product_id', 'rating'].
    """
    # Crear matriz usuario-producto
    user_product_matrix = data.pivot(index="user_id", columns="product_id", values="rating").fillna(0)

    # Modelo k-NN
    knn = NearestNeighbors(metric="cosine", algorithm="brute")
    knn.fit(user_product_matrix)

    # Guardar modelo entrenado
    joblib.dump(knn, "recommendation_model.pkl")
    return user_product_matrix

def recommend_for_user(user_id: int, data: pd.DataFrame, k=5):
    """
    user_id: ID del usuario para quien generar recomendaciones.
    data: DataFrame con interacciones.
    k: Número de vecinos más cercanos.
    """
    user_product_matrix = data.pivot(index="user_id", columns="product_id", values="rating").fillna(0)
    knn = joblib.load("recommendation_model.pkl")

    if user_id not in user_product_matrix.index:
        return []  # Usuario no encontrado

    distances, indices = knn.kneighbors(user_product_matrix.loc[[user_id]], n_neighbors=k)
    
    # Encontrar productos recomendados
    similar_users = indices.flatten().tolist()
    similar_data = user_product_matrix.iloc[similar_users]
    recommended_products = similar_data.sum(axis=0).sort_values(ascending=False).index.tolist()

    return recommended_products