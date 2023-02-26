
# author:LSQ
# e-mail:546397641@qq.com
# date_start:2022.07.02

import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from tkinter import *
from collections import OrderedDict
import pandas as pd



'''说明
Ebbinghaus_Memory_System.v1.5
生成艾宾浩斯记忆曲线复习计划表
复习间隔周期为1天,2天,4天,7天,15天
每组内容,共记忆6遍(1次记忆+5次复习)
2022.12.11升级,输出从.csv到.xlsx
修改为项目编号起止
--------------------------------
tkinter部分脚本也可以用class的方式写
'''

# 艾宾浩斯代码部分
def func(listTemp,n):
    for i in range(0,len(listTemp),n):
        yield listTemp[i:i+n]

def Ebbinghaus(unitNum,outFile,start_num,end_num):
    UnitUnitsDict = OrderedDict()
    totalList = [i for i in range(start_num,end_num+1)]
    print(totalList)
    temp = func(totalList,unitNum)
    # print(list(temp))
    for i,j in enumerate(temp):
        UnitUnitsDict[i+1] = j
        unitSumNum = i+1
    print(unitSumNum)
    dayMax = unitSumNum + 15
    timeList = [1,2,4,7,15]
    # 组和组出现的天数
    UnitDayDict = OrderedDict()
    for i in [k+1 for k in range(unitSumNum)]:
        listTemp = [i]
        for j in timeList:
            listTemp.append(i+j)
        UnitDayDict[i] = listTemp
    # print(UnitDayDict)
    # 天数和这一天包括哪些组
    DayUnitDict = OrderedDict()
    for k in [k+1 for k in range(dayMax)]:
        DayUnitDict[k] = []
        for i,j in UnitDayDict.items():
            for m in j:
                if m == k:
                    DayUnitDict[k].append(i)
                else:
                    pass
    
    # print(DayUnitDict)
    day_list = []
    begin_learn_list = []
    review_list = []
    for i,j in DayUnitDict.items():
        day_list.append('day-{0}'.format(i))
        if len(j) != 0:
            if i == 1:  # 第一天没有复习的任务
                begin_learn_list.append(';'.join([str(m) for m in UnitUnitsDict[j[-1]]]))
                review_list.append('No')
            elif i == j[-1]:  # 当天有初学组
                begin_learn_list.append(';'.join([str(m) for m in UnitUnitsDict[j[-1]]]))
                review_list.append(' | '.join([';'.join([str(n) for n in UnitUnitsDict[k]]) for k in j[:-1]]))
                # print('; '.join([str(m) for m in UnitUnitsDict[j[-1]]])+','+' || '.join(['; '.join([str(n) for n in UnitUnitsDict[k]]) for k in j[:-1]]))
                # print(str(UnitUnitsDict[j[-1]])+' | '+str([UnitUnitsDict[k] for k in j[:-1]]))
            else:
                begin_learn_list.append('No')
                review_list.append(' | '.join([';'.join([str(m) for m in UnitUnitsDict[k]]) for k in j]))
                # print('No,'+' || '.join([';'.join([str(m) for m in UnitUnitsDict[k]]) for k in j]))
                # print('[] | '+str([UnitUnitsDict[k] for k in j]))
        else:  # 当天没有学习任务
            begin_learn_list.append('No')
            review_list.append('No')
    # 整理，写入xlsx
    df = pd.DataFrame({'天数':day_list,'初学':begin_learn_list,'复习':review_list})
    df['打卡']='   :'
    df.to_excel(outFile, sheet_name='Sheet1',index=False)
                
# 编写按钮命令
def select_file():
    # 单个文件选择
    selected_file_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
    select_path.set(selected_file_path)  
def select_files():
    # 多个文件选择
    selected_files_path = filedialog.askopenfilenames()  # askopenfilenames函数选择多个文件
    select_path.set('\n'.join(selected_files_path))  # 多个文件的路径用换行符隔开
def select_folder():
    # 文件夹选择
    selected_folder = filedialog.askdirectory()  # 使用askdirectory函数选择文件夹
    select_path.set(selected_folder)

