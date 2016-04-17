import os
import time
import commands

__author__ = 'Basti_Schr'

# Source: https://www.arduino.cc/en/Tutorial/ColorCrossfader
# transformed to Python language for the Raspberry Pi


# Output
redPin = 22
grnPin = 17
bluPin = 24

# Color arrays in percent
black = [0,0,0]
white = [100,100,100]
red = [100,0,0]
green = [0,100,0]
yellow = [0,100,0]
blue = [0,0,100]
dimWhite = [30,30,30]
# make you own...

# init pigpiod
# os.popen("sudo -S %s"%( "pigpiod"), 'w').write('raspberry') # not necessary. Only after Reboot

# returns the current brightness of a pin
def getVal(Pin):
    out = commands.getstatusoutput('pigs gdc '+str(Pin))
    accVal = int(out[1])
    return accVal

# set init color
redVal = getVal(redPin)
grnVal = getVal(grnPin)
bluVal = getVal(bluPin)


wait = 0.001    # 10 ms delay
hold = 0        # optional hold after completed
DEBUG = False    # set Debug ON or OFF
loopCount = 60  # how many times should DEBUG report

# init color variables
prevR = redVal
prevG = grnVal
prevB = bluVal

if DEBUG:
    print(redVal)
    print(prevR)

def calculateStep(prevValue, endValue):
    step = endValue - prevValue # overall gap
    if step != 0:
        step = 1020.0 / step   # 1020 / step
    return step

def calculateVal(step, val, i):
    # print(int(i%step))
    if step != 0 and int(i % step) is 0:       # if step is non-zero and its time to change a value
        if step > 0:                      # increment the value if step is positive...
            val += 1
#            print("val++")
        elif step < 0:                    # ...or decrement it if step is negative
            val -= 1
#            print("val--")

    if val > 255:                         # defensive driving...
        val = 255
    elif val < 0:
        val = 0
    if DEBUG:
        print(val)
    return val


def analogWrite(pin, brightness):
    os.system("pigs p "+str(pin)+" "+str(brightness))


    # Main function
def crossFade(color):
    # convert to 0 - 255
    print(color)
    print(color[1])
    R = (int(color[0]) * 255) * 0.01
    G = (int(color[1]) * 255) * 0.01
    B = (int(color[2]) * 255) * 0.01

    global prevR, prevG, prevB
    global redPin, grnPin, bluPin

    # get initial value
    prevR = getVal(redPin)
    prevG = getVal(grnPin)
    prevB = getVal(bluPin)

    global redVal, grnVal, bluVal

    stepR = calculateStep(prevR, R)
    stepG = calculateStep(prevG, G)
    stepB = calculateStep(prevB, B)

    if DEBUG:
        print("Step size R G B: ")
        print(stepR, stepG, stepB)
        print("Values R G B")
        print(redVal, grnVal, bluVal)

    n = 0
    while n <= 1020:
        n += 1
        redVal = calculateVal(stepR, redVal, n)
        grnVal = calculateVal(stepG, grnVal, n)
        bluVal = calculateVal(stepB, bluVal, n)

        analogWrite(redPin, redVal)
        analogWrite(grnPin, grnVal)
        analogWrite(bluPin, bluVal)

        time.sleep(wait)

        if DEBUG:
            if n == 0 or n % loopCount == 0:
                print("Loop/RGB: "+str(n)+ ";")
                print("R"+str(redVal))
                print("G"+str(grnVal))
                print("B"+str(bluVal))
    
    print("Finish: current Vals: R G B")
    print(redVal, grnVal, bluVal)
    # update Vals
    prevR = redVal
    prevG = grnVal
    prevB = bluVal
    time.sleep(hold)        # Pause for optional 'wait' milliseconds before resuming the loop



##############
# write here the color in, whitch it should be


crossFade(red)
crossFade(green)
crossFade(blue)
crossFade(white)
crossFade(black)
