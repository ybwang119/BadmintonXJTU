##环境
1.为运行js脚本需要安装node环境，以及**crypto-js**库，在(JsToPy.py) line11更改路径
2.ocr识别中，需要安装库pytesseract，并在(.\yzm\ocr.py)line2 修改tesseract.exe所在的文件路径

##文件地图
> \_\_pycache\_\_       $~~~~$*缓存文件*

> aes.js                $~~~~~~~~~~~~~~$*AES加密*
JsToPy.py    $~~~~~~~$*将js文件转换为python执行*

>yzm
--accuary.txt $~~~~~~~$*不同方法输出的准确性*
--imagedata $~~~~~~~$*验证码样本库*
--imagedatares $~~~$*验证码滤波结果*
--**ocr.py** $~~~~~~~~~~~~~$*ocr识别算法*
--TESTANS.txt $~~~$*验证码样本库的标定数据*
get_yzm_database.py  $~~~$*获取验证码样本集*
image $~~~~~$*验证码存放路径*
image2 $~~~$*验证码识别结果存放路径*

>**PlayBadminton.py**$~~~$*羽毛球场馆预定的主函数*

>winmenu.exe $~~~$*封装后的查询可视化界面*
winmenu.py

>README.md
---
@Copyright lxt

