import config
import mysql.connector
import time
import sql

class M_Transactions : 
    connDB = None
    db = None
    def __init__ (self):
        self.connDB = mysql.connector.connect(
            host="remotemysql.com",
            user="O4pKtnrYIk",
            password="hd0iDziUDK",
            database="O4pKtnrYIk"
        )
        self.db = sql.Sql()

    def ListAllTxPerItemCore(self, user_id, item_id, page, pageSize):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM `Transactions` WHERE `maker_user_id` = "+str(user_id)+" AND `item_id` = "+str(item_id)+" AND `tx_type` = 'bid' LIMIT "+str(page)+" OFFSET "+str(pageSize))
        return mycursor.fetchall()

    def ListAllTxWalletCore(self, user_id, page, pageSize):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM `Transactions` WHERE `maker_user_id` = "+str(user_id)+" AND `tx_type` = 'wallet+' AND `tx_type` = 'wallet-' LIMIT "+str(page)+" OFFSET "+str(pageSize))
        return mycursor.fetchall()

    def MakeBidCore(self, user_id, item_id, bid_amount, user_total_balance):
        # passed all tests successfully
        ts = int(time.time() * 1000)
        cols = ["id"    ,"tx_type"  ,"amount"   ,"status","timestamp","maker_user_id","taker_user_id","item_id"]
        vals = ["NULL"  ,"bid"      , str(bid_amount),"4"     , str(ts)        , str(user_id)       , str(0)             ,str(item_id)]
        self.db.Insert("Transactions",cols,vals)


