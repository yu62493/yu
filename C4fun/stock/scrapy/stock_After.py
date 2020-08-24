import numpy as np
import datetime as dt
import time
from datetime import timedelta
import random
import httplib2
from urllib.parse import urlencode
import csv
import psycopg2


def stockdate(date):
    year  = date.year
    month = date.month
    day   = date.day
    sday = '{}{:02}{:02}'.format(year,month,day)
    return sday

def downloadTWSE(sdate,type):   
    url="https://www.twse.com.tw/exchangeReport/BFT41U"
    values = {'response' : 'csv', 'date' : stockdate(sdate), 'selectType' : type }       
   
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

def StoreDatabase(trade_date, type, stockID, stockName, Transaction_number, Transaction_count, Transaction_amount, Transaction_price, last_show_buy, last_show_sale, showLen):
    conn = psycopg2.connect(user = "stock",
                                    password = "XXXXXX",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "stockDB")
    cursor = conn.cursor()
    cursor.execute("delete from stockAfter where trade_date='" + trade_date +"' and type ='" + type +"'")
    conn.commit()
    cursor.close()

    cursor = conn.cursor()
    for i in range(showLen):
        cursor.execute("insert into stockAfter values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(trade_date,type,stockID[i],stockName[i],Transaction_number[i].replace(',',''), Transaction_count[i].replace(',',''), Transaction_amount[i].replace(',',''), Transaction_price[i].replace(',',''), last_show_buy[i].replace(',',''), last_show_sale[i].replace(',','')))
    conn.commit()
    cursor.close()
    conn.close()

def showStock(stockID, stockName, Transaction_number, Transaction_count, Transaction_amount, Transaction_price, last_show_buy, last_show_sale, showLen):
    print('stockID:',stockID[:showLen])
    print('stockName:',stockName[:showLen])
    print('Transaction_number',Transaction_number[:showLen])
    print('Transaction_count',Transaction_count[:showLen])
    print('Transaction_amount',Transaction_amount[:showLen])
    print('Transaction_price',Transaction_price[:showLen])
    print('last_show_buy',last_show_buy[:showLen])
    print('last_show_sale',last_show_sale[:showLen])


# download TWSE
def stock_main(downloadDate, type):
    strCSV = downloadTWSE(downloadDate,type) 
    srcCSV = list(csv.reader(strCSV.split('\n'), delimiter=','))
    
    #search stock list
    firstIndex=0
    lastIndex=0
    for i in range(len(srcCSV)):   
        row = srcCSV[i]
        if (len(row)>8):  #9 columns
            if (row[0]=="證券代號"):
                firstIndex=i+1       
            elif (row[0].strip() != ''):
                lastIndex=i+1    
                
    #get result           
    result = np.array(srcCSV[firstIndex:lastIndex])
    if (len(result)>0):
        stockID=result[:,0]
        stockName=result[:,1]
        Transaction_number=result[:,2]
        Transaction_count=result[:,3]
        Transaction_amount=result[:,4]
        Transaction_price=result[:,5]
        last_show_buy=result[:,6]
        last_show_sale=result[:,7]
        print('\nTWSE count=',len(stockID))
        showStock(stockID, stockName, Transaction_number, Transaction_count, Transaction_amount, Transaction_price, last_show_buy, last_show_sale, len(stockID))
        StoreDatabase(stockdate(downloadDate), type, stockID, stockName, Transaction_number, Transaction_count, Transaction_amount, Transaction_price, last_show_buy, last_show_sale, len(stockID))
    else:
        print(stockdate(downloadDate) + " 無資料")
    del srcCSV[:]
    del srcCSV

#j = 689
j = 1
while j < 5:
    downloadDate= dt.date.today() - timedelta(days=j)
#    types = ["01","02"]
    types = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","20"]
    i = 0
    while i < len(types):
        print(stockdate(downloadDate),'type=',types[i])
        stock_main(downloadDate,types[i])
        i += 1
        time.sleep(random.randint(3,20)) 
    j += 1
