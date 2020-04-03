import xlwings as xw
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import sched, time

wbt = xw.Book('Mahinda College batting 1st.xlsm')
wss = wbt.sheets[0]
s = sched.scheduler(time.time, time.sleep)
s.enter(0.1, 1, do_something, ())
 
#master.mainloop()
  #top.mainloop()   
  
s.run()
master = Tk()

#width, height = Image.open(image.png).size

canvas = Canvas(master, width=1280, height=720)
canvas.pack()

image = ImageTk.PhotoImage(file="score720.png")
canvas.create_image(0, 0, image=image, anchor=NW)


def do_something():
      
    
    Total_Runs = wss.range('B2').value
    Overs = wss.range('C2').value
    Balls = wss.range('D2').value
    Wickets = wss.range('E2').value
    Messages1 = wss.range('M2').value
    Messages2 = wss.range('A4').value  #Maati ayyata kiyanna oona
    Batsman_1 = wss.range('Z2').value
    Runs_1 = wss.range('AA2').value
    Balls_1 = wss.range('AB2').value
    Batsman_2 = wss.range('AF2').value
    Runs_2 = wss.range('AG2').value
    Balls_2 = wss.range('AH2').value
    Bowler = wss.range('AT2').value
    Wickets_B = wss.range('AX2').value
    Runs_B = wss.range('AU2').value
    Overs_B = wss.range('AV2').value
    Balls_B = wss.range('AW2').value

    
    print(Total_Runs)
    print(Overs)
    print(Balls)
    print(Wickets)
    print(Messages1)
    print(Batsman_1)
    print(Runs_1)
    print(Balls_1)
    print(Batsman_2)
    print(Runs_2)
    print(Balls_2)
    print(Bowler)
    print(Wickets_B)
    print(Runs_B)
    print(Overs_B)
    print(Balls_B)
    s.enter(0.1, 1, do_something, ())
   # master.mainloop()
   

s.enter(0.1, 1, do_something, ())
 
#master.mainloop()
  #top.mainloop()   
  
s.run()


