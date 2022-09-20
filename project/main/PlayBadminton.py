#!/usr/bin/env python3
#coding:utf-8
import datetime
import email
import queue
import threading
import schedule
from Crypto.Cipher import AES
import base64
from email.mime.text import MIMEText
import json
import re
import smtplib
import time
from urllib.parse import urlencode
from fileinput import filename
from random import random
import requests
from soupsieve import select

from yzm.ocr import *
from ua import ua_change

def userInfoRead():
    with open('docs/user_config.json','r') as f:
      data = json.loads(f.read(),)
      return data

def email(text:str,InfoList:list):
    '''使用stmp邮箱服务发送邮件
    text:要发送的字符信息
    InfoList[0]:email from whom, eg. ****@****.com
    InfoList[1]:email to whom, eg. ****@****.com
    InfoList[2]:smtp Sever地址,eg:smtp.qq.com
    InfoList[3]:开放的端口号
    InfoList[4]:授权密码而非账户密码
    '''
    msg = MIMEText(text, 'plain', 'utf-8')
    msg_From = InfoList[0];
    msg_To = InfoList[1]
    smtpSever = InfoList[2]
    smtpPort = InfoList[3]
    sqm = InfoList[4]

    msg['from'] = msg_From
    msg['to'] = msg_To
    msg['subject'] = 'Python自动邮件-羽毛球场预约%s' % time.ctime()
    smtp = smtplib
    smtp = smtplib.SMTP_SSL(smtpSever)

    #smtplib的connect（连接到邮件服务器）、login（登陆验证）、sendmail（发送邮件）
    smtp.connect(smtpSever, smtpPort)
    smtp.login(msg_From, sqm)
    smtp.sendmail(msg_From, msg_To, str(msg))
    print("email已发送")
    smtp.quit()

