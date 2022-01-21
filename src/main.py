from gpio_pulse_reader import startMonitoringPulses

# Configurations
# TODO: read from config file
BCM_CHANNEL = 24
RECORDING_INTERVAL_SECONDS = 5.0
PULSES_PER_KWH = 10000
BOUNCE_MS = 5 # 3ms seems to be just working for me, 2ms was too little, more in theory is a bit safer but loses pulses on higher consuption
              # 5ms bounce would mean maximum of 200 pulses per second -~> 71 kW consuption, it should never get that high in the house

# Helpers
SECONDS_PER_HOUR = 60*60

# Just print out pulses
totalPulses = 0
def reportUsage(pulseCount: int, pulseIntervalSeconds: float):
    
    # Keep track of total pulses from start of measurement
    global totalPulses
    totalPulses += pulseCount

    # Calculate current power and total enerygy consuption
    power = SECONDS_PER_HOUR / (pulseIntervalSeconds * PULSES_PER_KWH)
    totalEnergy = totalPulses / PULSES_PER_KWH

    # Report details
    print(f"Power: {power:0.1f} kW     Total: {totalEnergy:0.3f} kWh    Pulses: {pulseCount}    PulseInterval: {int(pulseIntervalSeconds*1000)}ms")


if __name__ == '__main__':

    # Start monitoring
    startMonitoringPulses(reportUsage, RECORDING_INTERVAL_SECONDS, BCM_CHANNEL, BOUNCE_MS)
