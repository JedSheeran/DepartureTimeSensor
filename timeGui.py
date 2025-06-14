import tkinter as tk
import distanceSensor
import threading

threading.Thread(target=distanceSensor.start, daemon=True).start()

root = tk.Tk()
root.title("Departure Time Tracker")
root.configure(bg="white")
root.attributes("-fullscreen", True)
#root.geometry("400x200")

#GUI Elements
#Title Label
title_label = tk.Label(
    root, 
    text="Departure Time Tracker", 
    font=("Arial", 38, "bold"),
    fg="#dd0032",
    bg="white"
)
title_label.pack(pady=(20, 10))

# Timer and Average Time Labels
timer_label = tk.Label(
    root, 
    text="Current Car: 00:00", 
    font=("Arial", 34),
    fg="#004f71",
    bg="white"
)
timer_label.pack(pady=10)

average_time_label = tk.Label(
    root, 
    text="Average Time: 00:00", 
    font=("Arial", 28),
    fg="#004f71",
    bg="white"
)
average_time_label.pack(side="left", anchor="w", padx=20, pady=10)

# Cars Counted Label
car_count_label = tk.Label(
    root, 
    text="Cars Counted: 0", 
    font=("Arial", 28),
    fg="#004f71",
    bg="white"
)
car_count_label.pack(side="right", anchor="e", padx=20)

# Function to update the timer label
# This function will be called every 100 milliseconds to update the timer label
def update_timer():
    elapsedTime = distanceSensor.getElapsedTime()
    formattedTime = distanceSensor.formatTime(elapsedTime)
    carNum = distanceSensor.carNum
    averageTime = distanceSensor.getHourlyAverage()
    #formattedTime = "00:00" 
    timer_label.config(text=f"Current Car: {formattedTime}")
    car_count_label.config(text=f"Car #{carNum}")
    root.after(100, update_timer)
    average_time_label.config(text=f"Average Time: {averageTime}")
    
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)
    
root.bind("<Escape>", exit_fullscreen)
root.bind("<q>", lambda e: root.destroy())

update_timer()
root.mainloop()
# This code creates a simple GUI using Tkinter to display the current departure time
