global DEBUG,CODE_PATH,DATASET_PATH,INFLUX_USER,INFLUX_PASS,INFLUX_URI,INFLUX_ORG,INFLUX_TOKEN,INFLUX_BUCKET,MYSQL_HOST,MYSQL_DB,MYSQL_USER,MYSQL_PASS,JAVA_PATH,CQ1,CQ2,CQ3,CQ5,CQ6

DEBUG = False
#DIRECTORIES PATHS
CODE_PATH = "C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\python\\"
DATASET_PATH = "C:\\_Workspace\\Kaire\\python\\ds\\"
JAVA_PATH = "C:\\Program Files\\Java\\jdk-19.0.1\\bin\\java.exe"
WORKERS_FILE = DATASET_PATH + "workers.csv"
ENV_FILE = DATASET_PATH + "environment.csv"

#INFLUXDB DATA
INFLUX_USER = "admin"
INFLUX_PASS = "admin123"
INFLUX_URI = "http://localhost:8086"
INFLUX_ORG = "kaire"
INFLUX_TOKEN = "xbvFfne7q1pC6ho94-T0A2_bUuXTR-psz4UpZZvV69XxutkRcd2hcAyVu8BQwdeFxFxburft7gtVIxJyQJAoFw=="
INFLUX_BUCKET = "kaire"

#ASUS_NOTE
#INFLUX_URI = "http://localhost:8086"
#INFLUX_ORG = "master"
#INFLUX_TOKEN = "HXMSb1ELN07jeL_6QYTTJPFoJtzzHozR2G7FnmoynrsSfwp79fPgpZgK-xjwW5oiOwWi4T_YIUKugLOCC6b6tQ=="


#MYSQLDB DATA
MYSQL_HOST = "127.0.0.1"
MYSQL_DB = "kaire"
MYSQL_USER = "root"
MYSQL_PASS = "admin"


#HRV PARAMETERS
global RR_MIN_NORMAL,RR_MAX_NORMAL,RR_MIN,RR_MAX
RR_MIN_NORMAL = 750
RR_MAX_NORMAL = 850
RR_MIN_STRESS = 775
RR_MAX_STRESS = 800