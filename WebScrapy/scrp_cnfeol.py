# -*- coding: utf-8 -*-
"""
cnfeol 報價資料收集

說明:
    cnfeol01 : 菲律宾红土镍矿港口价格
    cnfeol02 : 菲律宾红土镍矿外盘价格
    cnfeol03 : 铬矿外盘价格
    cnfeol04 : 镍铁早讯
    cnfeol05 : 全國主要地區高鎳鐵價格
    cnfeol06 : 普硅高鉻主流成交價格華北
    cnfeol07 : 國內鉬鐵承兌成交價
    cnfeol08 : 鉬鐵65-70%歐洲CFO鉬鐵氧化鉬價格
    cnfeol09 : 全國主要地區山西65 山西75 廣西75 貴州75 高碳錳鐵價格
    cnfeol10 : 北方區域錳鐵行情
    -----------------------------------------------------------------
    下列產生日期不固定,需要往前抓一天
    -----------------------------------------------------------------
    cnfeol11 : 太鋼青山張浦招標價格
    cnfeol12 : 太鋼寶鋼酒鋼青山鉻鐵月招標價格
    cnfeol13 : 太鋼寶鋼鉬鐵月招標價格

    代碼

"""
#General import
import os
import sys
import time
import datetime
import re
import decimal

from dateutil.parser import parse
from dateutil import parser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#custom import
from YUSCO.Util.account_parm import web_account_dic
from YUSCO.Scrapy.scrp_mariaDB import db_process, db_process2

#arg_url = "http://www.cnfeol.com/" 
arg_url = "http://www.cnfeol.com/member/membersignin.aspx"

print(sys.argv)
today = sys.argv[1]
#today = str(datetime.date.today() + datetime.timedelta(days=-1)).replace("-","")
#today = str(datetime.date.today()).replace("-","")
today_01 = str(int(today[4:6])) + '月' + str(int(today[6:8])) + '日'
today_02 = '（' + today[0:4] + '.' + str(int(today[4:6])) + '.' + str(int(today[6:8])) + '）'
today_03 = today[0:6] + '01'
month_01 = str(int(today[4:6])) + '月'
month_02 = today[0:4] + '年' + month_01
print('today:%s\t' % today)
print('today_01:%s\t today_02:%s\t today_03:%s' % (today_01,today_02,today_03))
print('month_01:%s\t month_02:%s' % (month_01,month_02))

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_path = "C:\selenium_driver_chrome\chromedriver.exe" #chromedriver.exe執行檔所存在的路徑
#driver = webdriver.Chrome(chrome_path)
driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)


def login(arg_url):
    acc = web_account_dic('cnfeol_acc')
    pwd = web_account_dic('cnfeol_pwd')
    driver.get(arg_url)
 #   driver.find_element_by_xpath("//*[@id='LoginBox']/a[2]").click()
    time.sleep(10)
    username = driver.find_element_by_xpath('//*[@id="TextBoxScreenName"]')
    username.send_keys(acc)
    password = driver.find_element_by_xpath("//*[@id='TextBoxPassword']")
    password.send_keys(pwd)
    driver.find_element_by_xpath("//input[@type='submit'][@name='ButtonLogin']").click()


