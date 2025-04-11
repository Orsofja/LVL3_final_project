import sqlite3
from config import DATABASE

quiz1_answers = [ (_,) for _ in (['', '', '', ''])]
quiz2_answers = [ (_,) for _ in (['', '', '', ''])]
quiz3_answers = [ (_,) for _ in (['', '', '', ''])]

class DB_Manager:
    def __init__(self, database):
        self.database = database # имя базы данных
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute("""CREATE TABLE projects(
                        result_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        user_name TEXT NOT NULL,
                        question1 TEXT,
                        question2 TEXT,
                        question3 TEXT,
                        quiz1 INTEGER,
                        quiz2 INTEGER,
                        quiz3 INTEGER,
                        FOREIGN KEY(quiz1) REFERENCES quiz1(quiz1))
                        FOREIGN KEY(quiz2) REFERENCES quiz2(quiz2))
                        FOREIGN KEY(quiz3) REFERENCES quiz3(quiz3))
                         """)

            conn.execute("""CREATE TABLE quiz1(
                         quiz1 INTEGER PRIMARY KEY,
                         quiz1_name TEXT )""")

            conn.execute("""CREATE TABLE quiz2(
                         quiz2 INTEGER PRIMARY KEY,
                         quiz2_name TEXT )""")

            conn.execute("""CREATE TABLE quiz2(
                         quiz3 INTEGER PRIMARY KEY,
                         quiz3_name TEXT )""")
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO quiz1 (quiz1_name) values(?)'
        data = quiz1_answers
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO quiz2 (quiz2_name) values(?)'
        data = quiz2_answers
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO quiz3 (quiz3_name) values(?)'
        data = quiz3_answers
        self.__executemany(sql, data)