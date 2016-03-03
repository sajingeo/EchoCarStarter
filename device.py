#!/usr/bin/env python
""" fauxmo_minimal.py - Fabricate.IO
    This is a demo python file showing what can be done with the debounce_handler.
    The handler prints True when you say "Alexa, device on" and False when you say
    "Alexa, device off".
    If you have two or more Echos, it only handles the one that hears you more clearly.
    You can have an Echo per room and not worry about your handlers triggering for
    those other rooms.
    The IP of the triggering Echo is also passed into the act() function, so you can
    do different things based on which Echo triggered the handler.
"""

import fauxmo
import logging
import time
import RPi.GPIO as GPIO

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

REMOTE_GPIO = 9

class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"My Car": 52000}

    def act(self, client_address, state):
        print "State", state, "from client @", client_address
        changeIOState(state)
        return True

def changeIOState(state): ##simulate long key press
    if state:
        GPIO.output(REMOTE_GPIO,GPIO.HIGH)
        time.sleep(4)
    else:
        GPIO.output(REMOTE_GPIO,GPIO.HIGH) ## check this if you two buttons to turn ON/OFF
        time.sleep(4)

    GPIO.output(REMOTE_GPIO,GPIO.LOW)

def setupIO():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(REMOTE_GPIO,GPIO.OUT)
    GPIO.output(REMOTE_GPIO,GPIO.LOW) #make sure the car is off

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    setupIO()
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
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
