## 环境
项目依赖库已打包好，执行`pip install -r requirements.txt`可快速添加依赖项
ocr识别中，除了需要安装python库pytesseract外，还需要另外下载tesseract程序并添加环境变量[win下载地址](https://digi.bib.uni-mannheim.de/tesseract/)，并在[line2](./project/main/yzm/ocr.py) 修改tesseract.exe所在的文件路径

在[用户参数配置](./docs/user_config.json)填写帐密、查询密码、预约偏好等信息，此部分涉及敏感信息
```json
//文件不能有中文注释,此处注释只为帮助规范数据格式
{
  "username":"****",
  "pwd":"******",
  "searchPwd":"******", //六位校园卡查询密码
  "priority":["19","18","20","10","11","15","16","09"], //按24h制表示的小时优先级列表,20表示预约20；00——21:59的场地
  "emailConfig":[
    {
      "from":"******@qq.com",
      "to":"*****@qq.com",
      "smtpServer":"smtp.qq.com",
      "port":"****",
      "AuthorizationCode":"******" //stmp服务授权码
    }
  ]
}
```
## 文件地图
```bash
BadmintonXJTU
│  .gitignore
│  README.md
│  tree.txt
|  requirements.txt
│  winmenu.exe #封装后的查询可视化界面
│  winmenu.py
├─bin
├─docs
│      DevLog.md           #开发日志
│      user_config.json
│      
└─project
    ├─main
    │  │  PlayBadminton.py
    │  │  thread.py
    │  │  ua.py
    │  │  
    │  └─yzm
    │      │  accuary.txt      #不同方法输出的准确性
    │      │  get_yzm_database.py
    │      │  ocr.py
    │      │  testAns.txt
    │      │  
    │      ├─image
    │      │      yzm.jpg
    │      │      yzmres.png
    │      │      
    │      ├─imagedata          #验证码样本库
    │      └─imageProcessed    
    ├─resource
    |       IPpond.txt         
    └─test
            aes.js
            JsToPy.py
            test.py
```    
---
@Copyright Ton

