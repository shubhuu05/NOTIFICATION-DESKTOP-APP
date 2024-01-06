from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import filedialog
from plyer import notification
from PIL import Image, ImageTk
import time
import threading
import schedule

t = Tk()
t.title('Notifier')
t.geometry("800x600")
img = Image.open("C:/Users/SHUBHAM NAVALE/Pictures/notify-label.png")
tkimage = ImageTk.PhotoImage(img)

# Notification history data
notification_history_data = []

# Customization options
custom_sound_path = StringVar(value="")  # Variable to store the custom sound file path
custom_duration = IntVar(value=10)  # Default duration in seconds

# Function to handle notification
def handle_notification(title, message, delay, icon_path=None):
    t.after(delay * 1000, lambda: notification.notify(
        title=title,
        message=message,
        app_name="Notifier",
        app_icon=icon_path,
        toast=True,
        timeout=custom_duration.get()
    ))

    # Add the notification to the history
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    notification_history_data.append((timestamp, title, message))

    # Update the history table
    update_history_table()

# Function to handle recurring notification
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

        # Add the notification to the history
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        notification_history_data.append((timestamp, title, message))

        # Update the history table
        update_history_table()

    # Schedule the job based on the provided interval (daily or weekly)
    if interval == "daily":
        schedule.every().day.at("09:00").do(job)  # Example: Notify daily at 9 AM
    elif interval == "weekly":
        schedule.every().monday.at("09:00").do(job)  # Example: Notify every Monday at 9 AM


# Remove the duplicate get_details function and modify the existing one
def get_details():
    get_title = title.get()
    get_msg = msg.get()
    get_time = time1.get()

    if get_title == "" or get_msg == "" or get_time == "":
        messagebox.showerror("Alert", "All fields are required!")
    else:
        int_time = int(float(get_time))
        min_to_sec = int_time * 60

        if recurring_var.get() == 1:
            handle_recurring_notification(get_title, get_msg, icon_path, recurring_interval.get())
            messagebox.showinfo("Recurring Notifier set",
                                f"Recurring notifications will be shown {recurring_interval.get()} at 9:00 AM")
        else:
            threading.Thread(target=handle_notification, args=(get_title, get_msg, min_to_sec, icon_path)).start()
            messagebox.showinfo("Notifier set", f"Notification will be shown in {get_time} minutes")

# Function to update the notification history table
def update_history_table():
    for i in history_table.get_children():
        history_table.delete(i)

    for item in notification_history_data:
        history_table.insert("", "end", values=item)

# Function to select a custom sound file
def select_custom_sound():
    file_path = filedialog.askopenfilename(filetypes=[("Sound files", "*.wav;*.mp3;*.m4a")])
    custom_sound_path.set(file_path)

# Rest of your Tkinter mainloop code...

# Add customization options UI
# Label - Custom Sound
custom_sound_label = Label(t, text="Custom Sound File", font=("poppins", 10))
custom_sound_label.place(x=20, y=220)

# Entry - Custom Sound
custom_sound_entry = Entry(t, textvariable=custom_sound_path, width=50, state="readonly")
custom_sound_entry.place(x=150, y=220)

# Button - Select Custom Sound
select_sound_button = Button(t, text="Select", command=select_custom_sound)
select_sound_button.place(x=600, y=215)

# Label - Custom Duration
custom_duration_label = Label(t, text="Custom Notification Duration (seconds)", font=("poppins", 10))
custom_duration_label.place(x=20, y=250)

# Entry - Custom Duration
custom_duration_entry = Entry(t, textvariable=custom_duration, width=5)
custom_duration_entry.place(x=300, y=250)

# Add a table for notification history
history_table = ttk.Treeview(t, columns=("Timestamp", "Title", "Message"), show="headings", height=10)
history_table.heading("Timestamp", text="Timestamp")
history_table.heading("Title", text="Title")
history_table.heading("Message", text="Message")
history_table.place(x=20, y=400)

# Add a scrollbar for the history table
scrollbar = ttk.Scrollbar(t, orient="vertical", command=history_table.yview)
scrollbar.place(x=770, y=400, height=200)
history_table.configure(yscrollcommand=scrollbar.set)





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

        # Using threading to handle the delay
        threading.Thread(target=handle_notification, args=(get_title, get_msg, min_to_sec)).start()
        msg.showinfo("Notifier set", "Notification will be shown in {} minutes".format(get_time))



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
msg1 = Entry(t, width="40", font=("poppins", 13))
msg1.place(x=123,height=30, y=120)

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
but.place(x=170, y=320)

t.resizable(0,0)
t.mainloop()


# Run the Tkinter main loop
t.mainloop()
