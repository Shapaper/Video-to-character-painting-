#-*-coding:utf-8-*-
import pygame
import os
#win.fill((255,255,255))
#text = u"H"        #将文本以unicode编码格式存储
#font = pygame.font.Font("F:\\SIMSUN.TTC", 60)  #设置字体
#ftext = font.render(text, True, (0,0,0))   #渲染字体
#win.blit(ftext,(0,0))
#pygame.display.update()
#pygame.image.save(win, os.path.join("1.png"))
##################
import cv2
import time
import subprocess
import imageio
import os
import re
from PIL import Image
from alive_progress import alive_bar
show_heigth = 64              
show_width = 240
print("请将视频放入《.video》文件夹内的自定义文件夹，视频名称改为main.mp4（必须是MP4）")
shipingpathh=input("视频名   如【文件 ./.video/1_sa_ri_lang/main.mp4 】为【1_sa_ri_lang】[目前支持中文了！]——那么你的视频是：")
shipingpath="./.video/"+str(shipingpathh)+"/main.mp4"
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
#生成一个ascii字符列表
char_len = len(ascii_char)
 
vc = cv2.VideoCapture(shipingpath)          #加载一个视频
from moviepy.editor import *

print("总计"+str(vc.get(7))+"帧，预计使用"+str(0.3*vc.get(7)*(1+3+3))+"MB硬盘空间用作  缓存  ！")
woyebuzhidao=input("请保证有足够的【硬盘】空间用作【缓存】！按回车键继续")

print("进行步骤1/6   提取视频声音")
video = VideoFileClip(shipingpath)
audio = video.audio
audio.write_audiofile('./huancun/ptest.mp3')

frames_nFPS=vc.get(5)#获取视频帧速率
if vc.isOpened():                       #判断是否正常打开
    rval , frame = vc.read()
else:
    rval = False
    
frame_count = 0
outputList = []                         #初始化输出列表
allzhengshu=int(vc.get(7))
print("进行步骤2/6   视频转为字符")
with alive_bar(int(allzhengshu)) as bar:
    while rval:   #循环读取视频帧  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #使用opencv转化成灰度图
        gray = cv2.resize(gray,(show_width,show_heigth))#resize灰度图
        text = ""
        for pixel_line in gray:
            for pixel in pixel_line:                    #字符串拼接
                text += ascii_char[int(pixel / 256 * char_len )]
            text += "\n"                                
        outputList.append(text)
        frame_count = frame_count + 1
        rval, frame = vc.read()
        bar()
###
print("进行步骤3/6   字符转为图片")
with alive_bar(int(allzhengshu)) as bar:   
    zhengshu=0
    
    pygame.init()     #需要初始化
    win = pygame.display.set_mode((1920,1080))
    font = pygame.font.SysFont("simsunnsimsun", 16) # 使用系统字体
    for frame in outputList:
        #os.system("cls")                    #清屏
        all_frame=frame.split('\n')
        win.fill((255,255,255))#清屏
        
        for i, v in enumerate(all_frame):
            #print(i, v)
            ftext = font.render(v, True, (0,0,0))   #渲染字体
            win.blit(ftext,(0,i*20))
            pygame.display.update()
        ####
        pygame.image.save(win, os.path.join("./huancun/picture/"+str(zhengshu)+".png"))
        
        zhengshu=zhengshu+1
        bar()
        #print(frame)
        #print()
        #print()
import numpy as np
import cv2
#读取一张图片
size = (1920,1080)
#print(size," ",frames_nFPS)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#完成写入对象的创建，第一个参数是合成之后的视频的名称，第二个参数是可以使用的编码器，第三个参数是帧率即每秒钟展示多少张图片，第四个参数是图片大小信息
videowrite = cv2.VideoWriter(r'./huancun/pvideo/ptest.avi',fourcc,frames_nFPS,size)#20是帧数，size是图片尺寸
cishua=0
print("进行步骤4/6   图片转为视频")
with alive_bar(int(allzhengshu)) as bar: 
    for filename in [r'./huancun/picture/{0}.png'.format(i) for i in range(allzhengshu)]:
        img = cv2.imread(filename)
        videowrite.write(img)
        cishua=cishua+1
        if img is None:
            print(filename + " is error!")
            continue
        bar()
    videowrite.release()
#print('end!')

print("进行步骤5/6   音轨视频混合")
cmd = f"ffmpeg -y -i ./huancun/pvideo/ptest.avi -i ./huancun/ptest.mp3 -acodec copy -vcodec copy ./huancun/pvideo/ptest.mp4"
process=subprocess.Popen(cmd,stderr=subprocess.PIPE,bufsize=0,encoding="utf-8",universal_newlines=True,shell=True)

