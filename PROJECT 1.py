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
# import mysql.connector as m # python -m pip install mysql-connector-python
import os
import math
import random
import smtplib
import sqlite3
from tkinter import ttk  # Import themed widgets


DATABASE_FILE = 'Notification.db'
TABLE_NAME = 'Notification'
USER_email=""
#To create a database The_Student
con1=sqlite3.connect(DATABASE_FILE)
cur_db=con1.cursor()
cur_db.execute(f"create table if not exists {TABLE_NAME} (name varchar(50), passwd varchar(50), mobile varchar(10), email varchar(50),notifi varchar(200));")
con1.commit()



# Function to find the table is exist or not
def is_table_exists(table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_FILE)
    
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # Execute a query to check if the table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # If the result is not None, the table exists
    return result is not None





def app_window():

    con1=sqlite3.connect(DATABASE_FILE)
    cur_db=con1.cursor()
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {USER_email.split('@')[0]} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Title TEXT,
        Message TEXT
    );
    '''
    a=cur_db.execute(create_table_query)
    con1.commit()
    con1.close()

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

            if sound_path:
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            con1 = sqlite3.connect(DATABASE_FILE)
            cur_db = con1.cursor()
            user_table_name = USER_email.split('@')[0]
            insert_query = f'''
            INSERT INTO {user_table_name} (Timestamp, Title, Message)
            VALUES (?, ?, ?);
            '''
            cur_db.execute(insert_query, (timestamp,title, message))
            con1.commit()
            con1.close()

            update_history_table()

        t.after(delay * 1000, show_notification)


    def update_history_table():
        try:
            # Clear the existing rows in the table
            for i in history_table.get_children():
                history_table.delete(i)

            # Connect to the database
            con1 = sqlite3.connect(DATABASE_FILE)
            cur_db = con1.cursor()
            user_table_name = USER_email.split('@')[0]

            # Select all rows from the user's table
            select_query = f'''
            SELECT Timestamp, Title, Message FROM {user_table_name};'''
            cur_db.execute(select_query)
            rows = cur_db.fetchall()
            con1.close()

            # Insert the retrieved rows into the table
            for row in rows:
                history_table.insert("", "end", values=row)

            print("Table updated successfully")

        except Exception as e:
            print("Error updating history table:", e)


    def delete_hist():
        # Clear the existing rows in the table
            for i in history_table.get_children():
                history_table.delete(i)

    def delete_hist_for_sure():
        # Connect to the SQLite database
        connection = sqlite3.connect(DATABASE_FILE)
        cur_db = connection.cursor()

        # Fetch all rows from the USER_email table
        cur_db.execute(f"SELECT * FROM {USER_email.split("@")[0]}")
        rows = cur_db.fetchall()

                
        # Delete the current row
        cur_db.execute(f"DELETE FROM {USER_email.split("@")[0]} WHERE rowid=?", (rows[0]))  # Assuming the rowid is used
        connection.commit()  # Commit the deletion for each row

        # Update the history table after each deletion
        update_history_table()

        # Close the connection
        connection.close()
        

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

    # Load and display the image
    img = Image.open("notify-label.png")
    tkimage = ImageTk.PhotoImage(img)
    img_label = Label(t, image=tkimage)
    img_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
    custom_sound_path = StringVar(value="")
    custom_duration = IntVar(value=10)

    # Controls
    labels_font = ("Arial", 10)
    entry_font = ("Arial", 13)

    # Title
    t_label = Label(t, text="Title to Notify", font=labels_font)
    t_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")

    title = Entry(t, font=entry_font)
    title.grid(row=1, column=1, padx=20, pady=5, sticky="w")

    # Message
    m_label = Label(t, text="Display Message", font=labels_font)
    m_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

    msg1 = Entry(t, font=entry_font)
    msg1.grid(row=2, column=1, padx=20, pady=5, sticky="w")

    # Time
    time_label = Label(t, text="Set Time (min)", font=labels_font)
    time_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")

    time1 = Entry(t, font=entry_font, width=5)
    time1.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    # Button
    but = Button(t, text="SET NOTIFICATION", font=("Arial", 10, "bold"), fg="#ffffff", bg="#528DFF", width=20,
                relief="raised", command=get_details)
    but.grid(row=4, column=0, columnspan=2, pady=10)

    # Custom Sound
    custom_sound_label = Label(t, text="Custom Sound File", font=labels_font)
    custom_sound_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")

    custom_sound_entry = Entry(t, textvariable=custom_sound_path, font="arial 12 bold", width=40, state=DISABLED,)
    custom_sound_entry.grid(row=5, column=1, padx=20, pady=5, sticky="w")

    select_sound_button = Button(t, text="Select", command=select_custom_sound)
    select_sound_button.grid(row=5, column=2, padx=10, pady=5, sticky="w")

    # Custom Duration
    custom_duration_label = Label(t, text="Custom Notification Duration (seconds)", font=labels_font)
    custom_duration_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")

    custom_duration_entry = Entry(t, textvariable=IntVar(), font=entry_font, width=5)
    custom_duration_entry.grid(row=6, column=1, padx=20, sticky="w")

    refresh_button=Button(t,text="Refresh",command=update_history_table)
    refresh_button.grid(row=6,column=2,sticky="w")
    refresh_button=Button(t,text="Clear",command=delete_hist_for_sure)
    refresh_button.grid(row=6,column=3,sticky="w")

    # History Table
    style = ttk.Style()
    style.theme_use("clam")

    history_frame = Frame(t)
    history_frame.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

    history_table = ttk.Treeview(history_frame, columns=("Timestamp", "Title", "Message"), show="headings", height=10)
    history_table.heading("Timestamp", text="Timestamp")
    history_table.heading("Title", text="Title")
    history_table.heading("Message", text="Message")

    vsb = ttk.Scrollbar(history_frame, orient="vertical", command=history_table.yview)
    vsb.pack(side='right', fill='y')
    history_table.configure(yscrollcommand=vsb.set)

    history_table.pack(side='left', fill='both', expand=True)

    # Update the history table
    update_history_table()

    # Configure resizing behavior
    t.columnconfigure(1, weight=1)
    t.rowconfigure(7, weight=1)

    # Start the main loop
    t.mainloop()


def register_window():
    root=Tk()
    root.title("Notifier")
    root.config(bg="MediumPurple1")
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
                email=e5.get()
                if is_table_exists(email.split('@')[0]):
                    clr()
                    a=msg.askyesno("Email ID already exist","If you wish to Login to the entered email\nClick \"OK\"")
                    print(a)

                    if a==True:
                        print(email)
                        root.destroy()

                        #TO check the entered password is right or wrong
                        def chck_cred():
                            con1=sqlite3.connect(DATABASE_FILE)
                            cur_db=con1.cursor()
                            cur_db.execute(f'select passwd from {TABLE_NAME} where email="{email}"')
                            a=cur_db.fetchone()
                            con1.commit()

                            print(a[0])

                            if a[0]==er2.get():
                                global USER_email
                                USER_email=email
                                msg.showinfo('Login Successfully','You have entered valid credentials')
                                lr1.destroy()
                                er1.destroy()
                                lr2.destroy()
                                er2.destroy()
                                blank_label.config(text="     Login Successfully     ")
                                login_button.config(text="Proceed",width=30,bg="white",fg="MediumPurple1",font="arial 18 bold",height=1,command=lambda:[rootk.destroy(),app_window()])
                                login_button.place(x=18,y=110)

                            else:
                                msg.showwarning("Invalid Password","You have entered the wrong password.\nTry Again")
                        rootk=Tk()
                        rootk.title("Desktop Notifier")
                        rootk.config(bg="MediumPurple1")
                        rootk.geometry("500x220")
                        rootk.minsize(500,220)
                        rootk.maxsize(500,220)

                        #Creating a blank textbox
                        blabel1=Label(rootk,bg="MediumPurple1")
                        blabel1.pack()
                        blank_label=Label(rootk,text="Please enter your Login Credentials",bg="MediumPurple1",fg="white",font="arial 20 bold",width=28,relief=RIDGE)
                        blank_label.pack()
                        blabel2=Label(rootk,bg="MediumPurple1")
                        blabel2.pack()
                        blabel3=Label(rootk,bg="MediumPurple1")
                        blabel3.pack()
                        blabel3=Label(rootk,bg="MediumPurple1")
                        blabel3.pack()
                        blabel3=Label(rootk,bg="MediumPurple1")
                        blabel3.pack()
                        blabel3=Label(rootk,bg="MediumPurple1")
                        blabel3.pack()
                        blabel3=Label(rootk,bg="MediumPurple1")
                        blabel3.pack()

                        #Creating Lable of Email
                        lr1=Label(rootk,text="Email ",relief=GROOVE,font=("arial",14,"bold"),bg="MediumPurple1")
                        lr1.place(anchor=CENTER,x=57,y=100)
                        #Creating Textbox of Email
                        er1=Label(rootk,width=25,text=email,font="calibri",fg="white",bg="MediumPurple1",justify=LEFT,anchor=W,relief="groove")
                        er1.place(anchor=CENTER,x=325,y=100)

                        #Creating Password Label
                        lr2=Label(rootk,text="Enter Password ",relief=GROOVE,font=("arial",14,"bold"),bg="MediumPurple1")
                        lr2.place(anchor=CENTER,x=105,y=140)
                        #Creating Password textbox
                        er2=Entry(rootk,width=23,show="*",font="calbri")
                        er2.place(anchor=CENTER,x=325,y=140)

                        login_button=Button(rootk,text="Login",bg="white",fg="MediumPurple1",font="arial 12 bold",height=20,width=50,relief=GROOVE)
                        login_button.pack(anchor=CENTER)
                        login_button.config(command=chck_cred)
                        
                        rootk.mainloop()
                else:
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
                        user_email=e5.get()
                        query=(f"insert into {TABLE_NAME} values('{e1.get()}','{e2.get()}',{e4.get()},'{e5.get()}','NA')")
                        cur_db.execute(query)
                        con1.commit()
                        con1.close()
                        a=msg.showinfo('Successfull Execution','User registeration successfully')
                        print(a)
                        if a=="ok":
                            clr()
                            global USER_email
                            USER_email=user_email
                            root.destroy()

                            rootk=Tk()
                            rootk.title("Desktop Notifier")
                            rootk.config(bg="MediumPurple1")
                            rootk.geometry("400x200")
                            rootk.minsize(400,200)
                            rootk.maxsize(400,200)

                            #Creating a blank textbox
                            blabel1=Label(rootk,bg="MediumPurple1")
                            blabel1.pack()

                            blabel=Label(rootk,text="Click  \"LOGIN\"  to continue...",bg="MediumPurple1",fg="white",font="arial 20 bold",width=28,relief=RIDGE)
                            blabel.pack()

                            blabel2=Label(rootk,bg="MediumPurple1")
                            blabel2.pack()

                            blabel3=Label(rootk,bg="MediumPurple1")
                            blabel3.pack()


                            #Creating a button to Register
                            b1=Button(rootk,text="Login",relief="groove",font=("arial",16,"bold"),height=1,command=lambda:[rootk.destroy(),app_window()])
                            b1.pack()
                            rootk.mainloop()


                        
                    except Exception as e:
                        print(e)
                        msg.showinfo("Unsuccessfull Execution","Error occured while Registering. Please retry")
                        clr()
                else:
                    msg.showinfo("Invalid OTP","Check your OTP again")
                    print("Check your OTP again")

            OTP1=str(random.randint(1000,9999))
            
            s=smtplib.SMTP_SSL("smtp.gmail.com",465)
            s.login('shubhuu5171@gmail.com',"gzstnwbzcfevtjea")
            send_to=e5.get()
            msgg=f"The OTP for User registeration is {OTP1} \n\nThanks for choosing us."
            s.sendmail('shubhuu5171@gmail.com',send_to,msgg)

            root1=Tk()
            root1.geometry("400x100")
            root1.title("OTP Verification")
            root1.config(background="MediumPurple1")
            l1=Label(root1,text=" Notifier ",font=("Times",15,"bold"),bg="MediumPurple1",fg="white",relief="ridge")
            l1.pack(pady=10)

            l2=Label(root1,text="Enter OTP:",font=('Calibri',10,'bold'),bg="salmon")
            l2.place(x=30,y=60)

            E2=Entry(root1,font=('Calibri',10,'bold'))
            E2.place(x=120,y=60)

            B2=Button(root1,text='Submit',command=verify,font=('Calibri',8,'bold'),bg="bisque",relief=GROOVE)
            B2.place(x=280,y=60)
    #Creating Name Label
    l1=Label(root,text="Enter Name",font=("arial",14,"bold"),bg="MediumPurple1")
    l1.place(anchor=CENTER,x=85,y=130)
    #Creating Textbox of Name Label
    e1=Entry(root,width=25,font="calibri")
    e1.place(anchor=CENTER,x=350,y=130)

    #Creating Password Label
    l2=Label(root,text="Enter Password",font=("arial",14,"bold"),bg="MediumPurple1")
    l2.place(anchor=CENTER,x=105,y=170)
    #Creating Password textbox
    e2=Entry(root,width=23,show="*",font="calbri")
    e2.place(anchor=CENTER,x=350,y=170)

    #Creating RPassword Label
    l3=Label(root,text="Re-Enter Password",font=("arial",14,"bold"),bg="MediumPurple1")
    l3.place(anchor=CENTER,x=120,y=210)
    #Creating RPassword textbox
    e3=Entry(root,width=23,font="calbri")
    e3.place(anchor=CENTER,x=350,y=210)
             
    #Creating Mobile No Label
    l4=Label(root,text="Enter Mobile",font=("arial",14,"bold"),bg="MediumPurple1")
    l4.place(anchor=CENTER,x=90,y=250)
    #Creating Textbox of Mobile No Label
    e4=Entry(root,width=25,font="calibri")
    e4.place(anchor=CENTER,x=350,y=250)

    #Creating Email Label
    l5=Label(root,text="Enter E-mail",font=("arial",14,"bold"),bg="MediumPurple1")
    l5.place(anchor=CENTER,x=90,y=290)
    #Creating Textbox of Email Label
    e5=Entry(root,width=25,font="calibri")
    e5.place(anchor=CENTER,x=350,y=290)

    #Creating a blank textbox
    blabel=Label(root,text="",bg="MediumPurple1",fg="red",font="arial 12 bold",width=40)
    blabel.place(x=55,y=330)

    #Creating a button to Register
    b1=Button(root,text="Register",relief="groove",font=("arial",13,"bold"),height=1)
    b1.place(anchor=CENTER,x=265.5,y=400)
    b1.config(command=chck_pass)
    
    #Creating a button to back
    b2=Button(root,text="Back",relief="groove",font=("arial",13,"bold"),width=6,height=1)
    b2.place(anchor=CENTER,x=167,y=450)
    b2.config(command=lambda:[destry(),main_window()])

    #Inserting a image
    image1=PhotoImage(file="logo.png")
    image1=image1.subsample(18,18)
    image_label=Label(root,text="REGISTER",font="times 12 bold",image=image1,bg="MediumPurple1",compound=TOP)
    image_label.pack(pady=8)

    #Creating a button to clear    
    b3=Button(root,text="Clear",relief="groove",font=("arial",13,"bold"),width=6,height=1)
    b3.place(anchor=CENTER,x=360,y=450)
    b3.config(command=clr)
    
    root.mainloop()




def login_window():
    def chck_cred():
        email=er1.get()
        if is_table_exists(email.split("@")[0]):
            con1=sqlite3.connect(DATABASE_FILE)
            cur_db=con1.cursor()
            cur_db.execute(f'select passwd from {TABLE_NAME} where email="{email}"')
            a=cur_db.fetchone()
            con1.commit()

            print(a[0])

            if a[0]==er2.get():
                global USER_email
                USER_email=email
                msg.showinfo('Login Successfully','You have entered valid credentials')
                lr1.destroy()
                er1.destroy()
                lr2.destroy()
                er2.destroy()
                blank_label.config(text="     Login Successfully     ")
                login_button.config(text="Proceed",width=30,bg="white",fg="MediumPurple1",font="arial 18 bold",height=1,command=lambda:[rootk.destroy(),app_window()])
                login_button.place(x=18,y=110)

            else:
                msg.showwarning("Invalid Password","You have entered the wrong password.\nTry Again")
        
        else:
            msg.showerror("Invalid Email ID", "The entered Email ID in not registered.\nKindly register yourself first.")

        

    rootk=Tk()
    rootk.title("Desktop Notifier")
    rootk.config(bg="MediumPurple1")
    rootk.geometry("500x220")
    rootk.minsize(500,220)
    rootk.maxsize(500,220)

    #Creating a blank textbox
    blabel1=Label(rootk,bg="MediumPurple1")
    blabel1.pack()
    blank_label=Label(rootk,text="Please enter your Login Credentials",bg="MediumPurple1",fg="white",font="arial 20 bold",width=28,relief=RIDGE)
    blank_label.pack()
    blabel2=Label(rootk,bg="MediumPurple1")
    blabel2.pack()
    blabel3=Label(rootk,bg="MediumPurple1")
    blabel3.pack()
    blabel3=Label(rootk,bg="MediumPurple1")
    blabel3.pack()
    blabel3=Label(rootk,bg="MediumPurple1")
    blabel3.pack()
    blabel3=Label(rootk,bg="MediumPurple1")
    blabel3.pack()
    blabel3=Label(rootk,bg="MediumPurple1")
    blabel3.pack()

    #Creating Lable of Email
    lr1=Label(rootk,text="Enter Email ",relief=GROOVE,font=("arial",14,"bold"),bg="MediumPurple1")
    lr1.place(anchor=CENTER,x=85,y=100)
    #Creating Textbox of Email
    er1=Entry(rootk,width=26,font="calibri")
    er1.place(anchor=CENTER,x=328,y=100)

    #Creating Password Label
    lr2=Label(rootk,text="Enter Password ",relief=GROOVE,font=("arial",14,"bold"),bg="MediumPurple1")
    lr2.place(anchor=CENTER,x=105,y=140)
    #Creating Password textbox
    er2=Entry(rootk,width=24,show="*",font="calbri")
    er2.place(anchor=CENTER,x=328,y=140)

    login_button=Button(rootk,text="Login",bg="white",fg="MediumPurple1",font="arial 12 bold",height=20,width=50,relief=GROOVE)
    login_button.pack(anchor=CENTER)
    login_button.config(command=chck_cred)
    
    rootk.mainloop()



def main_window():
    #Creating the application window ( " The Students " )
    win1=Tk()
    win1.title("Notifier")
    win1.config(bg="MediumPurple1")

    screen_width = win1.winfo_screenwidth()
    screen_height = win1.winfo_screenheight()
    x_dim=(screen_width-500)//2
    y_dim=(screen_height-350)//2
    
    win1.geometry(f"500x280+{x_dim}+{y_dim}")
    win1.minsize(500,280)
    win1.maxsize(500,280)
    
    #To destroy the window
    def destry():
        win1.destroy()

    def manager_login_window():
        
        # Function to handle the login process
        def validate_login():
            username = entry_username.get()
            password = entry_password.get()

            # Add your authentication logic here
            # For simplicity, let's assume a hardcoded username and password
            if authenticate(username, password):
                msg.showinfo("Login Successful", "Welcome, Manager!")
                manager_login_win.destroy()  # Close the manager login window after successful login
                # You can add more functionality here after successful login

                def fetch_emails():
                    # Connect to your SQLite database
                    conn = sqlite3.connect(DATABASE_FILE)
                    cursor = conn.cursor()

                    # Fetch emails from the "notification" table
                    cursor.execute(f"SELECT email FROM {TABLE_NAME}")
                    emails = cursor.fetchall()

                    # Close the connection
                    conn.close()

                    # Extract emails from the result
                    emails_list = ["Select User"]  # Adding "Select User" as the default option
                    emails_list.extend([email[0] for email in emails])

                    return emails_list


                def send_notification():
                    selected_email_value = selected_email.get()
                    notification_subject = "Manger Notification"  # Get the subject from the entry field
                    notification_message = notification_text.get("1.0", "end-1c")  # Get the text from the text box

                    # SMTP Configuration
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587  # TLS Port
                    smtp_username = "shubhuu5171@gmail.com"  # Update with your email
                    smtp_password = "gzstnwbzcfevtjea"  # Update with your password

                    # Create SMTP connection
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_username, smtp_password)

                        # Construct and send the email
                        email_message = f"Subject: {notification_subject}\n\n"
                        email_message += f"Dear Employee,\n\n{notification_message}\n\nBest Regards,\nShubham Navale\n(CEO)"
                        server.sendmail(smtp_username, selected_email_value, email_message)


                # def send_notification():
                #     selected_email_value = selected_email.get()
                #     notification_message = notification_text.get("1.0", "end-1c")  # Get the text from the text box

                #     s=smtplib.SMTP_SSL("smtp.gmail.com",465)
                #     s.login('shubhuu5171@gmail.com',"gzstnwbzcfevtjea")
                #     msgg=f"There is a notification from Shubham Navale (Manager):\n{notification_message}"
                #     s.sendmail('shubhuu5171@gmail.com',selected_email_value,msgg)

                win1 = Tk()
                win1.title("Notifier")
                win1.config(bg="MediumPurple1")

                screen_width = win1.winfo_screenwidth()
                screen_height = win1.winfo_screenheight()
                x_dim = (screen_width - 500) // 2
                y_dim = (screen_height - 350) // 2

                win1.geometry(f"500x350+{x_dim}+{y_dim}")
                win1.minsize(500, 350)
                win1.maxsize(500, 350)

                # Label for the Title
                l1 = Label(win1, text=" Notifier ", font=("Times", 30, "bold"), bg="MediumPurple1", fg="white", relief="ridge")
                l1.pack(pady=20)

                # Dropdown list for emails
                emails = fetch_emails()
                selected_email = StringVar(win1)
                selected_email.set(emails[0])  # Set default value
                email_dropdown = OptionMenu(win1, selected_email, *emails)
                email_dropdown.pack(pady=10)

                # Text box for notification message
                notification_text = Text(win1, height=6, width=40)
                notification_text.pack(pady=10)

                # Send Notification Button
                b2 = Button(win1, text="Send Notification", relief="groove", font=("arial", 10, "bold"), bg="Salmon", width=30, command=send_notification)
                b2.pack(pady=10)

                # Blank Label
                lblank1 = Label(win1, bg="MediumPurple1")
                lblank1.pack()

                win1.mainloop()

            else:
                msg.showerror("Login Failed", "Invalid username or password")

        # Authentication logic (replace this with your actual logic)
        def authenticate(username, password):
            return username == "admin" and password == "admin123"


        manager_login_win = Tk()
        manager_login_win.title("Manager Login")
        manager_login_win.geometry("400x200")
        manager_login_win.configure(bg='#333')

        # Add a logo (replace 'notify-label.png' with your actual image file)
        original_logo = PhotoImage(file='notify-label.png')

        # Resize the logo to fit the window
        window_width = 400
        window_height = 200
        resized_logo = original_logo.subsample(int(original_logo.width() / window_width), int(original_logo.height() / window_height))

        logo_label = ttk.Label(manager_login_win, image=resized_logo, background='#333')
        logo_label.grid(row=0, column=0, columnspan=2)

        # Create a frame for login details
        login_frame = ttk.Frame(manager_login_win, padding=(20, 10), style='TFrame')
        login_frame.grid(row=1, column=0, columnspan=2)

        # Labels and Entry Widgets for Manager Login
        ttk.Label(login_frame, text="Username:", foreground='#fff', background='#333', font=('Helvetica', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='e')
        entry_username = ttk.Entry(login_frame, font=('Arial', 12))
        entry_username.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(login_frame, text="Password:", foreground='#fff', background='#333', font=('Helvetica', 12, 'bold')).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        entry_password = ttk.Entry(login_frame, show="*", font=('Arial', 12))
        entry_password.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Manager Login Button with custom styling
        b_login_manager = ttk.Button(manager_login_win, text="Login", command=validate_login, style='TButton.Artistic.TButton')
        b_login_manager.grid(row=2, column=0, columnspan=2, pady=20)

        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#333')

        # Run the Tkinter event loop
        manager_login_win.mainloop()

        

    #Label for the Title
    l1=Label(win1,text=" Notifier ",font=("Times",30,"bold"),bg="MediumPurple1",fg="white",relief="ridge")
    l1.pack(pady=40)

    #Register Button
    b1=Button(win1,text="Register",relief="groove",font=("arial",13,"bold"),bg="LightGreen",width=15,height=1)
    b1.pack()
    b1.config(command=lambda:[destry(),register_window()])

    #Login Button
    b2=Button(win1,text="Login",relief="groove",font=("arial",13,"bold"),bg="LightBlue",width=15,height=1)
    b2.pack(pady=10)
    b2.config(command=lambda:[destry(),login_window()])

    #Manager Login Button
    b2=Button(win1,text="Manager Login",relief="groove",font=("arial",10,"bold"),bg="Salmon",width=30)
    b2.pack(pady=10)
    b2.config(command=lambda:[destry(),manager_login_window()])

    #Blank Label
    lblank1=Label(win1, bg="MediumPurple1")
    lblank1.pack()   

    win1.mainloop()



#Point of Execution
# register_window()
main_window()