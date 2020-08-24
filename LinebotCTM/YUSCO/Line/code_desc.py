from ..Core.DB_RDB import RDBConn
import pyodbc

# 客戶代碼
def db_orda011m(cust_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('ORD'))
        s_sql = "select short_name from orda010m where cust_no ='" + cust_no + "'"
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

# APN_NO 代碼
def db_micm060m(apn_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('MIC'))
        s_sql = "select remark from micm060m where code_type = '05' and code ='" + apn_no + "'"
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

