import globals as g
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = g.INFLUX_TOKEN
org = g.INFLUX_ORG
bucket = g.INFLUX_BUCKET

client = InfluxDBClient(url=g.INFLUX_URI, token=token)

query = 'from(bucket: "kaire")|> range(start: 2017-05-22T00:00:00Z, stop: 2017-05-22T23:00:00Z) |> filter(fn: (r) => r["sub"] == "S2")|> filter(fn: (r) => r["_field"] == "level" or r["_field"] == "uS")|> filter(fn: (r) => r["_measurement"] == "eda" or r["_measurement"] == "stress")|> aggregateWindow(every: 60s, fn: mean, createEmpty: false)|> yield(name: "mean")'
tables = client.query_api().query(query, org=org)
print(tables)

results = []
for table in tables:
  for record in table.records:
    results.append((record.get_field(), record.get_value()))

print(results)