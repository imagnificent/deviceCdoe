
import RPi.GPIO as GPIO
import time
import Raspberry_Pi_TCS3200_Color_Detector
import pressureSensor
import strandtest
import timeit
import random
import os
import sound
import ac
import json
import sys
import getopt
import csv
from neopixel import *
import argparse
import movementSensor
import readDistance
from functools import reduce
import writecsv
import data
import drawing
import readcsv
import traceback
import decimal

LED_COUNT1      = 7      # Number of LED pixels.
LED_COUNT2      = 6
LED_PIN1        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN2        = 13
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 64     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor pattern shift)
LED_CHANNEL1    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_CHANNEL2    = 1
LED_STRIP       = ws.WS2811_STRIP_GRB

PRESSURE1 = 12
PRESSURE2 = 4

def pressurewipe(strip,color,pressure,wait_ms=50):
     if pressure==1:
       for i in range(strip.numPixels()/2):
         strip.setPixelColor(i,color)
         strip.show()
         time.sleep(wait_ms/1000)
     else:
       for i in range(strip.numPixels()/2,strip.numPixels()):
         strip.setPixelColor(i,color)
         strip.show()
         time.sleep(wait_ms/1000)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def loop(no,color0,color,pattern,k,light,isSound,press):
	if pattern == 0 or pattern == 1:
	    distancePath = '/home/pi/deviceCode/distanceDict' + str(pattern) +'.txt'
	else:
	    distancePath = '/home/pi/deviceCode/distanceDict2.txt'
     	writepath = '/home/pi/deviceCode/data/data.csv'
        mode = 'a' if os.path.exists(writepath) else 'w'
        redValue = 255
        greenValue = 255
        blueValue = 255
        if color == "red" and light == True :
            redValue = 255
            greenValue = 0
            blueValue = 0
	    soundTrack = "/home/pi/red.mp3"
        elif color == "green" and light == True:
            redValue = 0
            greenValue = 255
            blueValue = 0
            soundTrack = "/home/pi/green.mp3"
        elif color == "blue" and light == True:
            redValue = 0
            greenValue = 0
            blueValue = 255
            soundTrack = "/home/pi/blue.mp3"
        elif color == "yellow" and light == True :
            redValue = 255
            greenValue = 255
            blueValue = 0
            soundTrack = "/home/pi/yellow.mp3"
	elif color == "black" and light == True :
	    redValue = 255
            greenValue = 255
            blueValue = 255
        elif color == "red" and light == False :
            soundTrack = "/home/pi/red.mp3"
        elif color == "green" and light == False:
            soundTrack = "/home/pi/green.mp3"
        elif color == "blue" and light == False:
            soundTrack = "/home/pi/blue.mp3"
        elif color == "yellow" and light == False :
            soundTrack = "/home/pi/yellow.mp3"
        elif color == "black" and light == False :
            redValue = 255
            greenValue = 255
            blueValue = 255

        colorState = False
        pressState1 = False
        pressState2 = False
	moveState = False
        colorWipe(strip1, Color(redValue, greenValue, blueValue))
	colorWipe(strip2, Color(0,0,0),1)
	colorWipe(strip2, Color(0,0,0),2)
	startTime = time.time()
	localTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(startTime))
	localDate = localTime.split(" ")[0]
	localOnlyTime = localTime.split(" ")[1]
	soundCount = 0
	timeOfGesture = 0
        dataForSend = ""
	positionDict = {}
	print(color0)
	print(color)
	if pattern == 0 or pattern == 1:
	    positionDict = {"red":0, "green":1, "black":2, "yellow":3, "blue": 4}
	elif pattern == 2:
	    positionDict = {"red":0, "blue":1, "green":2, "yellow":3, "black": 4}
	elif pattern == 3:
            positionDict = {"red":1, "blue":0, "green":2, "yellow":3, "black": 4}
        elif pattern == 4:
            positionDict = {"red":2, "blue":1, "green":0, "yellow":3, "black": 4}
        elif pattern == 5:
            positionDict = {"red":3, "blue":0, "green":2, "yellow":1, "black": 4}
        elif pattern == 6:
            positionDict = {"red":1, "blue":3, "green":0, "yellow":2, "black": 4}
        elif pattern == 7:
            positionDict = {"red":0, "blue":2, "green":3, "yellow":1, "black": 4}

	positionCode0 = positionDict.get(color0)
	positionCode1 = positionDict.get(color)
	print("positionCode0" + str(positionCode0))
	print("positionCode1" + str(positionCode1))
	if color != "black":
	    print("start")
	    if isSound:
	    	sound.pyplayBreak(soundTrack)
	elif color == "black" and light == False:
	    strandtest.theaterChase(strip1, Color(127, 127, 127))

	while(colorState == False):
          while(moveState == False):
                if movementSensor.movement():
		  if Raspberry_Pi_TCS3200_Color_Detector.loop() != color0:
                    moveStartTime = time.time()
                    moveState = True
                    print(moveStartTime)
		    print(moveStartTime - startTime)
		    colorWipe(strip2, Color(redValue,greenValue,blueValue),1)
        	    colorWipe(strip2, Color(redValue,greenValue,blueValue),2)

	  print("start detecting")
	  if press:

	    if pressureSensor.pressureEx(PRESSURE1): 
		pressurewipe(strip2,Color(255,255,255),1)
		print("1 press")
		pressState1 = True

            if pressureSensor.pressureEx(PRESSURE2):
                pressurewipe(strip2,Color(255,255,255),2)
                print("2 press")
                pressState2 = True

	    if pressureSensor.pressureEx(PRESSURE1) == False or pressureSensor.pressureEx(PRESSURE2) == False:
		count = 0
		state = False
		pressState1 = False
		pressState2 = False
		print("no press")
		while(count < 30):
		    if GPIO.input(PRESSURE1):
			count = count + 1
			pressurewipe(strip2,Color(redValue,greenValue,blueValue),1)
			print(count)
			pressState1 = False
			time.sleep(0.1)
		    else:
                        pressState1 = True
			pressurewipe(strip2,Color(255,255,255),1)
		    print("1" + str(pressState1))
		    if GPIO.input(PRESSURE2):
			count = count + 1
			pressurewipe(strip2,Color(redValue,greenValue,blueValue),2)
			print(count)
			pressState2 = False
			time.sleep(0.1)
		    else:
			pressState2 = True 
			pressurewipe(strip2,Color(255,255,255),2)
		    print("2" + str(pressState2))
		    if pressState1 and pressState2:
			count = 30
			state = True
        	count = 0
		print(soundCount)
		print(state)
	   	if state == False:
		    sound.pyplayBreak("/home/pi/press.mp3")
		    soundCount  = soundCount + 1
		elif state == True and soundCount > 0:
		    pressurewipe(strip2,Color(255,255,255),1)
		    pressurewipe(strip2,Color(255,255,255),2)
		    sound.pyplayBreak("/home/pi/correct.mp3")
		    soundCount = 0
		    timeOfGesture = timeOfGesture + 1

	  if Raspberry_Pi_TCS3200_Color_Detector.loop() == color:
		pressState1 = True
		pressState2 = True
	        if pressState1 and pressState2:
                    colorState = True
		    print("success")
                    sound.pyplay("/home/pi/success.mp3")
                    endTime = time.time()
		    reactionTime =  round(moveStartTime - startTime, 2)
		    costTime = endTime - moveStartTime
		    distance = k*float(readDistance.findDistance(positionCode0,positionCode1,readDistance.txt2dict(distancePath)))
		    print(distance)
		    velocity = distance/costTime
		    velocity = round(velocity,2)
		    costTime = round(costTime,2)
		    data = [localDate,localOnlyTime,color0,color,positionCode0,positionCode1,distance,velocity,reactionTime,costTime,str(timeOfGesture),no]
                    writecsv.writedata(writepath,mode,data)
                    dataList.append(data)
	  else:
		print("Wrong color")
