import pymysql

class SQL():
    def __init__(self, user:str, passwd:str, host:str, db:str, charset='utf8'):
        self.name = db
        self.__db = pymysql.connect(
            user=user,
            passwd=passwd,
            host=host,
            db=db,
            charset=charset
        )
        self.__cursor = self.__db.cursor(pymysql.cursors.DictCursor)

    def GetDB(self, sql:str):
        '''
        DB 데이터 선택하기
        "SELECT * FROM `newsdata` WHERE INDEX1 = '12345' AND INDEX2 = '1234';"`;        
        '''
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        return result

    def editDB(self, sql:str):
        '''      
        DB 데이터 삽입하기
        INSERT INTO `newsdata` (INDEX1, INDEX2) VALUES ('12345', '1234');

        DB 데이터 수정하기
        UPDATE `newsdata` SET INEDEX1 = '1234', INDEX2 = '12345' WHERE INDEX3 != '123456';

        DB 데이터 삭제하기
        DELETE FROM `newsdata` WHERE `INDEX1` IS NULL;
        '''
        self.__cursor.execute(sql)
        self.__db.commit()

    def GetDB_placeholder(self, sql:str, args):
        '''
        args = [[1, 2], [3, 4]]
        "SELECT * FROM `newsdata` WHERE INDEX1 = %s AND INDEX2 = %s;"
        '''
        self.__cursor.execute(sql, args)
        result = self.__cursor.fetchall()
        return result

    def editDB_placeholder(self, sql:str, args):
        '''
        args = [[1, 2], [3, 4]]
        "SELECT * FROM `newsdata` WHERE INDEX1 = %s AND INDEX2 = %s;"
        '''
        self.__cursor.execute(sql, args)
        self.__db.commit()
    
    def EraseAllData(self):
        sql = 'TRUNCATE TABLE ' + self.name
        self.__cursor.execute(sql)
        