def web_info_collect(driver, arg_tar, arg_dics):

	price = []
	if arg_tar == 'cnfeol01':
		arg_1 = today_01 + '菲律宾红土镍矿港口价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol01_getdata(datalist)
	elif arg_tar == 'cnfeol02':
		arg_1 = today_01 + '印尼红土镍矿外盘价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol02_indonesia_getdata(datalist)
		arg_1 = today_01 + '菲律宾红土镍矿外盘价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol02_philippines_getdata(datalist)
		arg_1 = today_01 + '镍矿海运费'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol02_ship_getdata(datalist)
	elif arg_tar == 'cnfeol03':
		arg_1 = today_01 + '铬矿外盘价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol03_getdata(datalist)
	elif arg_tar == 'cnfeol04':
		arg_1 = today_01 + '镍铁早讯'
		NewsContent = item02_content(arg_1,arg_dics['link'])
		if NewsContent:
			print(NewsContent)
			cnfeol04_getdata(NewsContent)
	elif arg_tar == 'cnfeol05':
		arg_1 = today_01 + '全国主要地区高镍铁价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol05_getdata(datalist)
	elif arg_tar == 'cnfeol06':
		arg_1 = '高碳铬铁行情早间必读' + today_02
		print(arg_1)
		NewsContent = item02_content(arg_1,arg_dics['link'])
		if NewsContent:
			print(NewsContent)
			cnfeol06_getdata(NewsContent)
	elif arg_tar == 'cnfeol07':
		arg_1 = today_01 + '国内钼铁价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol07_getdata(datalist)
	elif arg_tar == 'cnfeol08':
		arg_1 = today_01 + 'CFO钼铁氧化钼价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol08_getdata(datalist)
	elif arg_tar == 'cnfeol09':
		arg_1 = today_01 + '全国主要地区高碳锰铁价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol09_getdata(datalist)
	elif arg_tar == 'cnfeol10':
		arg_1 = today_01 + '锰铁行情汇总'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol10_getdata(datalist)
	elif arg_tar == 'cnfeol11':
		arg_1 = '江苏某钢厂' + today_01 + '高镍铁采购价'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol11_getdata(datalist,'02015')

		arg_1 = '华北某钢厂' + today_01 + '高镍铁招标价'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol11_getdata(datalist,'02016')

		arg_1 = '青山集团' + today_01 + '高镍铁采购价'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol11_getdata(datalist,'02017')

	elif arg_tar == 'cnfeol12':
		arg_1 = '宝钢德盛' + month_02 + '高碳铬铁招标价'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol12_getdata(datalist,'02070')

		arg_1 = '酒钢' + month_02 + '高碳铬铁招标价'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol12_getdata(datalist,'02071')

		arg_1 = '太钢' + month_02 + '高碳铬铁招标价'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol12_getdata(datalist,'02072')

		arg_1 = '青山' + month_02 + '高碳铬铁招标价'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol12_getdata(datalist,'02073')

	elif arg_tar == 'cnfeol13':
		arg_1 = '山西一钢厂' + month_01 + '钼铁招标价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol13_getdata(datalist,'02080')

		arg_1 = '上海一钢厂' + month_01 + '钼铁招标价格'
		datalist = item01_content(arg_1,arg_dics['link'])
		if datalist:
			print(datalist)
			cnfeol13_getdata(datalist,'02081')

	return price

def info_cnfeol():
    global err_log
    global err_flag
    err_flag = False

    print('開始 cnfeol 報價資料收集程序...')

    #LOG File
    log_name = "scrp_cnfeol_" + parser.parse(str(datetime.datetime.now())).strftime("%Y%m%d") + ".txt"
    err_log = open(log_name, 'a', encoding = 'UTF-8')

    tStart = time.time()#計時開始
    err_log.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

    #輸入帳號密碼登入網站
    login(arg_url)

    cnt = 0
    delay = 10 # seconds

    while True:
        try:
            element_present = EC.presence_of_element_located((By.ID, 'Bottom_Common_End'))
            WebDriverWait(driver, delay).until(element_present)
            print ("Page is ready!")
            break
        except TimeoutException:
            cnt += 1
            print ("Load cnt=" + str(cnt))
            if cnt >= 3:
                break

    #Target website arguments dict
    tar_args_dic = {
        'cnfeol01': {'link': 'http://www.cnfeol.com/niekuang_ab_19/all-1.aspx'},
        'cnfeol02': {'link': 'http://www.cnfeol.com/niekuang/p-2-1.aspx'},
        'cnfeol03': {'link': 'http://www.cnfeol.com/gekuang/p-2-1.aspx'},
        'cnfeol04': {'link': 'http://hjs.cnfeol.com/search.aspx?key=镍铁早讯&ie=utf-8&cl=0'},
        'cnfeol05': {'link': 'http://www.cnfeol.com/nietie/p-1-1.aspx'},
        'cnfeol06': {'link': 'http://hjs.cnfeol.com/search.aspx?key=高碳铬铁行情早间必读&ie=utf-8&cl=0'},
        'cnfeol07': {'link': 'http://www.cnfeol.com/mutie/p-1-1.aspx'},
        'cnfeol08': {'link': 'http://www.cnfeol.com/mutie/p-2-1.aspx'},
        'cnfeol09': {'link': 'http://www.cnfeol.com/mengtie/p-1-1.aspx'},
        'cnfeol10': {'link': 'http://www.cnfeol.com/mengtie/a-1.aspx'},
        'cnfeol11': {'link': 'http://www.cnfeol.com/nietie/p-3-1.aspx'},
        'cnfeol12': {'link': 'http://www.cnfeol.com/getie/p-3-1.aspx'},
        'cnfeol13': {'link': 'http://www.cnfeol.com/mutie/p-3-1.aspx'}
    }

    #執行各項報表抓取
    for tar, url in tar_args_dic.items():
        print('開始進行 ' + tar + ' 資料抓取.' )
        err_log.write('\n\n開始進行 ' + tar + ' 資料抓取.\n' )

        try:
            price = web_info_collect(driver, tar, url)

        except Exception as e:
            err_flag = True
            print("info_cnfeol -> " + tar + " 資料抓取錯誤，例外訊息如下:")
            print(e.args)
            print("\n\n")
            err_log.write("info_cnfeol -> " + tar + " 資料抓取錯誤，例外訊息如下:\n")
            err_log.write(str(e.args))
            err_log.write("\n\n")

    #關閉瀏覽器視窗
    driver.quit()

    tEnd = time.time()#計時結束
    err_log.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
    err_log.write("*** End LOG ***\n\n")

    # Close File
    err_log.close()

    #如果執行過程無錯誤，最後刪除log file
