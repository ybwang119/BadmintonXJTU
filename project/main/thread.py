

from time import sleep
from PlayBadminton import *
if __name__ == '__main__':
    userInfo = userInfoRead()
    mode = 1
    platid = 1
    if mode:
        start_time = "13:14:50" #08:40:00
        sub_thread = []
        for i in range(0,3):
            print("正在注册线程",i+1,'--------------')
            ydjd = YiDongJiaoDa(userInfo['username'],userInfo['pwd'],platid);
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
    else:
        ydjd = YiDongJiaoDa(userInfo['username'],userInfo['pwd'],platid)
        ydjd.login()
        schedule.every(10).minutes.do(bmt_for_thread,args=(ydjd,userInfo,mode))
        while 1:
            schedule.run_pending()
            sleep(1)
        