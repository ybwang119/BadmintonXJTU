from random import random
from time import sleep
import requests

def buildDatabase():
    url_yzm ='http://202.117.17.144/login/yzm.html?'+str(random())
    #http://202.117.17.144/login/yzm.html?0.7662397580325548
    for i in range(0,100):
        r = requests.get(url_yzm)
    print("获取验证码：",r.status_code)

    #频繁请求会被封IP！切记！！
    sleep(5000)
    with open('./imagedata/yzm'+str(i)+'.jpg','wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    buildDatabase();