#    if err_flag == False:
#        os.remove(log_name)

    print('\n\n\n本次cnfeol市場報價資訊抓取結束，等待下次執行...\n\n\n')

def item01_content(arg_1, arg_url):
	driver.get(arg_url)
	table = driver.find_element_by_id("contentlistcontainer")
	tddata = []

	flag = False
	for link_txt in table.find_elements_by_xpath(".//ul/li//a[text()='" + arg_1 + "']"): 
		tt = link_txt.get_attribute('href')
		flag = True
		print(tt)

	if flag:
		print(arg_1)
		driver.get(tt)
		table = driver.find_element_by_id("contentdetail_info_detail")
		for row in table.find_elements_by_xpath(".//table//tbody//tr"): 
			tddata.append([td.text for td in row.find_elements_by_xpath(".//td[text()]")])
	else:
		print(arg_1 + ",尚未產生")
    
	return tddata

def item02_content(arg_1, arg_url):
	driver.get(arg_url)
	table = driver.find_element_by_id("result_body")
	NewsContent = ""
	tt_1 = ""
	for link_txt in table.find_elements_by_xpath(".//div[@class='resultitem']//a[@class='title']"): 
		tt = link_txt.get_attribute('href')
		if (link_txt.text == arg_1):
			tt_1 = tt
		print(link_txt.text)
	if tt_1 != "":
		driver.get(tt_1)
		NewsContent = driver.find_element_by_xpath("//*[@id='contentdetail_info_detail']/p").text
		print(NewsContent)
    
	return NewsContent


def cnfeol01_getdata(datalist):
    global err_flag
    global err_log

    price_list = [['02020',today,datalist[1][4]],['02021',today,datalist[2][3]],
        ['02022',today,datalist[3][3]],['02023',today,datalist[4][3]],
        ['02024',today,datalist[5][3]],['02025',today,datalist[6][3]],
        ['02026',today,datalist[7][3]]]
    
    #寫入資料庫
    if len(price_list) > 0:
        print(price_list)
        result = db_process(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 處理 max min value
def max_min_Val(arg_string):

    target_str = re.compile(r'([0-9]+([.]{1}[0-9]+){0,1})-([0-9]+([.]{1}[0-9]+){0,1})')
    mo = target_str.search(arg_string)
    print(mo)
    if mo:
        min_val = mo.group(1)
        max_val = mo.group(3)
        val = str((decimal.Decimal(min_val) + decimal.Decimal(max_val))/2)
    else:
        min_val = str(0)
        max_val = str(0)
        val = arg_string
    return [val,max_val,min_val]

# 印尼紅土鎳礦外盤價
def cnfeol02_indonesia_getdata(datalist):
    global err_flag
    global err_log

    arg_FOB01 = datalist[1][4]
    list_FOB01 = max_min_Val(arg_FOB01)

    arg_CIF01 = datalist[3][2]
    list_CIF01 = max_min_Val(arg_CIF01)

    price_list = [
        ['02030',today,list_FOB01[0],list_FOB01[1],list_FOB01[2]],
        ['02031',today,list_CIF01[0],list_CIF01[1],list_CIF01[2]]
    ]

    #寫入資料庫
    if len(price_list) > 0:
        print(price_list)
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)


