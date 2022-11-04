import os
import pytesseract
from PIL import Image
import numpy as np 
import cv2
# from cv2 import erode,imread,imwrite
# tesseract.exe所在的文件路径
# pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'


# 求图像img中(x,y)处像素的中值c
def average(img, x, y,wid):
    sum = 0;
    for i in range(x-int((wid-1)/2),x+int((wid+1)/2)):
        for j in range(y-int((wid-1)/2),y+int((wid+1)/2)):
            gray = img.getpixel((i, j))  # 取出灰度值
            sum += gray;
    return int(sum/wid/wid)

def median(img, x, y, wid):

    L = []
    for i in range(x-int((wid-1)/2),x+int((wid+1)/2)):
        for j in range(y-int((wid-1)/2),y+int((wid+1)/2)):
            gray = img.getpixel((i, j))  # 取出灰度值
            L.append(gray)
    L.sort()
    c = L[4]
    return c

def erode_dilate(im, threshold=2):

    kernel = np.ones((threshold, threshold), np.uint8)
    erosion = cv2.erode(im, kernel, iterations=1)
    return erosion

def get_threshold(img):
    sum=0;
    rows, cols = img.size
    for i in range(0,rows):
        for j in range(0,cols):
            gray = img.getpixel((i,j));
            sum += gray;
    # print(sum/rows/cols)
    return 0.8*sum/rows/cols #此处为保留更多字符信息，取较小阈值

def cut_noise(img,x,y,wid,cut_flag):
    near_point = 0;
    for i in range(x-int((wid-1)/2),x+int((wid+1)/2)):
        for j in range(y-int((wid-1)/2),y+int((wid+1)/2)):
            gray = img.getpixel((i, j))  
            if gray == 0:      #0为黑
                near_point += 1;
    if near_point >= cut_flag:                    
        return 0
    else:
        return 255  

def ocr(path1,cut_flag,wid,path2=''):
    img1 = Image.open(path1)  # 原始    
    img1 = img1.convert("L");
    # img1.save('./image/灰度.jpg')

    w, h = img1.size
    img1 = img1.crop((1,1,w-2,h-2))
    # img1.save('./image/裁剪.jpg')
    threshold = get_threshold(img1); 
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(255)
    # 图片二值化
    imgt = img1.point(table, '1')
    # imgt.save('./image/去底.png');

    # cvimgt = cv2.cvtColor(np.array(imgt), cv2.COLOR_RGB2BGR)
    # cvimgt_erode = erode_dilate(cvimgt)
    # imgt = Image.fromarray(cv2.cvtColor(cvimgt_erode, int(cv2.COLOR_BGR2RGB)))
    # imgt.save('./image/膨胀.png');
    w, h = img1.size
    # cut_flag = 2;                           
    # for cut_flag in range(2,7):
    #     for wid in [3,5,7]:
    temp = int((wid-1)/2)
    img2 = Image.new('L', (w, h), 'white') 
    for x in range(0+temp, w-temp):
        for y in range(0+temp, h-temp):
            img2.putpixel((x,y),cut_noise(imgt,x,y,wid,cut_flag))                  
            # img2.save(r'./image2/cut' +str(cut_flag) +'_'+ str(wid) + '.jpg')
            # img2.save('./image/切除噪点.jpg')
            if path2 != '':
                img2.save(path2)
    w2, h2 = img2.size

    # #将图片分为四部分分别处理，但效果一般，准确率只有25%
    # crop_start = 0;
    # crop_dieta = int(w2/4);
    # ocr_text = ''
    # for i in range(0,4):
    #     sub_image = img2.crop((crop_start,0,crop_start + crop_dieta,h2));
    #     crop_start = crop_start + crop_dieta +1;
    #     ocr_text += pytesseract.image_to_string(sub_image,lang="eng",config='--psm 10')
    # # print(ocr_text)
    # text = ocr_text
    text = pytesseract.image_to_string(img2,lang="eng",config='--psm 7')
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text = "".join(filter(str.isalnum, text))
    text = text.upper();
    img1.close();
    imgt.close();
    img2.close();
    print(text)
    return text.replace('\n','');

if __name__ == '__main__':
    with open(r'/home/wuiten/BadmintonXJTU/project/main/yzm/TESTANS.txt','r',encoding='utf-8') as f:
        ans = f.read().splitlines();
        success_num = 0
        for i in range(0,80):
            text = ocr('/home/wuiten/BadmintonXJTU/project/main/yzm/imagedata/yzm'+str(i)+'.jpg',5,3)
            if text == ans[i]:
                success_num += 1
        print(success_num)
# with open(r'./yzm./testAns.txt','r',encoding='utf-8') as f:
#     ans = f.read().splitlines();
##确定参数，分析准确率  
# with open('./yzm./accuary.txt','a+',encoding='utf-8') as f:
#     for cut_flag in range(2,7):
#         for wid in [3,5,7]:
#             success_num = 0;
#             for i in range(0,80):
#                 # try:
#                 path1 = './imagedata/yzm'+str(i)+'.jpg'  
#                 path2 = './imagedatares/yzm'+str(i)+'.jpg'  
#                 text = ocr(path1, path2,cut_flag,wid).replace('\n','')
#                 if text == ans[i]:
#                     success_num += 1
#                 print(text)
#                 # except:
#                 #     print('none')
#             print(success_num/80)

#             f.write("cut_falg="+str(cut_flag)+'wid='+str(wid)+':')
#             f.write(format(success_num/80,".3f")+'\n')


