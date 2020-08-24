import numpy as np
import datetime as dt
import pandas as pd
import sqlite3
import time
from datetime import timedelta
import httplib2
from urllib.parse import urlencode
import csv
import random
import psycopg2

def twdate(date):
    year  = date.year-1911
    month = date.month
    day   = date.day
    twday = '{}/{:02}/{:02}'.format(year,month,day)
    return twday
    
def stockdate(date):
    year  = date.year
    month = date.month
    day   = date.day
    sday = '{}{:02}{:02}'.format(year,month,day)
    return sday

def downloadTWSE(sdate,type):   

#    url="http://www.twse.com.tw/exchangeReport/MI_INDEX"
    url="https://www.twse.com.tw/exchangeReport/MI_INDEX"
    values = {'response' : 'csv', 'date' : stockdate(sdate), 'type' : type }       
   
    agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    #httplib2.debuglevel = 1
    conn = httplib2.Http('.cache')
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'User-Agent': agent}
    resp, content = conn.request(url, 'POST', urlencode(values), headers)
    respStr = str(content.decode('cp950'));
    print(respStr);
    return respStr
 
def StoreDatabase(trade_date, type, stockID, stockName, Volume, Transaction_number, Transaction_amount, Price_Open, Price_Max, Price_Min, Price_Close, showLen):
#    conn = sqlite3.connect('D://IT_Project/Git/python_test/tiny/stock/stockDB.db3')
#    conn = sqlite3.connect('stockDB.db3')
    conn = psycopg2.connect(user = "stock",
                                    password = "XXXXXX",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "stockDB")
    cursor = conn.cursor()
    cursor.execute("delete from stockDay where trade_date='" + trade_date +"' and type ='" + type +"'")
    conn.commit()
    cursor.close()

    cursor = conn.cursor()
    for i in range(showLen):
        cursor.execute("insert into stockDay values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(trade_date,type,stockID[i],stockName[i],Volume[i].replace(',',''),Transaction_number[i].replace(',',''),Transaction_amount[i].replace(',',''),Price_Open[i].replace(',','').replace('-','0'),Price_Max[i].replace(',','').replace('-','0'),Price_Min[i].replace(',','').replace('-','0'),Price_Close[i].replace(',','').replace('-','0')))
#        cursor.execute("insert into stockDay values(?,?,?,?,?,?,?,?,?,?,?)",(trade_date,type,stockID[i],stockName[i],Volume[i].replace(',',''),Transaction_number[i].replace(',',''),Transaction_amount[i].replace(',',''),Price_Open[i],Price_Max[i],Price_Min[i],Price_Close[i]))
    conn.commit()
    cursor.close()
    conn.close()


def showStock(stockID, stockName, Volume, Transaction_number, Transaction_amount, Price_Open, Price_Max, Price_Min, Price_Close, showLen):
    print('stockID:',stockID[:showLen])
    print('stockName:',stockName[:showLen])
    print('Volume:',Volume[:showLen])
    print('Transaction_number:',Transaction_number[:showLen])
    print('Transaction_amount:',Transaction_amount[:showLen])
    print('Price_Open:',Price_Open[:showLen])
    print('Price_Max:',Price_Max[:showLen])
    print('Price_Min:',Price_Min[:showLen])
    print('Price_Close:',Price_Close[:showLen])

# download TWSE
def stock_main(downloadDate, type):
    strCSV = downloadTWSE(downloadDate,type) 

    srcCSV = list(csv.reader(strCSV.split('\n'), delimiter=','))
    
    #search stock list
    firstIndex=0
    lastIndex=0
    for i in range(len(srcCSV)):   
        row = srcCSV[i]
        if (len(row)>16):  #16 columns
            row[0]=row[0].strip(' =\"')
            row[1]=row[1].strip(' =\"')
            if (row[0]=="證券代號"):
                firstIndex=i+1       
            else :
                lastIndex=i+1    
                
    #get result           
    result = np.array(srcCSV[firstIndex:lastIndex])
    if (len(result)>0):
        stockID=result[:,0]
        stockName=result[:,1]
        Volume=result[:,2]
        Transaction_number=result[:,3]
        Transaction_amount=result[:,4]
        Price_Open=result[:,5]
        Price_Max=result[:,6]
        Price_Min=result[:,7]
        Price_Close=result[:,8]
        print('\nSTOCK_DAILY ==> TWSE count=',len(stockID))
        showStock(stockID, stockName, Volume, Transaction_number, Transaction_amount, Price_Open, Price_Max, Price_Min, Price_Close, len(stockID))
        StoreDatabase(stockdate(downloadDate), type, stockID, stockName, Volume, Transaction_number, Transaction_amount, Price_Open, Price_Max, Price_Min, Price_Close, len(stockID))
    else:
        print(stockdate(downloadDate) + " 無資料")
    del srcCSV[:]
    del srcCSV


def main():
    j = 0
    while j < 2:
        downloadDate= dt.date.today() - timedelta(days=j)
    #    types = ["01","02"]
        types = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","20"]
        i = 0
        while i < len(types):
            print('stock_daily ==> ',stockdate(downloadDate),'type=',types[i])
            stock_main(downloadDate,types[i])
            i += 1
            time.sleep(random.randint(5,10)) 
        j += 1
