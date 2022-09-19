

from time import sleep
from PlayBadminton import *
if __name__ == '__main__':
    userInfo = userInfoRead()
    mode = 1
    start_time = "18:53" #08:40:00
    sub_thread = []

    for i in range(0,3):
        print("正在注册线程",i+1)
        ydjd = YiDongJiaoDa(userInfo['username'],userInfo['pwd'],1);
        ydjd.login()
        # sub_thread = threading.Thread(target = badminton,args=(userInfo['username'],userInfo['pwd'],0,0))
        sub_thread.append( threading.Thread(target = bmt_for_thread,args=(ydjd,userInfo,mode)) )
    
    def schedule_thread():
        for i in range(0,3):
            sub_thread[i].start()
    schedule.every().day.at(start_time).do(schedule_thread)
    while 1:
        schedule.run_pending()
        sleep(1)