from influxdb import InfluxDBClient

import contant as constant


class InfluxClient:

    def __init__(self, database_name):
        self.client = self._create_connection(database_name)

    def _create_connection(self, database_name):
        client = InfluxDBClient(host=constant.influx_server_ip, port=constant.influx_server_port, database=database_name)
        return client

    def create_database(self, database_name):
        self.client.create_database(database_name)

    def write_into_database(self, write_json):
        self.client.write_points(write_json)
