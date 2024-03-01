from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import filedialog

# root=Tk()
# root.title("Desktop Notifier")
# root.config(bg="MediumPurple1")
# root.geometry("400x200")
# root.minsize(400,200)
# root.maxsize(400,200)

# #Creating a blank textbox
# blabel1=Label(root,bg="MediumPurple1")
# blabel1.pack()

# blabel=Label(root,text="Click  \"LOGIN\"  to continue...",bg="MediumPurple1",fg="white",font="arial 20 bold",width=28,relief=RIDGE)
# blabel.pack()

# blabel2=Label(root,bg="MediumPurple1")
# blabel2.pack()

# blabel3=Label(root,bg="MediumPurple1")
# blabel3.pack()


# #Creating a button to Register
# b1=Button(root,text="Login",relief="groove",font=("arial",16,"bold"),height=1,command=lambda:[])
# b1.pack()
# root.mainloop()

# email_address = "abc@gmail.com"

# # Split the email address at the "@" symbol
# username = email_address.split('@')[0]

# print("Username:", username)



rootk=Tk()
rootk.title("Desktop Notifier")
rootk.config(bg="MediumPurple1")
rootk.geometry("500x220")
rootk.minsize(500,220)
rootk.maxsize(500,220)

#Creating a blank textbox
blabel1=Label(rootk,bg="MediumPurple1")
blabel1.pack()
blabel=Label(rootk,text="     Login Successfully     ",bg="MediumPurple1",fg="white",font="arial 20 bold",width=28,relief=RIDGE)
blabel.pack()
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



blabel=Button(rootk,text="Proceed",bg="white",fg="MediumPurple1",font="arial 18 bold",width=30,relief=GROOVE)
blabel.place(x=18,y=110)

rootk.mainloop()