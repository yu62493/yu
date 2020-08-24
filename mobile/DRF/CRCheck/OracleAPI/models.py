# -*- coding: utf-8 -*- 

from django.db import models
from YUSCO.Core.DB_ORACLE import OracleDB_dic
import cx_Oracle
from YUSCO.Core.DB_RDB import RDBConn
import pyodbc
import json
import base64
import os 
from datetime import date

#os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8' 
#os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#os.environ['NLS_LANG'] = 'TRADITIONAL CHINESE_TAIWAN.ZHT16BIG5'
#os.environ['NLS_LANG'] = 'TRADITIONAL CHINESE_TAIWAN.ZHT16MSWIN950'
# Create your models here.
class OracleAPIDB(models.Model):

    def ck_getMECH003M(**kwargs):
        location_code = kwargs.get('location_code')
        ck_date = kwargs.get('ck_date')
        if location_code:
            try: 
                conn = cx_Oracle.connect(OracleDB_dic('RP547A_TQC'))
                s_sql = ("select count(*)  "
                        " from mech003m  where ck_date = '" + ck_date + "' and location_code in ('" + location_code + "')"  )
#                print(s_sql)
                cursor = conn.cursor()
                cursor.execute(s_sql)
                ck_list = cursor.fetchall()
#                print(ck_list)
            except cx_Oracle.DatabaseError as ex:
                ck_list = [0]
                print(ex)
            conn.close()
            result = ck_list      
        else:
            result = [0]
        return result
#   註解 : 採用 db_status = 'NEW' 用來區隔新增資料
    def getMECH002M_detail(**kwargs):
        location_code = kwargs.get('location_code')
        emplno = kwargs.get('emplno')
        deptno = kwargs.get('deptno')
        print('emplno ****', emplno)
        print('deptno ****', deptno)
        if location_code:
            try: 
                conn = cx_Oracle.connect(OracleDB_dic('RP547A_TQC'))
                s_sql = (" select 'NEW' as db_status, a.device_code, a.location_code,"
                        " (select device_name from mech001m where device_code = a.device_code) as device_name ,"
                        " a.ck_location, a.datum, "
                        " '' as ck_result, '' as ck_date, '' as ck_time, '' as ck_remark, '' as data_1, '' as data_2, '' as data_3, '' as data_4, " + emplno + " as maint_user "
#                       " from mech002m a where a.location_code in ('AP1-130101','AP1-130102','AP1-030101') ")
#                        " from mech002m a where a.location_code = '" + location_code + "'")
                        " from mech002m a where a.location_code in ( '" + location_code + "') and maint_dp = '" + deptno + "' ")

#                print(s_sql)
                cursor = conn.cursor()
                cursor.execute(s_sql)
                col_names = [i[0] for i in cursor.description]
                ck_list = [dict(zip(col_names, row)) for row in cursor]
#                ck_list = cursor.fetchall()
                print(ck_list)
            except cx_Oracle.DatabaseError as ex:
                ck_list = ['']
                print(ex)
            conn.close()
            result = ck_list      
        else:
            result = ['']
        return result

#   註解 : 採用 db_status = 'OLD' 用來區隔資料已存在
    def getMECH003M_detail(**kwargs):
        location_code = kwargs.get('location_code')
        ck_date = kwargs.get('ck_date')
        print(location_code)
        print(ck_date)
        if location_code:
            conn = cx_Oracle.connect(OracleDB_dic('RP547A_TQC'))
            s_sql = ("select 'OLD' as db_status, a.device_code, a.location_code, "
                            "(select device_name from mech001m where device_code = a.device_code) as device_name ,"
                            "(select ck_location from mech002m where location_code = a.location_code) as ck_location ,"
                            "(select datum from mech002m where location_code = a.location_code) as datum, "
                            " a.ck_result, a.ck_date, a.ck_time, a.ck_remark, a.data_1, a.data_2, a.data_3, a.data_4, a.maint_user "
                            " from mech003m a where a.location_code = '" + location_code + "' and a.ck_date = '" + ck_date + "' and rownum = 1 order by ck_time desc")
#            print(s_sql)
            cursor = conn.cursor()
            cursor.execute(s_sql)
            col_names = [i[0] for i in cursor.description]
            ck_list = [dict(zip(col_names, row)) for row in cursor]
