# 名字：NH4NO3nice
# 日期：2023年02月02日

import os
import re
import sys
import time

# # 安装所需函数库
# os.system('pip install pyautogui')
# os.system('pip install pillow')
# os.system('pip install pyperclip')

# # 导入函数库pyautogui和pypaperclip
import pyperclip
import pyautogui as pgi


class AutoClick():

    def __init__(self):
        """创建实例时，自动读取参数和指令文件"""
        self.ins_position, self.ins_picture = '', ''
        self.instrctions = ''
        self.read_parameter()
        self.read_ins()


    # # 读取传入参数
    def read_parameter(self):
        # # 获取传入参数（指令文件和定位图片）
        if len(sys.argv) == 1:
            self.ins_position = input('>>> 请输入指令文件地址: ')
            temp = input('>>> 是否有定位图片(Y/N): ')
            if temp[0].upper() == 'Y':
                self.ins_picture = input('>>> 请输入定位文件地址: ')
        elif len(sys.argv) == 2:
            self.ins_position = sys.argv[1]                  # 获取指令文件地址
            temp = input('>>> 是否有定位图片(Y/N): ')
            if temp[0].upper() == 'Y':
                self.ins_picture = input('>>> 请输入定位文件地址: ')
        elif len(sys.argv) == 3:
            self.ins_position, self.ins_picture = sys.argv[1:]
        else:
            print('>>> 无效参数输入！！！')
            sys.exit(0)  # 程序中断

        print('指令文件地址：' + self.ins_position + '\n' + '定位图片地址：' + self.ins_picture)


    # # 读取指令
    def read_ins(self):
        # # 读取指令文件
        with open(self.ins_position, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        self.instructions = [re.split(r'[、；]', i)[:-1] for i in lines]  # 以、，；三个分隔符分割指令
        for i in self.instructions:
            if len(i) <= 1:                 # 如果某行指令为空，则去除该行
                self.instructions.remove(i)
        # # 对指令排序
        self.instructions.sort(key=lambda n: int(n[0]))


    # # 执行指令
    def action(self):
        res = pgi.confirm(text='是否现在执行命令？', title='提示', buttons=['是', '否']) # OK和Cancel按钮的消息弹窗
        if res == '是':
            # # 执行指令
            for step in self.instructions:      # 执行步骤
                # 执行每一步的具体指令
                ins_s = step[1].split('：')     # 分割具体指令
                if ins_s[0] == '鼠标移动':
                    self.mouse_move(ins_s[1])
                elif ins_s[0] == '点击':
                    self.mouse_click(ins_s[1])
                elif ins_s[0] == '输入':
                    self.keyboard_input(ins_s[1])
                elif ins_s[0] == '按下':
                    self.keyboard_press(ins_s[1])
                elif ins_s[0] == '休眠':
                    time.sleep(float(ins_s[1]))
        else:
            sys.exit(0)

    
    # # 执行鼠标移动指令
    def mouse_move(self, direcion):

        move_dir = re.split(r'[“”]', direcion)[:2]       # 鼠标移动的方位由“”给出
        
        if move_dir[0] == '图':        # 如果方向是由截图给出
            # # 获取图片在屏幕中的中心坐标
            position = pgi.locateCenterOnScreen(self.ins_picture + '\\' + move_dir[1] + '.png')
            pgi.moveTo(position[0], position[1], duration=0.25)     # 鼠标移动到截图的中心位置，时间间隔0.25s
        elif move_dir[0] == '坐标':     # 如果给出具体坐标
            # # 获取坐标x,y
            position = re.split(r'[(,)]', move_dir[1])[1:-1]
            position = [float(i) for i in position]     # 将字符串坐标转化为浮点数
            pgi.moveTo(position[0], position[1], duration=0.25)     # 鼠标移动到指定坐标位置，时间间隔0.25s
        elif '移' in move_dir[0]:       # 如果给出具体移动方向和移动距离
            distance = float(move_dir[1])       # 将具体移动距离转化为浮点数
            if move_dir[0] == '左移':
                pgi.moveRel(-1 * distance, 0, duration=0.25)
            elif move_dir[0] == '右移':
                pgi.moveRel(distance, 0, duration=0.25)  
            elif move_dir[0] == '上移':
                pgi.moveRel(0, -1 * distance, duration=0.25)     
            elif move_dir[0] == '下移':
                pgi.moveRel(0, distance, duration=0.25)
            else:
                print("鼠标移动的指令出错！！！应该为上移、下移、左移或右移")
                sys.exit(0)     # 程序中断
        else:
            print("鼠标移动的指令出错！！！")
            sys.exit(0)     # 程序中断


    # # 执行鼠标点击指令
    def mouse_click(self, way):

        method = re.split(r'[击【】]', way)[:-1]        # 以击【】三个分隔符分割，分割结果为三个元素的列表eg.['右单', '2次', '间隔2秒']

        # # 确定左/右击
        if '左' in method[0]:
            dir = 'left'
            method[0] = method[0].replace('左', '')     # 删除‘左’字
        elif '右' in method[0]:
            dir = 'right'
            method[0] = method[0].replace('右', '')     # 删除‘右’字
        else:       # 如果未指定左右，则默认左击
            dir = 'left'

        # # 确定循环点击次数，及循环间隔
        num = int(method[1][:-1])
        duration = float(method[2][2:-1])    
        # 执行点击指令
        for i in range(num):
            # # 判断单击、双击或三击
            if method[0] == '单' or method[0] == '':
                pgi.click(button=dir)
            elif method[0] == '双':
                pgi.doubleClick(button=dir)
            elif method[0] == '三':
                pgi.tripleClick(button=dir)
            time.sleep(duration)        # 程序休眠

    
    # # 执行键盘输入指令
    def keyboard_input(self, input):

        # # 粘贴
        pyperclip.copy(input)
        # # 复制
        pgi.keyDown('ctrl')
        pgi.keyDown('v')
        pgi.keyUp('ctrl')
        pgi.keyUp('v')


    # # 执行键盘按键指令
    def keyboard_press(self, key):
        key = re.split(r'[“”]', key)[1]
        pgi.press('enter')


if __name__ == "__main__":
    auto = AutoClick()      # 创建实例
    auto.action()           # 执行指令