# 菲律賓紅土鎳礦外盤價
def cnfeol02_philippines_getdata(datalist):
    global err_flag
    global err_log

    print(datalist)

    arg_FOB01 = datalist[1][4]
    list_FOB01 = max_min_Val(arg_FOB01)

    arg_FOB02 = datalist[2][3]
    list_FOB02 = max_min_Val(arg_FOB02)

    arg_FOB03 = datalist[3][3]
    list_FOB03 = max_min_Val(arg_FOB03)

    arg_FOB04 = datalist[4][3]
    list_FOB04 = max_min_Val(arg_FOB04)

    arg_FOB05 = datalist[5][3]
    list_FOB05 = max_min_Val(arg_FOB05)

    arg_FOB06 = datalist[6][3]
    list_FOB06 = max_min_Val(arg_FOB06)

    arg_FOB07 = datalist[7][3]
    list_FOB07 = max_min_Val(arg_FOB07)

    arg_FOB08 = datalist[8][3]
    list_FOB08 = max_min_Val(arg_FOB08)

    arg_FOB09 = datalist[9][3]
    list_FOB09 = max_min_Val(arg_FOB09)

    arg_FOB10 = datalist[10][3]
    list_FOB10 = max_min_Val(arg_FOB10)

    arg_FOB11 = datalist[11][3]
    list_FOB11 = max_min_Val(arg_FOB11)

    arg_CIF01 = datalist[13][3]
    list_CIF01 = max_min_Val(arg_CIF01)

    arg_CIF02 = datalist[14][3]
    list_CIF02 = max_min_Val(arg_CIF02)

    arg_CIF03 = datalist[15][3]
    list_CIF03 = max_min_Val(arg_CIF03)

    arg_CIF04 = datalist[16][3]
    list_CIF04 = max_min_Val(arg_CIF04)

    arg_CIF05 = datalist[17][3]
    list_CIF05 = max_min_Val(arg_CIF05)

    arg_CIF06 = datalist[18][3]
    list_CIF06 = max_min_Val(arg_CIF06)

    arg_CIF07 = datalist[19][3]
    list_CIF07 = max_min_Val(arg_CIF07)

    arg_CIF08 = datalist[20][3]
    list_CIF08 = max_min_Val(arg_CIF08)

    arg_CIF09 = datalist[21][3]
    list_CIF09 = max_min_Val(arg_CIF09)

    arg_CIF10 = datalist[22][3]
    list_CIF10 = max_min_Val(arg_CIF10)

    arg_CIF11 = datalist[23][3]
    list_CIF11 = max_min_Val(arg_CIF11)

    price_list = [
        ['02032',today,list_FOB01[0],list_FOB01[1],list_FOB01[2]],
        ['02033',today,list_FOB02[0],list_FOB02[1],list_FOB02[2]],
        ['02034',today,list_FOB03[0],list_FOB03[1],list_FOB03[2]],
        ['02035',today,list_FOB04[0],list_FOB04[1],list_FOB04[2]],
        ['02036',today,list_FOB05[0],list_FOB05[1],list_FOB05[2]],
        ['02037',today,list_FOB06[0],list_FOB06[1],list_FOB06[2]],
        ['02038',today,list_FOB07[0],list_FOB07[1],list_FOB07[2]],
        ['02039',today,list_FOB08[0],list_FOB08[1],list_FOB08[2]],
        ['02040',today,list_FOB09[0],list_FOB09[1],list_FOB09[2]],
        ['02041',today,list_FOB10[0],list_FOB10[1],list_FOB10[2]],
        ['02042',today,list_FOB11[0],list_FOB11[1],list_FOB11[2]],
        ['02043',today,list_CIF01[0],list_CIF01[1],list_CIF01[2]],
        ['02044',today,list_CIF02[0],list_CIF02[1],list_CIF02[2]],
        ['02045',today,list_CIF03[0],list_CIF03[1],list_CIF03[2]],
        ['02046',today,list_CIF04[0],list_CIF04[1],list_CIF04[2]],
        ['02047',today,list_CIF05[0],list_CIF05[1],list_CIF05[2]],
        ['02048',today,list_CIF06[0],list_CIF06[1],list_CIF06[2]],
        ['02049',today,list_CIF07[0],list_CIF07[1],list_CIF07[2]],
        ['02050',today,list_CIF08[0],list_CIF08[1],list_CIF08[2]],
        ['02051',today,list_CIF09[0],list_CIF09[1],list_CIF09[2]],
        ['02052',today,list_CIF10[0],list_CIF10[1],list_CIF10[2]],
        ['02053',today,list_CIF11[0],list_CIF11[1],list_CIF11[2]]

    ]

    print(price_list)

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 鎳礦海運費
# 02054 --> 菲律賓Zambales
# 02055 --> 菲律賓Surigao
# 02056 --> 印尼Sulawesi
def cnfeol02_ship_getdata(datalist):
    global err_flag
    global err_log

    print(datalist)

    arg_Zambales = datalist[1][2]
    list_Zambales = max_min_Val(arg_Zambales)
    arg_Surigao = datalist[2][1]
    list_Surigao = max_min_Val(arg_Surigao)
    arg_Sulawesi = datalist[3][2]
    list_Sulawesi = max_min_Val(arg_Sulawesi)

    price_list = [
        ['02054',today,list_Zambales[0],list_Zambales[1],list_Zambales[2]],
        ['02055',today,list_Surigao[0],list_Surigao[1],list_Surigao[2]],
        ['02056',today,list_Sulawesi[0],list_Sulawesi[1],list_Sulawesi[2]]
    ]
    print(price_list)

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 鉻礦外盤價格
# 02060 --> 南非鉻礦(42-44%精礦)
# 02061 --> 南非鉻礦(40-42%精礦)
# 02062 --> 土耳其鉻礦(40-42%精礦)
# 02063 --> 伊朗鉻礦(40-42%精礦)
def cnfeol03_getdata(datalist):
    global err_flag
    global err_log

    for i1,i2 in enumerate(datalist):
        tempidx_1 = datalist[i1][0]
        tempidx_2 = datalist[i1][1]
        arg_1 = datalist[i1][4]
        if (tempidx_1 == '南非铬矿') and (tempidx_2 == '42-44%精矿'):
            print(arg_1)
            list01 = max_min_Val(arg_1)
        elif (tempidx_1 == '南非铬矿') and (tempidx_2 == '40-42%精矿'):
            print(arg_1)
            list02 = max_min_Val(arg_1)
        elif (tempidx_1 == '土耳其铬矿') and (tempidx_2 == '40-42%块矿'):
            print(arg_1)
            list03 = max_min_Val(arg_1)
        elif (tempidx_1 == '伊朗铬矿') and (tempidx_2 == '40-42%块矿'):
            print(arg_1)
            list04 = max_min_Val(arg_1)
    price_list = [
        ['02060',today,list01[0],list01[1],list01[2]],
        ['02061',today,list02[0],list02[1],list02[2]],
        ['02062',today,list03[0],list03[1],list03[2]],
        ['02063',today,list04[0],list04[1],list04[2]]
    ]
    print(price_list)
    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)


