from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import date ,timedelta  
import re
import time

chrome_path = "C:\selenium_driver_chrome\chromedriver.exe" #chromedriver.exe執行檔所存在的路徑
driver = webdriver.Chrome(chrome_path)
# driver = webdriver.Firefox()

today = str(date.today() + timedelta(days=-1)).replace("-","")
#today = str(date.today()).replace("-","")
print(today)
today_01 = today[4:6] + '月' + today[6:8] + '日'
print(today_01)
arg_url = "http://www.cnfeol.com/" 

#def login(arg_url):
#	driver.get(arg_url)
#	username = driver.find_element_by_name("Signin_MemberName")
#	username.send_keys("yusco01")
#	password = driver.find_element_by_name("Signin_MemberPassword")
#	password.send_keys("6231580")
#	driver.find_element_by_xpath("//input[@type='submit'][@name='Signin_Submit']").click()

def login(arg_url):
	driver.get(arg_url)
	driver.find_element_by_xpath("//*[@id='LoginBox']/a[2]").click()
	time.sleep(10)
	username = driver.find_element_by_xpath('//*[@id="TextBoxScreenName"]')
	username.send_keys("yusco01")
	password = driver.find_element_by_xpath("//*[@id='TextBoxPassword']")
	password.send_keys("6231580")
	driver.find_element_by_xpath("//input[@type='submit'][@name='ButtonLogin']").click()
 	
def item01_content(arg_1, arg_url):
	driver.get(arg_url)
	table = driver.find_element_by_id("contentlistcontainer")

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
			print([td.text for td in row.find_elements_by_xpath(".//td[text()]")])
	else:
		print(arg_1 + ",尚未產生")

def item02_content(arg_1, arg_url):
	driver.get(arg_url)
	table = driver.find_element_by_id("result_body")
	tt_1 = ""
	for link_txt in table.find_elements_by_xpath(".//div[@class='resultitem']//a[@class='title']"): 
		tt = link_txt.get_attribute('href')
		if (link_txt.text == arg_1):
			tt_1 = tt
		print(link_txt.text)
	if tt_1 != "":
		driver.get(tt_1)
		aa = driver.find_element_by_xpath("//*[@id='contentdetail_info_detail']/p").text
		print(aa)
		target_str = re.compile(r'NI8-10％([0-9]+)-([0-9]+)')
		mo = target_str.search(aa)

		print(mo.group(0))
		print(mo.group(1))
		print(mo.group(2))


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


"""
#菲律宾红土镍矿港口价格
arg_1 = today_01 + '菲律宾红土镍矿港口价格'
arg_url = "http://www.cnfeol.com/niekuang_ab_19/all-1.aspx"
item01_content(arg_1,arg_url)

#菲律宾红土镍矿外盘价格
arg_1 = today_01 + '菲律宾红土镍矿外盘价格'
arg_url = "http://www.cnfeol.com/niekuang/p-2-1.aspx"
item01_content(arg_1,arg_url)

#铬矿外盘价格
arg_1 = today_01 + '铬矿外盘价格'
arg_url = "http://www.cnfeol.com/gekuang/p-2-1.aspx"
item01_content(arg_1,arg_url)
"""

#全国主要地区高镍铁价格
arg_1 = today_01 + '全国主要地区高镍铁价格'
arg_url = "http://www.cnfeol.com/nietie/p-1-1.aspx"
item01_content(arg_1,arg_url)

#镍铁早讯
#arg_1 = today_01 + "镍铁早讯"
#arg_url = "http://hjs.cnfeol.com/search.aspx?key=镍铁早讯&ie=utf-8&cl=0"
#item02_content(arg_1,arg_url)

# logout
#driver.get("http://www.cnfeol.com/member/membersignout.aspx")

print ("end of prog...")

#driver.close()


#for row in table.find_elements_by_xpath(".//ul"): 
#	print([td.text for td in row.find_elements_by_xpath(".//li/span[text()]")])

#for link in table.find_elements_by_xpath("//*[@href]"):
#    print(link.get_attribute('href'))

#for td in table.find_elements_by_xpath(".//ul/li//span[text()]"): 
#    	print(td.text)

#for link in table.find_elements_by_xpath(".//ul/li//a[@href]"): 
#    	print(link.get_attribute('href'))

#driver.find_element_by_xpath(".//ul/li//a[text()='11月21日菲律宾红土镍矿港口价格']").click()
