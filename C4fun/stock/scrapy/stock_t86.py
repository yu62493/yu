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
    url="https://www.twse.com.tw/fund/T86"
    values = {'response' : 'csv', 'date' : stockdate(sdate), 'selectType' : type }       
   
    agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    #httplib2.debuglevel = 1
    conn = httplib2.Http('.cache')
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'User-Agent': agent}
    resp, content = conn.request(url, 'POST', urlencode(values), headers)
    respStr = str(content.decode('cp950'));
#    print(respStr);
    return respStr


def StoreDatabase(trade_date, type, stockID, stockName, ForeignInvestor_buy01, ForeignInvestor_sell01, ForeignInvestor_01, ForeignInvestor_buy02, ForeignInvestor_sell02, ForeignInvestor_02, InvestmentTrust_buy, InvestmentTrust_sell, InvestmentTrust, Dealer, Dealer_buy01, Dealer_sell01, Dealer_01, Dealer_buy02, Dealer_sell02, Dealer_02, TOTAL, showLen):

    conn = psycopg2.connect(user = "stock",
                                    password = "XXXXXX",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "stockDB")
    cursor = conn.cursor()
    cursor.execute("delete from stockt86 where trade_date='" + trade_date +"' and type ='" + type +"'")
    conn.commit()
    cursor.close()

    cursor = conn.cursor()
    for i in range(showLen):
        cursor.execute("insert into stockt86 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
           (trade_date,type,stockID[i],stockName[i],ForeignInvestor_buy01[i].replace(',',''), \
            ForeignInvestor_sell01[i].replace(',',''), ForeignInvestor_01[i].replace(',',''), \
            ForeignInvestor_buy02[i].replace(',',''), ForeignInvestor_sell02[i].replace(',',''), \
            ForeignInvestor_02[i].replace(',',''), InvestmentTrust_buy[i].replace(',',''), \
            InvestmentTrust_sell[i].replace(',',''), InvestmentTrust[i].replace(',',''), \
            Dealer[i].replace(',',''), Dealer_buy01[i].replace(',',''), Dealer_sell01[i].replace(',',''), \
            Dealer_01[i].replace(',',''), Dealer_buy02[i].replace(',',''), Dealer_sell02[i].replace(',',''), \
            Dealer_02[i].replace(',',''), TOTAL[i].replace(',','')
           )
        )
    conn.commit()
    cursor.close()
    conn.close()

def showstock(stockID, stockName, ForeignInvestor_buy01, ForeignInvestor_sell01, ForeignInvestor_01, ForeignInvestor_buy02, ForeignInvestor_sell02, ForeignInvestor_02, InvestmentTrust_buy, InvestmentTrust_sell, InvestmentTrust, Dealer, Dealer_buy01, Dealer_sell01, Dealer_01, Dealer_buy02, Dealer_sell02, Dealer_02, TOTAL, showLen):
    print('stockID:',stockID[:showLen])
    print('stockName:',stockName[:showLen])
    print('ForeignInvestor_buy01:',ForeignInvestor_buy01[:showLen])
    print('ForeignInvestor_sell01:',ForeignInvestor_sell01[:showLen])
    print('ForeignInvestor_01:',ForeignInvestor_01[:showLen])
    print('ForeignInvestor_buy02:',ForeignInvestor_buy02[:showLen])
    print('ForeignInvestor_sell02:',ForeignInvestor_sell02[:showLen])
    print('ForeignInvestor_02:',ForeignInvestor_02[:showLen])
    print('InvestmentTrust_buy:',InvestmentTrust_buy[:showLen])
    print('InvestmentTrust_sell:',InvestmentTrust_sell[:showLen])
    print('InvestmentTrust:',InvestmentTrust[:showLen])
    print('Dealer:',Dealer[:showLen])
    print('Dealer_buy01:',Dealer_buy01[:showLen])
    print('Dealer_sell01:',Dealer_sell01[:showLen])
    print('Dealer_01:',Dealer_01[:showLen])
    print('Dealer_buy02:',Dealer_buy02[:showLen])
    print('Dealer_sell02:',Dealer_sell02[:showLen])
    print('Dealer_02:',Dealer_02[:showLen])
    print('TOTAL:',TOTAL[:showLen])


# download TWSE
def stock_main(downloadDate, type):
    strCSV = downloadTWSE(downloadDate,type) 
    srcCSV = list(csv.reader(strCSV.split('\n'), delimiter=','))
    
    #search stock list
    firstIndex=0
    lastIndex=0
    for i in range(len(srcCSV)):   
        row = srcCSV[i]
        if (len(row)>19):  #20 columns
            if (row[0]=="證券代號"):
                firstIndex=i+1       
            elif (row[0].strip() != ''):
                lastIndex=i+1    
                
    #get result           
    result = np.array(srcCSV[firstIndex:lastIndex])
#    print(result)
 
    if (len(result)>0):
        stockID=result[:,0]
        stockName=result[:,1]
        ForeignInvestor_buy01=result[:,2]
        ForeignInvestor_sell01=result[:,3]
        ForeignInvestor_01=result[:,4]
        ForeignInvestor_buy02=result[:,5]
        ForeignInvestor_sell02=result[:,6]
        ForeignInvestor_02=result[:,7]
        InvestmentTrust_buy=result[:,8]
        InvestmentTrust_sell=result[:,9]
        InvestmentTrust=result[:,10]
        Dealer=result[:,11]
        Dealer_buy01=result[:,12]
        Dealer_sell01=result[:,13]
        Dealer_01=result[:,14]
        Dealer_buy02=result[:,15]
        Dealer_sell02=result[:,16]
        Dealer_02=result[:,17]
        TOTAL=result[:,18]

        stockID, stockName, ForeignInvestor_buy01, ForeignInvestor_sell01, ForeignInvestor_01, ForeignInvestor_buy02, ForeignInvestor_sell02, ForeignInvestor_02, InvestmentTrust_buy, InvestmentTrust_sell, InvestmentTrust, Dealer, Dealer_buy01, Dealer_sell01, Dealer_01, Dealer_buy02, Dealer_sell02, Dealer_02, TOTAL
        
        print('\nTWSE count=',len(stockID))
        showstock(stockID, stockName, ForeignInvestor_buy01, ForeignInvestor_sell01, ForeignInvestor_01, ForeignInvestor_buy02, ForeignInvestor_sell02, ForeignInvestor_02, InvestmentTrust_buy, InvestmentTrust_sell, InvestmentTrust, Dealer, Dealer_buy01, Dealer_sell01, Dealer_01, Dealer_buy02, Dealer_sell02, Dealer_02, TOTAL, len(stockID))
        StoreDatabase(stockdate(downloadDate), type, stockID, stockName, ForeignInvestor_buy01, ForeignInvestor_sell01, ForeignInvestor_01, ForeignInvestor_buy02, ForeignInvestor_sell02, ForeignInvestor_02, InvestmentTrust_buy, InvestmentTrust_sell, InvestmentTrust, Dealer, Dealer_buy01, Dealer_sell01, Dealer_01, Dealer_buy02, Dealer_sell02, Dealer_02, TOTAL, len(stockID))
    else:
        print(stockdate(downloadDate) + " 無資料")
    del srcCSV[:]
    del srcCSV


#j = 405
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
        time.sleep(random.randint(3,15)) 
    j += 1
