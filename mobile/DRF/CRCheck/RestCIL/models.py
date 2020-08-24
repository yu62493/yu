from django.db import models

# Create your models here.
from YUSCO.Core.DB_SQL import SQLConn
import pyodbc
import json

class RestCILDB(models.Model):

    def getData():

        Conn = pyodbc.connect(SQLConn('NTSR12','PER'))
        cursor = Conn.cursor()
        cursor.execute("select * from Per.dbo.cila030m ")
        row = cursor.fetchone()
        while row: 
            print(row)
            row = cursor.fetchone()



    def insCILA030M(CKData):
        result = True
        CC = json.loads(CKData)
        print(CKData)

        Conn = pyodbc.connect(SQLConn('NTSR12','PER'))

        s_sql = ( " insert into cila030m(take_date,take_time,mtl_no,"
                " take_qty, work_no1, remark) values "
                "('" + CC["TAKE_DATE"] + "','" + CC["TAKE_TIME"] + "','" + CC["MTL_NO"] + "',"
                "  " + CC["TAKE_QTY"] + ",'','" + CC["REMARK"] + "')")
        print(s_sql)
        Conn.execute(s_sql)
        Conn.commit()
        return result

    def getCILA020M():
        Conn = pyodbc.connect(SQLConn('NTSR12', 'PER'))
        s_sql = "select work_no1 from cila020m where maint_list_done_ck <> 'Y' "
        cursor = Conn.cursor()
        cursor.execute(s_sql)
        col_names = [i[0] for i in cursor.description]
        wkno_list = [dict(zip(col_names, row)) for row in cursor]
        Conn.close()
        result = wkno_list
        return result