#	return data
def main():
	GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        Raspberry_Pi_TCS3200_Color_Detector.setup()
        pressureSensor.setup(PRESSURE1)
	pressureSensor.setup(PRESSURE2)
	writepath = '/home/pi/deviceCode/data/data.csv'
	#no = int(readcsv.getNo(writepath)) + 1
	no = 1
        global strip1
        global strip2
            # Process arguments
        parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', default=1, help='change the exercise mode')
	parser.add_argument('-t', '--times', default=5, help='num of exercise')
        parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
	parser.add_argument('-p', '--pattern', default = 2, help='pattern of exercise')
	parser.add_argument('-k', '--ratio', default = 3, help='distance = k*distanceUnit')
	args = parser.parse_args()
	times = int(args.times)
	mode = int(args.mode)
	pattern = int(args.pattern)
	k = float(args.pattern)
	print(mode)
	print(times)
	print(pattern)

	if args.clear:
            print("clear")
        # Create NeoPixel object with appropriate configuration.
        strip1 = Adafruit_NeoPixel(LED_COUNT1, LED_PIN1, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL1, LED_STRIP)
        strip2 = Adafruit_NeoPixel(LED_COUNT2, LED_PIN2, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL2, LED_STRIP)
        # Intialize the library (must be called once before other functions).
        strip1.begin()
        strip2.begin()

	colorDict = {0:"red",1:"green",2:"blue",3:"yellow",4:"black"}
	global dataList
	dataList = []
	dataforJson  = ""
	if mode != 3:
