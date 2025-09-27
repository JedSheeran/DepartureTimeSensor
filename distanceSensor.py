import time
import googleSheet
from datetime import datetime, timedelta
from gpiozero import DistanceSensor
#import threading

# Declare the ultrasonic sensor
#Global State
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=2, max_distance=2.5)
carNum = 0
carInRange = False
startTime = None
running = True
prevCarTime = None

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

# Function to get the elapsed time for other scripts
def getElapsedTime():
    if carInRange and startTime:
        return time.time() - startTime
    return 0

# Function to get the average time for the current hour
# This function reads all rows from the Google Sheet, filters them by the current hour
def getAverageTimeForHour():
    allRows = googleSheet.readAllRows()
    oneHourAgo = datetime.now() - timedelta(hours=1)
    times = []
    for row in allRows:
        dateStr = row[2]  # Assuming the date is in the third column
        try:
            dateObj = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
            if dateObj >= oneHourAgo:
                timeStr = row[1]  # Assuming the time is in the second column
                try:
                    minutes, seconds = map(int, timeStr.split(':'))
                    totalSeconds = minutes * 60 + seconds
                    times.append(totalSeconds)
                except ValueError:
                    continue
        except ValueError:
            continue
    if times:
        averageSeconds = sum(times) / len(times)
        return formatTime(averageSeconds)
    return "00:00"

def stopLoop():
    global running
    running = False

# Main loop
# This loop waits for a car to arrive and then records the time it leaves
# It uses the ultrasonic sensor to detect the car's presence
# The loop runs indefinitely until interrupted by the user
def start():
    global carNum, carInRange, startTime, running, prevCarTime
    try:
        while running:
            now = datetime.now().time()
            if now >= datetime.strptime("22:15", "%H:%M").time() or now <= datetime.strptime("06:30", "%H:%M").time():
                print("Outside of operating hours. Waiting until 6:00 AM to resume.")
                time.sleep(60)  # Sleep for 1 minute before checking again
            else:
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
                prevCarTime = departureTime
                writeToGoogleSheet(carNum, departureTime, getCurrentTime())
                

                #waits for 1 second before checking again
                time.sleep(1)
        
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
