import time
from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.1)
carNum = 0
departureTime = 0

try:
    while True:
        print(ultrasonic.distance)
        ultrasonic.wait_for_in_range()
        start = time.time()
        carNum+=1
        print("***In range***")

        ultrasonic.wait_for_out_of_range()
        end = time.time()
        departureTime = end-start
        print(end - start)
        print("***Out of range***")
        with open("departure_time.txt", "a") as file:
            file.write("Car # ", carNum, "   Time at Window: ", departureTime, "\n")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram stopped by user.")
    


def carAtWindow():
    start = time.time()
    carNum+=1
    if ultrasonic.out_of_range():
        end = time.time()
        departureTime = end - start
        with open("departure_time.txt", "a") as file:
            file.write("Car # ", carNum, "   Time at Window: ", departureTime, "\n")
        return
    return




def noCarAtWindow():
    end = timeit.timeit()
