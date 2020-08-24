
# -*- coding: utf-8 -*-
"""
MAIL_SENDER 郵件發送

@Usage: 
	發送郵件程式
	def SEND_MAIL(arg_recipient, arg_subject, arg_msg, arg_msg_type)

	傳入參數說明:
		arg_recipient: 收件者MAIL
		arg_subject: 郵件主旨
		arg_msg: 郵件內容
		arg_msg_type: 郵件內文型態('plain': 純文字, 'html': 網頁)

	return err_code
	err_code 代表意義 
	0: 正常結束
	1: 缺少收件者MAIL參數
	2: 其他錯誤

@Note: 


"""
import smtplib
import datetime
from email.mime.text import MIMEText


def SEND_MAIL(arg_recipient, arg_subject, arg_msg, arg_msg_type):
	rt_code = 0

	#取得郵件發送系統參數
	sender_host = '100.1.1.5'
	sender_port = '25'
	sender_mail = 'yu62493@mail.yusco.com.tw'
	sender_id = 'YUSCO\\ecmail'
	sender_pwd = '!ecyucrmdmc'

	rt_desc = ""
	if len(arg_recipient) == 0:
		rt_code = 1
		rt_desc = "缺少收件者MAIL參數."

	if len(arg_subject) == 0:
		arg_subject = "無主旨"

	if len(arg_msg) == 0:
		arg_msg = " "

	if len(arg_msg_type) == 0:
		arg_msg_type = "plain"

	if rt_code == 0:
		curr_dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		recipient = arg_recipient

		msg = MIMEText(arg_msg, arg_msg_type)
		msg['Subject'] = arg_subject
		msg['From'] = sender_mail
		msg['To'] = recipient

		try:
			server = smtplib.SMTP(sender_host, sender_port)
			server.ehlo()
			server.login(sender_id, sender_pwd)
			server.send_message(msg)
			server.quit()
			print(curr_dt + ' Email sent.')
		except Exception as e:
			rt_code = 5
			print(str(e))
			print("Err exception from MAIL_SENDER")
			print(str(e.args[0]))
			f = open("MAIL_SENDER_LOG.txt", "a")
			f.write("MAIL_SENDER Err:\n" + curr_dt + "\n" + str(e.args) + "\n\n")
			f.close()
			print('The mail not sent.')

	return rt_code, rt_desc

if __name__ == '__main__':
	print('請勿直接執行本程式...')	