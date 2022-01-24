# Helper for reading pulses and getting pulse count during measuring period and time difference between pulses
# TODO: Add support to read multiple GPIO's at the same time? 

import RPi.GPIO as GPIO
import time
from typing import Callable

def startMonitoringPulses(callback: Callable[[int, float], None], reportingPeriodSeconds: float, rpiBcmPin: int, bounceMilliseconds: int):
    """Starts listening to pulses in given Raspberry Pi input channel

    Parameters
    ----------
    callback: Callable[[int, float], None]
        Callback for getting back energy levels, gets number of pulses in last reporting period (int) and average time difference between pulses in last reporting period (float)
        TODO: How to handle long running callbacks?
    reportingPeriodSeconds : float
        Number of seconds before reporting number of pulses and time diff between pulses
    rpiBcmPin : int
        Channel number in Raspberry Pi BCM/GPIO convetion
    bounceMilliseconds : int
        Number of milliseconds to wait for signal stabilization before pulse is counter again. Helps to avoid counting pulses twice

    Returns
    -------
    Nothing
    """    
    try:
        # Prepare channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rpiBcmPin, GPIO.IN)

        # Prepare callback for counting pulses
        pulseCount = 0
        def pulseCounterInterrupt(channel):
            nonlocal pulseCount
            pulseCount += 1

        # Start listening
        GPIO.add_event_detect(rpiBcmPin, GPIO.RISING, callback=pulseCounterInterrupt, bouncetime=bounceMilliseconds)  # add rising edge detection on a channel (with small bounce to not register flashes twice)

        print(f"Start monitoring pin 'GPIO{rpiBcmPin}' on {reportingPeriodSeconds}s refresh rate with {bounceMilliseconds}ms bouncetime")
        while True:
            # Sleep for interval (note: this is not accurate since all the steps in while after this should reduce the sleep amount, not sure how relevant this is)
            time.sleep(reportingPeriodSeconds)
           
            # Capture last interval pulse count and zero the counter
            lastIntervalPulses = pulseCount
            pulseCount = 0

            # Calculate pulse difference in seconds
            pulseInterval = reportingPeriodSeconds / lastIntervalPulses
            
            # Report via callback
            callback(lastIntervalPulses, pulseInterval) 


    finally:
        GPIO.cleanup()
