import tkinter as tk
from tkinter import ttk, Button, Label
import matplotlib
import matplotlib.pyplot as plt
import time
import cloud 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 
matplotlib.use('TkAgg')


print(cloud.get_things_and_props)
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state('normal')
        self.tabsys = ttk.Notebook(self)
        
        self.configure(bg='#AED830')
        self.attributes('-topmost',True)
        self.humidity =[

        ]
        self.temperature=[
        
        ]
        self.time_local=[ 
                        ]
        self.geometry("500x350")
        self.fig =(plt.figure(figsize=(7,3), num='Terrarium data', facecolor='white'))
        self.title("Terrarium data")
        self.canvas = FigureCanvasTkAgg(self.fig, 
                               master = self) 
        
        #self.canvas.draw() 
        self.canvas.get_tk_widget().pack( side="bottom", expand=True)
        #self.canvas.get_tk_widget().configure(bg='#AED830')
        #self.canvas.get_tk_widget().configure(height=0)
    # placing the canvas on the Tkinter window 


        self.titlabel = ttk.Label(
            self,
            text="Humidity and temperature",
            background='#AED830',
            font=('sans-serif',15),
            width= 64,borderwidth=0,

        )
        self.tpcolor =Label(self, background='#83A324', width='2',relief= 'raised')
        self.hmcolor= Label(self, background='#D5EC8F', width='2',relief= 'raised')
        self.titlabel.configure(padding=0,)
        self.button = Button(
            self, 
            text="Refresh data", font=(("sans-serif"),10),activebackground='#CCE581',bg='#88A631',relief="flat"
               )

        self.button['command'] = self.updat
        self.titlabel.pack(side="top")
        self.humlabel = Label(
            self, 
            text="Humidity", font=(("sans-serif"),10),bg='#AED830',width=7
        )
        self.temlabel= Label(

            self,
            text="Temperature", font=(("sans-serif"),10),bg='#AED830', width=8

        )
       
        self.humlabel.pack(side='left')
        self.hmcolor.pack(side='left')
        self.temlabel.pack(side='left')
        self.tpcolor.pack(side='left')
        self.button.pack(side='right')
        plt.grid(True)
    #   plt.ylabel('Rate')
        self.old = 0
        self.updat()
        
    
    def new_data(self):


        self.after(2000, self.new_data)
        self.time = time.perf_counter()
        if self.time - self.old >= 120:
            self.old= self.time
            self.updat()

    def updat (self):
        #self.after(2000)
        
        self.time_size = time.localtime()
        print("fvdsz")
        self.humidity.append(cloud.cloudhum())
        self.temperature.append(cloud.cloudtep())
        self.time_local.append(f'{self.time_size[3]}:{int(((self.time_size[4])/10)-(((self.time_size[4])%10)/10))}{(self.time_size[4])%10}')
        
        if len(self.temperature) >= 8 and self.time_local[len(self.time_local)-1] == self.time_local[len(self.time_local)-2]:
            print(len(self.temperature))
            self.temperature.pop(0)
            self.humidity.pop(0) 
            self.time_local.pop(0)
        plt.axis((self.time_local[0],self.time_local[len(self.time_local)-1],0,100))
        plt.plot(self.time_local,self.humidity,'#D5EC8F')
        plt.plot(self.time_local,self.temperature,'#83A324')
        #self.canvas.get_tk_widget().destroy()
        #plt.plot().clear
        self.after(100,self.new_data())
        cloud.value= []
        #self.canvas.get_tk_widget().destroy()
        #self.canvas.get_tk_widget().pack( side="bottom", expand=True)
        self.canvas.draw()
        
        






if __name__ == '__main__':
    app = App()
    app.mainloop()