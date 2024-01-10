import cv2
import numpy as np
import pyautogui
import os
import time
import sys
from PIL import Image
import pyperclip
import tkinter
from tkinter import Tk, TkVersion, filedialog
import tkinter as tk
from tkinter import ttk

#全局变量，根据输入赋值
file_path=None

#经验
#1.图片加载要几秒时间
#所以每点一下停几秒
#2.桌面上不能有太多相同图片
#会导致找不到

 

def mouseClick(clickTimes,lOrR,img,reTry):
    #尝试次数
    if reTry == 1:
        while True:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                break
            print("未找到匹配图片,0.1秒后重试")
            time.sleep(0.1)
    #死循环
    elif reTry == -1:
        while True:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
            time.sleep(0.1)
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                print("重复")
                i += 1
            time.sleep(0.1)
 
 



# 定义一个函数work，参数为img
def work(instructions):
   # 在此处添加针对图片的键鼠操作代码

   instruction=instructions.split(" ")
   # 获取指令类型
   instruction_type = int(instruction[0])
   # 获取指令内容
   content = instruction[1]
   # 根据指令类型进行相应的操作
   if instruction_type == 1:
        retry=int(instruction[2])
        mouseClick(1,"left",content,retry)
        print("单击左键",content)
   elif instruction_type == 2:
       retry=int(instruction[2])
       mouseClick(2,"left",content,retry)
       print("双击左键",content)
   elif instruction_type == 3:
       retry=int(instruction[2])
       mouseClick(1,"right",content,retry)
       print("单击右键",content)
   elif instruction_type == 4:
       # 输入内容
       input_content = str(content)
       pyperclip.copy(input_content)
       pyautogui.hotkey('ctrl','v')
       time.sleep(0.5)
       print("输入:",input_content)  
       
   elif instruction_type == 5:
       # 等待时间
       wait_time = int(instruction[1])
       time.sleep(wait_time)
       print("等待",wait_time,"秒")
   elif instruction_type == 6:
       # 滚屏操作
        scroll = content
        pyautogui.scroll(int(scroll))
        print("滚轮滑动",int(scroll),"距离")             

   

def main():
    
    with open(file_path, "r") as f:
        cmds = f.readlines()

    cmd = [path.strip() for path in cmds]

    for instruction in cmds:
        work(instruction)
        
        
def run_once():
    main()
    
    
        
        
      
class ScriptRunnerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.title("datasave helpers version_1.0")

        # 设置窗口大小
        self.geometry("1000x900")

        # 设置菜单
        self.create_menu()

        # 创建控制面板
        self.create_control_panel()
        
        self.create_table()

    def create_menu(self):
        # 创建菜单栏
        menu_bar = tk.Menu(self)

        # 创建"File"菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Run Once", command=run_once)
        file_menu.add_command(label="Run Multiple", command=self.run_multiple)
        file_menu.add_separator()
        file_menu.add_command(label="Select", command=self.read_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # 创建"Options"菜单
        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Run Once", command=run_once)
        options_menu.add_command(label="Run Multiple", command=self.run_multiple)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        
        # 创建"Author"菜单
        author_menu = tk.Menu(menu_bar, tearoff=0)
        author_menu.add_command(label="About the Author", command=self.show_author_info)
        menu_bar.add_cascade(label="Author", menu=author_menu)

        # 创建"Error"菜单
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="error", command=self.show_error_info)
        help_menu.add_command(label="warning", command=self.show_warning_info)
        help_menu.add_command(label="info", command=self.show_info_info)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        # 应用菜单栏
        self.config(menu=menu_bar)

    def create_control_panel(self):
        # 创建控制面板
        control_panel = ttk.LabelFrame(self, text="Control Panel")
        #放在左边
        control_panel.pack(side=tk.LEFT,padx=10,pady=10,fill=tk.Y,expand=True)

        # 按钮样式
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10, relief="groove", borderwidth=2, foreground="blue")

        # 按钮
        self.once_button = ttk.Button(control_panel, text="Run Once", command=run_once, style="TButton")
        self.once_button.pack(padx=10, pady=10,fill=tk.X)
        
        
        # 创建标签
        self.loop_label = ttk.Label(control_panel, text="Loop Count:")
        self.loop_label.pack(padx=5, pady=5)

        # 创建输入框
        self.loop_entry = ttk.Entry(control_panel, width=10)
        self.loop_entry.pack(padx=5, pady=5)


        self.multiple_button = ttk.Button(control_panel, text="Run Multiple", command=self.run_multiple, style="TButton")
        self.multiple_button.pack(padx=10, pady=10,fill=tk.X)
        
        
        # 显示文件路径
        self.file_path_label = ttk.Label(control_panel, text="File path: None")
        self.file_path_label.pack(padx=10, pady=10,fill=tk.X)
        
        # 创建文件选择器
        file_selector = ttk.Button(control_panel, text="Select File", command=self.read_file)
        file_selector.pack(padx=10, pady=10,fill=tk.X)
        
        # 创建表格
    def create_table(self):    
        #放在右边
        self.table = ttk.Treeview(columns=("Column1", "Column2", "Column3"), show="headings")
        self.table.heading("Column1", text="操作类型")
        self.table.heading("Column2", text="操作内容")
        self.table.heading("Column3", text="等待时间")
        #右边
        self.table.pack(side=tk.RIGHT,padx=10,pady=10,fill=tk.BOTH,expand=True)

    def run_multiple(self):
        # 获取循环次数
        loop_count = int(self.loop_entry.get())

        # 循环运行
        for i in range(loop_count):
            # 运行一次
            run_once()

            # 更新表格
            self.table.delete(*self.table.get_children())
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    values = line.strip().split()
                    self.table.insert("", "end", values=values)


    def read_file(self):
        # 打开文件选择器
        global file_path
        file_path = tk.filedialog.askopenfilename()

        # 更新文件路径标签
        self.file_path = file_path
        self.file_path_label.config(text=f"File path: {file_path}")

        # 读取文件内容并显示在表格中
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                values = line.strip().split()
                self.table.insert("", "end", values=values)

    def select_file(self):
        # 打开文件选择器
        global file_path
        file_path = tk.filedialog.askopenfilename()

        # 更新文件路径标签
        self.file_path = file_path
        self.file_path_label.config(text=f"File path: {file_path}")
        
        
    def show_author_info(self):
        # 显示作者信息
        author_info = tk.Toplevel(self)
        author_info.title("About the Author")
        author_info.geometry("400x300")
        author_info_label = ttk.Label(author_info, text="This application was developed by the author.")
        author_info_label.pack(pady=10)

    def show_error_info(self):
        # 显示错误信息
        error_info = tk.Toplevel(self)
        error_info.title("Report an Error")
        error_info.geometry("400x300")
        error_info_label = ttk.Label(error_info, text="#1.图片加载要几秒时间，所以每点一下停几秒\n\n"
                                     "2.桌面上不能有太多相同图片，会导致找不到")
        error_info_label.pack(pady=10)
        
    def show_warning_info(self):
        # 显示警告信息
        warning = tk.Toplevel(self)
        warning.title("Warning")
        warning.geometry("400x300")
        warning_label = ttk.Label(warning, text="This application is still in development.")
        warning_label.pack(pady=10)
        
    def show_info_info(self):
        # 显示信息
        info = tk.Toplevel(self)
        info.title("Information")
        info.geometry("500x400")
        info_label = ttk.Label(info, text="This application is used to automatically click the screen.\n\n"
                               "The correct txt file should contain the following content:\n\n"
                                        "1 D:\adesktop\vscode\jiaoben_python\txt_auto\img\1.png 1\n\n"
                                        "5 3\n\n"
                                        "1 D:\adesktop\vscode\jiaoben_python\txt_auto\img\2.png 1\n\n"
                                        "5 10\n\n"
                                        "1 D:\adesktop\vscode\jiaoben_python\txt_auto\img\3.png 1\n\n"
                                        "5 3")
        info_label.pack(pady=10)
    

    
if __name__ == "__main__":  
    
    #预设 
    #file_path="D:\\adesktop\\vscode\\jiaoben_python\\txt_auto\\cmd.txt" 
    #输入
    #file_path=str(input("Enter a file path:"))
    
    #print("file_path: " + file_path)
    
    #改为在界面上选择文件
    app = ScriptRunnerApp()
    app.mainloop()  
            
   