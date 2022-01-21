
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS

# TODO: We should be using with-statement to guard against problems

class InfluxWriter:

    def __init__(self, influxUrl: str, influxOrg: str, influxToken: str):
        self._url = influxUrl
        self._org = influxOrg
        self._token = influxToken
    

    def connect(self):
        # TODO: Error handling
        # Create client if needed
        if (not hasattr(self, "_client")):
            self._client = InfluxDBClient(url=self._url, token=self._token, org=self._org)

        # Create async writer if needed
        if (not hasattr(self, "_writer")):
            # TODO: Set success, error and retry callbacks
            self._writer = self._client.write_api(write_options=ASYNCHRONOUS)


    def writeAsync(self, bucket: str, dictionary: dict):
        if (not hasattr(self, "_writer")):
            raise Exception("Writer not connected to InfluxDB")

        self._writer.write(bucket, self._org, dictionary)

    