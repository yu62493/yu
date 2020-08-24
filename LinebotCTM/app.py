from flask import Flask, request, abort ,send_from_directory

from linebot import (LineBotApi, WebhookHandler, WebhookParser)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, 
    TemplateSendMessage, ConfirmTemplate, PostbackTemplateAction, MessageTemplateAction, 
    ButtonsTemplate, URITemplateAction, CarouselTemplate, CarouselColumn
    )
from YUSCO.Line.get_coil import db_pcmb030m, db_pcmb020m, db_pcmb025h, db_shpa011m, db_wipb040_041h, db_tqcl500m
from YUSCO.Line.get_photo import get_CombinePhoto, cr_pass
from YUSCO.Util.comm_code import OperCode_dic, OperCodePhoto_dic
from YUSCO.Util.linebot_parm import linebot_dic
from YUSCO.Line.status_rep import coil_status_rep,coil_wip_report,coil_order_rep,coil_tqc_report,coil_pcm_report
from YUSCO.Util.linebot_auth_mail import Auth_MAIL
from YUSCO.Util.linebot_auth_token import AUTH_URL_TOKEN,check_auth
from YUSCO.Core.DB_ORACLE import OracleDB_dic

#import YUSCO.Util.LINE_BOT_AUTH_MAIL as LINE_BOT_AUTH_MAIL
#import YUSCO.Util.LINE_BOT_AUTH_TOKEN as LB_AUTH_TOKEN
import cx_Oracle
import os

app = Flask(__name__)

@app.route('/YUSCO/<path:path>')
def send_images(path):
    return send_from_directory('YUSCO', path)