def event():
    '''按钮事件'''
    start_num = int(entry0.get())
    end_num = int(entry2.get())
    unitNum = int(entry1.get())
    downloadPath = select_path.get()
    fileName = file_name.get()
    conserveValue = msgbox.askyesno(title='提示',message='是否保存')  # 提示框之后,运行生成代码 返回值true/false
    '''补充知识
    不可关闭对话框
    msgbox.askquestion('确认操作', '确认执行此次操作吗？') # 返回值yes/no
    msgbox.askyesno('确认操作', '确定执行？') # 返回值true/false
    可关闭对话框
    msgbox.askokcancel('确认操作', '该操作需要慎重~')  # 返回值true/false
    msgbox.askretrycancel('确认操作', '如果操作，无法撤销~')  # 返回值true/false
    '''
    if conserveValue:
        # print(totalNum)
        # print(downloadPath)
        outFile = os.path.join(downloadPath,fileName+'.xlsx')
        Ebbinghaus(unitNum,outFile,start_num,end_num)
    else:
        pass
    
def quit():
    root.destroy()

root = tk.Tk()
root.title('HOME')
# root.title('Ebbinghaus Memory System v.1.3')
root.geometry('300x200')  # 窗口长x窗口宽
frame_show = Frame(width=800,height=400,bg="#008080")  # 窗口在电脑屏幕显示位置:X轴坐标+屏幕Y轴坐标;title的背景颜色

LableTitle0=tk.Label(root,text='<艾宾浩斯记忆法> 计划表生成器 v1.7',width=40,height=1).place(x=0,y=0)

entry0 = tk.StringVar()  # 初始化
entry2 = tk.StringVar()  # 初始化
# entry0.set('请输入数字')  #文本框中默认的信息
# place是插件坐标
Lable0=tk.Label(root,text='项目编号 (整数)',width=13,height=1).place(x=0,y=30)
Lable0=tk.Label(root,text='Start',width=5,height=1).place(x=93,y=30)
Entry0 = tk.Entry(root,textvariable=entry0,width=7).place(x=130,y=30)
Lable0=tk.Label(root,text='>>',width=3,height=1).place(x=185,y=30)
Lable0=tk.Label(root,text='End',width=4,height=1).place(x=205,y=30)
Entry0 = tk.Entry(root,textvariable=entry2,width=7).place(x=235,y=30)
# Lable00=tk.Label(root,text='个  (整数)',width=7,height=1).place(x=140,y=30)

entry1 = tk.StringVar()
# entry1.set('请输入数字')
Lable1=tk.Label(root,text='个数/单元 (整数)',width=13,height=1).place(x=0,y=60)
Entry1 = tk.Entry(root,textvariable=entry1,width=7).place(x=100,y=60)
# Lable00=tk.Label(root,text='个  (整数)',width=7,height=1).place(x=140,y=60)

select_path = tk.StringVar()
select_path.set('点击按钮: 选择文件夹')
Lable2=tk.Label(root, text="下载地址").place(x=0,y=90)
Entry2=tk.Entry(root, textvariable = select_path,width=32).place(x=60,y=90)
# tk.Button(root, text="选择单个文件", command=select_file).place(x=10,y=40)
# tk.Button(root, text="选择多个文件", command=select_files).place(x=10,y=75)
Button2 = tk.Button(root, text="选择文件夹", command=select_folder).place(x=10,y=160)

file_name = tk.StringVar()
# file_name.set('请输入文件名')
Lable3=tk.Label(root, text="文件名").place(x=0,y=120)
Entry3=tk.Entry(root, textvariable = file_name).place(x=60,y=120)

Button0 = tk.Button(root,text='点击生成',width=8,height=1,command=event).place(x=110,y=160)  # width:按钮长；height:按钮高

Button1 = tk.Button(root,text='退出',width=8,height=1,command=quit).place(x=210,y=160)

# for child in root.winfo_children(): child.grid_configure(padx=5, pady=5)
# Entry3.focus()  # focus(),初始光标所在位置 一直有问题？

# for child in frame_show.winfo_children(): child.grid_configure(padx=5, pady=5)
# root.bind('<Return>', event)

root.mainloop()