# 鎳鐵早訊
# 02001 --> 高鎳鐵主流成交價格
# 02002 --> 低鎳鐵主流成交價格

def cnfeol04_getdata(NewsContent):
    global err_flag
    global err_log

    target_Hstr = re.compile(r'NI8-10％([0-9]+)-([0-9]+)（-）/([0-9]+)-([0-9]+)')
    High_Ni = target_Hstr.search(NewsContent)

    target_Lstr = re.compile(r'NI1.5-1.8％([0-9]+)-([0-9]+)（-）/([0-9]+)-([0-9]+)')
    Low_Ni = target_Lstr.search(NewsContent)

    print(High_Ni)
    H_max = High_Ni.group(3)
    H_min = High_Ni.group(4)
    H_vul = str((decimal.Decimal(H_max) + decimal.Decimal(H_min))/2)

    print(Low_Ni)
    L_max = Low_Ni.group(3)
    L_min = Low_Ni.group(4)
    L_vul = str((decimal.Decimal(L_max) + decimal.Decimal(L_min))/2)
    

    price_list = [
        ['02001',today,H_vul,H_max,H_min],
        ['02002',today,L_vul,L_max,L_min]
    ]
    print(price_list)

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 全國主要地區高鎳鐵價格
# 02003 --> 全國主要地區高鎳鐵價格(內蒙)
# 02004 --> 全國主要地區高鎳鐵價格(江蘇)
# 02005 --> 全國主要地區高鎳鐵價格(遼寧)
# 02006 --> 全國主要地區高鎳鐵價格(山東)
def cnfeol05_getdata(datalist):
    global err_flag
    global err_log

    for i1,i2 in enumerate(datalist):
        tempidx_1 = datalist[i1][6]
        arg_1 = datalist[i1][4]
        if (tempidx_1 == '内蒙'):
            print(arg_1)
            list01 = max_min_Val(arg_1)
        elif (tempidx_1 == '江苏'):
            print(arg_1)
            list02 = max_min_Val(arg_1)
        elif (tempidx_1 == '辽宁'):
            print(arg_1)
            list03 = max_min_Val(arg_1)
        elif (tempidx_1 == '山东'):
            print(arg_1)
            list04 = max_min_Val(arg_1)
    price_list = [
        ['02003',today,list01[0],list01[1],list01[2]],
        ['02004',today,list02[0],list02[1],list02[2]],
        ['02005',today,list03[0],list03[1],list03[2]],
        ['02006',today,list04[0],list04[1],list04[2]]
    ]
    print(price_list)

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

