import time
import googleSheet 
from datetime import datetime
from gpiozero import DistanceSensor
import threading

# Declare the ultrasonic sensor
#Global State
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5)
carNum = 0
carInRange = False
startTime = None
running = True

# Function to write to Google Sheets
def writeToGoogleSheet(carNumVar, timeVar, dateVar):
    # Call the function from googleSheet.py to write to Google Sheets
    googleSheet.writeToGoogleSheet(carNumVar, timeVar, dateVar)
    return

# Function to get the current time
# This function returns the current time in the format YYYY-MM-DD HH:MM:SS
def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

# Function to format time in MM:SS
# This function takes a number of seconds and returns a string in the format MM:SS
# For example, if the input is 65, the output will be "01:05"
def formatTime(seconds):
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(minutes):02}:{int(seconds):02}"

def getElapsedTime():
    if carInRange and startTime:
        return time.time() - startTime
    return 0

def stopLoop():
    global running
    running = False

# Main loop
# This loop waits for a car to arrive and then records the time it leaves
# It uses the ultrasonic sensor to detect the car's presence
# The loop runs indefinitely until interrupted by the user
try:
    while running:
        print("waiting for car to arrive...")
        ultrasonic.wait_for_in_range()
        startTime = time.time()
        carNum = carNum + 1
        carInRange = True
        print("***In range***")

        # Wait for the car to leave
        ultrasonic.wait_for_out_of_range()
        carInRange = False
        end = time.time()
        departureTime = formatTime(end - startTime)
        print("Car# ", carNum, "Time at Window: ", departureTime)
        print("***Out of range***")
        writeToGoogleSheet(carNum, departureTime, getCurrentTime())

        #waits for 1 second before checking again
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nProgram stopped by user.")