import tkinter as tk

def main():
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
        font=("Arial", 35),
        fg="#004f71",
        bg="white"
    )
    average_time_label.pack(in_=bottom_frame, side="left", anchor="w", padx=20)

    # Last Cars Time Label
    last_car_time_label = tk.Label(
        root, 
        text="Last Cars Time: 00:00", 
        font=("Arial", 35),
        fg="#004f71",
        bg="white"
    )
    last_car_time_label.pack(in_=bottom_frame, side="right", anchor="e", padx=20)

    def get_average_time():
        average_time_label.config(text=f"Average Time: 00:00")
        root.after(60000, get_average_time)  # Update every minute

    get_average_time()
    root.mainloop()

if __name__ == "__main__":
    main()