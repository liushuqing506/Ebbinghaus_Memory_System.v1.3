

import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from tkinter import *
from collections import OrderedDict


'''说明
Ebbinghaus_Memory_System.v1.3
生成艾宾浩斯遗忘曲线复习计划表
复习间隔周期为1天,2天,4天,7天,15天
每组内容,共记忆6遍(1次记忆+5次复习)
--------------------------------
tkinter部分脚本也可以用class的方式写
'''

# 艾宾浩斯代码部分
def func(listTemp,n):
    for i in range(0,len(listTemp),n):
        yield listTemp[i:i+n]

def Ebbinghaus(totalNum,unitNum,outFile):
    UnitUnitsDict = OrderedDict()
    totalList = [i+1 for i in range(totalNum)]
    temp = func(totalList,unitNum)
    for i,j in enumerate(temp):
        UnitUnitsDict[i+1] = j
        unitSumNum = i+1

    dayMax = unitSumNum + 15
    timeList = [1,2,4,7,15]
    # 组和组出现的天数
    UnitDayDict = OrderedDict()
    for i in [k+1 for k in range(unitSumNum)]:
        listTemp = [i]
        for j in timeList:
            listTemp.append(i+j)
        UnitDayDict[i] = listTemp
    # 天数和这一天的组数
    DayUnitDict = OrderedDict()
    for k in [k+1 for k in range(dayMax)]:
        DayUnitDict[k] = []
        for i,j in UnitDayDict.items():
            for m in j:
                if m == k:
                    DayUnitDict[k].append(i)
                else:
                    pass

    # outFile = 'plan.csv'
    with open(outFile,'w') as fw:
        fw.writelines('天数,初学,复习\n')
        for i,j in DayUnitDict.items():
            fw.writelines('day-{0},'.format(i))
            if i == j[-1]:
                fw.writelines('{0},{1}\n'.format('; '.join([str(m) for m in UnitUnitsDict[j[-1]]]),' || '.join(['; '.join([str(n) for n in UnitUnitsDict[k]]) for k in j[:-1]])))
                # print('; '.join([str(m) for m in UnitUnitsDict[j[-1]]])+','+' || '.join(['; '.join([str(n) for n in UnitUnitsDict[k]]) for k in j[:-1]]))
                # print(str(UnitUnitsDict[j[-1]])+' | '+str([UnitUnitsDict[k] for k in j[:-1]]))
            else:
                fw.writelines('{0},{1}\n'.format('No',' || '.join([';'.join([str(m) for m in UnitUnitsDict[k]]) for k in j])))
                # print('No,'+' || '.join([';'.join([str(m) for m in UnitUnitsDict[k]]) for k in j]))
                # print('[] | '+str([UnitUnitsDict[k] for k in j]))
                
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
    totalNum = int(entry0.get())
    unitNum = int(entry1.get())
    downloadPath = select_path.get()
    fileName = file_name.get()
    conserveValue = msgbox.askyesno(title='提示',message='是否保存')  # 提示框之后,运行生成代码 返回值true/false
    '''说明
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
        outFile = os.path.join(downloadPath,fileName+'.csv')
        Ebbinghaus(totalNum,unitNum,outFile)
    else:
        pass
    
def quit():
    root.destroy()

root = tk.Tk()
root.title('HOME')
# root.title('Ebbinghaus Memory System v.1.3')
root.geometry('300x200')  # 窗口长x窗口宽
frame_show = Frame(width=800,height=400,bg="#008080")  # 窗口在电脑屏幕显示位置:X轴坐标+屏幕Y轴坐标;title的背景颜色

LableTitle0=tk.Label(root,text='艾宾浩斯遗忘曲线计划表生成器 v.1.3',width=40,height=1).place(x=0,y=0)

entry0 = tk.StringVar()
# entry0.set('请输入数字')  #文本框中默认的信息
# place是插件坐标
Lable0=tk.Label(root,text='项目总数',width=8,height=1).place(x=0,y=30)
Entry0 = tk.Entry(root,textvariable=entry0,width=10).place(x=60,y=30)
Lable00=tk.Label(root,text='个  (整数)',width=7,height=1).place(x=140,y=30)

entry1 = tk.StringVar()
# entry1.set('请输入数字')
Lable1=tk.Label(root,text='个数/单元',width=8,height=1).place(x=0,y=60)
Entry1 = tk.Entry(root,textvariable=entry1,width=10).place(x=60,y=60)
Lable00=tk.Label(root,text='个  (整数)',width=7,height=1).place(x=140,y=60)

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