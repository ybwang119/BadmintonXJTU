## 环境
1.为运行js脚本需要安装node环境，以及**crypto-js**库，在(JsToPy.py) line11更改路径
2.ocr识别中，需要安装库pytesseract，并在(.\yzm\ocr.py)line2 修改tesseract.exe所在的文件路径

## 文件地图
```bash
BadmintonXJTU
│  .gitignore
│  README.md
│  tree.txt
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
    └─test
            aes.js
            JsToPy.py
            test.py
```    
---
@Copyright lxt

