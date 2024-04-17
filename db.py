import re
import pymysql
from config import db_host,db_user,db_password,db_name,db_charset

class DatabaseManager:
    def __init__(self,cursorclass=False):
        # cursorclass为False,普通的游标,返回没有字段名的数据,为True,返回带有字段名的数据,使得每一行数据都是一个字典
        if cursorclass is False:
            self.connection = pymysql.connect(host=db_host,user=db_user,password=db_password,db=db_name,charset=db_charset,port=3306)
        else:
            self.connection = pymysql.connect(host=db_host,user=db_user,password=db_password,db=db_name,charset=db_charset,cursorclass=pymysql.cursors.DictCursor,port=3306)
        self.cursor=self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def exeDML(self,sql,*args):
        try:
            count = self.cursor.execute(sql,args)
            self.connection.commit()
            return count
        except Exception as e:
            print(e)
            if self.connection:
                self.connection.rollback()
        finally:
            self.close()

    def fetch_one(self,sql,*args):
        try:
            self.cursor.execute(sql,args)
            return self.cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            self.close()


    def fetch_all(self,sql,*args):
        try:
            self.cursor.execute(sql,args)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            self.close()

if __name__=="__main__":
    db=DatabaseManager()


