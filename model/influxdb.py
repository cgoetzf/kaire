import globals as g
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = g.INFLUX_TOKEN
org = g.INFLUX_ORG
bucket = g.INFLUX_BUCKET

client = InfluxDBClient(url=g.INFLUX_URI, token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

#data = "mem,host=host2 used_percent=26.43234543"
#write_api.write(bucket, org, data)


#sequence = ["mem,host=host2 used_percent=21.43234543",
#            "mem,host=host2 available_percent=11.856523"]
#write_api.write(bucket, org, sequence)

#import csv
#with open('EDA_Test.csv', newline='') as csvfile:
#	reader = csv.DictReader(csvfile)
#	for row in reader:
#		print(row)
#		print(row[0], row[1])
	#	point = Point("eda").tag("s", row['Subject']).field("us", row['Measure']).timestamp(row['Timestamp'])
	#	write_api.write(bucket, org, point)

import pandas as pd

df = pd.read_csv ('stress.csv', sep=r'\s*;\s*',header=0, encoding='ascii', engine='python')
df = df.reset_index()  # make sure indexes pair with number of rows
for index, row in df.iterrows():
	#print(row['Subject'])
	point = Point("stress").tag("sub", row['subject']).field("level", row['measure']).time(row['timestamp'], WritePrecision.S)
	write_api.write(bucket, org, point)
    #print(row['c1'], row['c2'])