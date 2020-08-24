import mysql.connector
import datetime
from ..Core.DB_Maria import MariaConn

def db_process(arg_data):

    config = MariaConn('F23101','scrapydb')
    #建立資料庫連線
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    err_flag = False
    for item in arg_data:
        try:
            str_sql = 'delete from scrp011m where linked_item="' + item[0] + '" and data_date="' + item[1] + '"'
            cursor.execute(str_sql)

            str_sql  = 'insert into scrp011m (linked_item,data_date,vul,dt_last_maint) values ('
            str_sql += '"' + item[0] + '",'
            str_sql += '"' + item[1] + '",'
            str_sql += '"' + item[2] + '",'
            str_sql += '"' + str(datetime.datetime.now()) + '"'
            str_sql += ')'

            cursor.execute(str_sql)
            conn.commit()
            result_str = 'linked_item=' + item[0] + ' data_date=' + item[1] + ' vaule=' + item[2] + ' 資料庫寫入成功.'
        except (mysql.connector.Error, mysql.connector.Warning) as e:
            err_flag = True
            print(str_sql)
            print(e)
            result_str = "\nDB操作發生錯誤...\n" + str_sql + "\nError msg:\n" + str(e) + "\n"

    # 關閉連線
    conn.close()

    return err_flag, result_str

def db_process2(arg_data):

    config = MariaConn('F23101','scrapydb')
    #建立資料庫連線
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    err_flag = False
    for item in arg_data:
        try:
            str_sql = 'delete from scrp011m where linked_item="' + item[0] + '" and data_date="' + item[1] + '"'
            cursor.execute(str_sql)

            str_sql  = 'insert into scrp011m (linked_item,data_date,vul,vul_max,vul_min,dt_last_maint) values ('
            str_sql += '"' + item[0] + '",'
            str_sql += '"' + item[1] + '",'
            str_sql += '' + item[2] + ','
            str_sql += '' + item[3] + ','
            str_sql += '' + item[4] + ','
            str_sql += '"' + str(datetime.datetime.now()) + '"'
            str_sql += ')'

            cursor.execute(str_sql)
            conn.commit()
            result_str = 'linked_item=' + item[0] + ' data_date=' + item[1] + ' vaule=' + item[2] + ' 資料庫寫入成功.'
        except (mysql.connector.Error, mysql.connector.Warning) as e:
            err_flag = True
            print(str_sql)
            print(e)
            result_str = "\nDB操作發生錯誤...\n" + str_sql + "\nError msg:\n" + str(e) + "\n"

    # 關閉連線
    conn.close()

    return err_flag, result_str
