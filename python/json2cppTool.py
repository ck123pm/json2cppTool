# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
from json2cppFull import *

class Menu():
   
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Json2cpp")
        self.window.geometry("900x900")
        self.window.resizable(0,0)

        # self.hasHead = tk.IntVar()
        # self.hasHead.set(1)
        self.filelist = []
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()



        '''
        整体布局
        '''
        self.frameTop = tk.Frame(self.window)
        self.frameTop.grid(row = 0,column = 0)
        self.frameDown = tk.Frame(self.window)
        self.frameDown.grid(row = 1,column=0)

        tk.Button(self.frameTop,text = "Help",command = self.showHelp).grid(row = 0,column =0, sticky=tk.NS)

        tk.Label(self.frameDown,text = "Json文件:").grid(row = 0,column = 0)
        tk.Label(self.frameDown,text = "输出路径:").grid(row = 1,column = 0)

        self.input = tk.Entry(self.frameDown,width = 100,textvariable=self.input_path)
        self.input.grid(row=0,column=1,padx = 10,pady = 10)
        self.output = tk.Entry(self.frameDown,width = 100,textvariable=self.output_path)
        self.output.grid(row=1,column=1,padx = 10,pady = 10)
        
        tk.Button(self.frameDown,text = "选择",command = self.selectFiles).grid(row = 0,column = 2)
        tk.Button(self.frameDown,text = "选择",command = self.selectOutputPath).grid(row = 1,column = 2)
        # tk.Checkbutton(self.frameDown,text = "是否包含外节点",variable = self.hasHead,onvalue = 1,offvalue = 0).grid(row = 2,column = 0)
        tk.Button(self.frameDown,text = "生成",command = self.generate).grid(row = 2,column = 2)

        tk.Label(self.frameDown,text = "Json数据:").grid(row = 3,column = 0)
        self.text_raw = tk.Text(self.frameDown,width =100,height = 30)
        self.text_raw.grid(row = 4,column = 1)
        self.scroll_Y1 = tk.Scrollbar(self.frameDown,orient=tk.VERTICAL,command=self.text_raw.yview)
        self.scroll_Y1.grid(row = 4,column = 2,sticky=tk.N+tk.S+tk.W)
        self.text_raw['yscrollcommand']= self.scroll_Y1.set
        self.scroll_X1 = tk.Scrollbar(self.frameDown,orient=tk.HORIZONTAL,command=self.text_raw.xview)
        self.scroll_X1.grid(row = 5,column = 1,sticky=tk.N+tk.W+tk.E)
        self.text_raw['xscrollcommand']= self.scroll_X1.set

        tk.Label(self.frameDown,text = "生成结果:").grid(row = 6,column = 0)
        self.text_result = tk.Text(self.frameDown,width =100,height =20)
        self.text_result.grid(row = 7,column = 1)
        self.scroll = tk.Scrollbar(self.frameDown,orient=tk.VERTICAL,command=self.text_result.yview)
        self.scroll.grid(row = 7,column = 2,sticky=tk.N+tk.S+tk.W)
        self.text_result['yscrollcommand']= self.scroll.set



        self.window.mainloop()

    def showHelp(self):
        tkinter.messagebox.showinfo(title='Help', message='''
        使用说明：

        1.支持导入多个json文件，生成对应的cpp文件

        2.支持输入json数据，生成对应的cpp文件

        3.默认生成路径为当前路径

        4.json数据必须包含外部节点，例如
        {
            "UserInfo": {
                "employeeNo": "", 
                "name": "",
            }
        }
        ''')
    def selectFiles(self):
        default_dir = r"./"
        fname = filedialog.askopenfilenames(title=u"select files",
                                     initialdir=(os.path.expanduser(default_dir)))
        self.filelist=fname
        self.input_path.set(fname)

    def selectOutputPath(self):
        default_dir = r"./"
        pname = filedialog.askdirectory(title=u"select path",
                                     initialdir=(os.path.expanduser(default_dir)))
        self.output_path.set(pname)
    
    def insertResult(self,result):
        self.text_result.insert('end',result+'\n')


    def generate(self):
        if len(self.output_path.get()) == 0:
            path = os.getcwd()+'/'
        else:
            path = str(self.output_path.get())+'/'
        
        if len(self.input.get()) != 0:
            Json2cpp().run(self.filelist,path,self.insertResult)
            
        if len(self.text_raw.get('1.0','end')) > 1:
            Json2cpp().runJsonData(str(self.text_raw.get('1.0','end')),path, self.insertResult)
        self.text_result.insert('end','--------------------\n')

    # def setHasHead(self):
    #     self.hasHead = 

def main():
    menu = Menu()

if __name__ == '__main__':
    main()