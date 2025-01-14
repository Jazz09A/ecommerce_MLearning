import sqlite3

DB_PATH = 'db/database.db'
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
if __name__ == '__main__':
    alter_table()

