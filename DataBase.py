import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('rating.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class Rating:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS rating 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 user_name VARCHAR(70),
                                 result INTEGER
                                 )''')
        cursor.close()
        self.connection.commit()

    def add_user(self, user_name, result):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM rating WHERE user_name = ?', (str(user_name),))
        row = cursor.fetchone()
        if row and int(row[2]) < result:
            cursor.execute('''DELETE FROM rating WHERE user_name = ?''', (str(user_name),))
            cursor.execute('''INSERT INTO rating 
                              (user_name, result) 
                              VALUES (?,?)''', (str(user_name), str(result)))
        elif not row:
            cursor.execute('''INSERT INTO rating 
                                          (user_name, result) 
                                          VALUES (?,?)''', (str(user_name), str(result)))
        self.connection.commit()

    def find_user(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rating")
        rows = cursor.fetchall()
        rows = sorted(rows, key=lambda x: int(x[2]), reverse=True)
        for i in range(len(rows)):
            if rows[i][1] == user_name:
                break
        else:
            return None
        return i + 1, user_name, int(rows[i][2])

    def return_first_5(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rating")
        rows = cursor.fetchall()
        rows = sorted(rows, key=lambda x: int(x[2]), reverse=True)
        return rows[:5]

    def return_all_lines(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rating")
        rows = cursor.fetchall()
        rows = sorted(rows, key=lambda x: int(x[2]), reverse=True)
        return rows


db = DB()
table = Rating(db.get_connection())
table.init_table()
table.add_user('ru', 2394021)
table.add_user('omnomnom', 78787)
table.add_user('bestplayerever', 23424)