#            ck_list = cursor.fetchall()
#            print(ck_list)
            conn.close()

            result = ck_list      
        
        else:
            result = ['fail']
        return result

    def insMECH003M(CKData):
        result = True
        CC = json.loads(CKData)
        print(CKData)
        print(CC["CK_REMARK"])
        print(CC["CK_RESULT"])
        if CC["CK_RESULT"] == 'true':
            CC["CK_RESULT"] = 'Y'
        else:
            CC["CK_RESULT"] = 'N'


        conn = cx_Oracle.connect(OracleDB_dic('RP547A_TQC'))
        cursor = conn.cursor()
#        s_sql = " delete from mech003m where location_code = '" + CC["LOCATION_CODE"] + "' and ck_date = '" + CC["CK_DATE"] + "' and ck_time = '" + CC["CK_TIME"] + "'"
#        print(s_sql)
#        cursor.execute(s_sql)

        s_sql = ( " insert into mech003m(device_code, location_code, ck_result, ck_date, ck_time, ck_remark, data_1, data_2,"
                " data_3, data_4, maint_user) values "
                "('" + CC["DEVICE_CODE"] + "','" + CC["LOCATION_CODE"] + "','" + CC["CK_RESULT"] + "',"
                " '" + CC["CK_DATE"] + "','" + CC["CK_TIME"] + "','" + CC["CK_REMARK"] + "'," + CC["DATA_1"] + "," + CC["DATA_2"] + ","
                "  " + CC["DATA_3"] + "," + CC["DATA_4"] + ",'" + CC["MAINT_USER"] + "')")
        print('hihi test', s_sql)
        cursor.execute(s_sql)
        conn.commit()
        conn.close()

        return result

    def saveIMAGES(CKData):
        result = True

        today = date.today()
        d1 = today.strftime("%Y%m%d")
        print("d1 =", d1)
        s_path = 'D:/crcheck/photos/' + d1

        CC = json.loads(CKData)
        print(CC["LOCATION_CODE"])
        print(CC["CK_DATE"])
        print(CC["CK_TIME"])

        try:
            os.makedirs(s_path)
        except FileExistsError:
            # directory already exists
            pass        

        conn = cx_Oracle.connect(OracleDB_dic('RP547A_TQC'))
        cursor = conn.cursor()
        s_sql = " delete from mech005m where location_code = '" + CC["LOCATION_CODE"] + "' and ck_date = '" + CC["CK_DATE"] + "' and ck_time = '" + CC["CK_TIME"] + "'" 
        print(s_sql)
        cursor.execute(s_sql)

        s_sql = ( " insert into mech005m(location_code, ck_date, ck_time, seqno, maint_user) values"
                "('" + CC["LOCATION_CODE"] + "','" + CC["CK_DATE"] + "','" + CC["CK_TIME"] + "',"
                " '01','" + CC["MAINT_USER"] + "')")
        print('hihi test', s_sql)
        cursor.execute(s_sql)
        conn.commit()
        conn.close()


        imgdata = base64.b64decode(CC["IMAGE01"])
        filename = os.path.join(s_path, CC["LOCATION_CODE"] + CC["CK_DATE"] + CC["CK_TIME"] + '01.jpg')  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

        return result


    def getIMAGES(CKData):

        CC = json.loads(CKData)
        print(CC["LOCATION_CODE"])
        print(CC["CK_DATE"])
        print(CC["CK_TIME"])

        s_path = 'D:/crcheck/photos/' + CC["CK_DATE"]

        filename = os.path.join(s_path, CC["LOCATION_CODE"] + CC["CK_DATE"] + CC["CK_TIME"] + '01.jpg')  # I assume you have a way of picking unique filenames
        print(filename)

        with open(filename, "rb") as img_file:
            data = img_file.read()
#            result = base64.b64encode(img_file.read())

        return base64.b64encode(data)

"""         try: 
            conn = cx_Oracle.connect(OracleDB_dic('RP547A_TQC'))
            s_sql = ( " insert into mech003m("
                    " a.ck_location, a.datum  "
                    " from mech002m a where a.location_code = '" + location_code + "'")
            print(s_sql)
            cursor = conn.cursor()
            cursor.execute(s_sql)
            ck_list = cursor.fetchall()
            print(ck_list)
        except cx_Oracle.DatabaseError as ex:
            ck_list = ['']
            print(ex)
        conn.close()
 """

"""         try:
            conn = pyodbc.connect(RDBConn('WIP'))
            s_sql = (
                    " select "  
                    " a.coil_no, a.station, a.schd_no, a.date_last_maint, a.class_code, a.qc_remark, a.defect_code1 "
                    " from wipb040h a limit to 10 rows "
            )
            result = list(conn.execute(s_sql))
            print(result)
            conn.close()
        except Exception as e:
            print('Error: something worng, except message : ' + str(e))
 """

