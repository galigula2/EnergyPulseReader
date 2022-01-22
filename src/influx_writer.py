
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS

def writeToInfluxAsync(influxUrl: str, influxOrg: str, influxToken: str, bucket: str, dictionary: dict):
    with InfluxDBClient(url=influxUrl, token=influxToken, org=influxOrg) as influx: 
        writer = influx.write_api(write_options=ASYNCHRONOUS)
        writer.write(bucket, influxOrg, dictionary)
