import mysql.connector as connector
from mysql.connector import Error

class Connection:
    conn = None
    cursor = None
    is_alive = True
    
    def __init__(self, database, username, password):
        try:
            self.conn = connector.connect(host='localhost',
                                     database=database,
                                     user=username,
                                     password=password)

            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()

        except Error as e:
            is_alive = False
            print("Error while connecting : ", e)

    def getTranslate(self, word, searchFrom, getFrom, idIndex):
        self.cursor.execute(
            "SELECT * FROM " + searchFrom + " WHERE word LIKE '%" +
            word + "%'")

        translate = {}
        
        similarWords = self.cursor.fetchall()
        similarWords.reverse()
        
        for i in similarWords:
            # i[0] is id
            
            self.cursor.reset()
            
            originalWord = str(i[1])
            
            self.cursor.execute(
                "SELECT * FROM translate WHERE " + searchFrom +
                "_id = '" + str(i[0]) + "'")

            translateId = str(self.cursor.fetchone()[idIndex])
            
            self.cursor.reset()
            
            self.cursor.execute(
                "SELECT * FROM " + getFrom + " WHERE id = '" + translateId + "'")

            fetch = self.cursor.fetchone()

            if fetch is None:
                continue
            
            translated = fetch[1]

            translate[originalWord] = translated

        return translate
            
    def getTurksihFromEnglish(self, word):
        return self.getTranslate(word, "english", "turkish", 2)

    def getEnglishFromTurkish(self, word):        
        return self.getTranslate(word, "turkish", "english", 3)
