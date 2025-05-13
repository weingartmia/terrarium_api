
from tkinter import ttk, Button, Label,Frame, Listbox
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import time
import cloud 
from collections import defaultdict
import os
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 
matplotlib.use('TkAgg')




class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state('normal')
        self.maincolor= '#000000'
        self.forecolor='#FFFFFF'
        self.humidcolor='#4F4D53'
        self.tempcolor='#AE88F5'
        self.activecolor='#B1A8C2'
        self.buttoncolor='#1D1C1D'
        #self.fig =(plt.figure(figsize=(7,3), num='Terrarium data', facecolor='white'))
        self.tabs =defaultdict(Listbox)
        self.cans =defaultdict(FigureCanvasTkAgg)
        
        plt.style.use('dark_background')
        self.style= ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook', background=f'{self.maincolor}',foreground=f'{self.forecolor}')
        self.style.configure('TNotebook.Tab', background=f'{self.maincolor}',foreground=f'{self.forecolor}')
        self.style.map("TNotebook", background= [("selected", f'{self.maincolor}')],foreground=[("selected",f'{self.forecolor}')])
        self.tabsys = ttk.Notebook(self)
        self.butsys = Frame(self, width=10, background=f'{self.maincolor}',relief='flat')
        self.configure(bg=f'{self.maincolor}')
        self.attributes('-topmost',True)
        self.humidity =defaultdict(list)
        

        self.temperature=defaultdict(list)
        self.time_local=[]
        self.geometry("500x350")
        
        self.title("Terrarium data")

        self.titlabel = Label(
            self,
            text="Humidity and temperature",
            background=f'{self.buttoncolor}',
            foreground=f'{self.forecolor}',
            font=('sans-serif',15),
            width= 64,borderwidth=0,

        )
        self.tpcolor =Label(self.butsys, background=f'{self.tempcolor}', width=2,relief= 'raised')
        self.temlabel= Label(

            self.butsys,text="Temperature", font=(("sans-serif"),10),
        bg=f'{self.maincolor}',foreground=f'{self.forecolor}', width=9

        )
        self.hmcolor= Label(self.butsys, background=f'{self.humidcolor}', width=2,relief= 'raised')
        

        self.humlabel = Label(
            self.butsys, 
             text="Humidity", foreground=f'{self.forecolor}',font=(("sans-serif"),10),bg=f'{self.maincolor}',width=7
         )
        self.button = Button( 
            self.butsys, 
            text="Refresh data", font=(("sans-serif"),10),activebackground=f'{self.activecolor}',bg=f'{self.maincolor}', foreground=f'{self.forecolor}',relief="sunken", command=self.updat
               )
        self.but2 = Button( 
            self.butsys, 
            text="Last values", font=(("sans-serif"),10),activebackground=f'{self.activecolor}',bg=f'{self.maincolor}',foreground=f'{self.forecolor}',relief="sunken", command=self.fbut2
               )
        self.but3 = Button( 
            self.butsys, 
            text="Older values", font=(("sans-serif"),10),activebackground=f'{self.activecolor}',bg=f'{self.maincolor}',foreground=f'{self.forecolor}',relief="sunken", command=self.fbut3
               )



        self.titlabel.pack()
        

        for cloud.thing in cloud.things:
                
                self.tabs[f'{cloud.thing.name}'] = Listbox(self.tabsys)
                self.tabsys.add(self.tabs[f'{cloud.thing.name}'], text =f'{cloud.thing.name}')
                
    
                
        self.button.pack(side='left')
        self.but2.pack(side='left')
        self.but3.pack(side='left')
        self.humlabel.pack(expand=True,side='left')
        self.hmcolor.pack(expand=True,side='left')
        self.temlabel.pack(expand=True,side='left')
        self.tpcolor.pack(expand=True,side='left')
        
        self.butsys.pack(side='top')
        
        
        
        self.switch =False
        self.old = 0
        self.updat()
    
    def fbut2(self):
        print(self.switch)
        if self.switch== False:
            self.switch=True
        self.updat()
    def fbut3(self):
         print(self.switch)
         if self.switch ==True:
              self.switch=False
         self.updat()
         
    def new_data(self):


        self.after(2000, self.new_data)
        self.time = time.perf_counter()
        if self.time - self.old >= 600:
            self.old= self.time
            self.updat()

    def updat (self):
       
        
        self.time_size = time.localtime()
       
        
        cloud.get_things_and_props()  
        self.tabbing()   
        self.new_data()
    def tabbing(self):

        self.num=0
        self.time_local.append(f'{self.time_size[3]}:{int(((self.time_size[4])-((self.time_size[4])%10))/10)}{(self.time_size[4])%10}')
        
        
        for cloud.thing in cloud.things:
                print(cloud.value)

                self.fig, self.plots = plt.subplots()
                self.tabsys.forget(self.tabs[f'{cloud.thing.name}'])
                self.x = 0
                self.val = cloud.value[f'{cloud.thing.name}'][self.x]

                self.humidity[f'{cloud.thing.name}'].append(self.val)
                self.x = self.x + 1

                self.val = cloud.value[f'{cloud.thing.name}'][self.x]
                self.temperature[f'{cloud.thing.name}'].append(self.val)
                self.tabs[f'{cloud.thing.name}'] = Listbox(self.tabsys)
                self.tabsys.add(self.tabs[f'{cloud.thing.name}'], text =f'{cloud.thing.name}')
                
                self.cans[f'{cloud.thing.name}'] = FigureCanvasTkAgg(self.fig, 
                               master = self.tabs[f'{cloud.thing.name}'])

                self.canv =self.cans[f'{cloud.thing.name}']
            

               
                self.plots.grid(True)
                if self.switch==True and len(self.time_local)>7:

                        self.plots.plot(self.time_local[-8:],self.humidity[f'{cloud.thing.name}'][-8:],f'{self.humidcolor}')
                        self.plots.plot(self.time_local[-8:],self.temperature[f'{cloud.thing.name}'][-8:],f'{self.tempcolor}')
                        self.plots.set_ylim(ymin=0, ymax=100)
                else:

                    xmin=self.time_local[0]
                    xmax=self.time_local[len(self.time_local)-1]
                    self.plots.axis([xmin,xmax,0,100])
                    self.plots.plot(self.time_local,self.humidity[f'{cloud.thing.name}'],f'{self.humidcolor}')
                    self.plots.plot(self.time_local,self.temperature[f'{cloud.thing.name}'],f'{self.tempcolor}')

                plt.tight_layout()
                self.canv.get_tk_widget().pack(side='bottom')
                
                self.drw()
        self.tabsys.pack(expand=True, side='bottom', fill='none')
    def drw(self):
        self.after(1, self.wtime())
        self.canv.draw()
   
    def wtime(self):
         print(self.cans[f'{cloud.thing.name}'])
         self.after(5, self.tabpack())
         


    def tabpack (self):
        
        cloud.value[f'{cloud.thing.name}'] =[]
        
         
           




if __name__ == '__main__':
    app = App()
    app.mainloop()