

from time import sleep
from PlayBadminton import *
if __name__ == '__main__':
    # def test():
    #     print('rtest')
    userInfo = userInfoRead()
    mode = 1
    platid = 0
    start_time = "08:40:00" #08:40:00
    if mode:
        sub_thread = []
        for i in range(0,3):
            print("正在注册线程",i+1,'--------------')
            ydjd = YiDongJiaoDa(userInfo['username'],userInfo['pwd'],platid);
            ydjd.login()
            sub_thread.append( threading.Thread(target = bmt_for_thread,args=(ydjd,userInfo,mode)) )
            # sub_thread.append( threading.Thread(target = test) )
        schedule_break_flag = False
        def schedule_thread():
            global schedule_break_flag 
            schedule_break_flag= True
            for i in range(0,3):
                sub_thread[i].start()
        schedule.every().day.at(start_time).do(schedule_thread)
        while not schedule_break_flag:
            schedule.run_pending()
            sleep(1)
    else:
        ydjd_floor1 = YiDongJiaoDa(userInfo['username'],userInfo['pwd'],1,'2022-10-05')
        ydjd_floor1.login()
        ydjd_floor3 = YiDongJiaoDa(userInfo['username'],userInfo['pwd'],0,'2022-10-05')
        ydjd_floor3.session = ydjd_floor1.session
        schedule.every(120).seconds.do(bmt_for_thread,ydjd=ydjd_floor1,userInfo=userInfo,mode=mode)
        schedule.every(120).seconds.do(bmt_for_thread,ydjd=ydjd_floor3,userInfo=userInfo,mode=mode)
        while 1:
            schedule.run_pending()
            sleep(1)
        