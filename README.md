# EnergyPulseReader

Python code for an application reading pulses from Raspberry Pi digital input signals and forwarding calculated energy consumptions to InfluxDB.

TODO: Push instant power to grafana through MQTT
TODO: below


### Features

TODO

### Requirements

TODO

### Building

TODO

### Installation

TODO

### Configuration

TODO

### Running

TODO

### Docker

Build image with `docker build -t energy-pulse-reader .`

Need to be run with --privileged because we need access to GPIO memory sections

You need to mount the ini-file as /pulsereader/energypulsereader.ini when running the container!

