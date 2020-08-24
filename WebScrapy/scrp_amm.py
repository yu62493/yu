# -*- coding: utf-8 -*-
"""
amm 報價資料收集

說明:
    info_amm(): 主要模組，進行登入網站，並呼叫其他抓取報表程序
    web_info_collect(driver, arg_url): 爬取網頁資料

    代碼
    03001: 取Mid價格Ferro-chrome Japan import 8-9% C, basis 60% Cr, CIF Japan, duty unpaid, $ per lb contained chrome
    03002: 取Mid價格Ferro-chrome China import 50% Cr US $ per Ib contained chrome CIF Shanghai

    PS:
    amm 網站切換headless模式會出現不明錯誤，保留開視窗設定.

"""
#General import
import os
import sys
import time
import datetime
import mysql.connector

from dateutil.parser import parse
from dateutil import parser
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

#custom import
#from yusco_project.YUSCO.Util.account_parm import web_account_dic
from YUSCO.Util.account_parm import web_account_dic
from YUSCO.Core.DB_Maria import MariaConn

def web_info_collect(driver, arg_tar, arg_url):

    driver.get(arg_url)
    table = driver.find_element_by_class_name("historical-table")
    p_date = table.find_elements_by_xpath(".//table//tbody//tr//td[@class='price-date ng-binding']")[0].text
    mid_price = table.find_elements_by_xpath(".//table//tbody//tr//td[@class='ng-scope']//div//span[@class='ng-binding ng-scope']")[2].text

    if float(mid_price) > 0: 
        price = [arg_tar, parser.parse(p_date).strftime("%Y%m%d"), mid_price]

    return price

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

def info_amm():
    global err_log
    global err_flag
    err_flag = False

    print('開始 amm 報價資料收集程序...')

    #LOG File
    log_name = "scrp_amm_" + parser.parse(str(datetime.datetime.now())).strftime("%Y%m%d") + ".txt"
    err_log = open(log_name, 'a', encoding = 'UTF-8')

    tStart = time.time()#計時開始
    err_log.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

    acc = web_account_dic('amm_acc')
    pwd = web_account_dic('amm_pwd')
    #print(acc)
    #print(pwd)

    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(5)

    driver.get("https://www.amm.com/")
    driver.find_element_by_xpath('//*[@id="mhHeader_loginInfo_lnkLogin"]').click()

    #輸入帳號密碼登入網站
    elem = driver.find_element_by_xpath('//*[@id="username"]')
    elem.send_keys(acc)
    elem = driver.find_element_by_xpath('//*[@id="password"]')
    elem.send_keys(pwd)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/form/fieldset/div[2]/div[2]/div[1]/button').click()

    #Target website arguments dict
    tar_args_dic = {
        '03001': 'https://www.amm.com/pricing/Ferro-Chrome/Ferro-chrome-Japan-import-8-9-C-basis-60-Cr-CIF-Japan-duty-unpaid--per-lb-contained-chrome-ymgnlh4zd32s',
        '03002': 'https://www.amm.com/pricing/Ferro-Chrome/Ferro-chrome-China-import-50-Cr-US--per-Ib-contained-chrome-CIF-Shanghai-qs7l6lwpsshg'
    }

    #執行各項報表抓取
    price_all = []
    for tar, url in tar_args_dic.items():
        print('開始進行 ' + tar + ' 資料抓取.' )
        err_log.write('\n\n開始進行 ' + tar + ' 資料抓取.\n' )

        try:
            price = web_info_collect(driver, tar, url)
            err_log.write(str(price) + '\n')
            print(price)

            if len(price) > 0:
                price_all.append(price)

            err_log.write('來源 ' + tar + ' 資料抓取完畢.\n' )

        except Exception as e:
            err_flag = True
            print("info_amm -> " + tar + " 資料抓取錯誤，例外訊息如下:")
            print(e.args)
            print("\n\n")
            err_log.write("info_amm -> " + tar + " 資料抓取錯誤，例外訊息如下:\n")
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

    print('\n\n\n本次amm市場報價資訊抓取結束，等待下次執行...\n\n\n')

if __name__ == '__main__':
    info_amm()