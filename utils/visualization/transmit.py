import json
import time

import influx_client


def regex_filter():
    pass


def read_from_csv_file(file_name):
    write_json = []
    # start_timestamp_value = int(round(time.time() * 1000))
    real_timestamp_value = int(round(1616914800 * 1000))
    start_timestamp_value = 0

    with open('../../csv/' + file_name + '.csv') as f:
        first_line = f.readline()
        field_name = first_line.split(",")[0]
        for index, line in enumerate(f.readlines()):
            if index == 0:
                start_timestamp_value = int(float(line.split(",")[1].strip()) * 10)
            field_value = float(line.split(",")[0].strip())
            # timestamp_value = int((int(float(line.split(",")[1].strip()) * 10) + start_timestamp_value) / 1000)
            timestamp_value = (int(float(line.split(",")[1].strip()) * 10 - start_timestamp_value) + real_timestamp_value) * 1000000
            print(timestamp_value)
            print(field_value)

            write_json.append({
                "measurement": file_name,
                "time": timestamp_value,
                "fields": {
                    field_name: field_value,
                    "field_unit": "%"
                }
            })

    return write_json



if __name__ == '__main__':
    file_name = "29_6"
    write_json = read_from_csv_file(file_name)
    database_name = "drop_rate"

    client = influx_client.InfluxClient(database_name)
    client.create_database(database_name)
    client.write_into_database(write_json)

