#!/usr/bin/env python
""" 
EchoCarStarter this is a drivative of Fauxmo.py (https://github.com/makermusings/fauxmo)
This emulates a weemo device on the network.
The weemo device name can be set in the script and the can be found by an amazon echo.
"""

import fauxmo
import logging
import time
import RPi.GPIO as GPIO
import sys
import time

DEVICE_NAME = "My Car" ## edit name of device
DEVICE_PORT = 52000
REMOTE_GPIO = 9  ## edit this to the correct GPIO to 74HC4052

logging.basicConfig(level=logging.CRITICAL) ## disable debug logs

class device_handler(object):
    def __init__(self, name):
        self.name = name
    def on(self):
        print self.name, "ON"
        logging.debug("turning car ON")
        changeIOState(True)
        return True

    def off(self):
        logging.debug("turning car OFF")
        changeIOState(False)
        return True


def setupIOs():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(REMOTE_GPIO,GPIO.OUT)
    GPIO.output(REMOTE_GPIO,GPIO.LOW) #make sure the car is off

def changeIOState(state): ##simulate long key press
    if state:
        GPIO.output(REMOTE_GPIO,GPIO.HIGH)
        time.sleep(4)
    else:
        GPIO.output(REMOTE_GPIO,GPIO.HIGH) ## check this if you two buttons to turn ON/OFF
        time.sleep(4)

    GPIO.output(REMOTE_GPIO,GPIO.LOW)

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        fauxmo.DEBUG = True
    
    setupIOs()

    p = fauxmo.poller()

    u = fauxmo.upnp_broadcast_responder()

    u.init_socket()

    p.add(u)

    d = device_handler(DEVICE_NAME)
    
    fauxmo.fauxmo(DEVICE_NAME, u, p, None, DEVICE_PORT, d) #attach call back

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
        finally:
            GPIO.cleanup()
