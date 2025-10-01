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
    text="Current Car \n00:00", 
    font=("Arial", 104, "bold"),
    fg="#004f71",
    bg="white",
    justify="center",
    anchor="center"
)
timer_label.pack(pady=10, fill="both", expand=True)

bottom_frame = tk.Frame(root, bg="white")
bottom_frame.pack(fill="x", side="bottom", pady=10)

# Hourly Average Time Label
average_time_label = tk.Label(
    root, 
    text="Average Time: 00:00", 
    font=("Arial", 28),
    fg="#004f71",
    bg="white"
)
average_time_label.pack(in_=bottom_frame, side="left", anchor="w", padx=20)

# Last Cars Time Label
last_car_time_label = tk.Label(
    root, 
    text="Last Cars Time: 00:00", 
    font=("Arial", 28),
    fg="#004f71",
    bg="white"
)
last_car_time_label.pack(in_=bottom_frame, side="right", anchor="e", padx=20)


# Function to update the timer label
# This function will be called every 100 milliseconds to update the timer label
def update_timer():
    elapsedTime = distanceSensor.getElapsedTime()
    formattedTime = distanceSensor.formatTime(elapsedTime)
    #carNum = distanceSensor.carNum
    #formattedTime = "00:00" 
    timer_label.config(text=f"\nCurrent Car\n{formattedTime}\n\n")
    last_car_time_label.config(text=f"Last Cars Time: {distanceSensor.prevCarTime}")
    root.after(100, update_timer)

# Function to get and update the average time label
# This function will be called every 60 seconds to update the average time label
def get_average_time():
    averageTime = distanceSensor.getAverageTimeForHour()
    average_time_label.config(text=f"Average Time: {averageTime}")
    root.after(60000, get_average_time)  # Update every minute
    
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)
    
root.bind("<Escape>", exit_fullscreen)
root.bind("<q>", lambda e: root.destroy())

get_average_time() #need to see if this works might get hung every minute
update_timer()
root.mainloop()
# This code creates a simple GUI using Tkinter to display the current departure time
