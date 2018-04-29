#!/usr/local/bin/python
# -*- coding: utf-8 -*-
##
#  @filename   :   main.cpp
#  @brief      :   7.5inch e-paper display demo
#  @author     :   Yehui from Waveshare
#
#  Copyright (C) Waveshare     July 28 2017
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##

import epd7in5
import Image
import ImageDraw
import ImageFont
import numpy as np
import calendar
import time
import requests
import sys
import urllib
import json
import urllib2
# import operator
import os
import random
# import threading
from datetime import datetime

# fonts
font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
font_cal = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
font_day = ImageFont.truetype('fonts/Roboto-Black.ttf', 110)
font_day_str = ImageFont.truetype('fonts/Roboto-Light.ttf', 35)
font_month_str = ImageFont.truetype('fonts/Roboto-Light.ttf', 25)

font_weather_icons = ImageFont.truetype('fonts/weathericons-regular-webfont.ttf', 35)
font_weather_degree = ImageFont.truetype('fonts/Roboto-Light.ttf', 25)
font_tasks_list_title = ImageFont.truetype('fonts/Roboto-Light.ttf',30)
font_tasks_list = ImageFont.truetype('fonts/tahoma.ttf',12)
font_tasks_due_date = ImageFont.truetype('fonts/tahoma.ttf',9)

font_icons  = ImageFont.truetype('fonts/Byom-Icons-Trial.ttf',15) 

reload(sys)
sys.setdefaultencoding('utf-8')

# epd
epd = epd7in5.EPD()
EPD_WIDTH = 640
EPD_HEIGHT = 384

# image
image = None
draw = None

def main():

    init()
    displayCalendar()

    # execution interval
    wait = 60
    refresh_time = 1000
    start_time = time.time() + refresh_time

    while True:
        print('restart  : current time ' + str(time.time()/60) + ' started time ' + str(start_time/60))
        if (time.time() - start_time) > 0:
            start_time = time.time() + refresh_time # rest refresh time
            displayCalendar()
        time.sleep(wait)
           
def init():
    global epd, image, draw, EPD_HEIGHT, EPD_WIDTH
    epd.init()
    # Initialise the image and the draw
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
    draw = ImageDraw.Draw(image)

def refresh():
    global edp, image
    epd.display_frame(epd.get_frame_buffer(image))
    print('   refreshed at %s' % (time.strftime('%H:%M:%S')))
    save_image()

def save_image():
    global image
    ary = np.array(image)

    # Split the three channels
    r, g, b = np.split(ary, 3, axis=2)
    r = r.reshape(-1)
    g = r.reshape(-1)
    b = r.reshape(-1)

    # Standard RGB to grayscale 
    bitmap = list(map(lambda x: 0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2], zip(r, g, b)))
    bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap > 128).astype(float),255)
    im = Image.fromarray(bitmap.astype(np.uint8))
    im.save('sample.bmp')

def choose_random_loading_image():
    images = os.listdir("bmp/")
    loading_image = random.randint(0,len(images)-1)
    return images[loading_image]

def displayCalendar():

    global font, font_cal, font_day, font_day_str, font_month_str
    global image, draw

    print('Displaying calendar...')

    calendar.setfirstweekday(calendar.MONDAY)  #set the first day of the week 
    LINEHEIGHT = 20

    # For simplicity, the arguments are explicit numerical coordinates


    #Calendar Strings
    cal_day_str = time.strftime("%A")
    cal_day_number  = time.strftime("%d")
    cal_month_str  = time.strftime("%B")+' '+ time.strftime("%Y")

    date = datetime.now()
    cal_month_cal = str(calendar.month(date.year,date.month)).replace(time.strftime("%B")+' ' +time.strftime("%Y"),' ')

    cal_width = 240

    #this section is to center the calendar text in the middle

    #the Day string "Monday" for Example
    w_day_str,h_day_str = font_day_str.getsize(cal_day_str)
    x_day_str = (cal_width/2)-(w_day_str/2)
    #y_day_str = (epd2in9.EPD_HEIGHT/2)-(h/2)

    #the settings for the Calenday today number
    w_day_num,h_day_num = font_day.getsize(cal_day_number)
    x_day_num = (cal_width/2)-(w_day_num/2)

    #the settings for the Calenday Month String
    w_month_str,h_month_str = font_month_str.getsize(cal_month_str)
    x_month_str = (cal_width/2)-(w_month_str/2)

    #the settings for the Calenday display (didn't work)
    #w_month_cal_str,h_month_cal_str = font_day_str.getsize(cal_month_cal)
    #x_month_cal_str = (cal_width/2)-(w_month_cal_str/2)

    
    draw.rectangle((0,0,240, 384), fill = 0)
    draw.text((15, 190),cal_month_cal , font  = font_cal, fill = 255)
    draw.text((x_day_str,25),cal_day_str,font = font_day_str,fill = 255)
    draw.text((x_day_num,50),cal_day_number,font = font_day,fill = 255)
    draw.text((x_month_str,165),cal_month_str,font = font_month_str,fill = 255)
    refresh()

if __name__ ==  '__main__':
    main()
