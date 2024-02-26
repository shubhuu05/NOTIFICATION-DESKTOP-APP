# 26-02-24
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import filedialog
import pygame
from plyer import notification
from PIL import Image, ImageTk
import time
import threading
import schedule
import mysql.connector as m # python -m pip install mysql-connector-python
import os
import math
import random
import smtplib
import sqlite3

DATABASE_FILE = 'Notification.db'
TABLE_NAME = 'Notification'

#To create a database The_Student
con1=sqlite3.connect(DATABASE_FILE)
cur_db=con1.cursor()
cur_db.execute(f"create table if not exists {TABLE_NAME} (name varchar(50), passwd varchar(50), mobile varchar(10), email varchar(50));")
con1.commit()



def app_window():
    # Functions for the Use
    def handle_notification(title, message, delay, icon_path=None):
        sound_path = custom_sound_path.get()

        def show_notification():
            notification.notify(
                title=title,
                message=message,
                app_name="Notifier",
                app_icon=icon_path,
                timeout=custom_duration.get()
            )

            # Play the selected sound
            if sound_path:
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()

        t.after(delay * 1000, show_notification)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        notification_history_data.append((timestamp, title, message))
        update_history_table()


    def handle_recurring_notification(title, message, icon_path, interval):
        def job():
            notification.notify(
                title=title,
                message=message,
                app_name="Notifier",
                app_icon=icon_path,
                toast=True,
                timeout=custom_duration.get()
            )

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            notification_history_data.append((timestamp, title, message))
            update_history_table()

        if interval == "daily":
            schedule.every().day.at("09:00").do(job)
        elif interval == "weekly":
            schedule.every().monday.at("09:00").do(job)

    def update_history_table():
        for i in history_table.get_children():
            history_table.delete(i)

        for item in notification_history_data:
            history_table.insert("", "end", values=item)

    def select_custom_sound():
        file_path = filedialog.askopenfilename(filetypes=[("Sound files", "*.wav;*.mp3;*.m4a")])
        custom_sound_path.set(file_path)

    # get details and setup notification
    def get_details():
        get_title = title.get()
        get_msg = msg1.get()
        get_time = time1.get()

        if get_title == "" or get_msg == "" or get_time == "":
            msg.showerror("Alert", "All fields are required!")
        else:
            int_time = int(float(get_time))
            min_to_sec = int_time * 60

            threading.Thread(target=handle_notification, args=(get_title, get_msg, min_to_sec)).start()
            msg.showinfo("Notifier set", "Notification will be shown in {} minutes".format(get_time))

    pygame.mixer.init()
    t = Tk()
    t.title('Notifier')

    # Calculate the center coordinates
    screen_width = t.winfo_screenwidth()
    screen_height = t.winfo_screenheight()

    window_width = 650  # Adjust the width of the window as needed
    window_height = 650  # Adjust the height of the window as needed

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2


    t.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # t.minsize(700,700)
    # t.maxsize(700,700)



    #Image 
    img = Image.open(r"C:\Users\ABHISHEK YEWALE\Downloads\NOTIFICATION-DESKTOP-APP\notify-label.png")
    tkimage = ImageTk.PhotoImage(img)
    img_label = Label(t, image=tkimage)
    img_label.grid()

    notification_history_data = []
    custom_sound_path = StringVar(value="")
    custom_duration = IntVar(value=10)



    #Controls 1
    # Label - Title
    t_label = Label(t, text="Title to Notify", font=("poppins", 10))
    t_label.place(x=20, y=70)

    # ENTRY - Title
    title = Entry(t, width="25", font=("poppins", 13))
    title.place(x=130, y=70)

    # Label - Message
    m_label = Label(t, text="Display Message", font=("poppins", 10))
    m_label.place(x=20, y=120)

    # ENTRY - Message
    msg1 = Entry(t, width="40", font=("poppins", 13))
    msg1.place(x=130, height=30, y=120)

    # Label - Time
    time_label = Label(t, text="Set Time", font=("poppins", 10))
    time_label.place(x=20, y=175)

    # ENTRY - Time
    time1 = Entry(t, width="5", font=("poppins", 13))
    time1.place(x=130, y=175)

    # Label - min
    time_min_label = Label(t, text="min", font=("poppins", 10))
    time_min_label.place(x=180, y=180)

    but = Button(t, text="SET NOTIFICATION", font=("poppins", 10, "bold"), fg="#ffffff", bg="#528DFF", width=20,
                relief="raised",
                command=get_details,
                )
    but.place(x=170, y=320)



    #Controls 2
    # Label - Custom Sound
    custom_sound_label = Label(t, text="Custom Sound File", font=("poppins", 10))
    custom_sound_label.place(x=20, y=250)

    # Entry - Custom Sound
    custom_sound_entry = Entry(t, textvariable=custom_sound_path, width=50, state="readonly")
    custom_sound_entry.place(x=150, y=250)

    # Button - Select Custom Sound
    select_sound_button = Button(t, text="Select", command=select_custom_sound)
    select_sound_button.place(x=500, y=245)

    # Label - Custom Duration
    custom_duration_label = Label(t, text="Custom Notification Duration (seconds)", font=("poppins", 10))
    custom_duration_label.place(x=20, y=280)

    # Entry - Custom Duration
    custom_duration_entry = Entry(t, textvariable=custom_duration, width=5)
    custom_duration_entry.place(x=300, y=280)



    #Controls 3
    # Add a table for notification history
    history_table = ttk.Treeview(t, columns=("Timestamp", "Title", "Message"), show="headings", height=10)
    history_table.heading("Timestamp", text="Timestamp")
    history_table.heading("Title", text="Title")
    history_table.heading("Message", text="Message")
    history_table.place(x=20, y=400)

    # Add a scrollbar for the history table
    scrollbar = ttk.Scrollbar(t, orient="vertical", command=history_table.yview)
    scrollbar.place(x=623, y=400, height=225)
    history_table.configure(yscrollcommand=scrollbar.set)


    t.resizable(0,0)
    t.mainloop()





