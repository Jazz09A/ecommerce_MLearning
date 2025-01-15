import joblib
import numpy as np
from sklearn.neighbors import NearestNeighbors
from app.ml.data_loader import load_user_interactions

# Cargar el modelo entrenado
try:
    model: NearestNeighbors = joblib.load('C:/Users/yuher/OneDrive/Escritorio/proyecto-ecommerce/backend/app/ml/recommendation_model.pkl')
except FileNotFoundError:
    model = None

def recommend_products(user_id, num_recommendations=5):
    global model
    print("model", model)
    """Recomendar productos basados en el modelo KNN entrenado."""

    # Cargar las interacciones del usuario
    df = load_user_interactions()

    # Eliminar duplicados y agregar calificaciones si es necesario
    df = df.groupby(['user_id', 'product_id']).agg({'rating': 'mean'}).reset_index()
    print("df funcion recommended products",df)
    # Crear la matriz de usuario-producto
    user_item_matrix = df.pivot(index='user_id', columns='product_id', values='rating').fillna(0)

    # Verificar si el usuario existe en la matriz
    if user_id not in user_item_matrix.index:
        print(f"User ID {user_id} not found in user-item matrix.")
        return []

    # Obtener las características del usuario
    user_vector = user_item_matrix.loc[user_id].values.reshape(1, -1)
    print("user_vector", user_vector)

    # Ajustar el número de vecinos a la cantidad de usuarios disponibles
    n_neighbors = min(num_recommendations, len(user_item_matrix) - 1)  # Restar 1 porque el propio usuario no se cuenta

    # Hacer las recomendaciones
    distances, indices = model.kneighbors(user_vector, n_neighbors=n_neighbors)

    recommended_products = user_item_matrix.columns[indices.flatten()].tolist()
    print("recommended_products", recommended_products)
    return recommended_products