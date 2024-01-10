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
from PIL import Image, ImageDraw,ImageFont



#全局变量，根据输入赋值
file_path=None

#经验
#1.图片加载要几秒时间
#所以每点一下停几秒
#2.桌面上不能有太多相同图片
#会导致找不到

  
class ScriptRunnerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.title("datasave helpers version_2.0")

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
        file_menu.add_command(label="Run Once", command=self.run_once)
        file_menu.add_command(label="Run Multiple", command=self.run_multiple)
        file_menu.add_separator()
        file_menu.add_command(label="Select", command=self.read_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # 创建"Options"菜单
        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Run Once", command=self.run_once)
        options_menu.add_command(label="Run Multiple", command=self.run_multiple)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        
        # 创建"Author"菜单
        author_menu = tk.Menu(menu_bar, tearoff=0)
        author_menu.add_command(label="About the Author", command=self.show_author_info)
        menu_bar.add_cascade(label="Author", menu=author_menu)

        # 创建"Help"菜单
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
        control_panel.pack(side=tk.LEFT,padx=10,pady=10,fill=tk.X,expand=True)
        
        # 按钮样式
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10, relief="groove", borderwidth=2, foreground="blue")
           
        self.label = ttk.Label(control_panel, text="请输入检测坐标的次数：")
        self.label.pack(padx=10, pady=10,fill=tk.X)

        self.entry = ttk.Entry(control_panel, width=10)
        self.entry.pack(padx=5, pady=5,fill=tk.X)
        
        self.button = ttk.Button(control_panel, text="确定", command=self.get_value)
        self.button.pack(padx=5, pady=5,fill=tk.X)
 
        self.MAX_POSITION = 0       

        #检测鼠标坐标
        self.cursor_button=ttk.Button(control_panel,text="Get Cursor Position",command=self.get_cursor_position,style="TButton")
        self.cursor_button.pack(padx=10, pady=10,fill=tk.X)

        # 按钮
        self.once_button = ttk.Button(control_panel, text="Run Once", command=self.run_once, style="TButton")
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
        self.table.heading("Column3", text="重复次数")
        #右边
        self.table.pack(side=tk.RIGHT,padx=10,pady=10,fill=tk.BOTH,expand=True)
        
        # 创建文本控件以编辑表格内容
        self.text = tk.Text(self.table.master, width=10, height=10)
        self.text.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 隐藏文本控件
        self.text.pack_forget()
 
        # 设置垂直滚动条
        yscrollbar = ttk.Scrollbar(self.table, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 捕获鼠标悬停事件以显示滚动条
        self.table.bind("<Enter>", lambda event: self.table.master.focus_set())
        self.table.bind("<Leave>", lambda event: self.table.master.focus_set())
        
        
        # 修改表格内容
        def modify_table():
            self.text.pack_forget()
            self.text.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
            self.text.delete(1.0, tk.END)
            for item in self.table.get_children():
                self.table.delete(item)
                row = self.table.item(item)
                self.text.insert(tk.END, f"{row['values'][0]} {row['values'][1]} {row['values'][2]}\n")

        # 复制表格内容
        def copy_table():
            self.text.delete(1.0, tk.END)
            for item in self.table.get_children():
                row = self.table.item(item)
                self.text.insert(tk.END, f"{row['values'][0]} {row['values'][1]} {row['values'][2]}\n")

        # 更新表格内容
        def update_table():
            for item in self.table.get_children():
                self.table.delete(item)
            self.text.delete(1.0, tk.END)
            for line in self.text.get("1.0", tk.END).split("\n"):
                values = line.split(" ")
                if len(values) == 3:
                    self.table.insert("", "end", values=values)

        # 添加菜单
        menu = tk.Menu(self.table)
        menu.add_command(label="修改", command=modify_table)
        menu.add_command(label="复制", command=copy_table)
        menu.add_command(label="更新", command=update_table)

        # 添加右键菜单
        def on_right_click(event):
            menu.post(event.x_root, event.y_root)

        self.table.bind("<Button-3>", on_right_click)
            
            
    
    def get_value(self):
        self.MAX_POSITION = int(self.entry.get())
        self.destroy()        
            
    def get_cursor_position(self):
       
       
        save_path = os.path.join(os.path.dirname(__file__), "screenshot")
        #编译成exe文件前改成以下代码
        #save_path = os.path.join(os.path.dirname(sys.executable), "screenshot")
        
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        position_history = []
        count = 0

        while True:
            x, y = pyautogui.position()
            print(f"当前鼠标坐标: ({x}, {y})")

            # 将坐标添加到列表中
            position_history.append((x, y))

            # 检测到五个坐标后截屏并标记
            count += 1
            if count == self.MAX_POSITION:
                print("开始截屏并标记...")

                # 截屏
                screenshot = pyautogui.screenshot()

                coordinates=position_history
                # 标记坐标
                draw = ImageDraw.Draw(screenshot)
                for i, (x, y) in enumerate(position_history):
                    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 0, 0))
                    draw.text((x + 10, y - 10), str(coordinates[i]), font=ImageFont.truetype("arial.ttf", 20), fill=(0, 0, 0))  # 在标记点附近添加坐标
                
                #screenshot.show() 
  
                # 保存标记后的图片 时间格式为"年月日时分"
                screenshot.save(os.path.join(save_path, f"screenshot_{time.strftime('%Y_%m_%d_%H_%M')}.png"))
                
                save_path =os.path.join(save_path, f"screenshot_{time.strftime('%Y_%m_%d_%H_%M')}.png")
                # 打开图像文件
                image = Image.open(save_path)

                # 显示图像
                image.show()
                
                # 清空坐标列表
                position_history = []
                count = 0
                
                
                #去除这个可实现套娃哦
                break;

            time.sleep(2) 
            
    

    def mouseClick(self,clickTimes,lOrR,img,reTry):
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
    
    def take_screenshot(self,count):
        screenshot = pyautogui.screenshot()
        if(count%10==0&count!=0):
            screenshot.show()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screenshot

   
    def find_image(self,image_to_find, screenshot):
        
         #确保image_to_find和screenshot具有相同数量的通道（例如3通道的BGR图像或1通道的灰度图像
        if len(image_to_find.shape) == 2:
                image_to_find = cv2.cvtColor(image_to_find, cv2.COLOR_GRAY2BGR)
       
        if len(screenshot.shape) == 2:
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2BGR)
        
        result = cv2.matchTemplate(screenshot, image_to_find, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.9:  # 设置匹配阈值，可根据实际情况调整
            return True
        else:
            return False   
    
         
    # 定义一个函数work，参数为img
    def work(self,instructions):
    # 在此处添加针对图片的键鼠操作代码

        instruction=instructions.split(" ")
        # 获取指令类型
        instruction_type = int(instruction[0])
        # 获取指令内容
        content = instruction[1]
        count=0
        # 根据指令类型进行相应的操作
        if instruction_type == 1:
            retry=int(instruction[2])
            while True:
                image_to_find=cv2.imread(content,0)
                screenshot=self.take_screenshot(count)
                exist=self.find_image(image_to_find,screenshot)
                if exist:
                    self.mouseClick(1, "left", content, retry)
                    print("单击左键",content)
                    break
                else:
                    count+=1
                    print("未找到图像，继续截屏",content)
                    time.sleep(1)  # 设置等待时间，可根据实际情况调整                
        elif instruction_type == 2:
            retry=int(instruction[2])
            while True:
                image_to_find=cv2.imread(content,0)
                screenshot=self.take_screenshot(count)
                exist=self.find_image(image_to_find,screenshot)
                if exist:
                    self.mouseClick(2, "left", content, retry)
                    print("双击左键" ,content)
                    break
                else:
                    count+=1
                    print("未找到图像，继续截屏...")
                    time.sleep(1)  # 设置等待时间，可根据实际情况调整                
        elif instruction_type == 3:
             retry=int(instruction[2])
             while True:
                image_to_find=cv2.imread(content,0)
                screenshot=self.take_screenshot(count)
                exist=self.find_image(image_to_find,screenshot)
                if exist:
                    self.mouseClick(1, "right", content, retry)
                    print("单击右键" ,content)
                    break
                else:
                    count+=1
                    print("未找到图像，继续截屏...")
                    time.sleep(1)  # 设置等待时间，可根据实际情况调整                
        elif instruction_type == 4:
            # 输入内容
            input_content = str(content)
            pyperclip.copy(input_content)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)
            print("输入:",input_content)  
        elif instruction_type == 6:
            # 滚屏操作
                scroll = content
                pyautogui.scroll(int(scroll))
                print("滚轮滑动",int(scroll),"距离")  
                
                


    def main(self):
        
        with open(self.file_path, "r") as f:
            cmds = f.readlines()

        cmd = [path.strip() for path in cmds]

        for instruction in cmds:
            self.work(instruction)
            
    def run_once(self):
        self.main()


    def run_multiple(self):
        # 获取循环次数
        loop_count = int(self.loop_entry.get())

        # 循环运行
        for i in range(loop_count):
            # 运行一次
            self.run_once()

            # 更新表格
            self.table.delete(*self.table.get_children())
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    values = line.strip().split()
                    self.table.insert("", "end", values=values)


    def read_file(self):
        # 打开文件选择器
        self.file_path = tk.filedialog.askopenfilename()
        
        self.file_path_label.config(text=f"File path: {self.file_path}")

        # 读取文件内容并显示在表格中
        with open(self.file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                values = line.strip().split()
                self.table.insert("", "end", values=values)

    def select_file(self):
        # 打开文件选择器
        self.file_path = tk.filedialog.askopenfilename()

        self.file_path_label.config(text=f"File path: {self.file_path}")
        
        
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
            