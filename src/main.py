from gpio_pulse_reader import startMonitoringPulses
from influx_writer import InfluxWriter
from pulse_accumulator import PulseAccumulator
import time

# Pulse reader settings
BCM_CHANNEL = 24
RECORDING_INTERVAL_SECONDS = 5.0
PULSES_PER_KWH = 10000
BOUNCE_MS = 5 # 3ms seems to be just working for me, 2ms was too little, more in theory is a bit safer but loses pulses on higher consuption
              # 5ms bounce would mean maximum of 200 pulses per second -~> 71 kW consuption, it should never get that high in the house

# Measurement settings
MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES = 1

# InfluxDB settings
INFLUXDB_URL="http://localhost:8086"
INFLUXDB_ORG="Talonvalvonta"
INFLUXDB_BUCKET = "testi"
INFLUXDB_TOKEN="29yLn5IdQN3qTE0EwZhTZ_LKInnQyZpDsFzRp_i4JdNCBXCRqpHS_2pnTDvXRprdwY__X5uvem5dtk3OgLcxlA==" # Test token, will be removed later

# Helpers
SECONDS_PER_HOUR = 60*60

# Connect to influxdb for long term storage
influx = InfluxWriter(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_TOKEN)
influx.connect()

# Prepare accumulator to count pulses towards accumulation period  
pulseAccumulator = PulseAccumulator(60 * MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES)

# Reader side callback
def reportUsage(pulseCount: int, pulseIntervalSeconds: float):
    # Keep track of total pulses for the accumulation period
    global pulseAccumulator
    accPeriodEndedWithPulseCount = pulseAccumulator.accumulate(pulseCount)

    # Calculate current power and send it directly to visualization
    power = SECONDS_PER_HOUR / (pulseIntervalSeconds * PULSES_PER_KWH)
    print(f"Power: {power:0.1f} kW     Pulses: {pulseCount}    PulseInterval: {int(pulseIntervalSeconds*1000)}ms")
      
    # If the accumulation period has ended store energy consumpton to long term database
    if accPeriodEndedWithPulseCount is not None:
        # Report details
        totalEnergyInAccumulationPeriod = accPeriodEndedWithPulseCount / PULSES_PER_KWH
        print(f"Total: {totalEnergyInAccumulationPeriod:0.3f} kWh spent in last {MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES} minutes") 

        # Write to long term storage
        global influx
        influx.writeAsync(INFLUXDB_BUCKET, {
            "measurement": "testimittaus2",
            "fields": {
                f"electricityTotal_{MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES}min_Wh": int(totalEnergyInAccumulationPeriod * 1000) 
            }
        })



if __name__ == '__main__':

    # Start monitoring
    startMonitoringPulses(reportUsage, RECORDING_INTERVAL_SECONDS, BCM_CHANNEL, BOUNCE_MS)
