import sqlite3
import pandas as pd
import os

DB_PATH = "C:/Users/yuher/OneDrive/Escritorio/proyecto-ecommerce/backend/db/database.db"

def load_user_interactions():
    """Cargar las interacciones de los usuarios desde la base de datos."""
    
    try:
        # Verificar si la base de datos existe y es accesible
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"La base de datos no existe en la ruta {DB_PATH}")

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        query = '''
        SELECT user_id, product_id, event_type, rating, timestamp
        FROM interactions
        '''
        
        # Ejecutar la consulta y almacenar los resultados
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Si no hay datos, lanzar advertencia
        if not rows:
            print("No se encontraron interacciones en la base de datos.")
        
        # Convertir los resultados a un DataFrame
        columns = ['user_id', 'product_id', 'event_type', 'rating', 'timestamp']
        df = pd.DataFrame(rows, columns=columns)
        print("df load user interactions before group by")
        print(df)
        # Cerrar la conexión a la base de datos
        connection.close()
        
        # Eliminar duplicados (en caso de que haya varias interacciones del mismo usuario con el mismo producto)
        df = df.groupby(['user_id', 'product_id']).agg({
            'rating': 'mean',  # Usamos el rating promedio para los duplicados
            'timestamp': 'max'  # Tomamos la última interacción
        }).reset_index()

        print("df load user interactions")
        print(df)
        return df
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        return pd.DataFrame()  # Devuelve un DataFrame vacío si la base de datos no existe
    except Exception as e:
        print(f"Error al cargar las interacciones: {e}")
        return pd.DataFrame()

def create_user_item_matrix(df):
    """Crear la matriz de usuarios y productos a partir de las interacciones."""
    try:
        if df.empty:
            print("El DataFrame está vacío. No se puede crear la matriz.")
            return None
        
        # Crear la matriz de usuarios y productos (user-item matrix)
        user_item_matrix = df.pivot(index='user_id', columns='product_id', values='rating').fillna(0)

        return user_item_matrix

    except Exception as e:
        print(f"Error al crear la matriz de usuarios y productos: {e}")
        return None

# Cargar las interacciones
df = load_user_interactions()

# Crear la matriz de usuarios y productos
user_item_matrix = create_user_item_matrix(df)

if user_item_matrix is not None:
    print("Matriz de usuarios y productos creada con éxito:")
    print(user_item_matrix)
else:
    print("No se pudo crear la matriz.")