#普硅高鉻主流成交價格華北
# 02007 --> 普硅高鉻主流成交價格華北
def cnfeol06_getdata(NewsContent):
    global err_flag
    global err_log

    target_Hstr = re.compile(r'华北([0-9]+)-([0-9]+)')
    High_Cr = target_Hstr.search(NewsContent)

    print(High_Cr)
    H_max = High_Cr.group(1)
    H_min = High_Cr.group(2)
    H_vul = str((decimal.Decimal(H_max) + decimal.Decimal(H_min))/2)

    price_list = [
        ['02007',today,H_vul,H_max,H_min]
    ]
    print(price_list)

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

#國內鉬鐵承兌成交價
# 02008 --> 國內鉬鐵承兌成交價
def cnfeol07_getdata(datalist):
    global err_flag
    global err_log

    arg_1 = datalist[2][6]
    list01 = max_min_Val(arg_1)
    price_list = [
        ['02008',today,list01[0],list01[1],list01[2]]
    ]
    print(price_list)
    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

#鉬鐵65-70%歐洲CFO鉬鐵氧化鉬價格
# 02009 --> 國內鉬鐵承兌成交價
def cnfeol08_getdata(datalist):
    global err_flag
    global err_log

    max_vul = datalist[1][2]
    min_vul = datalist[1][1]
    vul = str((decimal.Decimal(max_vul) + decimal.Decimal(min_vul))/2)
    price_list = [
        ['02009',today,vul,max_vul,min_vul]
    ]
    print(price_list)

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 全國主要地區山西65 山西75 廣西75 貴州75 高碳錳鐵價格
# 02010 --> 全國主要地區高碳錳鐵(山西femn65c7.0P≤0.2)
# 02011 --> 全國主要地區高碳錳鐵(廣西femn75c7.0P≤0.2)
# 02012 --> 全國主要地區高碳錳鐵(山西femn75c7.0P≤0.2)
# 02013 --> 全國主要地區高碳錳鐵(貴州femn75c7.0P≤0.2)
def cnfeol09_getdata(datalist):
    global err_flag
    global err_log

    arg_flag01 = True
    arg_flag02 = True
    arg_flag03 = True
    arg_flag04 = True
    for i1,i2 in enumerate(datalist):
        if len(datalist[i1]) == 7 :
            tempidx_1 = datalist[i1][1]
            tempidx_2 = datalist[i1][6]
            arg_1 = datalist[i1][4]
            if tempidx_1 == 'femn65c7.0P≤0.2' and tempidx_2 == '山西' and arg_flag01 :
                list01 = max_min_Val(arg_1)
                arg_flag01 = False
            elif tempidx_1 == 'femn75c7.0P≤0.2' and tempidx_2 == '广西' and arg_flag02 :
                list02 = max_min_Val(arg_1)
                arg_flag02 = False
            elif tempidx_1 == 'femn75c7.0P≤0.2' and tempidx_2 == '山西' and arg_flag03 :
                list03 = max_min_Val(arg_1)
                arg_flag03 = False
            elif tempidx_1 == 'femn75c7.0P≤0.2' and tempidx_2 == '贵州' and arg_flag04 :
                list04 = max_min_Val(arg_1)
                arg_flag04 = False

    price_list = [
        ['02010',today,list01[0],list01[1],list01[2]],
        ['02011',today,list02[0],list02[1],list02[2]],
        ['02012',today,list03[0],list03[1],list03[2]],
        ['02013',today,list04[0],list04[1],list04[2]]
    ]
    print(price_list)
    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 北方區域錳鐵行情
