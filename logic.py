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
            conn.execute("""CREATE TABLE results(
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

    def insert_result(self, data):
        sql = """INSERT INTO results
        (user_id, user_name, question1, question2, question3, quiz1, quiz2, quiz3) 
        values(?, ?, ?, ?)""" 
        self.__executemany(sql, data)

    def get_quiz1(self):
        sql="SELECT quiz1_name from quiz1" 
        return self.__select_data(sql)
        
    def get_quiz2(self):
        sql="SELECT quiz2_name from quiz2" 
        return self.__select_data(sql)
    
    def get_quiz3(self):
        sql="SELECT quiz3_name from quiz3" 
        return self.__select_data(sql)

    def get_quiz1_id(self, quiz1_name):
        sql = 'SELECT quiz1_id FROM status WHERE quiz1_name = ?'
        res = self.__select_data(sql, (quiz1_name,))
        if res: return res[0][0]
        else: return None

    def get_quiz2_id(self, quiz2_name):
        sql = 'SELECT quiz2_id FROM status WHERE quiz2_name = ?'
        res = self.__select_data(sql, (quiz2_name,))
        if res: return res[0][0]
        else: return None


    def get_quiz3_id(self, quiz3_name):
        sql = 'SELECT quiz3_id FROM status WHERE quiz3_name = ?'
        res = self.__select_data(sql, (quiz3_name,))
        if res: return res[0][0]
        else: return None

    def get_results(self, user_id):
        sql="""SELECT * FROM results 
        WHERE user_id = ?""" 
        return self.__select_data(sql, data = (user_id,))
        
    def get_result_id(self, user_name, user_id):
        return self.__select_data(sql='SELECT reslut_id FROM results WHERE user_name = ? AND user_id = ?  ', data = (user_name, user_id,))[0][0]
      
    def get_result_info(self, user_id, user_name):
        sql = """
        SELECT user_name, questiion1, question2, question3, quiz1_name, quiz2_name, quiz3_name FROM projects 
        JOIN quiz1 ON
        quiz1.quiz1_id = results.quiz1_id
        JOIN quiz2 ON
        quiz2.quiz2_id = results.quiz2_id
        JOIN quiz3 ON
        quiz3.quiz3_id = results.quiz3_id
        WHERE user_name=? AND user_id=?
        """
        return self.__select_data(sql=sql, data = (user_name, user_id))


    def update_results(self, param, data):
        sql = f"""UPDATE results SET {param} = ? 
        WHERE user_name = ? AND user_id = ?""" 
        self.__executemany(sql, [data]) 


    def delete_result(self, user_id, project_id):
        sql = """DELETE FROM results 
        WHERE user_id = ? AND result_id = ? """ 
        self.__executemany(sql, [(user_id, project_id)])

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()
