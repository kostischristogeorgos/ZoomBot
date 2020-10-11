import datetime
import time
import pyautogui
import webbrowser
import csv

# Getting the current Date, Hour, Minutes
day = datetime.datetime.now()
hour = day.hour
minutes = day.minute
day = day.strftime("%A")


# Opening the csv file and parsing the data into a list
# Data is a list consisting Day, Class Start Time, Zoom Link
with open('Schedule.csv', 'r', newline='') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    data = []
    for row in reader:
        class_day = row[0]
        class_time = int(row[1])
        class_link = row[2]
        data.append([class_day, class_time, class_link])


def StartCheck():
    no_class_today = True
    
    # Iterating through the information list and getting the details of each class
    for i in range(len(data)):
        class_day = data[i][0]
        class_time = data[i][1]
        class_link = data[i][2]
        cur_hour = hour
        cur_min = minutes

        # If the day is the current day it checks the time and calls the JoinMeeting function 5 minutes before the class
        if day == class_day:
            no_class_today = False 
            time_dif = class_time - cur_hour

            # Checks if the time difference between the class and the current time is positive or equal to 0
            if time_dif >= 0:
                while True:

                    # If the time difference is more than one hour it updates the hour and minutes
                    # If the minutes == 60 it means one hour has passed so we update the hour too
                    # In all cases we put the program to sleep for 1 minute
                    if time_dif >= 2:
                        print("Time is:", cur_hour, ":", cur_min, "I wait for one minute until time is: ",
                              class_time - 1, ":", 55)
                        if cur_min == 60:
                            cur_min = 0
                            time_dif = time_dif - 1
                            cur_hour = cur_hour + 1
                            time.sleep(60)  # needs to be 60
                        else:
                            time.sleep(60)  # needs to be 60
                            cur_min = cur_min + 1
                        continue

                    # If the hour diff is less than 1 hour and minutes are >=55 or the class has started (time_dif == 0)
                    # We call the function that connects to the meeting
                    if (cur_min >= 55 and time_dif == 1) or time_dif == 0:
                        JoinMeeting(class_link)
                        time.sleep(25)  # Time for the connecting function to operate
                        print("Connected to class")
                        return

                    else:
                        # If current time diff from the start of the class is more than 5 minutes and less than 1 hour
                        # it puts the program into sleep for 60 seconds and updates the time difference
                        print("Time is:", cur_hour, ":", cur_min, "I wait for one minute until time is: ",
                              class_time - 1, ":", 55)
                        time.sleep(60)  # needs to be 60
                        cur_min = cur_min + 1
            else:
                # Displays the past classes that couldn't connect to
                print("Can't connect to the class that starts at:", class_time, "because time is:", cur_hour, ":",
                      cur_min)
                continue
        else:
            continue
    if no_class_today:
        print("You don't have a class today")
    end = input("Press any key to exit")


# Program does not work on Mozilla Firefox, preferably use Google Chrome, Opera or Edge
# Connects the meeting 5 minutes before the start of the class.
# The program doesn't work if you run it more than one hour after class start
# Calling the StartCheck function which controls program flow
StartCheck()