duration = None
cishua=0
with alive_bar(int(allzhengshu)) as bar:
    while process.poll() is None:
        line = process.stderr.readline().strip()
        if line:
            duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)

            frame = re.search(r'frame=         (?P<frame>\S+)', line)
            if frame is None:
                frame = re.search(r'frame=        (?P<frame>\S+)', line)
                if frame is None:
                    frame = re.search(r'frame=       (?P<frame>\S+)', line)
                    if frame is None:
                        frame = re.search(r'frame=      (?P<frame>\S+)', line)
                        if frame is None:
                            frame = re.search(r'frame=     (?P<frame>\S+)', line)
                            if frame is None:
                                frame = re.search(r'frame=    (?P<frame>\S+)', line)
                                if frame is None:
                                    frame = re.search(r'frame=   (?P<frame>\S+)', line)
                                    if frame is None:
                                        frame = re.search(r'frame=  (?P<frame>\S+)', line)
                                        if frame is None:
                                            frame = re.search(r'frame= (?P<frame>\S+)', line)
                                            if frame is None:
                                                frame = re.search(r'frame=(?P<frame>\S+)', line)
            if (frame is not None) and (frame!=''):
                wcframe=str(frame.group())
                for wcc in range(cishua,int(wcframe[wcframe.find('frame=')+6:len(wcframe)])):
                    bar()
                cishua=int(wcframe[wcframe.find('frame=')+6:len(wcframe)])
                #print(wcframe[wcframe.find('frame=')+6:wcframe.find("'>")])
                #print(frame[frame.find('frame=')+5:frame.find("'>")])
    for wcc in range(cishua,int(allzhengshu)):
        bar()
print("进行步骤6/6   压缩比特率")
cmd = f"ffmpeg -y -i ./huancun/pvideo/ptest.mp4 -b:v 20000k -bufsize 20000k ./.video/"+str(shipingpathh)+"/output.mp4"
process=subprocess.Popen(cmd,stderr=subprocess.PIPE,bufsize=0,encoding="utf-8",universal_newlines=True,shell=True)

duration = None
cishua=0
with alive_bar(int(allzhengshu)) as bar:
    while process.poll() is None:
        line = process.stderr.readline().strip()
        if line:
            duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)

            frame = re.search(r'frame=         (?P<frame>\S+)', line)
            if frame is None:
                frame = re.search(r'frame=        (?P<frame>\S+)', line)
                if frame is None:
                    frame = re.search(r'frame=       (?P<frame>\S+)', line)
                    if frame is None:
                        frame = re.search(r'frame=      (?P<frame>\S+)', line)
                        if frame is None:
                            frame = re.search(r'frame=     (?P<frame>\S+)', line)
                            if frame is None:
                                frame = re.search(r'frame=    (?P<frame>\S+)', line)
                                if frame is None:
                                    frame = re.search(r'frame=   (?P<frame>\S+)', line)
                                    if frame is None:
                                        frame = re.search(r'frame=  (?P<frame>\S+)', line)
                                        if frame is None:
                                            frame = re.search(r'frame= (?P<frame>\S+)', line)
                                            if frame is None:
                                                frame = re.search(r'frame=(?P<frame>\S+)', line)
            if frame is not None:
                wcframe=str(frame.group())
                for wcc in range(cishua,int(wcframe[wcframe.find('frame=')+6:len(wcframe)])):
                    bar()
                cishua=int(wcframe[wcframe.find('frame=')+6:len(wcframe)])
                #print(wcframe[wcframe.find('frame=')+6:wcframe.find("'>")])
                #print(frame[frame.find('frame=')+5:frame.find("'>")])
    for wcc in range(cishua,int(allzhengshu)):
        bar()

print("删除临时图片籍中(时间较长，请稍后)")
cmd = f"rmdir /s/q .\huancun\picture"
print(cmd)
subprocess.call(cmd,shell=True)
cmd = f"md .\huancun\picture"
print(cmd)
subprocess.call(cmd,shell=True)

print("删除临时视频1/2中")
cmd = f"del /q .\huancun\pvideo\ptest.avi"
print(cmd)
subprocess.call(cmd,shell=True)

print("删除临时视频2/2中")
cmd = f"del /q .\huancun\pvideo\ptest.mp4"
print(cmd)
subprocess.call(cmd,shell=True)

print("删除临时音频中")
cmd = f"del /q .\huancun\ptest.mp3"
print(cmd)
subprocess.call(cmd,shell=True)
