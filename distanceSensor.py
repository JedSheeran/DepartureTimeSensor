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
carLog = [] # stores car number, time at window, and date/time

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
def getAverageTimeForHour():
    global carLog
    oneHourAgo = datetime.now() - timedelta(hours=1)
    times = [int(m) * 60 + int(s) for (c, d, t) in carLog if t >= oneHourAgo for m, s in [d.split(':')] if len(d.split(':')) == 2]
    if times:
        averageSeconds = sum(times) / len(times)
        return formatTime(averageSeconds)
    return "00:00"

# Function to log car data
def logCar(carNumVar, timeVar):
    global carLog
    now = datetime.now()

    oneHourAgo = now - timedelta(hours=1)
    carLog = [(c, d, t) for (c, d, t) in carLog if t >= oneHourAgo]

    carLog.append((carNumVar, timeVar, now))

# Function to check if current time is within operating hours
def withinHours():
    global afterOperatingHours
    now = datetime.now().time()
    if now >= datetime.strptime("22:00", "%H:%M").time() or now <= datetime.strptime("06:30", "%H:%M").time():
        print("Outside of operating hours. Waiting until 6:30 AM to resume.")
        afterOperatingHours = True
        return afterOperatingHours
    afterOperatingHours = False
    return afterOperatingHours
    


def checkSensor():
    global carNum, carInRange, startTime, prevCarTime
    withinHours()
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
            logCar(carNum, formattedTime)
            writeToGoogleSheet(carNum, formattedTime, currentTime)
