from datetime import datetime
import tkinter

from numpy import empty
import PlayBadminton
def fun():
    print(un.get(),pwd.get(),platid.get(),mode.get(),date.get())
    info = PlayBadminton.badminton(un.get(),pwd.get(),platid.get(),mode.get(),date.get())
    info_str = ''
    flag=0;
    for i in info:
        if not info[i]:
            continue;
        else:
            flag=1;
            info_str += str(i) +'\n'
            for detail in info[i]:
                info_str += str(detail) +'\n'
    if flag==0:
        info_str = "场馆已约满"
    print(info,type(info))
    text.delete(1.0,tkinter.END)
    text.insert(tkinter.INSERT,info_str)
    


win = tkinter.Tk()
win.title("XJTU羽毛球场地预约")
sw = win.winfo_screenwidth()
sh = win.winfo_screenheight()
ww = 400
wh = 400
x = (sw-ww) / 2
y = (sh-wh) / 2
win.geometry("%dx%d+%d+%d" %(ww,wh,x,y))


label_un = tkinter.Label(win,text="账号")
label_un.grid(row=0,)
label_pwd = tkinter.Label(win,text="密码")
label_pwd.grid(row=1,padx=10,pady=0)
label_date = tkinter.Label(win,text="预定日期")
label_date.grid(row=2,padx=10,pady=0)
un = tkinter.Entry(win,textvariable=tkinter.StringVar(value='2191411814'),)
un.grid(row=0,column=1)
pwd = tkinter.Entry(win,textvariable=tkinter.StringVar(value=''),show='*')
pwd.grid(row=1,column=1)
date = tkinter.Entry(win,textvariable=tkinter.StringVar(value=datetime.today().strftime("%Y-%m-%d")),)
date.grid(row=2,column=1)

mode = tkinter.IntVar()
mode1 = tkinter.Radiobutton(win,text="全局扫描",value=0,variable=mode)
mode1.grid(row=3,column=0,sticky='w')
mode2 = tkinter.Radiobutton(win,text="今天起第五天单日扫描",value=1,variable=mode)
mode2.grid(row=3,column=1,sticky='w',pady=[10,0])

platid = tkinter.IntVar()
mode1 = tkinter.Radiobutton(win,text="一楼羽毛球场",value=0,variable=platid)
mode1.grid(row=4,column=0,sticky='w')
mode2 = tkinter.Radiobutton(win,text="三楼羽毛球场",value=1,variable=platid)
mode2.grid(row=4,column=1,sticky='w')

button  = tkinter.Button(win,text='START',command=fun)
button.grid(row=5,columnspan=2,pady=10)

text = tkinter.Text(win,width=55,height=10)
text.grid(row=6,columnspan=2)

scroll = tkinter.Scrollbar()
scroll.grid(row=6,columnspan=2,sticky='e'+'n'+'s')
scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)

win.mainloop()#将窗体显示出来

