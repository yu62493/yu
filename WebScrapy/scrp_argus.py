# -*- coding: utf-8 -*-
"""
Argus Metals 報價資料收集

說明:
    info_argus(): 主要模組，進行登入網站，並呼叫其他抓取報表程序
    web_info_collect(driver, arg_url): 爬取網頁資料

    每日
    01001: 取Last價格LME Nickel 3M Official
    01002: 取Last價格LME Nickel Cash Official (產銷資訊網->市場資訊->LME Ni項目: 相同資料來源)
    01003: LME Nickel Trading Volume
    01004: LME Nickel Warehouse Stocks
    01005: Iron ore fines 62% Fe (ICX) cfr Qingdao USD/dmt

    每週五清晨
    01006: 取Last價格Charge chrome fob US warehouse
    01007: 取Last價格Ferro-chrome HC min 60-65% Cr 6-8% C fob US warehouse (per lb Cr)
    01008: 取Last價格Ferro-molybdenum min 65% Mo max 1.5% Si fob North America warehouse (per lb Mo)
    01009: 取Last價格Ferro-manganese HC min 80% Mn 6-8% C fob North America warehouse
    01010: 取Last價格Ferro-titanium 70% Ti fob North America warehouse
    01011: 取Last價格Stainless steel 304 (18-8) scrap solids cif Rotterdam USD/mt

    每週五下午
    01012: SHFE Warehouse Stocks

    每周六清晨
    01013: 取Last價格LME Copper Cash Official

    不定期
    01014: 每月最後一個工作日鈮鐵價格Ferro-niobium 65% Nb fob US warehouse
    01015: 南非對歐洲鉻鐵季合約價Charge chrome 52% Cr ddp Europe (per lb Cr)

"""
#General import
import os
import sys
import time
import re
import datetime
import mysql.connector

from dateutil import parser
from dateutil.parser import parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

#custom import
#rom yusco_project.YUSCO.Util.account_parm import web_account_dic
from YUSCO.Util.account_parm import web_account_dic
from YUSCO.Core.DB_Maria import MariaConn

def sw_device(driver):
    try:
        title = driver.find_elements_by_xpath('/html/body/div[2]/div/div/h2')[0].text
        #print(title)

        if title == "Switch Device":
            driver.find_element_by_xpath("//input[@value='Switch Device']").click()
    except:
        print("No need to switch device.")

def web_info_collect(driver, arg_tar, arg_url, arg_unit):
    driver.get(arg_url)

    #若有出現Switch Device按鈕，就點下去
    sw_device(driver)

    driver.find_element_by_xpath('//*[@id="Unit"]/option[text()="' + arg_unit + '"]').click()

    #讀取報價table
    elem = driver.find_elements_by_xpath('//*[@id="assessment_price_table_data"]')[0]
    #print(elem)

    thdata = []
    tddata = []
    for rows in elem.find_elements(By.TAG_NAME, "tr"):
        th = [elm.text for elm in rows.find_elements(By.TAG_NAME, "th")]
        td = [elm.text for elm in rows.find_elements(By.TAG_NAME, "td")]
        td = list(filter(None, td))
        thdata.append(th)
        tddata.append(td)

    thdata = list(filter(None, thdata))[0]
    tddata = list(filter(None, tddata))
    tddata = tddata[:-1]
    #print(thdata)
    #print(tddata)

    price = []
    for sub_ls in tddata:
        #price.append([arg_tar, sub_ls[0], sub_ls[3]])
        p = re.sub("[^-0-9^.]", "", sub_ls[3])

        if float(p) > 0: 
            price.append([arg_tar, parser.parse(sub_ls[0]).strftime("%Y%m%d"), p])

    #print(price)
    return price[0]

def db_process(arg_data):
    global err_log
    global err_flag

    config = MariaConn('F23101','scrapydb')
    #建立資料庫連線
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

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
            print('linked_item=' + item[0] + ' data_date=' + item[1] + ' vaule=' + item[2] + ' 資料庫寫入成功.')
        except (mysql.connector.Error, mysql.connector.Warning) as e:
            err_flag = True
            print(str_sql)
            print(e)
            err_log.write("\nDB操作發生錯誤...\n" + str_sql + "\nError msg:\n" + str(e) + "\n")

    # 關閉連線
    conn.close()

