import mysql.connector

class SafeStatDB:
    def __init__(self, host="localhost", database="safestat", user="safestatUser", password="safestat123") -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        db = mysql.connector.connect(host=self.host, database=self.database, user=self.user, password=self.password, auth_plugin='mysql_native_password')
        return db

    def entity_exists(self, entity, val):
        db = self.connect()
        cursor=db.cursor()
        sqls = {
            'crime':"""SELECT * FROM Crimes WHERE link=%s""",
            'loc':"""SELECT * FROM Locs WHERE loc=%s""",
            'tag':"""SELECT * FROM Tags WHERE tag=%s""",
            }
        sql = sqls[entity]
        val = (val,)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if len(result) == 0:
            return False
        else:
            return True

    def insert_loc(self, loc):
        db = self.connect()
        cursor = db.cursor()
        sql = "INSERT INTO Locs (loc)" \
            " VALUES (%s)"
        val = (loc,)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        
    def insert_tag(self, tag):
        db = self.connect()
        cursor = db.cursor()
        sql = "INSERT INTO Tags (tag)" \
            " VALUES (%s)"
        val = (tag,)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        
    def insert_crime(self, link, published, tag, text):
        if len(text)>200:
            text = text[:200]
        db = self.connect()
        cursor = db.cursor()
        sql = "INSERT INTO Crimes (link, published, tag, news_text)" \
            " VALUES (%s,%s,%s,%s)"
        val = (link, published, tag, text,)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        
    def insert_loc_crime(self, link, loc):
        db = self.connect()
        cursor = db.cursor()
        sql = "INSERT INTO LocCrimes (link, loc)" \
            " VALUES (%s, %s)"
        val = (link, loc,)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()