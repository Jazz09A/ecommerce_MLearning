import sqlite3

DB_PATH = 'database.db'
def delete_user(user_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    delete_user(1)
