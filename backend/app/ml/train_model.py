import sqlite3
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# Conectar a la base de datos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Obtener interacciones del usuario
cursor.execute('SELECT user_id, product_id, rating FROM interactions')
data = cursor.fetchall()

# Crear DataFrame
df = pd.DataFrame(data, columns=['user_id', 'product_id', 'rating'])

# Preprocesamiento (normalización si es necesario)
scaler = StandardScaler()
df['rating_scaled'] = scaler.fit_transform(df[['rating']])

# Entrenar el modelo KNN
knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(df[['rating_scaled']])

# Obtener recomendaciones para un usuario
user_id = 1  # Ejemplo de ID de usuario
distances, indices = knn.kneighbors(df[df['user_id'] == user_id][['rating_scaled']])

# Guardar las recomendaciones en la base de datos
for idx in indices[0]:
    recommended_product = df.iloc[idx]['product_id']
    cursor.execute('INSERT INTO recommendations (user_id, product_id, score) VALUES (?, ?, ?)',
                   (user_id, recommended_product, 1))  # Poner el puntaje inicial
conn.commit()
conn.close()
