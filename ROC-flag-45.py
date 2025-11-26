# 導入 doc
from browser import document as doc
from browser import html
import math

# 建立畫布
canvas = html.CANVAS(width = 600, height = 400)
canvas.id = "taiwan_flag"
doc["brython_div1"] <= canvas

canvas = doc["taiwan_flag"]
ctx = canvas.getContext("2d")

flag_w = canvas.width
flag_h = canvas.height
circle_x = flag_w/4
circle_y = flag_h/4

#--------------------------------------
#  函數：繪製中華民國國旗（無旋轉版）
#--------------------------------------
def draw_flag():
    # 先畫滿地紅
    ctx.fillStyle='rgb(255, 0, 0)'
    ctx.fillRect(0,0,flag_w,flag_h)

    # 再畫青天
    ctx.fillStyle='rgb(0, 0, 150)'
    ctx.fillRect(0,0,flag_w/2,flag_h/2)

    # 畫十二道光芒白日
    ctx.beginPath()
    star_radius = flag_w/8
    angle = 0
    for i in range(24):
        angle += 5*math.pi*2/12
        toX = circle_x + math.cos(angle)*star_radius
        toY = circle_y + math.sin(angle)*star_radius
        if (i):
            ctx.lineTo(toX, toY)
        else:
            ctx.moveTo(toX, toY)
    ctx.closePath()
    ctx.fillStyle = '#fff'
    ctx.fill()

    # 白日:藍圈
    ctx.beginPath()
    ctx.arc(circle_x, circle_y, flag_w*17/240, 0, math.pi*2)
    ctx.closePath()
    ctx.fillStyle = 'rgb(0, 0, 149)'
    ctx.fill()

    # 白日:白心
    ctx.beginPath()
    ctx.arc(circle_x, circle_y, flag_w/16, 0, math.pi*2)
    ctx.closePath()
    ctx.fillStyle = '#fff'
    ctx.fill()

#--------------------------------------
# 函數：旋轉整面國旗 angle 度
#--------------------------------------
def rotate_flag(angle_deg):
    # 清空畫布
    ctx.clearRect(0, 0, flag_w, flag_h)

    # 保存座標系統
    ctx.save()

    # 旋轉中心移到畫布中心
    ctx.translate(flag_w/2, flag_h/2)

    # Canvas 的角度是用弧度 & 正角是逆時針
    angle_rad = -angle_deg * math.pi / 180
    ctx.rotate(angle_rad)

    # 再移回左上角
    ctx.translate(-flag_w/2, -flag_h/2)

    # 畫國旗
    draw_flag()

    # 還原座標系統
    ctx.restore()

#--------------------------------------
# 在此選擇旋轉角度：
#--------------------------------------

#rotate_flag(0)   # 不旋轉
rotate_flag(45)  # 順時針 45°