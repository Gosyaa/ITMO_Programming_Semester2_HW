import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect('transport.db')
        self.cursor = self.con.cursor()
        command = 'CREATE TABLE IF NOT EXISTS Transport(ID INT, Тип TEXT, Грузоподъёмность REAL, Длина REAL, Ширина REAL, Высоста REAL, Свободен INT);'
        self.cursor.execute(command)
    def insert_new(self, id, type, cap, l, w, h):
        new_log = (id, type, cap, l, w, h, 1)
        self.cursor.execute('INSERT INTO Transport VALUES(?, ?, ?, ?, ?, ?, ?);', new_log)
        self.con.commit()
    def delete(self, id):
        self.cursor.execute('DELETE FROM Transport WHERE ID = {};'.format(id))
        self.con.commit()
    def free(self):
        self.cursor.execute('SELECT * FROM Transport WHERE Свободен = 1;')
        res = self.cursor.fetchall()
        return res
    def booked(self):
        self.cursor.execute('SELECT * FROM Transport WHERE Свободен = 0;')
        res = self.cursor.fetchall()
        return res
    def all(self):
        self.cursor.execute('SELECT * FROM Transport;')
        res = self.cursor.fetchall()
        return res
    def size(self, m, l=-1, w=-1, h=-1):
        self.cursor.execute('SELECT * FROM Transport WHERE Грузоподъёмность >= {} AND Длина >= {} AND Ширина >= {} AND Высоста >= {};'.format(m, l, w, h))
        res = self.cursor.fetchall()
        return res
    def get(self, id):
        self.cursor.execute('SELECT * FROM Transport WHERE ID = {}'.format(id))
        res = self.cursor.fetchone()
        return res
    def book(self, id):
        a = self.get(id)
        a = list(a)
        a[-1] = 0
        a = tuple(a)
        self.delete(id)
        self.cursor.execute('INSERT INTO Transport VALUES(?, ?, ?, ?, ?, ?, ?);', a)
        self.con.commit()
    def unbook(self, id):
        a = self.get(id)
        a = list(a)
        a[-1] = 1
        a = tuple(a)
        self.delete(id)
        self.cursor.execute('INSERT INTO Transport VALUES(?, ?, ?, ?, ?, ?, ?);', a)
        self.con.commit()
    def unique(self, id):
        self.cursor.execute('SELECT * FROM Transport WHERE ID = {}'.format(id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return True
        else:
            return False