#			strandtest.theaterChase(strip1, Color(127, 127, 127))
			colorDict = {0:"red",1:"green",2:"blue",3:"yellow",4:"black",}
            		colorCode0 = 4
            		num = 0
            		sound.pyplay("/home/pi/start.mp3")
			#loop("black",1,4,1,True,False)
            		try:
			    colorCode1 = random.randint(0,3)
            		    while(num < times):
                		colorCode2 = random.randint(0,3)
				print(colorCode1)
                		while(colorCode1 == colorCode2) :
                    			colorCode2 = random.randint(0,3)
                		if mode == 0:
					dataList.append(loop(no,"black",colorDict.get(colorCode1),pattern,k,True,True,True))
					dataList.append(loop(no,colorDict.get(colorCode1),"black",pattern,k,True,True,True))
				elif mode == 1:
					print('start appending')
					loop(no,colorDict.get(colorCode0),colorDict.get(colorCode1),pattern,k,True,True,False)
					#print(dataList)
					colorCode0 = colorCode1
				elif mode == 2:
					dataList.append(loop(no,"black",colorDict.get(colorCode1),pattern,k,False,True,True))
					dataList.append(loop(no,colorDict.get(colorCode1),"black",pattern,k,True,True,True))
				colorCode1 = colorCode2
                		num = num + 1
			    sound.pyplay("/home/pi/finish.mp3")
                            colorWipe(strip1, Color(0,0,0))
                            colorWipe(strip2, Color(0,0,0))
			    if mode == 1 and pattern != 0 and pattern != 1: 
			        os.system('sudo python drawing.py -n ' + str(no) + ' -p ' + str(pattern) )
			        os.system('sudo python data.py -n ' + str(no))

			except BaseException, e:
                             colorWipe(strip1, Color(0,0,0))
                             colorWipe(strip2, Color(0,0,0))
			     print(e.message)
			     print 'traceback.print_exc():'; traceback.print_exc()

                        totalDistance = 0
                        totalReactionTime = 0
                        totalVelocity = 0
                        totalCostTime = 0
                        totalGesture = 0
                        for data in dataList:
                             	#totalDistance = totalDistance + data[6]
                             	totalVelocity = totalVelocity + data[7]
                             	totalReactionTime = totalReactionTime + data[8]
				print totalReactionTime
                             	#totalCostTime = totalCostTime + data[9]
                             	#totalGesture = totalGesture + int(data[10])
                        averageVelocity = round(totalVelocity / times, 1)
                        averageReactionTime = round(totalReactionTime / times, 2)
                        #averageCostTime = round(totalCostTime / times, 2)
                        #averageGesture= totalGesture / times
                        dataforJson = str(times) + ","+ str(averageVelocity) +","+ str(averageReactionTime)
                        print(dataforJson)
                        return dataforJson
	elif mode == 3:
			colorLimit = []
			sound.pyplay("/home/pi/adjustment.mp3")
	    		colorWipe(strip1, Color(255,0,0))
	    		time.sleep(3)
	    		colorLimit = ac.test()
			with open("/home/pi/deviceCode/red.txt","w") as f:
                        	f.write(json.dumps(colorLimit))
	    			f.close()

			colorWipe(strip1, Color(0,255,0))
			sound.pyplay("/home/pi/move.mp3")
            		time.sleep(3)
	    		colorLimit = ac.test()
                        with open("/home/pi/deviceCode/green.txt","w") as f:
                                f.write(json.dumps(colorLimit))
	    			f.close()

			colorWipe(strip1, Color(255,255,0))
                        sound.pyplay("/home/pi/move.mp3")
            		time.sleep(3)
	    		colorLimit = ac.test()
                        with open("/home/pi/deviceCode/yellow.txt","w") as f:
                                f.write(json.dumps(colorLimit))
				f.close()

			colorWipe(strip1, Color(0,0,255))
                        sound.pyplay("/home/pi/move.mp3")
			time.sleep(3)
	    		colorLimit = ac.test()
	                with open("/home/pi/deviceCode/blue.txt","w") as f:
                                f.write(json.dumps(colorLimit))
				f.close()

	   		colorWipe(strip1, Color(255,255,255))
                        sound.pyplay("/home/pi/move.mp3")
	    		time.sleep(3)
	    		colorLimit = ac.test()
                        with open("/home/pi/deviceCode/black.txt","w") as f:
                                f.write(json.dumps(colorLimit))
				f.close()
			sound.pyplay("/home/pi/adjustsuccess.mp3")
			colorWipe(strip1, Color(0,0,0))

def str2float(s):
     L=s.split('.');
     return reduce(lambda x,y:y+x*10,map(int,L[0]))+reduce(lambda x,y:y+x*10,map(int,L[1]))/10**len(L[1])

def destory():
	GPIO.cleanup()

if __name__ == "__main__":
    print("start")
    try:
	main()
    except KeyboardInterrupt:
	destory()
	print("exit")
