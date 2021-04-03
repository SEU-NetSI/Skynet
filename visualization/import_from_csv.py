import influx_client


def read_from_csv_file(table_name):
    write_json = []
    start_timestamp_value = 0

    with open('../../csv/' + table_name + '.csv') as f:
        first_line = f.readline()
        field_name = first_line.split(",")[0]
        for index, line in enumerate(f.readlines()):
            if index == 0:
                start_timestamp_value = int(float(line.split(",")[1].strip()))
            field_value = float(line.split(",")[0].strip())
            timestamp_value = int(float(line.split(",")[1].strip()) - start_timestamp_value)

            write_json.append({
                "measurement": table_name,
                "time": timestamp_value,
                "fields": {
                    field_name: field_value,
                    "field_unit": "%"
                }
            })

    return write_json


if __name__ == '__main__':
    file_name = "29_20"
    database_name = "drop_rate"

    client = influx_client.InfluxClient(database_name)
    client.create_database(database_name)
    client.write_points(read_from_csv_file(file_name))
