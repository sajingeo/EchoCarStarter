#!/usr/bin/env python
""" 
Sensory.py this is a drivative of Fauxmo.py, example-minimal.py
This emulates a weemo device on the network.
The weemo device name can be set in the script and the can be found by an amazon echo.
"""

import fauxmo
import logging
import time
import RPi.GPIO as GPIO
import random
import sys
import time
import RPi.GPIO as GPIO

DEVICE_NAME = {"My Car":0} ## edit name of device
REMOTE_GPIO = 9  ## edit this to the correct GPIO to 74HC4052

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(9,GPIO.OUT)

GPIO.output(9, GPIO.LOW) #make sure you dont start the car

logging.basicConfig(level=logging.DEBUG) ## disable debug logs


class device_handler(object):
    def on(self):
        print self.name, "ON"
        logging.debug("turning car ON")
        GPIO.output(9,GPIO.HIGH)
        time.sleep(4)
        GPIO.output(9,GPIO.LOW)
        return True

    def off(self):
        logging.debug("turning car OFF")
        GPIO.output(9,GPIO.HIGH) ## check this if you two buttons to turn ON/OFF
        time.sleep(4)
        print self.name, "OFF"
        GPIO.output(9,GPIO.LOW)
        return True

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        fauxmo.DEBUG = True
    
    p = fauxmo.poller()

    u = fauxmo.upnp_broadcast_responder()

    u.init_socket()

    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    
    for trig, port in DEVICE_NAME.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

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