import mysql.connector
import config

class Sql():
    connDB = None
    def __init__ (self):
        self.connDB = mysql.connector.connect(
            host="remotemysql.com",
            user="O4pKtnrYIk",
            password="hd0iDziUDK",
            database="O4pKtnrYIk"
        )
    
    def Insert(self, table, columns, values):
        mycursor = self.connDB.cursor()
        strCol = "`" + "`,`".join(columns) + "`"
        strVal = "'" + "','".join(values) + "'"
        strVal = strVal.replace("'NULL'","NULL")
        sql_ = (""  
            "INSERT INTO `"+table+"` ("+strCol+")"
            "VALUES ("+strVal+");"
        "")
        
        #config.ReturnJsonError(str(sql_))
        mycursor.execute(sql_)
        self.connDB.commit()
    
    def Select(self, table, cond):
        mycursor = self.connDB.cursor()
        sql_ = "SELECT * FROM `"+table+"` WHERE " + cond
        mycursor.execute(sql_)
        return self.connDB.fetchall()

    def Update(self, table, col, val, cond):
        mycursor = self.connDB.cursor()
        # UPDATE `Items` SET `min_required_users` = '99' WHERE `Items`.`id` = 3;
        sql_ = "UPDATE `"+table+"` SET `"+col+"` = '"+val+"' WHERE "+cond
        mycursor.execute(sql_)
        self.connDB.commit()

