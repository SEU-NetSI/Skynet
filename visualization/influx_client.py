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

    def write_points(self, write_json):
        self.client.write_points(write_json, time_precision="ms")

    def write_a_point(self, table_name, timestamp_in_ms, fields):
        write_json = []
        write_json.append({
            "measurement": table_name,
            "time": timestamp_in_ms,
            "fields": fields
        })
        self.write_points(write_json)

    def write_some_points(self, table_name, timestamp_in_ms_list, fields_list):
        write_json = []
        for index, timestamp in timestamp_in_ms_list:
            write_json.append({
                "measurement": table_name,
                "time": timestamp,
                "fields": fields_list[index]
            })
        self.write_points(write_json)


def get_influx_client(database_name):
    return InfluxClient(database_name)
