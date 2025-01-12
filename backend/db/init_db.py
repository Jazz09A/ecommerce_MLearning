import sqlite3

def create_tables():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        hashed_password TEXT,
        signup_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        preferences TEXT,
        disabled BOOLEAN DEFAULT 0
    )
    ''')

    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        stock INTEGER,
        image TEXT,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create interactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        event_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        rating INTEGER CHECK (rating >= 1 AND rating <= 5),
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')

    # Create categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    ''')

    # Create recommendations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        score REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')

    # Create carts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    # Create cart_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_items (
        cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price_at_time REAL,
        FOREIGN KEY (cart_id) REFERENCES carts (cart_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')

    # Create product_categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_categories (
        product_id INTEGER,
        category_id INTEGER,
        PRIMARY KEY (product_id, category_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id),
        FOREIGN KEY (category_id) REFERENCES categories (category_id)
    )
    ''')

    # Create payments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        cart_id INTEGER,
        amount REAL,
        payment_method TEXT,
        payment_status TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (cart_id) REFERENCES carts (cart_id)
    )
    ''')

    # Create orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT,
        total REAL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    # Create order_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price_at_time REAL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON interactions (user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_product_id ON interactions (product_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id_recommendations ON recommendations (user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_product_id_recommendations ON recommendations (product_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id_carts ON carts (user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cart_id_cart_items ON cart_items (cart_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_product_id_cart_items ON cart_items (product_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id_payments ON payments (user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cart_id_payments ON payments (cart_id)')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_tables()
    print("Database initialized successfully.")