class YiDongJiaoDa(object):
    def __init__(self,username,passward,PlatFlag,date='') -> None:
        '''
        username:登录平台用户名；passward：登录平台密码
        PlatFlag：0表示一楼 1表示三楼
        date：要预定的日期，格式为2022-06-11
        '''
        self.username = username;
        self.passward = passward;
        self.session = requests.session();
        self.session.keep_alive = False;
        self.session.headers['User-Agent'] = ua_change();
        print('随机配置UA信息',self.session.headers['User-Agent'])
        #41 一楼 42 三楼
        self.platid = ['41','42'][PlatFlag];
        self.allplat = {};
        
        if date == '':
            today = datetime.datetime.today()
            five_days_after = today + datetime.timedelta(days=5)
            self.date = five_days_after.strftime("%Y-%m-%d")
        else:
            self.date = date

    def login(self):
        def encrypt_pwd(pwd):
            ''' AES-ECB encrypt '''
            publicKey='0725@pwdorgopenp'
            publicKey = publicKey.encode('utf-8')
            # pkcs7 padding
            BS = AES.block_size
            pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
            pwd = pad(pwd)
            cipher = AES.new(publicKey, AES.MODE_ECB)
            pwd = cipher.encrypt(pwd.encode('utf-8'))
            return str(base64.b64encode(pwd), encoding='utf-8')
    
        card_data = {
            'flowID': '510',
            'type': '1',
            'apptype': '4',
            'Url': 'http%3a%2f%2f202.117.17.144',
            'MenuName': '场馆预订',
            'EMenuName': '场馆预订',
        }
        r = self.session.post('http://card.xjtu.edu.cn/Page/Page',json=card_data,allow_redirects=True)
        
        #---------------------openplatform   login-------------------------
        url_openplatform =  'https://org.xjtu.edu.cn/openplatform/g/admin/login';
        data = {             #密码经过AES加密
            "loginType": 1,
            "jcaptchaCode": "",
            "username": self.username,
            "pwd": encrypt_pwd(self.passward),
        }        
        r = self.session.post(url_openplatform,json=data);
        print('openplatform:',r.status_code,"\n统一认证平台提示:",r.json()['message']);

        #手动配置cookie open_Platform_User
        self.session.cookies.set('open_Platform_User', r.json()['data']['tokenKey'] , domain='org.xjtu.edu.cn')

        #---------------------getRedirectUrl-------------------------
        url_getRedirectUrl = 'https://org.xjtu.edu.cn/openplatform/oauth/auth/getRedirectUrl';
        t =int(round(time.time()*1000));
        param = {
            'userType': 1,
            'personNo': self.username,
            '_': str(t),
        }
        r = self.session.get(url=url_getRedirectUrl,params=param,allow_redirects=False);
        print("getRedirectUrl:",r.status_code,"\n重定向URL：",r.json()['message']);
        #开发者面板没有显示响应，但其实有响应的，返回的信息包含下次请求的跳转url,
        #包含以下关键信息 code state usertype service
        url_caslogin = r.json()['data'];
        # print(url_caslogin)

        #---------------------返回cas之前验证登录信息-------------------------
        r = self.session.get(url_caslogin);
        print("caslogin ",r.status_code);
        temp_content = r.text;

        #正则匹配数据
        lt = re.findall(r'name="lt" value="([0-9a-zA-Z-]+)',temp_content)[0]
        execution = re.findall(r'name="execution" value="([0-9a-zA-Z]+)',temp_content)[0]
        orgCode = re.findall(r'name="orgCode"  value="([0-9a-zA-Z]+)',temp_content)[0]
        print("lt:",lt,"orgcode:",orgCode)
        data={
            'username': ' ',   
            'password': ' ',
            # 'vcode': '',
            'lt': lt,
            'execution': execution,
            'orgCode': orgCode,
            'usertype': '1',
            'userEmployeeno': self.username,
            '_eventId': 'submit'
        }
        self.session.keep_alive = True;
        r = self.session.post(url_caslogin,data=data,allow_redirects=False)
        try:
            print("caslogin2:",r.status_code);
        except:
            print("error_caslogin2")

        #获取url
        url_ContechFirstPage = re.findall(r'window.location.href="(.*?)"',r.text)[0];
        print("已获得ticket ",url_ContechFirstPage)

        #该步耗时较长
        print("正在加载，请稍后……")
        r =self.session.get(url_ContechFirstPage,allow_redirects=False);
        print("url_ContechFirstPage",r.status_code)

        r = self.session.get('http://card.xjtu.edu.cn/',allow_redirects=False);
        print("card",r.status_code,"\n",re.findall(r'<div class="name">(.*?)</div>',r.text)[0])

        self.session.cookies.set('from', 'undefined' , domain='202.117.17.144')
        #返回之后五天的全部空场，用字典表示{时间：场地信息}
        card_data = {
            'flowID': '510',
            'type': '1',
            'apptype': '4',
            'Url': 'http%3a%2f%2f202.117.17.144',
            'MenuName': '场馆预订',
            'EMenuName': '场馆预订',
        }
        r = self.session.post('http://card.xjtu.edu.cn/Page/Page',json=card_data,allow_redirects=False)
        print("card",r.status_code)
        url_cardticket =re.findall(r"window.location.href = '(.*?)'",r.text)[0];
        print("url_cardticket",url_cardticket)

        r = self.session.get(url_cardticket,allow_redirects=False);
        # print("card",r.status_code,"\ntext:",r.text)

    def search(self,mode):
        '''
        mode = 0 全局扫描  mode = 1 单日查询（只查看第五天场地）
        无需登录即可搜索
        '''
        #-------------------------202.117.17.144-----------------------------------------------
        r = self.session.get('http://202.117.17.144/index.html') #http://202.117.17.144/index.html
        print("202.117.17.144",r.status_code)
        if r.status_code==200:
            print("欢迎进入体育场馆预定系统")

        #返回值为html有可用信息
        url_BMT1 = 'http://202.117.17.144/product/show.html?id=' +self.platid;
        r = self.session.get(url_BMT1);
        print("id=",self.platid,r.status_code);

        #-----------------------------获取场地信息-------------------------------
        #五天的全部场地信息，用字典存储
        AllPlatTable = {};
        today = datetime.datetime.today()

        start  = 0 if mode == 0 else 5;
        for i in  range(start,6):
            tomorrow = today + datetime.timedelta(days=i)
            date = tomorrow.strftime("%Y-%m-%d")
            t =int(round(time.time()*1000));
            param = {
                's_dates': date,
                'serviceid': self.platid,
                'type': 'day',
                #场地1~场地10的url编码 js用此console.log(decodeURIComponent(decodeURI(str)))
                'coordinatedes': '2_badminton_%25E5%259C%25BA%25E5%259C%25B01%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B02%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B03%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B04%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B05%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B06%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B07%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B08%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B09%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B010',
                'json': 'html',
                '_':t,
            }
            url_getarea ='http://202.117.17.144/product/getarea.html'
            r = self.session.get(url_getarea,params=param)

            param['_'] = int(round(time.time()*1000));
            url_getokinfo= 'http://202.117.17.144/product/findOkArea.html';
            r = self.session.get(url_getokinfo,params=param,timeout=10)
    
            content = r.text;
            pattern = r'"id":([0-9]+).*?"sname":"(场地[\d]+).*?"status":([\d]).*?"time_no":"([0-9:-]+).*?"stockid":([0-9:-]+)';
            plat = re.findall(pattern,content,re.S)
            print(date,'可选场地信息:')
            PlatTable = [];                              #收集某一天的全部空场信息
            for i in plat:
                if(i[2]=='1'):
                    print(i)
                    PlatTable.append(i)
            if not PlatTable:
                print('无空余场地')
            AllPlatTable[date] = PlatTable;   

            '''
            param['_'] = int(round(time.time()*1000));            
            url_getlockinfo ='http://202.117.17.144/product/findLockArea.html';
            r = self.session.get(url_getlockinfo,params=param)
            '''
        self.allplat = AllPlatTable

    def select(self,priority:list) -> list:
        '''
        从已查询列表中按优先级次序选择场地,返回一个场地信息
        priority:按24h制的小时优先级列表,20表示预约20；00——21:59的场地
        实例['20','21','19','09','16']
        '''
        DayPlatTable =self.allplat[self.date]
        if not DayPlatTable:
            return []
        for time in priority:
            for plat in DayPlatTable:
                if(plat[3][0:2] == time):
                    return list(plat)
        
    def book(self,isEmail:bool, selectplat, InfoList:list = [] ) -> str:
        '''
        isEmail 是否发送邮件
        selectplat 选择的场地
        InfoList 为邮箱配置的端口密码等
        '''
        print("正在预定,请稍后…………")
        if not selectplat:
            print("无可约信息")
            return 'null'
        #--------------------------------------------------
        url_booklimit = 'http://202.117.17.144/order/booklimt.html';
        t =int(round(time.time()*1000));
        param = {
            'serviceid': self.platid,
            'num': '1',
            'date': self.date,
            '_':t,
        }
        r = self.session.get(url_booklimit,params=param);

        #encodeurl格式卡了小一天。有两个注意的点：1.设置content-type格式 2.进行urlencode编码
        url_buylist = 'http://202.117.17.144/order/show.html?id='+self.platid;
        try:
            data = {
               'param':{"stock":{selectplat[4]:"1"},"istimes":"1","address":self.platid,"stockdetailids":selectplat[0]}
            }
            self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
            #本人觉得post发送已经经过一次urlencode编码了，此处存疑
            r = self.session.post(url_buylist,data=urlencode(data),allow_redirects=False);        #urllib.parse.urlencode(data)
            print(r.status_code,r.url)
            #self.session.headers.pop('Content-Type')
            if r.status_code ==200:
                print("表单提交成功")
        except:
            print("error")
        
        info_for_nextpost =re.findall(r'_param=eval\((.*?)\);var',r.text)[0]

        for i in range(0,11):
            num = str(random());
            url_yzm ='http://202.117.17.144/login/yzm.html?' + num;
            #http://202.117.17.144/login/yzm.html?0.7662397580325548
            r = self.session.get(url_yzm)
            with open('./image/yzm.jpg','wb') as f:
                f.write(r.content)

            text = ocr('project/main/yzm/image/yzm.jpg',5,3)
            print(text);
            url_book ='http://202.117.17.144/order/book.html';
            data = {
                'param':json.dumps(json.loads(info_for_nextpost)),
                'yzm': text,
                'json': 'true',
                }
            self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
            r = self.session.post(url_book, data=urlencode(data), allow_redirects=False);    
            print("验证码提交:",r.status_code,r.json()['message']) 
            if r.json()['message'] =='验证码有误！' :
                continue
            elif r.json()['message'] =='未支付' :
                if isEmail and not InfoList:
                    email_inf = '您的羽毛球场预约小助手已为您预约成功了\n场地信息:\n'+ \
                        self.date + '一楼  'if(self.platid =='41')else'三楼 ' +selectplat[1] + '  ' + selectplat[3];
                    email(email_inf,InfoList)
                break;

        orderid = re.findall(r'"orderid":"([\d]*?)"',r.text)[0]
        print("orderid",orderid);
        return orderid

    def buy(self,orderid,querypwd):
        '''
        orderid 为预定后返回的订单号  querypwd为一卡通查询密码
        '''
        print("正在购买，请稍后…………")
        url_showpay ='http://202.117.17.144/pay/paymentPlatform/showpay.html'
        param = {
            'orderid': orderid,
            'payid': '6',
            'json': 'html',
            '_': int(round(time.time()*1000))
        }
        r =self.session.get(url_showpay,params=param);
        print("url_payplat",r.status_code)

        # tranamt account sno toaccount thirdsystem thirdorderid ordertype sign orderdesc praram1 thirdurl
        param_for_next = re.findall(r'name="(.*?)".*?value="(.*?)"',r.text)
        data={};
        for p in param_for_next:
            data[p[0]] = p[1]
        url_creatorder ='http://202.117.1.244:9001/Order/CreateOrder';
        r = self.session.post(url_creatorder,urlencode(data))
        print("第三方支付系统已唤起",r.status_code)
        #得到信息中有orderid_2
        orderid_2 = re.findall(r"orderid: '(.*?)'",r.text)[0];
        print("orderid_2",orderid_2)

        url_updateOrder = 'http://202.117.1.244:9001/Order/UpdateOrderLastpayids'
        r = self.session.post(url_creatorder,data={'orderid':orderid_2,'payid':'4'},allow_redirects=False)
        print("提交orderid_2",r.status_code)

        url_PaySynAccType ='http://202.117.1.244:9001/Pay/SynAccType?orderid='+orderid_2+'&payid=4'
        r = self.session.get(url_PaySynAccType)
        print("跳转一卡通支付",r.status_code)
        

        key = re.findall(r'"key-button key-([\d])"',r.text)

        passwd = '';
        for i in querypwd:
            passwd += str(key.index(i))
        data={
            'inputStr':re.findall(r'name="inputStr" value="(.*?)"',r.text)[0],
            'orderid': orderid_2,
            'payid': '4',
            'acctype': '000',
            'paytype': 'SynAccType',
            'rdoacctype': '000',
            'passwd': passwd
        }
        url_CommonPcPay = 'http://202.117.1.244:9001/Pay/CommonPcPay'
        r = self.session.post(url_CommonPcPay,data=urlencode(data), allow_redirects=False)
        print('Pay',r.status_code)
        if r.status_code==302:
            print("支付成功")
            return True
    
