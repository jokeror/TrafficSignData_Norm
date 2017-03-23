# -*- coding: cp936 -*-
import cv2
import numpy as np
from os import listdir
from sys import exit

"""
功能：读取path路径下的jpg文件，找出该图片信息中所有的轮廓，
      手动选择并保存合适的交通标志照片块
使用：(1)修改 "三个" path
      (2)运行程序
      (3)点击合适的交通标志照片块的内部区域
      (4)若选择合适，则按下 's' 键保存
      (5)按下‘q' 键可以跳过当前照片块或照片
      (5)按下‘b' 键可以直接跳过当前照片及一些G后续可能出现的照片块
注意：(1)关于读写 txt 文件：如果 txt 文件已经存在，程序运行结束但未（完全）关闭时，
         可能会出现空白文档的现象，将程序完全关闭（杀掉进程？？），
         再次打开该 txt 文档时便会正常显示。
         故推荐->不手动新建 txt 文件，让程序自动新建。
    
"""

order_num = 0 
read_path =  'H:\\TrafficSignData\' 
save_path =  'E:\\TL\\' 
txt_path  =  'E:\\TL\\labels.txt'


# ----------- Mouse response function ------------------
# ------------------ 鼠标响应函数 -----------------------
def choose_contours(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # ix, iy 为鼠标按下时的位置 
        ix, iy = -1,-1
        ix ,iy = x, y
        for i in contours:
            cnt = i
            x,y,w,h = cv2.boundingRect(cnt)
            # 判断鼠标按下的位置是否在某个照片块之内
            if (x < ix <x+w) and (y<iy<y+h):

                # 显示照片块
                key = param[1][y:y+h,x:x+w]
                cv2.imshow('piece',key)

                # 按键响应
                k= cv2.waitKey(0)&0xFF
                if k == ord('Q'):
                    cv2.destroyWindow('piece')
                elif k == ord('W'):
                    # 保存照片块
                    # 变 ‘+’ 的数量
                    param[0] += 1

                    save_pic =  save_path + str(order_num) + param[0]*'+'+ '.jpg'
                    cv2.imwrite(save_pic,key)
                    cv2.destroyAllWindows()
                    
                    # --- txt 文件写入------
                    
                    add_txt = str(order_num)+".jpg "
                    txt.write(add_txt)
                    add_txt = str(x) + " "+str(y)+" "+str(w)+" "+str(h)
                    txt.write(add_txt)
                    txt.write("\n")
                    # ---- 写入结束 --------

                    cv2.rectangle(show,(x,y),(x+w,y+h),(255,255,255),2)
                    cv2.imshow(str(order_num) + '.jpg',show)
                    key = []
                    
                    cv2.setMouseCallback(str(order_num) + '.jpg', choose_contours,[plus,save])
                    
#                elif k == ord('E'):
#                    break
                elif k == ord('E'):
                    exit()
                    
                        
# --------------- main project  ------------------
# ------------------- 主程序 -----------------
# 获取该路径下需要处理的照片数
file_list = listdir(read_path)
Len = len(file_list)

# 打开保存信息的 txt 文件， 如果不存在该文件，则自动创建一新的 txt 文件
start_picture = int(raw_input('start pic is ?\n'))
if start_picture == 1:
    txt = open(txt_path,'w')
else :
    txt = open(txt_path,'a')


for order_num in xrange(start_picture,Len+1):
    plus= 0

    read_pic =  read_path + str(order_num) + '.jpg' 
    
    img =cv2.imread(read_pic)
    img = cv2.resize(img,(960,640),cv2.INTER_LINEAR )
    save = img.copy()
    show = img.copy()
    # 分分分分分分分分分分分分分分分分分分分
    newImg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,thresh = cv2.threshold(newImg,127,255,0)
    _, contours, hierarchy = cv2.findContours(thresh, 1,2)
    for i in contours:
        cnt = i
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(show,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.destroyAllWindows()
    cv2.imshow(str(order_num) + '.jpg',show)
    k = cv2.waitKey(0)&0xFF
    while k != ord('Y'):
        if k == ord('A'):
            show = img.copy()
            newImg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            ret,thresh = cv2.threshold(newImg,127,255,0)
            _, contours, hierarchy = cv2.findContours(thresh, 1,2)
            for i in contours:
                cnt = i
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(show,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.destroyAllWindows()
            cv2.imshow("show",show)
            k = cv2.waitKey(0)&0xFF
        elif k == ord('S'):
            show = img.copy()
            thresh = cv2.Canny(img,100,200)
            _, contours, hierarchy = cv2.findContours(thresh, 1,2)
            for i in contours:
                cnt = i
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(show,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.destroyAllWindows()
            cv2.imshow(str(order_num) + '.jpg',show)
            k = cv2.waitKey(0)&0xFF
        elif k == ord('D'):
            show = img.copy()
            hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
            h,s,v = cv2.split(hsv)
            ret,thresh = cv2.threshold(s,120,255,0)
            _, contours, hierarchy = cv2.findContours(thresh, 1,2)
            for i in contours:
                cnt = i
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(show,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.destroyAllWindows()
            cv2.imshow(str(order_num) + '.jpg',show)
            k = cv2.waitKey(0)&0xFF
        elif k == ord('F'):
            show = img.copy()
            b,g,r = cv2.split(img)
            ret,thresh = cv2.threshold(r,120,255,0)
            _, contours, hierarchy = cv2.findContours(thresh, 1,2)
            for i in contours:
                cnt = i
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(show,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.destroyAllWindows()
            cv2.imshow(str(order_num) + '.jpg',show)
            k = cv2.waitKey(0)&0xFF
        elif k == ord('G'):
            show = img.copy()
            b,g,r = cv2.split(img)
            ret,thresh = cv2.threshold(g,120,255,0)
            _, contours, hierarchy = cv2.findContours(thresh, 1,2)
            for i in contours:
                cnt = i
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(show,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.destroyAllWindows()
            cv2.imshow(str(order_num) + '.jpg',show)
            k = cv2.waitKey(0)&0xFF
        elif k == ord('H'):
            show = img.copy()
            b,g,r = cv2.split(img)
            ret,thresh = cv2.threshold(b,120,255,0)
            _, contours, hierarchy = cv2.findContours(thresh, 1,2)
            for i in contours:
                cnt = i
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(show,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.destroyAllWindows()
            cv2.imshow(str(order_num) + '.jpg',show)
            k = cv2.waitKey(0)&0xFF
        elif k == ord('E'):
            exit()
        else:
            break;
    """
    method=raw_input('what method ?\n')
    if method == 'g':
        newImg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        ret,thresh = cv2.threshold(newImg,127,255,0)
    elif method == 'c':
        thresh = cv2.Canny(img,100,200)
    elif method == 'h':
        hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
        h,s,v = cv2.split(hsv)
        ret,thresh = cv2.threshold(s,120,255,0)
    elif method == 'r':
        b,g,r = cv2.split(img)
        ret,thresh = cv2.threshold(r,120,255,0)
    elif method == 'g':
        b,g,r = cv2.split(img)
        ret,thresh = cv2.threshold(g,120,255,0)
    elif method == 'b':
        b,g,r = cv2.split(img)
        ret,thresh = cv2.threshold(b,120,255,0)
        
    _, contours, hierarchy = cv2.findContours(thresh, 1,2)

    for i in contours:
        cnt = i
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    """
    # 后续处理 ：
    #cv2.destroyAllWindows()
    #cv2.imshow('TrafficSign',show)
    # print 'suitable ?'

    # ??????
    
    # 调用鼠标相应函数S
    print 'Now You Can Use Your Mouse!'
    cv2.setMouseCallback(str(order_num) + '.jpg', choose_contours,[plus,save])

    cv2.waitKey()
    cv2.destroyAllWindows()


# 关闭 txt 文档
txt.close()
cv2.waitKey()
cv2.destroyAllWindows()
print 'OVER'

