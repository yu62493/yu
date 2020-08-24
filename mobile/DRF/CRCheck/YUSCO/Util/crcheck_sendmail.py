# -*- coding: utf-8 -*-
"""
crcheck_sendmail 點檢設備異常及時傳送MAIL

@Note: 


"""
import os
import smtplib

import hashlib
import cx_Oracle
import json
from datetime import datetime, timedelta, time
from email.mime.text import MIMEText

### 以下import自行開發公用程式 ###
from YUSCO.Util.mail_sender import SEND_MAIL
from YUSCO.Core.DB_ORACLE import OracleDB_dic


def CRcheck_Auth_MAIL(CKData):

	rt_code = 1
	CC = json.loads(CKData)
	#print('CKData=========',CKData)
	print('CK_REMARK=====',CC["CK_REMARK"])
	print('CK_RESULT=====',CC["CK_RESULT"])
	print('DATA_1=====',CC["DATA_1"])
	print('DATA_2=====',CC["DATA_2"])
	print('DATA_3=====',CC["DATA_3"])
	print('DATA_4=====',CC["DATA_4"])

	if CC["DATA_1"] == 'null':
		CC["DATA_1"] = 0

	if CC["DATA_2"] == 'null':
		CC["DATA_2"] = 0

	if CC["DATA_3"] == 'null':
		CC["DATA_3"] = 0

	if CC["DATA_4"] == 'null':
		CC["DATA_4"] = 0

	#如點檢設備正常則不寄送MAIL
	#DATA_1、DATA_2 震動值管制大於15屬異常
	#DATA_3、DATA_4 溫度值管制大於90屬異常
	if CC["CK_RESULT"] != 'true' or int(CC["DATA_1"]) > 15 or int(CC["DATA_2"]) > 15 or \
		int(CC["DATA_3"]) > 90 or int(CC["DATA_4"]) > 90:

		#建立資料庫連線
		conn = cx_Oracle.connect(OracleDB_dic('RP547A_TQC'))

		#抓取設備相關中文名稱
		s_sql = "select ck_location,maint_dp, "
		s_sql = s_sql + "(select kind from mech001m where device_code = mech002m.device_code) as kind, "
		s_sql = s_sql + "(select device_name from mech001m where device_code = mech002m.device_code) as device_name, "
		s_sql = s_sql + "(select employee_name from mechpriv where employee_id = '" + CC["MAINT_USER"] + "') as ck_personnel "
		s_sql = s_sql + "from MECH002M where location_code ='" + CC["LOCATION_CODE"] + "'"

		#print('s_sql===',s_sql)
		cursor = conn.cursor()
		try:
			cursor.execute(s_sql)
			result = cursor.fetchone()
		except cx_Oracle.DatabaseError as e:
			error, = e.args
			print("抓取點檢相關中文名稱 錯誤:\n")
			print(s_sql + "\n")
			print("sql_code=" + str(error.code) + "\n")
			print("err_msg=" + error.message + "\n")

		#Close SQL connection
		conn.close

		#如抓取點檢相關中文名稱失敗則不寄送MAIL
		if result == None:
			return rt_code

		duty_dp = ''
		if result[1] == 'O':
			duty_dp = '操作'
		elif result[1] == 'M':
			duty_dp = '機修'
		elif result[1] == 'E':
			duty_dp = '儀電'

		ck_datetime = datetime.strptime(CC["CK_DATE"]+' '+CC["CK_TIME"], "%Y%m%d %H%M%S")
		ck_datetime = ck_datetime.strftime("%Y/%m/%d %H:%M:%S")

		#抓取發送郵件時間
		mail_sen_dt = (datetime.today()).strftime("%Y/%m/%d %H:%M:%S")
		arg_yu_empl_no = "63125"
		print("準備寄送郵件\n")


		#recipient = "yu" + str(arg_yu_empl_no) + "@mail.yusco.com.tw"
		recipient = "hong.yuan0831@gmail.com;aaaaa59874@gmail.com;alvan16888@gmail.com;yu62493@gmail.com"
		subject = "冷軋廠點檢設備異常通知 " + mail_sen_dt

		msg_body  = '<html><head></head>'
		msg_body  = '<body>'
		
		msg_body += ' <table border=0 bgcolor="#E0E0E0">'
		msg_body += ' <TR bgcolor="#FF0000">'
		msg_body += '	<TD align="center"  style="width:50"><font color="#FFFFFF"><b>區域</font></TD>'
		msg_body += '	<TD align="center"  style="width:110"><font color="#FFFFFF"><b>點檢設備</font></TD>'
		msg_body += '	<TD align="center"  style="width:150"><font color="#FFFFFF"><b>點檢部位</font></TD>'
		if int(CC["DATA_1"]) > 0 or int(CC["DATA_2"]) > 0 or int(CC["DATA_3"]) > 0 or int(CC["DATA_4"]) > 0:
			msg_body += '	<TD align="center"  style="width:60"><font color="#FFFFFF"><b>振動值WI</font></TD>'
			msg_body += '	<TD align="center"  style="width:60"><font color="#FFFFFF"><b>振動值WO</font></TD>'
			msg_body += '	<TD align="center"  style="width:60"><font color="#FFFFFF"><b>溫度值WI</font></TD>'
			msg_body += '	<TD align="center"  style="width:60"><font color="#FFFFFF"><b>溫度值WO</font></TD>'

		msg_body += '	<TD align="center"  style="width:130"><font color="#FFFFFF"><b>點檢時間</font></TD>'
		msg_body += '	<TD align="center"  style="width:180"><font color="#FFFFFF"><b>備註</font></TD>'
		msg_body += '	<TD align="center"  style="width:40"><font color="#FFFFFF"><b>權責單位</font></TD>'
		msg_body += '	<TD align="center"  style="width:50"><font color="#FFFFFF"><b>點檢人員</font></TD>'
		msg_body += ' </TR>'
		msg_body += ' <TR bgcolor="#FCFCFC">'
		msg_body += '	<TD align="left" >' + result[2] +'</TD>'
		msg_body += '	<TD align="left" >' + result[3] +'</TD>'
		msg_body += '	<TD align="left" >' + result[0] +'</TD>'

		if int(CC["DATA_1"]) > 0 or int(CC["DATA_2"]) > 0 or int(CC["DATA_3"]) > 0 or int(CC["DATA_4"]) > 0:
			msg_body += '	<TD align="left" >' + CC["DATA_1"] +'</TD>'
			msg_body += '	<TD align="left" >' + CC["DATA_2"] +'</TD>'
			msg_body += '	<TD align="left" >' + CC["DATA_3"] +'</TD>'
			msg_body += '	<TD align="left" >' + CC["DATA_4"] +'</TD>'

		msg_body += '	<TD align="center" >' + ck_datetime +'</TD>'
		msg_body += '	<TD align="left" >' + CC["CK_REMARK"] +'</TD>'
		msg_body += '	<TD align="left" >' + duty_dp +'</TD>'
		msg_body += '	<TD align="left" >' + result[4] +'</TD>'
		msg_body += ' </TR>'

		msg_body += ' </table>'		
		msg_body += ' <br>'

		msg_body += '<br><br><br>'
		msg_body += 'ps:<br>'
		msg_body += '1. 震動值管制大於15屬異常.<br>'
		msg_body += '2. 溫度值管制大於90屬異常.<br>'
		msg_body += '3. 本郵件自動發送，請勿回覆本郵件.<br>'
		msg_body += '</body></html>'
		rt_code, rt_desc = SEND_MAIL(recipient, subject, msg_body, 'html')
		print("郵件發送回傳=>code=" + str(rt_code) + ",  desc=" + rt_desc)

	return rt_code

if __name__ == '__main__':
	Auth_Downtime_MAIL()