ngrok_url = linebot_dic('ngrok')
# Channel Access Token
line_bot_api = LineBotApi(linebot_dic('line_token'))
# Channel Secret
parser = WebhookParser(linebot_dic('webhook_token'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_id = str(event.source.user_id)
        result = check_auth(line_id)
        text=event.message.text
        command_text = text[:3].lower().strip()
        if len(text) > 3 :
            command_id = text[2].lower()
        else:
            command_id = '0'

        if result:
            if (command_text == '/au'):
                line_bot_api.reply_message(
                    event.reply_token,
                    [ 
                        TextSendMessage(text='已獲授權,請直接輸入鋼捲編號使用')
                    ]
                )                                
            elif (command_id == 's'):
                coil_no = text.strip().upper()
                resultA = coil_pcm_report(coil_no)
                if resultA:
                    Choice01_str = '/st' + coil_no
                    Choice02_str = '/wp' + coil_no
                    Choice03_str = '/tq' + coil_no

                    buttons_template = ButtonsTemplate(
                    title=coil_no, text="鋼捲查詢系統", actions=[
                        MessageTemplateAction(label='訂單查詢', text=Choice01_str),
                        MessageTemplateAction(label='品檢相關', text=Choice02_str),
                        MessageTemplateAction(label='機械性質', text=Choice03_str)
                    ])
                    template_message = TemplateSendMessage(alt_text='請選擇下列選項進行查詢', template=buttons_template)

                    line_bot_api.reply_message(
                        event.reply_token,
                        [ 
                            template_message,
                            ImageSendMessage(
                                original_content_url= ngrok_url + 'YUSCO/Line/images/PCM' + coil_no + 'Report.png',
                                preview_image_url= ngrok_url + 'YUSCO/Line/images/PCM' + coil_no + 'Report.png')
                        ]
                    )                 
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        [ 
                            TextSendMessage(text='輸入之鋼捲編號於製程記錄檔中無紀錄')
                        ]
                    )                
            else:
                if(command_text=='/me'):
                    content = str(event.source.user_id)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=content)
                    )
                elif(command_text=='/pr'):
                    profile = line_bot_api.get_profile(str(event.source.user_id))
                    print(profile.display_name)
                    print(profile.user_id)
                    print(profile.picture_url)
                    print(profile.status_message)
                elif(command_text=='/id'):
                    line_bot_api.reply_message(
                        event.reply_token,
                        [ 
                            TextSendMessage(text='已調整為直接輸入產品編號查詢\uDBC0\uDC84')
                        ]
                    )            
                elif(command_text=='/st'):
                    flag = 0
                    coil_no = text.upper()[3:]
                    resultA = db_pcmb020m(coil_no)
                    if not resultA:
                        resultA = db_shpa011m(coil_no)
                        if not resultA:
                            resultA = db_pcmb025h(coil_no)
                            if not resultA:
                                print('找不到產品')
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    [ 
                                        TextSendMessage(text='產品編號:' + coil_no + ';' + '找不到')
                                    ]
                                )            
                            else:
                                flag = 3
                        else:
                            flag = 2
                    else:
                        flag = 1

                    if flag > 0:
                        print(resultA)
                        order_no_item = resultA[0][3]
                        coil_order_rep(order_no_item)
                        if flag == 1:
                            textContent = ( '產品編號:{};目前在製擋中\uDBC0\uDC84 \n'
                                            '目前產線:{} \n'
                                            '缺陷1:{}').format(coil_no, resultA[0][1], resultA[0][2])
                        elif flag == 2:
                            textContent = ( '產品編號:{};已經交運\uDBC0\uDC84 \n'
                                            '產品碼:{} \n'
                                            '交運單號:{} \n'
                                            '產品厚度:{} \n'
                                            '交運重量:{}' ).format(coil_no, resultA[0][1], resultA[0][2], str(resultA[0][5]),str(resultA[0][4]) )
                        elif flag == 3:
                            textContent = ( '產品編號:{};目前庫存中\uDBC0\uDC84 \n'
                                            '產品碼:{} \n'
                                            '缺陷1:{}' ).format(coil_no, resultA[0][1], resultA[0][2])
                        line_bot_api.reply_message(
                            event.reply_token,
                            [ 
                                TextSendMessage(text=textContent),
                                ImageSendMessage(
                                    original_content_url= ngrok_url + 'YUSCO/Line/images/ORD' + order_no_item + 'Report.png',
                                    preview_image_url= ngrok_url + 'YUSCO/Line/images/ORD' + order_no_item + 'Report.png')
                            ]
                        )
                elif(command_text=='/wp'):
                    coil_no = text.upper()[3:]
                    print(coil_no)
                    resultA = db_wipb040_041h(coil_no)
                    if resultA:
                        path_str = ""
                        photoid_list = []
                        for i1,i2 in enumerate(resultA):
                            photo_id = resultA[i1][1] + ',' + resultA[i1][0].strip() + ',' + resultA[i1][3] + ',' + resultA[i1][2].strip()
                            path_str = path_str + resultA[i1][1] + "-->"
                            photoid_list.append('/im' + photo_id)
                        path_str = path_str[:-3]

                        if (len(photoid_list) == 1):
                            buttons_template = ButtonsTemplate(
                            title=coil_no, text=path_str, actions=[
                                MessageTemplateAction(label=resultA[i1][1], text=photoid_list[i1])
                            ])
                        elif (len(photoid_list) == 2):
                            buttons_template = ButtonsTemplate(
                            title=coil_no, text=path_str, actions=[
                                MessageTemplateAction(label=resultA[i1][1], text=photoid_list[i1]),
                                MessageTemplateAction(label=resultA[i1-1][1], text=photoid_list[i1-1])
                            ])
                        elif (len(photoid_list) == 3):
                            buttons_template = ButtonsTemplate(
                            title=coil_no, text=path_str, actions=[
                                MessageTemplateAction(label=resultA[i1][1], text=photoid_list[i1]),
                                MessageTemplateAction(label=resultA[i1-1][1], text=photoid_list[i1-1]),
                                MessageTemplateAction(label=resultA[i1-2][1], text=photoid_list[i1-2])
                            ])
                        else:
                            buttons_template = ButtonsTemplate(
                            title=coil_no, text=path_str, actions=[
                                MessageTemplateAction(label=resultA[i1][1], text=photoid_list[i1]),
                                MessageTemplateAction(label=resultA[i1-1][1], text=photoid_list[i1-1]),
                                MessageTemplateAction(label=resultA[i1-2][1], text=photoid_list[i1-2]),
                                MessageTemplateAction(label=resultA[i1-3][1], text=photoid_list[i1-3])
                            ])
                        template_message = TemplateSendMessage(alt_text='點選產線查詢', template=buttons_template)

                        line_bot_api.reply_message(
                            event.reply_token,
                            [ 
                                template_message
                            ]
                        )

                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            [ 
                                TextSendMessage(text='輸入之鋼捲編號於WIP記錄檔中無紀錄')
                            ]
                        )                
                elif(command_text=='/tq'):
                    coil_no = text.upper()[3:]
                    resultA = db_shpa011m(coil_no)
                    if resultA:  
                        product_code = resultA[0][1]
                        result = db_tqcl500m(coil_no,product_code)
                        if result:
                            test_id = result[0][0].strip()
                            coil_tqc_report(test_id,product_code)
                            line_bot_api.reply_message(
                                event.reply_token,
                                [ 
                                    ImageSendMessage(
                                        original_content_url= ngrok_url + 'YUSCO/Line/images/TQC' + test_id + product_code + 'Report.png',
                                        preview_image_url= ngrok_url + 'YUSCO/Line/images/TQC' + test_id + product_code + 'Report.png')
                                ]
                            )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            [ 
                                TextSendMessage(text='輸入之鋼捲編號尚未交運,無機械性質')
                            ]
                        )                

                elif(command_text=='/im'):
                    cmd_line = text[3:]
                    
                    cmd_list = cmd_line.split(",")
                    pos_idx = len(cmd_line) - 1 - cmd_line[::-1].index(',')
                    photo_id = cmd_line[0:pos_idx].replace(',','')
                    
                    coil_no = cmd_list[1]
                    station = cmd_list[0]
                    schd_no = cmd_list[3]
                    data_date = cmd_list[2]
                    resultW = coil_wip_report(coil_no,station,schd_no)
                    # qc 再處理通知單中的 特放產品
                    resultPass = cr_pass(coil_no,station,schd_no,data_date)
                    # 特放品是 qc_sp_remark 非空白
                    # 為了取代拋送非特放的非必要性,改用相關資料傳送
                    pass_txt = 'coil_no : {} \nstation : {} \nschd_no : {} \n非特放品'.format(coil_no,station,schd_no)
                    if resultPass:
                        if resultPass[0][2].strip() != '':
                            pass_txt = '特放品 : {}'.format(resultPass[0][2])
                    result = get_CombinePhoto(photo_id)

                    if result :
                        if resultW:
                            line_bot_api.reply_message(
                                event.reply_token,
                                [ 
                                    TextSendMessage(text=pass_txt),
                                    ImageSendMessage(
                                        original_content_url= ngrok_url + 'YUSCO/Line/images/WIP' + coil_no + station + 'Report.png',
                                        preview_image_url= ngrok_url + 'YUSCO/Line/images/WIP' + coil_no + station + 'Report.png'),
                                    ImageSendMessage(
                                        original_content_url= ngrok_url + 'YUSCO/Line/images/' + photo_id + '.png',
                                        preview_image_url= ngrok_url + 'YUSCO/Line/images/' + photo_id + '.png')
                                ]
                            )
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                [ 
                                    TextSendMessage(text=pass_txt),
                                    TextSendMessage(text='WIP無相關檢驗資料'),
                                    ImageSendMessage(
                                        original_content_url= ngrok_url + 'YUSCO/Line/images/' + photo_id + '.png',
                                        preview_image_url= ngrok_url + 'YUSCO/Line/images/' + photo_id + '.png')
                                ]
                            )
                            
                    else:
                        if resultW:
                            line_bot_api.reply_message(
                                event.reply_token,
                                [ 
                                    TextSendMessage(text=pass_txt),
                                    ImageSendMessage(
                                        original_content_url= ngrok_url + 'YUSCO/Line/images/WIP' + coil_no + station + 'Report.png',
                                        preview_image_url= ngrok_url + 'YUSCO/Line/images/WIP' + coil_no + station + 'Report.png'),
                                    TextSendMessage(text='品檢線無相關缺陷照片')
                                ]
                            )
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                [ 
                                    TextSendMessage(text=pass_txt),
                                    TextSendMessage(text='WIP無相關檢驗資料'),
                                    TextSendMessage(text='品檢線無相關缺陷照片')
                                ]
                            )

                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=text+',看不懂')
                    )
                    
        elif(command_text=='/au'):
            empl_no = text[3:]
            print(empl_no)                
            profile = line_bot_api.get_profile(str(event.source.user_id))

            print('工號' + empl_no + '進行身分驗證.')

            #發送認證信件
            rt_code = Auth_MAIL(empl_no, str(event.source.user_id))
            
            if rt_code == 0:
                msg = '你好，請至公司信箱收取認證信件'
            elif rt_code == 1:
                msg = '帳號' + empl_no + '已驗證過，不再重複認證.'
            elif rt_code == 2:
                msg = '帳號' + empl_no + '短時間重複認證請求.'
            else:
                msg = '其他原因錯誤，驗證請求失敗.'

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg)
            )
        elif(command_text=='/sp'):
            conform_txt = text[3:8]
            empl_no = text[8:].strip()
            line_userid = event.source.user_id
            print(conform_txt)
            print(empl_no)
            print()
            if conform_txt == '62493':
                #建立資料庫連線
                conn = cx_Oracle.connect(OracleDB_dic('RP547A_TQC'))
                cursor = conn.cursor()

                strsql  = "insert into LINEBOT_USER (EMPL_NO,LINE_USERID,TOKEN,USER_STATE"
                strsql += ") values ("
                strsql += "'" + empl_no + "', "
                strsql += "'" + line_userid + "', "
                strsql += "'62493',"
                strsql += "'Y' "
                strsql += ") "
                try:
                    cursor.execute(strsql)
                    conn.commit()
                except cx_Oracle.DatabaseError as e:
                    print(strsql + "\n")
                    print(str(e))
                cursor.close()
                conn.close()

        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='未經授權,無法讀取,請輸入 /au工號,進行認證,例如 : /au62493 ,如依然無法使用請洽生產資訊處')
            )
            
    return 'OK'


@app.route("/auth", methods=['GET'])
def user_auth():
    token = request.args.get('token')

    #郵件驗證
    rt_code, line_userid = AUTH_URL_TOKEN(token)

    msg = ""
    if rt_code == 0:
        msg = '你已通過驗證，歡迎使用!'
    else:
        msg = '驗證失敗'

    return msg

@app.route("/", methods=['GET'])
def basic_url():
    return 'OK'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
