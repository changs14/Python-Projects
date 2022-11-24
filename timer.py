"""########################## TIMER APP ##########################"""
"""This program will simulate a countdown timer app. Users will be able to set the time
    to countdown from as well as showing current time 24hr. 
"""

from tkinter import *
import time
from playsound import playsound

############################################ FUNCTIONS #############################################
#Create function that displays the current time in 24hr clock
def clock():
    clock_time = time.strftime('%H: %M: $S %p')
    curr_time.config(text = clock_time)
    curr_time.after(1000, clock)

#Create a function to start the timer
def countdown():
    times = int(hrs.get())*3600 +int(mins.get())*60 + int(sec.get())
    
    while times > -1:
        minute, second = (times//60), (times % 60)
        hour = 0

        if minute > 60:
            hour, minute = (minute//60), (minute%60)

        seconds.set(second)
        minutes.set(minute)
        hours.set(hour)

        root.update()
        time.sleep(1)

        if(times == 0): 
            playsound('Loud_Alarm_Clock_Buzzer.mp3')
            seconds.set('00')
            minutes.set('00')
            hours.set('00')

        times -= 1

################################################################################################################

#Display window settings
root = Tk()                                      #Init the window
root.geometry('400x350')                         #Set height and width
root.config(bg = 'blanched almond')              #Background colour
root.title('Timer For My Lazy Ass')              #Title of app
Label(root, text = 'Countdown Clock and Timer', font = 'lithograph 20 bold', bg = 'papaya whip').pack()

curr_time = Label(root, font='lithograph 20 bold', text = '', fg = 'gray25', bg = 'papaya whip')
curr_time.place(x = 190, y = 70)
clock()

#Display input text field for user time
#Display seconds
seconds = StringVar()
Entry(root, textvariable = seconds, width = 2, font = 'lithograph 20').place(x=250, y=155)
seconds.set('00')

#Display minutes
minutes = StringVar()
Entry(root, textvariable = minutes, width = 2, font = 'lithograph 20').place(x=225, y=155)
minutes.set('00')

#Display hours
hours = StringVar()
Entry(root, textvariable = hours, width = 2, font = 'lithograph 20').place(x=2, y=155)
hours.set('00')

#Create start button
Label(root, font='lithograph 15 bold', text = 'Set Time', bg = 'papaya whip').place(x = 40 ,y = 150)
Button(root, text = 'START', bd = '5', command = countdown, bg = 'antique white', font = 'lithograph 10 bold').place(x=150, y=210)

#Run application
root.mainloop()