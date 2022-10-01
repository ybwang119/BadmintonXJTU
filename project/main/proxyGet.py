import datetime
from random import random
import re
from time import sleep
import requests
from SpiderAgency import ua_change

def check_proxy(ip, port) -> bool:
    try:
        # 设置重连次数
        requests.adapters.DEFAULT_RETRIES = 3
        proxy = f"http://{ip}:{port}"
        res = requests.get(url="http://icanhazip.com/",timeout=15,proxies={"http": proxy})
        proxyIP = res.text.replace('\n','')
        if (proxyIP == ip):
            print("代理IP:'" + proxyIP + "'有效！")
            return True
        else:
            print("代理IP无效！")
            return False
    except:
        print("The request failed")
        return False

def get_IP_pond():
    base_url = 'https://www.kuaidaili.com/free/inha/'
    IP_pond = {};
    for i in range(0,5):
        url = base_url + str(i) +'/'
        print(url)
        headers= {'User-Agent': ua_change(),'Accept-Language':'zh-CN,zh;q=0.9'};
        r = requests.get(url,headers=headers)
        pattern = r'<td data-title="IP">([0-9\.]+)</td>.*?<td data-title="PORT">([0-9]+)</td>'
        get_res = re.findall(pattern,r.text,re.S)
        for i in get_res:
            IP_pond[i[0]] = i[1]
        sleep(2 + 3*random())

    base_url2 = 'http://www.kxdaili.com/dailiip/2/'
    for i in range(1,6):
        url = base_url + str(i) +'.html'
        print(url)
        headers= {'User-Agent': ua_change(),'Accept-Language':'zh-CN,zh;q=0.9'};
        r = requests.get(url,headers=headers)
        pattern = r'<td>([0-9\.]+)</td>.*?<td>([0-9]+)</td>'
        get_res = re.findall(pattern,r.text,re.S)
        for i in get_res:
            IP_pond[i[0]] = i[1]
        sleep(2 + 3*random())
    print(IP_pond)
    # IP_pond={'120.194.55.139': '6969', '60.170.204.30': '8060', '188.131.233.175': '8118', '222.74.73.202': '42055', '47.106.105.236': '80', '120.220.220.95': '8085', '61.216.185.88': '60808', '183.64.239.19': '8060', '183.247.202.208': '30001', '61.216.156.222': '60808', '27.42.168.46': '55481', '47.56.69.11': '8000', '223.82.60.202': '8060', '223.96.90.216': '8085', '202.109.157.65': '9000', '47.105.91.226': '8118', '210.5.10.87': '53281', '122.9.101.6': '8888', '202.116.32.236': '80', '47.113.90.161': '83', '115.29.170.58': '8118', '183.236.123.242': '8060', '117.114.149.66': '55443', '39.108.101.55': '1080', '182.139.110.128': '9000', '112.14.47.6': '52024', '121.13.252.60': '41564', '121.13.252.61': '41564', '117.41.38.19': '9000', '183.247.199.215': '30001', '117.41.38.16': '9000', '117.93.180.62': '9000', '113.252.44.133': '8080', '117.41.38.18': '9000', '202.109.157.63': '9000', '222.66.202.6': '80', '117.94.126.227': '9000', '101.200.127.149': '3129', '150.109.32.166': '80', '202.109.157.61': '9000', '61.150.96.27': '36880', '113.254.249.138': '8193', '183.236.232.160': '8080', '58.215.201.98': '56566'}
    #check if usable
    IP_pond_filtered = {};
    for IP in IP_pond:
        if check_proxy(IP,IP_pond[IP]):
            IP_pond_filtered[IP] = IP_pond[IP]
    print(IP_pond_filtered)
    return IP_pond_filtered

def init_ip_pond():
    proxy_dict = get_IP_pond();
    proxy_list = []
    for ip in proxy_dict:
        proxy_list.append(ip + ':' + proxy_dict[ip]) 
    return proxy_list

def proxy_change(proxy_list):
    return random.choice(proxy_list)
    
if __name__ == '__main__':
    with open('project/resource/IPpond.txt','a+',encoding='utf-8') as f:
        f.write(datetime.datetime.now().__str__())
        IP_pond = get_IP_pond()
        for IP in IP_pond:
            f.write('\n' + IP + ':' + IP_pond[IP] );