def info_argus():
    global err_log
    global err_flag

    print('開始 Argus Metals 報價資料收集程序...')

    err_flag = False
    str_date = parser.parse(str(datetime.datetime.now())).strftime("%Y%m%d")

    #LOG File
    log_name = "scrp_argus_" + str_date + ".txt"
    err_log = open(log_name, 'a', encoding = 'UTF-8')

    tStart = time.time()#計時開始
    err_log.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

    acc = web_account_dic('argus_acc')
    pwd = web_account_dic('argus_pwd')
    #print(acc)
    #print(pwd)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver.implicitly_wait(10)

    driver.get("https://metals.argusmedia.com/n?ulog=True")

    #輸入帳號密碼登入網站
    elem = driver.find_element_by_name("Username")
    elem.send_keys(acc)
    elem = driver.find_element_by_name("Password")
    elem.send_keys(pwd)
    driver.find_element_by_xpath("//*[@id='buttonSubmitLogin']").click()

    #若有出現Switch Device按鈕，就點下去
    sw_device(driver)

    #Target website hyperlink dict
    tar_link_dic = {
        '01001': {'link': 'https://metals.argusmedia.com/price/assessment/lme-nickel-3-month-official',
                  'unit': 'MT'},
        '01002': {'link': 'https://metals.argusmedia.com/price/assessment/lme-nickel-cash-official',
                  'unit': 'MT'},
        '01003': {'link': 'https://metals.argusmedia.com/price/assessment/lme-nickel-trading-volume',
                  'unit': 'MT'},
        '01004': {'link': 'https://metals.argusmedia.com/price/assessment/lme-nickel-warehouse-stocks',
                  'unit': 'MT'},
        '01005': {'link': 'https://metals.argusmedia.com/price/assessment/PA00120250800',
                  'unit': 'dmt'},
        '01006': {'link': 'https://metals.argusmedia.com/price/assessment/PA00162710000',
                  'unit': 'MT'},
        '01007': {'link': 'https://metals.argusmedia.com/price/assessment/PA00187170000',
                  'unit': 'LB'},
        '01008': {'link': 'https://metals.argusmedia.com/price/assessment/PA00187290000',
                  'unit': 'LB'},
        '01009': {'link': 'https://metals.argusmedia.com/price/assessment/PA00187260000',
                  'unit': 'MT'},
        '01010': {'link': 'https://metals.argusmedia.com/price/assessment/PA00162700000',
                  'unit': 'MT'},
        '01011': {'link': 'https://metals.argusmedia.com/price/assessment/PA00162820000',
                  'unit': 'MT'},
        '01012': {'link': 'https://metals.argusmedia.com/price/assessment/shfe-nickel-warehouse-stocks',
                  'unit': 'MT'},
        '01013': {'link': 'https://metals.argusmedia.com/price/assessment/lme-copper-cash-official',
                  'unit': 'MT'},
        '01014': {'link': 'https://metals.argusmedia.com/price/assessment/PA00162680000',
                  'unit': 'MT'},
        '01015': {'link': 'https://metals.argusmedia.com/price/assessment/PA00142990000',
                  'unit': 'LB'}
    }

    #執行各項報表抓取
    price_all = []
    for tar, args in tar_link_dic.items():
        print('\n\n開始進行 ' + tar + ' 資料抓取.' )
        err_log.write('\n\n開始進行 ' + tar + ' 資料抓取.\n' )

        try:
            price = web_info_collect(driver, tar, args['link'], args['unit'])
            err_log.write(str(price) + '\n')
            print(price)

            if len(price) > 0:
                price_all.append(price)

            err_log.write('來源 ' + tar + ' 資料抓取完畢.\n' )
            
        except Exception as e:
            err_flag = True
            print("info_argus -> " + tar + " 資料抓取錯誤，例外訊息如下:")
            print(e.args)
            print("\n\n")
            err_log.write("info_argus -> " + tar + " 資料抓取錯誤，例外訊息如下:\n")
            err_log.write(str(e.args))
            err_log.write("\n\n")

    #關閉瀏覽器視窗
    driver.quit()

    #寫入資料庫
    if len(price_all) > 0:
        #print(price_all)
        db_process(price_all)

    tEnd = time.time()#計時結束
    err_log.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
    err_log.write("*** End LOG ***\n\n")

    # Close File
    err_log.close()

    #如果執行過程無錯誤，最後刪除log file
    if err_flag == False:
        os.remove(log_name)

    print('\n\n\n本次argus市場報價資訊抓取結束，等待下次執行...\n\n\n')

if __name__ == '__main__':
    info_argus()