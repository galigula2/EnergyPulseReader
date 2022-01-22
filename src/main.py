from gpio_pulse_reader import startMonitoringPulses
from influx_writer import writeToInfluxAsync
from pulse_accumulator import PulseAccumulator
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read('../energypulsereader.ini')
BCM_CHANNEL = config.getint("PulseReader", "BCM_CHANNEL")
RECORDING_INTERVAL_SECONDS = config.getfloat("PulseReader", "RECORDING_INTERVAL_SECONDS")
PULSES_PER_KWH = config.getint("PulseReader", "PULSES_PER_KWH")
BOUNCE_MS = config.getint("PulseReader", "BOUNCE_MS")
MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES = config.getint("Measurements", "MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES")
INFLUXDB_URL=config.get("InfluxDB", "URL")
INFLUXDB_ORG=config.get("InfluxDB", "ORG")
INFLUXDB_BUCKET = config.get("InfluxDB", "BUCKET")
INFLUXDB_TOKEN=config.get("InfluxDB", "TOKEN")

# Helpers
SECONDS_PER_HOUR = 60*60

# Prepare accumulator to count pulses towards accumulation period  
pulseAccumulator = PulseAccumulator(60 * MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES)

# Reader side callback
def reportUsage(pulseCount: int, pulseIntervalSeconds: float):
    # Keep track of total pulses for the accumulation period
    global pulseAccumulator
    accPeriodEndedWithPulseCount = pulseAccumulator.accumulate(pulseCount)

    # Calculate current power and send it directly to visualization through MQTT
    power = SECONDS_PER_HOUR / (pulseIntervalSeconds * PULSES_PER_KWH)
    print(f"Power: {power:0.1f} kW     Pulses: {pulseCount}    PulseInterval: {int(pulseIntervalSeconds*1000)}ms")
      
    # If the accumulation period has ended store energy consumpton to long term database
    if accPeriodEndedWithPulseCount is not None:
        # Report details
        totalEnergyInAccumulationPeriod = accPeriodEndedWithPulseCount / PULSES_PER_KWH
        print(f"Total: {totalEnergyInAccumulationPeriod:0.3f} kWh spent in last {MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES} minutes") 

        # Write to long term storage
        writeToInfluxAsync(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_BUCKET, {
            "measurement": "electricity",
            "fields": {
                f"consumption_{MEAS_ACCUMULATED_ENERGY_REPORTING_INTERVAL_MINUTES}min_Wh": int(totalEnergyInAccumulationPeriod * 1000) 
            }
        })



if __name__ == '__main__':

    # Start monitoring
    startMonitoringPulses(reportUsage, RECORDING_INTERVAL_SECONDS, BCM_CHANNEL, BOUNCE_MS)
