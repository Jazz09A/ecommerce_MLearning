import os
import sqlite3

DB_PATH = 'C:/Users/yuher/OneDrive/Escritorio/proyecto-ecommerce/backend/db/database.db'
def delete_user(user_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()


    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))

    connection.commit()
    connection.close()


def alter_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('ALTER TABLE users ADD COLUMN payment_method TEXT')

    connection.commit()
    connection.close()

def get_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    return tables

def delete_cart(cart_id: int):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
    try:
        cursor.execute('DELETE FROM carts WHERE cart_id = ?', (cart_id,))
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error al eliminar el carrito: {e}")
    
def delete_cart_item(cart_item_id: int):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
    try:    
        cursor.execute('DELETE FROM cart_items WHERE cart_item_id = ?', (cart_item_id,))
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error al eliminar el item del carrito: {e}")

def insert_fake_data():
    """Inserta datos falsos en las tablas de la base de datos para pruebas."""
    try:
        # Verificar si la base de datos existe
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"La base de datos no existe en la ruta {DB_PATH}")
        
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # # Insertar usuarios
        # cursor.executemany('''
        #     INSERT INTO users (user_id, username, email, hashed_password, signup_date, preferences, disabled)
        #     VALUES (?, ?, ?, ?, ?, ?, ?)
        # ''', [
        #     (1, "john_doe", "john.doe@example.com", "$2b$12$1oOsklPQE4Qv07jeERpOl.Vg.qlcFT0CvafRs2EegZoTCU15qbVIi", "2025-01-13 14:47:41", None, 0),
        #     (2, "jane_doe", "jane.doe@example.com", "$2b$12$hz706eVEOe3z.djpNAOjMOOOISWbRjZTEYLCjf2loQlfiklBspOGe", "2025-01-13 14:48:13", None, 0),
        #     (3, "test_user", "test.user@example.com", "$2b$12$dCZI0qftoitMIK3wvyVXeeFetnCExnoaAscA4vHJtcoeEZcyS2nJu", "2025-01-13 14:48:21", None, 0),
        #     (4, "alvaro", "alvaro@example.com", "$2b$12$Caj6rWmCxLuudyASp1zyUuFN.6E2WpMxacHoaXghrkP./v8AC3nbq", "2025-01-13 14:48:48", None, "credit-card")
        # ])
        
        # Insertar productos
        # cursor.executemany('''
        #     INSERT INTO products (product_id, name, category, price, stock, image, description, created_at)
        #     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        # ''', [
        #     (101, 'Producto A', 'Electrónica', 99.99, 50, 'img/productA.jpg', 'Producto de electrónica A', '2025-01-10 14:00:00'),
        #     (102, 'Producto B', 'Electrónica', 129.99, 30, 'img/productB.jpg', 'Producto de electrónica B', '2025-01-10 14:05:00'),
        #     (103, 'Producto C', 'Ropa', 49.99, 100, 'img/productC.jpg', 'Producto de ropa C', '2025-01-10 14:10:00'),
        #     (104, 'Producto D', 'Ropa', 79.99, 80, 'img/productD.jpg', 'Producto de ropa D', '2025-01-10 14:15:00'),
        #     (105, 'Producto E', 'Accesorios', 19.99, 200, 'img/productE.jpg', 'Producto de accesorios E', '2025-01-10 14:20:00'),
        #     (106, 'Producto F', 'Accesorios', 39.99, 150, 'img/productF.jpg', 'Producto de accesorios F', '2025-01-10 14:25:00'),
        #     (107, 'Producto G', 'Hogar', 89.99, 60, 'img/productG.jpg', 'Producto de hogar G', '2025-01-10 14:30:00'),
        #     (108, 'Producto H', 'Hogar', 119.99, 40, 'img/productH.jpg', 'Producto de hogar H', '2025-01-10 14:35:00')
        # ])

        # Insertar categorías
        cursor.executemany('''
            INSERT INTO categories (category_id, name)
            VALUES (?, ?)
        ''', [
            (1, 'Electrónica'),
            (2, 'Ropa'),
            (3, 'Accesorios'),
            (4, 'Hogar')
        ])

        # Relacionar productos con categorías
        cursor.executemany('''
            INSERT INTO product_categories (product_id, category_id)
            VALUES (?, ?)
        ''', [
            (101, 1),
            (102, 1),
            (103, 2),
            (104, 2),
            (105, 3),
            (106, 3),
            (107, 4),
            (108, 4)
        ])

        # Insertar interacciones de usuario
        cursor.executemany('''
            INSERT INTO interactions (user_id, product_id, event_type, rating, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', [
            (1, 101, 'view', 1, '2025-01-15 14:05:00'),
            (1, 102, 'add_to_cart', 2, '2025-01-15 14:10:00'),
            (2, 103, 'view', 1, '2025-01-15 14:15:00'),
            (2, 104, 'checkout', 3, '2025-01-15 14:20:00'),
            (3, 105, 'view', 1, '2025-01-15 14:25:00'),
            (3, 106, 'add_to_cart', 2, '2025-01-15 14:30:00'),
            (4, 107, 'checkout', 3, '2025-01-15 14:35:00'),
            (4, 108, 'purchase', 4, '2025-01-15 14:40:00')
        ])

        # # Insertar recomendaciones
        # cursor.executemany('''
        #     INSERT INTO recommendations (user_id, product_id, score, created_at)
        #     VALUES (?, ?, ?, ?)
        # ''', [
        #     (1, 102, 0.95, '2025-01-15 14:05:00'),
        #     (2, 103, 0.90, '2025-01-15 14:15:00'),
        #     (3, 106, 0.85, '2025-01-15 14:25:00'),
        #     (4, 107, 0.80, '2025-01-15 14:35:00')
        # ])

        connection.commit()
        connection.close()
        print("Datos falsos insertados correctamente.")

    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")
        connection.rollback()
        connection.close()
        
def randomize_product_ids():
    """Randomly update the product_id in the interactions table to a value between 1 and 14."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # Generate a random product_id for each row
        cursor.execute('''
            UPDATE interactions
            SET product_id = ABS(RANDOM() % 14) + 1
        ''')
        
        connection.commit()
        print("Product IDs randomized successfully.")
    except Exception as e:
        print(f"Error updating product IDs: {e}")
    finally:
        connection.close()
        
def add_more_interactions():
    connection = sqlite3.connect(DB_PATH)   
    cursor = connection.cursor()

    interactions_data = [
        (1, 1, 'view', 1, '2025-01-15 14:05:00'),
        (1, 2, 'add_to_cart', 2, '2025-01-15 14:10:00'),
        (1, 3, 'view', 1, '2025-01-15 14:15:00'),
        (1, 4, 'checkout', 3, '2025-01-15 14:20:00'),
        (2, 3, 'view', 1, '2025-01-15 14:25:00'),
        (2, 4, 'add_to_cart', 2, '2025-01-15 14:30:00'),
        (2, 5, 'checkout', 3, '2025-01-15 14:35:00'),
        (2, 6, 'purchase', 4, '2025-01-15 14:40:00'),
        (3, 1, 'view', 1, '2025-01-15 14:45:00'),
        (3, 2, 'add_to_cart', 2, '2025-01-15 14:50:00'),
        (3, 3, 'checkout', 3, '2025-01-15 14:55:00'),
        (3, 4, 'purchase', 4, '2025-01-15 15:00:00'),
        (4, 5, 'view', 1, '2025-01-15 15:05:00'),
        (4, 6, 'add_to_cart', 2, '2025-01-15 15:10:00'),
        (4, 7, 'checkout', 3, '2025-01-15 15:15:00'),
        (4, 8, 'purchase', 4, '2025-01-15 15:20:00'),
        (1, 5, 'view', 1, '2025-01-15 15:25:00'),
        (1, 6, 'add_to_cart', 2, '2025-01-15 15:30:00'),
        (1, 7, 'checkout', 3, '2025-01-15 15:35:00'),
        (1, 8, 'purchase', 4, '2025-01-15 15:40:00'),
        (2, 5, 'view', 1, '2025-01-15 15:45:00'),
        (2, 6, 'add_to_cart', 2, '2025-01-15 15:50:00'),
        (2, 7, 'checkout', 3, '2025-01-15 15:55:00'),
        (2, 8, 'purchase', 4, '2025-01-15 16:00:00'),
        (3, 1, 'view', 1, '2025-01-15 16:05:00'),
        (3, 2, 'add_to_cart', 2, '2025-01-15 16:10:00'),
        (3, 3, 'checkout', 3, '2025-01-15 16:15:00'),
        (3, 4, 'purchase', 4, '2025-01-15 16:20:00'),
        (4, 5, 'view', 1, '2025-01-15 16:25:00')
    ]

    cursor.executemany('''
        INSERT INTO interactions (user_id, product_id, event_type, rating, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', interactions_data)
    connection.commit()
    print("Más interacciones agregadas correctamente.")
    connection.close()

def delete_last_interaction():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM interactions WHERE rowid = (SELECT MAX(rowid) FROM interactions)')
    connection.commit()
    connection.close()

def delete_last_cart_item():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM cart_items WHERE rowid = (SELECT MAX(rowid) FROM cart_items)')
    connection.commit()
    connection.close()
    
def delete_cart_items_null():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM cart_items WHERE product_id IS NULL')
    connection.commit()
    connection.close()

if __name__ == '__main__':
    delete_last_interaction()


