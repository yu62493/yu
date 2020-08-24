# -*- coding: utf-8 -*-
"""
fubao 報價資料收集

說明:
    info_fubao(): 主要模組，進行登入網站，並呼叫其他抓取報表程序
    web_info_collect(driver, arg_tar, arg_dics): 爬取網頁資料
    trt_fubaol01(arg_data): 個別網頁資料處理
    trt_fubaol02(arg_data): 個別網頁資料處理

    代碼
    fubao01: '04001' -> LZ廢鋼一級剪料
             '04002' -> LZ廢鋼二級壓塊
    fubao02: '04003' -> 沙鋼廢鋼爐一

"""
#General import
import os
import sys
import time
import datetime
import mysql.connector

from dateutil.parser import parse
from dateutil import parser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

#custom import
#from yusco_project.YUSCO.Util.account_parm import web_account_dic
from YUSCO.Util.account_parm import web_account_dic
from YUSCO.Core.DB_Maria import MariaConn

def web_info_collect(driver, arg_tar, arg_dics):
    driver.get(arg_dics['link'])
    table = driver.find_element_by_xpath('//*[@id="#"]/div/table')
    tddata = []
    for tr in table.find_elements_by_xpath('//tr'):
        tddata.append([td.text for td in tr.find_elements_by_xpath('td')])

    price = []
    if len(tddata) > 0:
        if arg_tar == 'fubao01':
            p = trt_fubaol01(tddata)
        elif arg_tar == 'fubao02':
            p = trt_fubaol02(tddata)
        else:
            p = []
        
        if len(p) > 0:
            price += p

    return price

def trt_fubaol01(arg_data):
    #縮小資料範圍，只取需要的部分
    sub_data = arg_data[1:3]

    p_all = []
    for data in sub_data:
        if data[0] == '剪料':
            grp_code = '04001'
        elif data[0] == '次级压块':
            grp_code = '04002'
        else:
            grp_code = ''
            
        if len(grp_code) > 0 and float(data[5]) > 0:
            p = [grp_code, parser.parse(data[7]).strftime("%Y%m%d"), data[5]]
            p_all.append(p)

    return p_all

def trt_fubaol02(arg_data):
    #縮小資料範圍，只取需要的部分
    sub_data = [arg_data[4]]

    p_all = []
    for data in sub_data:
        if data[0] == '炉一':
            grp_code = '04003'
        else:
            grp_code = ''
            
        if len(grp_code) > 0 and float(data[5]) > 0:
            p = [grp_code, parser.parse(data[7]).strftime("%Y%m%d"), data[5]]
            p_all.append(p)

    return p_all

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

def info_fubao():
    global err_log
    global err_flag
    err_flag = False

    print('開始 fubao 報價資料收集程序...')

    #LOG File
    log_name = "scrp_fubao_" + parser.parse(str(datetime.datetime.now())).strftime("%Y%m%d") + ".txt"
    err_log = open(log_name, 'a', encoding = 'UTF-8')

    tStart = time.time()#計時開始
    err_log.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

    acc = web_account_dic('fubao_acc')
    pwd = web_account_dic('fubao_pwd')
    #print(acc)
    #print(pwd)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver.implicitly_wait(5)

    #輸入帳號密碼登入網站
    driver.get('http://www.f139.com/') 
    elem=driver.find_element_by_id("userName")
    elem.send_keys(acc)
    elem=driver.find_element_by_id("passWord")
    elem.send_keys(pwd)
    elem=driver.find_element_by_xpath('//*[@id="loginForm"]/input[5]')
    elem.click()

    #Target website arguments dict
    tar_args_dic = {
        'fubao01': {'link': 'http://data.f139.com/list.do?pid=&vid=75&qw=5:231'},
        'fubao02': {'link': 'http://data.f139.com/list.do?pid=&vid=75&qw=5:215'}
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
                price_all += price

            err_log.write('來源 ' + tar + ' 資料抓取完畢.\n' )

        except Exception as e:
            err_flag = True
            print("info_fubao -> " + tar + " 資料抓取錯誤，例外訊息如下:")
            print(e.args)
            print("\n\n")
            err_log.write("info_fubao -> " + tar + " 資料抓取錯誤，例外訊息如下:\n")
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

    print('\n\n\n本次fubao市場報價資訊抓取結束，等待下次執行...\n\n\n')

if __name__ == '__main__':
    info_fubao()