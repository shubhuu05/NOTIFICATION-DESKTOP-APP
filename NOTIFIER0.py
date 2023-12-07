from tkinter import *
from plyer import notification
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import threading

t = Tk()
t.title('Notifier')
t.geometry("500x300")
img = Image.open("C:/Users/SHUBHAM NAVALE/Pictures/notify-label.png")
tkimage = ImageTk.PhotoImage(img)

# Function to handle notification
def handle_notification(title, message, delay):
    t.after(delay * 1000, lambda: notification.notify(
        title=title,
        message=message,
        app_name="Notifier",
        app_icon=r"C:\Users\SHUBHAM NAVALE\Downloads\Notifier-Desktop-app-master\Notifier-Desktop-app-master\ico.ico",
        toast=True,
        timeout=1000000
    ))

# get details and setup notification
def get_details():
    get_title = title.get()
    get_msg = msg.get()
    get_time = time1.get()

    if get_title == "" or get_msg == "" or get_time == "":
        messagebox.showerror("Alert", "All fields are required!")
    else:
        int_time = int(float(get_time))
        min_to_sec = int_time * 60

        # Using threading to handle the delay
        threading.Thread(target=handle_notification, args=(get_title, get_msg, min_to_sec)).start()
        messagebox.showinfo("Notifier set", "Notification will be shown in {} minutes".format(get_time))



img_label = Label(t, image=tkimage).grid()

# Label - Title
t_label = Label(t, text="Title to Notify",font=("poppins", 10))
t_label.place(x=12, y=70)

# ENTRY - Title
title = Entry(t, width="25",font=("poppins", 13))
title.place(x=123, y=70)

# Label - Message
m_label = Label(t, text="Display Message", font=("poppins", 10))
m_label.place(x=12, y=120)

# ENTRY - Message
msg = Entry(t, width="40", font=("poppins", 13))
msg.place(x=123,height=30, y=120)

# Label - Time
time_label = Label(t, text="Set Time", font=("poppins", 10))
time_label.place(x=12, y=175)

# ENTRY - Time
time1 = Entry(t, width="5", font=("poppins", 13))
time1.place(x=123, y=175)

# Label - min
time_min_label = Label(t, text="min", font=("poppins", 10))
time_min_label.place(x=175, y=180)


but = Button(t, text="SET NOTIFICATION", font=("poppins", 10, "bold"), fg="#ffffff", bg="#528DFF", width=20,
             relief="raised",
             command=get_details)
but.place(x=170, y=230)

t.resizable(0,0)
t.mainloop()