from picamera2 import Picamera2, Preview
import time
import cv2
import numpy as np
import serial
import RPi.GPIO as GPIO
#set up serial communication
ser = serial.Serial('dev/ttyUSB0',baudrate = 100000, bitsize = serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO,timeout=1)
#GPIO Setup
pins = [5, 19, 21, 26]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

for pin in pins:
    GPIO.output(pin, GPIO.LOW)
#Element Decleration
cap_matrix = np.zeros((3,3))
intensity_values = []
threshold = 128
high = 0
chosen_M = []
Commands =[]
Direction =""
#activate picam2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()
#List of Active Matrix's
M1 = np.array([[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]])
#Straight
M2 = np.array([[ 1,  1,  1],
               [ 1,  1,  1],
               [ 1,  1, -1]])
#slow right
M3 = np.array([[ 1,  1,  1],
               [ 1,  1,  1],
               [ 1, -1, -1]])
#Hard Right
M4 = np.array([[ 1,  1,  1],
               [ 1,  1,  1],
               [-1,  1,  1]])
#Slow Left
M5 = np.array([[ 1,  1,  1],
              [ 1,  1,  1],
              [-1,  1, -1]])
#Slow Down - Could be perp Line
M6 = np.array([[ 1,  1,  1],
               [ 1,  1,  1],
               [-1, -1,  1]])
#Hard Right
M7 = np.array([[ 1,  1,  1],
               [ 1,  1,  1],
               [-1, -1, -1]])
#Forward
M8 = np.array([[ 1,  1,  1],
                [ 1,  1, -1],
                [ 1,  1, -1]])
#Sharp Right
M9 = np.array([[ 1,  1,  1],
                [ 1,  1, -1],
                [ 1, -1, -1]])
#Right
M10 = np.array([[ 1,  1,  1],
                [ 1, -1, -1],
                [ 1, -1, -1]])
#Sharp Right
M11 = np.array([[ 1,  1,  1],
                [-1,  1,  1],
                [-1,  1,  1]])
#Sharp Left
M12 = np.array([[ 1,  1,  1],
                [-1,  1, -1],
                [-1,  1, -1]])
#Forward
M13 = np.array([[ 1,  1,  1],
                [-1, -1,  1],
                [-1, -1,  1]])
#slow Left
M14 = np.array([[ 1,  1,  1],
                [-1, -1, -1],
                [-1, -1, -1]])
#forward
M15 = np.array([[ 1,  1, -1],
                [ 1,  1, -1],
                [ 1,  1, -1]])
#left
M16 = np.array([[ 1,  1, -1],
                [ 1, -1, -1],
                [-1, -1, -1]])
#slow right
M17 = np.array([[ 1,  1, -1],
                 [-1,  1, -1],
                 [ 1,  1,  1]])
#forward
M18 = np.array([[ 1,  1, -1],
                 [-1,  1, -1],
                 [-1,  1, -1]])
#forward (slight left)
M19 = np.array([[ 1, -1, -1],
                 [ 1, -1, -1],
                 [ 1, -1, -1]])
#Move to Right
M20 = np.array([[-1,  1,  1],
                 [-1,  1,  1],
                 [-1,  1,  1]])
#Right
M21 = np.array([[-1,  1, -1],
                 [ 1,  1,  1],
                 [-1,  1, -1]])
#Pause - 30 seconds
M22 = np.array([[-1, -1, -1],
                 [ 1,  1,  1],
                 [ 1,  1,  1]])
#forward
M23 = np.array([[-1, -1, -1],
                 [ 1,  1, -1],
                 [ 1,  1, -1]])
#sharp Left
M24 = np.array([[-1, -1, -1],
                 [-1,  1,  1],
                 [-1,  1,  1]])
#Sharp Right
M25 = np.array([[-1, -1, -1],
                 [-1, -1, -1],
                 [ 1,  1,  1]])
#forward
M26 = np.array([[-1, -1, -1],
                 [-1, -1, -1],
                 [-1, -1, -1]])
#stationary

Collection = [M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12,M13,M14,M15,M16,M17,M18,M19,M20,M21,M22,M23,M24,M25,M26]
#Image Processing tool

