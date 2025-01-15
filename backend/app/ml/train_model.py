from sklearn.neighbors import NearestNeighbors
import joblib
from data_loader import load_user_interactions

def train_recommendation_model():
    """Entrenar el modelo de recomendación utilizando KNN."""
    
    # Cargar los datos de interacciones
    df = load_user_interactions()
    print("df",df)
    # Crear una matriz de características (user_id, product_id, rating)
    user_item_matrix = df.pivot(index='user_id', columns='product_id', values='rating').fillna(0)
    
    # Entrenar el modelo KNN
    model = NearestNeighbors(n_neighbors=10, algorithm='ball_tree')
    model.fit(user_item_matrix.values)
    
    # Guardar el modelo entrenado
    joblib.dump(model, 'C:/Users/yuher/OneDrive/Escritorio/proyecto-ecommerce/backend/app/ml/recommendation_model.pkl')
    
    print("Modelo de recomendación entrenado y guardado.")

train_recommendation_model()
