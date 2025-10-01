import time
import googleSheet
from datetime import datetime, timedelta
from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=2, max_distance=2.5)
carNum = 0
carInRange = False
startTime = None
prevCarTime = None
afterOperatingHours = False

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

def getPrevCarȚime():
    return prevCarTime

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

def withinHours():
    global afterOperatingHours
    now = datetime.now().time()
    if now >= datetime.strptime("15:36", "%H:%M").time() and now <= datetime.strptime("15:37", "%H:%M").time():
        print("Outside of operating hours. Waiting until 6:30 AM to resume.")
        afterOperatingHours = True
        return afterOperatingHours
    afterOperatingHours = False
    return afterOperatingHours


def checkSensor():
    global carNum, carInRange, startTime, prevCarTime
    if afterOperatingHours:
        return 
    
    #print("***Waiting for car***")
    if ultrasonic.in_range and not carInRange:
        carInRange = True
        startTime = time.time()
        carNum += 1
        print("***In range***")
    elif not ultrasonic.in_range and carInRange:
        carInRange = False
        if startTime:
            elapsedTime = time.time() - startTime
            formattedTime = formatTime(elapsedTime)
            currentTime = getCurrentTime()
            prevCarTime = formattedTime
            print("Car# ", carNum, "Time at Window: ", prevCarTime)
            print("***Out of range***")
            writeToGoogleSheet(carNum, formattedTime, currentTime)