def register_window():
    root=Tk()
    root.title("Notifier")
    root.config(bg="Purple")
    root.geometry("500x500")
    root.minsize(500,500)
    root.maxsize(500,500)



    #To destroy the window
    def destry():
        root.destroy()

    #Functions related to Register Button
    def chck_pass():
        if(e1.get()=="" or e2.get()=="" or e3.get()=="" or e4.get()=="" or e5.get()==""):
            blabel.config(text="Please enter all the required details for registeration!")
        else:
            if((e2.get())==(e3.get())):
                e3.config(fg="black")
                blabel.config(text="")
                register_DB()    
            else:
                e3.config(fg="red")
                blabel.config(text="Password does not match !")


                
    #Creating Funtion of Clear button
    def clr():
        e1.delete(first=0,last=300)
        e2.delete(first=0,last=300)
        e3.delete(first=0,last=300)
        e4.delete(first=0,last=300)
        e5.delete(first=0,last=300)
        blabel.config(text="")




    #Connection of Database
    def register_DB():
            def verify():
                if(OTP1 == E2.get()):
                    try:
                        root1.destroy()
                        con1=sqlite3.connect(DATABASE_FILE)
                        cur_db=con1.cursor()
                        query=(f"insert into {TABLE_NAME} values('{e1.get()}','{e2.get()}',{e4.get()},'{e5.get()}')")
                        cur_db.execute(query)
                        con1.commit()
                        a=msg.showinfo('Successfull Execution','User registeration successfully')
                        print(a)
                        if a=="ok":
                            clr()
                            b2.destroy()
                            b3.destroy()
                            b1.config(text="Login",font="arial 18 bold",command=lambda:[destry(),app_window()])
                            blabel.config(text="Login", font="arial 14 bold", fg="green")


                        


                    except Exception as e:
                        print(e)
                        msg.showinfo("Unsuccessfull Execution","Error occured while Registering. Please retry")
                        clr()
                else:
                    msg.showinf("Invalid OTP","Check your OTP again")
                    print("Check your OTP again")

            OTP1=str(random.randint(1000,9999))
            
            s=smtplib.SMTP_SSL("smtp.gmail.com",465)
            s.login('shubhuu5171@gmail.com',"gzstnwbzcfevtjea")
            send_to=e5.get()
            msgg=f"The OPT for Student registeration is {OTP1} \n\nThanks for choosing us."
            s.sendmail('shubhuu5171@gmail.com',send_to,msgg)

            root1=Tk()
            root1.geometry("400x100")
            root1.title("OTP Verification")
            root1.config(background="LightBlue")
            l1=Label(root1,text=" THE STUDENTS ",font=("Times",15,"bold"),bg="LightBlue",fg="grey",relief="ridge")
            l1.pack(pady=10)

            l2=Label(root1,text="Enter OTP:",font=('Calibri',10,'bold'),bg="salmon")
            l2.place(x=30,y=60)

            E2=Entry(root1,font=('Calibri',10,'bold'))
            E2.place(x=120,y=60)

            B2=Button(root1,text='Submit',command=verify,font=('Calibri',8,'bold'),bg="bisque",relief=GROOVE)
            B2.place(x=280,y=60)





        



        
    #Creating Name Label
    l1=Label(root,text="Enter Name",font=("arial",14,"bold"),bg="lightblue")
    l1.place(anchor=CENTER,x=85,y=130)
    #Creating Textbox of Name Label
    e1=Entry(root,width=25,font="calibri")
    e1.place(anchor=CENTER,x=350,y=130)

    #Creating Password Label
    l2=Label(root,text="Enter Password",font=("arial",14,"bold"),bg="lightblue")
    l2.place(anchor=CENTER,x=105,y=170)
    #Creating Password textbox
    e2=Entry(root,width=23,show="*",font="calbri")
    e2.place(anchor=CENTER,x=350,y=170)

    #Creating RPassword Label
    l3=Label(root,text="Re-Enter Password",font=("arial",14,"bold"),bg="lightblue")
    l3.place(anchor=CENTER,x=120,y=210)
    #Creating RPassword textbox
    e3=Entry(root,width=23,font="calbri")
    e3.place(anchor=CENTER,x=350,y=210)
             
    #Creating Mobile No Label
    l1=Label(root,text="Enter Mobile",font=("arial",14,"bold"),bg="lightblue")
    l1.place(anchor=CENTER,x=90,y=250)
    #Creating Textbox of Mobile No Label
    e4=Entry(root,width=25,font="calibri")
    e4.place(anchor=CENTER,x=350,y=250)

    #Creating Email Label
    l1=Label(root,text="Enter E-mail",font=("arial",14,"bold"),bg="lightblue")
    l1.place(anchor=CENTER,x=90,y=290)
    #Creating Textbox of Email Label
    e5=Entry(root,width=25,font="calibri")
    e5.place(anchor=CENTER,x=350,y=290)

    #Creating a blank textbox
    blabel=Label(root,text="",bg="lightblue",fg="red",font="arial 12 bold",width=40)
    blabel.place(x=55,y=330)

    #Creating a button to Register
    b1=Button(root,text="Register",relief="groove",font=("arial",13,"bold"),height=1)
    b1.place(anchor=CENTER,x=265.5,y=400)
    b1.config(command=chck_pass)
    
    #Creating a button to back
    b2=Button(root,text="Back",relief="groove",font=("arial",13,"bold"),width=6,height=1)
    b2.place(anchor=CENTER,x=167,y=450)
    b2.config(command=lambda:[destry(),app_window()])

    #Inserting a image
    image1=PhotoImage(file="logo.png")
    image1=image1.subsample(18,18)
    image_label=Label(root,text="REGISTER",font="times 12 bold",image=image1,bg="lightblue",compound=TOP)
    image_label.pack(pady=8)

    #Creating a button to clear    
    b3=Button(root,text="Clear",relief="groove",font=("arial",13,"bold"),width=6,height=1)
    b3.place(anchor=CENTER,x=360,y=450)
    b3.config(command=clr)
    
    root.mainloop()





#Point of Execution
# register_window()
register_window()