def bmt_for_winmenu(un,pwd,platid,mode,date=''):
    ydjd = YiDongJiaoDa(un,pwd,platid,date);
    ydjd.search(mode);
    return ydjd.allplat

def bmt_for_thread(ydjd:YiDongJiaoDa, userInfo,mode):
    '''为线程创建的调用接口。
    mode：0表示检漏模式；1表示定时抢场地模式
    '''
    
    if mode:
        circulation_num = 5
        while (circulation_num):
            ydjd.search(mode)
            selectplat = ydjd.select(userInfo['priority'])
            if selectplat:
                id = ydjd.book(True,selectplat,userInfo['emailConfig']);
                if id != 'null':
                    ydjd.buy(id,userInfo['searchPwd']);
                    return 
            time.sleep(5);
            circulation_num -= 1;
    else:        
        #由于定时任务是相互独立的，在抢到一定数量的场地之后应当及时关停程序，否则会无休止地执行下去
        ydjd.search(mode)
        selectplat = ydjd.select(userInfo['priority'])
        if selectplat:
            id = ydjd.book(True,selectplat,userInfo['emailConfig']);
            if id != 'null':
                ydjd.buy(id,userInfo['searchPwd']);
                return True
        return False

if __name__ == '__main__':
    userInfo = userInfoRead();
    ydjd = YiDongJiaoDa(userInfo['username'],userInfo['pwd'],0);
    ydjd.login();
    ydjd.search(0);
    selectplat = ydjd.select(userInfo['priority'])
    id = ydjd.book(True,selectplat,userInfo['emailConfig']);
    if id != 'null':
        ydjd.buy(id,userInfo['searchPwd']);

    
   