# 02014 --> 北方區域Mn75%
def cnfeol10_getdata(datalist):
    global err_flag
    global err_log

    for i1,i2 in enumerate(datalist):
        if len(datalist[i1]) == 4:
            tempidx_1 = datalist[i1][0]
            arg_1 = datalist[i1][1]
            if tempidx_1 == '高碳75c7.0P<0.2':
                target_str = re.compile(r'([0-9]+-[0-9]+)（北方地区）')
                mo = target_str.search(arg_1)
                if mo:
                    print(tempidx_1, arg_1)
                    print(mo.group(1))
                    list01 = max_min_Val(arg_1)

    price_list = [
        ['02014',today,list01[0],list01[1],list01[2]]
    ]
    print(price_list)

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 太鋼青山張浦招標價格
# 02015 --> 江蘇某鋼廠 招標價格(張家港浦項)
# 02016 --> 江蘇某鋼廠 招標價格(太鋼)
# 02017 --> 江蘇某鋼廠 招標價格(青山鼎信)
def cnfeol11_getdata(datalist, arg_itemno):
    global err_flag
    global err_log

    arg_1 = datalist[1][2]
    list01 = max_min_Val(arg_1)
    price_list = [
        [arg_itemno,today,list01[0],list01[1],list01[2]]
    ]
    print(price_list)

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 太鋼寶鋼酒鋼青山鉻鐵月招標價格
# 02070 --> 高碳鉻鐵月份招標價(寶鋼德盛)
# 02071 --> 高碳鉻鐵月份招標價(酒鋼)
# 02072 --> 高碳鉻鐵月份招標價(太鋼)
# 02073 --> 高碳鉻鐵月份招標價(青山)
# 此為記錄月份 ,故資料庫存放日期一律為當月1號
def cnfeol12_getdata(datalist, arg_itemno):
    global err_flag
    global err_log

    arg_flag01 = True
    for i1,i2 in enumerate(datalist):
        tempidx_1 = datalist[i1][1]
        if tempidx_1 == month_01 and arg_flag01:
            arg_1 = datalist[i1][3]
            arg_flag01 = False

    if not arg_flag01:
        print(arg_1)

        price_list = [
            [arg_itemno,today_03,arg_1]
        ]
        print(price_list)
    else:
        price_list = []

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

# 太鋼寶鋼鉬鐵月招標價格
# 02080 --> 鉬鐵月招標價格(山西 太鋼)
# 02081 --> 鉬鐵月招標價格(上海 寶鋼)
# 此為記錄月份 ,故資料庫存放日期一律為當月1號
def cnfeol13_getdata(datalist, arg_itemno):
    global err_flag
    global err_log

    arg_flag01 = True
    for i1,i2 in enumerate(datalist):
        tempidx_1 = datalist[i1][1]
        print(month_01, tempidx_1)
        if tempidx_1 == month_01 and arg_flag01:
            arg_1 = datalist[i1][3]
            arg_flag01 = False

    if not arg_flag01:
        print(arg_1)
        list01 = max_min_Val(arg_1)
        price_list = [
            [arg_itemno,today_03,list01[0],list01[1],list01[2]]
        ]
        print(price_list)
    else:
        price_list = []

    #寫入資料庫
    if len(price_list) > 0:
        result = db_process2(price_list)
        err_flag = result[0]
        err_log.write(result[1])
        print(result)

if __name__ == '__main__':
    info_cnfeol()