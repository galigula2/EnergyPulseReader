
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS

# TODO: Log error on problems

def testConnectionToInflux(influxUrl: str, influxOrg: str, influxToken: str, bucketName: str) -> bool:
    with InfluxDBClient(url=influxUrl, token=influxToken, org=influxOrg) as influx: 
        bucket = influx.buckets_api().find_bucket_by_name(bucketName)
        if (bucket is not None):
            print(f"Successfully read bucket info from InfluxDB. influxUrl:'{influxUrl}', influxOrg:'{influxOrg}', bucket:'{bucketName}'" )
            return True
        else:
            print(f"Couldn't read bucket info from InfluxDB. influxUrl:'{influxUrl}', influxOrg:'{influxOrg}', bucket:'{bucketName}'" )
            return False

def writeToInfluxAsync(influxUrl: str, influxOrg: str, influxToken: str, bucket: str, dictionary: dict):
    with InfluxDBClient(url=influxUrl, token=influxToken, org=influxOrg) as influx: 
        writer = influx.write_api(write_options=ASYNCHRONOUS)
        writer.write(bucket, influxOrg, dictionary)
