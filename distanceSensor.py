import time
import googleSheet 
from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.1)
carNum = 0
departureTime = 0

def writeToGoogleSheet(carNumVar, timeVar):
    googleSheet.writeToGoogleSheet(carNumVar, timeVar)
    return

try:
    while True:
        print(ultrasonic.distance)
        ultrasonic.wait_for_in_range()
        start = time.time()
        carNum = carNum + 1
        print("***In range***")

        ultrasonic.wait_for_out_of_range()
        end = time.time()
        departureTime = end-start
        print(end - start)
        print("***Out of range***")
        writeToGoogleSheet(carNum, departureTime)
       # with open("departure_time.txt", "a") as file:
        #    file.write("Car # ", carNum, "   Time at Window: ", departureTime, "\n")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram stopped by user.")