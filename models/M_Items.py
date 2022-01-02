import config
import mysql.connector
import jwt
import time
import sys
import hashlib
import json

class M_Items : 
    connDB = None
    def __init__ (self):
        self.connDB = mysql.connector.connect(
            host="remotemysql.com",
            user="O4pKtnrYIk",
            password="hd0iDziUDK",
            database="O4pKtnrYIk"
        )

    def ListAllItems(self):
        # https://images.samsung.com/is/image/samsung/tr-fhd-t5300-ue40t5300auxtk-frontblack-237104952
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Items")
        return mycursor.fetchall()


    def CreateItemCore(self, args):
        mycursor = self.connDB.cursor()
        lastIdBeforeInsert = mycursor.lastrowid
        # ts stores the time in milliseconds
        ts = int(time.time() * 1000)
        core = {}
        try:
            sql = (""  
                "INSERT INTO `Items` (`id`, `item_name`, `creation_date`, `last_user`, `last_price`, `img_url`, `bid_starting_date`, `min_required_users`, `users_list`, `normal_price`, `remaining_time`, `status`)"
                "VALUES (NULL, '"+args["item_name"]+"', '"+str(ts)+"', '1', '"+args["price"]+"', '"+args["item_img"]+"', '"+args["bid_start_date"]+"', '"+args["min_users"]+"', '1,', '"+args["item_normal_price"]+"', '"+args["remaining_time"]+"', '0');"
            "")
            mycursor.execute(sql)
            self.connDB.commit()
            core = {
                "success": lastIdBeforeInsert != mycursor.lastrowid,
            }
        except Exception as e:
            pass
            core = {
                "success": lastIdBeforeInsert != mycursor.lastrowid,
                "message": str(e)
            }
        parsedCore = json.dumps(core)
        return parsedCore

    def ListFutureItemsCore(self, timestamp, count=10):
        # https://images.samsung.com/is/image/samsung/tr-fhd-t5300-ue40t5300auxtk-frontblack-237104952
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM `Items` WHERE `bid_starting_date` > "+str(timestamp)+" LIMIT " + str(count))
        return mycursor.fetchall()

    def ListPastItemsCore(self, timestamp, count=10):
        # https://images.samsung.com/is/image/samsung/tr-fhd-t5300-ue40t5300auxtk-frontblack-237104952
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM `Items` WHERE `bid_starting_date` < "+str(timestamp)+" LIMIT " + str(count))
        return mycursor.fetchall()