while True:
    #Image Processing
    frame = picam2.capture_array()
    cv2.GaussianBlur(frame, (5,5), 0)
    roi = frame[0:480,0:640]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, BI = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    #seperating into [3x3] matrix images
    TL = BI[0:int(320/3), 0:int(320/3)]
    TM = BI[0:int(320/3), int(320/3):int(320/3)*2]
    TR = BI[0:int(320/3), 2*int(320/3):320]
    ML = BI[int(320/3):int(320/3)*2, 0:int(320/3)]
    MM = BI[int(320/3):int(320/3)*2, int(320/3):int(320/3)*2]
    MR = BI[int(320/3):int(320/3)*2, 2*int(320/3):320]
    BL = BI[int(320/3)*2:320, 0:int(320/3)]
    BM = BI[int(320/3)*2:320, int(320/3):int(320/3)*2]
    BR = BI[int(320/3)*2:320, 2*int(320/3):320]
    regions = [TL,TM,TR,ML,MM,MR,BL,BM,BR]
    #mean thresholding into -1/1
    for i in regions:
        intensity = np.mean(i)
        if intensity < threshold:
            intensity_values.append(-1)
        else:
            intensity_values.append(1)
    #make values into matrix
    id_matrix = np.array(intensity_values).reshape((3,3))
    #matrix comparison process
    for i in Collection:
        if high < np.sum(id_matrix*i):
            chosen_M = i
            high = np.sum(id_matrix*i)
    

    #GPIO Comands
    if GPIO.input(5) == GPIO.HIGH: #ARM Drone/Launch
        Commands = [1500,1500,1800,1500,1850,1000,1000]
        if GPIO.input(26) == GPIO.HIGH: #Estop
            Commands = [1500,1500,900,1500,1850,1850,1000]
        elif GPIO.input(21) == GPIO.HIGH: #linefollowing mode
            if np.array_equal(M1, chosen_M): #straight
                Direction = 'straight'
                Commands = [1500,1500,1700,1500,1850,1000,1000]
            elif np.array_equal(M2, chosen_M): #slow Right
                Direction = 'Slow Right'
                Commands = [1500,1500,1600,1600,1850,1000,1000]
            elif np.array_equal(M3, chosen_M): #Hard Right
                Direction = 'Hard Right'
                Commands = [1500,1500,1550,1700,1850,1000,1000]
            elif np.array_equal(M4, chosen_M): #Slow Left
                Direction = 'Slow Left'
                Commands = [1500,1500,1600,1400,1850,1000,1000]
            elif np.array_equal(M5, chosen_M): #Slow down - Perpline
                Direction = 'Slow down - perpline'
                Commands = [1500,1500,1550,1500,1850,1000,1000]
            elif np.array_equal(M6, chosen_M): #Hard Left
                Direction = 'Hard Left'
                Commands = [1500,1500,1550,1300,1850,1000,1000]
            elif np.array_equal(M7, chosen_M): #Forward 
                Direction = 'Forward'
                Commands = [1500,1500,1700,1500,1850,1000,1000]
            elif np.array_equal(M8, chosen_M): #Sharp Right
                Direction = 'Sharp right'
                Commands = [1500,1500,1550,1800,1850,1000,1000]
            elif np.array_equal(M9, chosen_M): #Right
                Direction = 'Right'
                Commands = [1500,1500,1600,1700,1850,1000,1000]
            elif np.array_equal(M10, chosen_M): #Sharp Right
                Direction = 'Sharp right'
                Commands = [1500,1500,1550,1800,1850,1000,1000]
            elif np.array_equal(M11, chosen_M): #Sharp Left
                Direction = 'Sharp left'
                Commands = [1500,1500,1550,1200,1850,1000,1000]
            elif np.array_equal(M12, chosen_M): #Forward
                Direction = 'Forward'
                Commands = [1500,1500,1700,1500,1850,1000,1000]
            elif np.array_equal(M13, chosen_M): #Slow Left
                Direction = 'Slow Left'
                Commands = [1500,1500,1550,1400,1850,1000,1000]
            elif np.array_equal(M14, chosen_M): #Forward
                Direction = 'Forward'
                Commands = [1500,1500,1700,1500,1850,1000,1000]
            elif np.array_equal(M15, chosen_M): #Left
                Direction = 'Left'
                Commands = [1500,1500,1600,1200,1850,1000,1000]
            elif np.array_equal(M16, chosen_M): #Slow Left
                Direction = 'Slow Left'
                Commands = [1500,1500,1550,1800,1850,1000,1000]
            elif np.array_equal(M17, chosen_M): #Forward
                Direction = 'Forward'
                Commands = [1500,1500,1700,1500,1850,1000,1000]
            elif np.array_equal(M18, chosen_M): #Forward
                Direction = 'Forward'
                Commands = [1500,1500,1700,1500,1850,1000,1000]
            elif np.array_equal(M19, chosen_M): #Move to Right
                Direction = 'Forward'
                Commands = [1500,1500,1600,1500,1850,1000,1000]
            elif np.array_equal(M20, chosen_M): #Right
                Direction = 'Right'
                Commands = [1500,1500,1550,1700,1850,1000,1000]
            elif np.array_equal(M21, chosen_M): #Pause
                Direction = 'Pause Perp line'
                Commands = [1500,1500,1500,1500,1850,1000,1000]
            elif np.array_equal(M22, chosen_M): #Forward
                Direction = 'Forward'
                Commands = [1500,1500,1700,1500,1850,1000,1000]
            elif np.array_equal(M23, chosen_M): #Sharp Left
                Direction = 'Sharp Left'
                Commands = [1500,1500,1550,1200,1850,1000,1000]
            elif np.array_equal(M24, chosen_M): #Sharp Right
                Direction = 'Sharpt Right'
                Commands = [1500,1500,1550,1800,1850,1000,1000]
            elif np.array_equal(M25, chosen_M): #Forward
                Direction = 'Forward'
                Commands = [1500,1500,1700,1500,1850,1000,1000]
            elif np.array_equal(M26, chosen_M): #No Line
                Direction = 'No Line'
                Commands = [1500,1500,1500,1500,1850,1000,1000]
        elif GPIO.input(19) == GPIO.HIGH:#hovering
            Commands = [1500,1500,1500,1500,1850,1000,1000]

    #Reseting values for next iteration
    intensity_values = []
    chosen_M = []
    high = 0
    #send commands to Arduino
    for i in Commands:
        ser.write(f"{i}\n".encode())
        time.sleep(0.01)
    #30 Second wait
    if np.array_equal(M21, Chosen_M):
        time.sleep(30)
        Commands = [1500,1500,1700,1500,1850,1000,1000]
        for i in Commands:
            ser.write(f"{i}\n".encode())
            time.sleep(0.01)
        time.sleep(0.5) #time to clear perp line
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
picam2.close()
cv2.destroyAllWindows()


