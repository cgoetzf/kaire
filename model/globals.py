global CODE_PATH,DATASET_PATH,INFLUX_USER,INFLUX_PASS,INFLUX_URI,INFLUX_ORG,INFLUX_TOKEN,INFLUX_BUCKET,MYSQL_HOST,MYSQL_DB,MYSQL_USER,MYSQL_PASS,JAVA_PATH,CQ1,CQ2,CQ3,CQ5,CQ6

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
global COEFFICIENT,IBI_MIN_NORMAL,IBI_MAX_NORMAL,IBI_MIN,IBI_MAX
COEFFICIENT = 10
IBI_MIN_NORMAL = 750
IBI_MAX_NORMAL = 850
IBI_MIN_STRESS = 775
IBI_MAX_STRESS = 800


#SPARQL QUERIES
#Which possible stressors are identified for each location and time?
CQ1 = """
PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/1/kaire#>
SELECT ?worker ?psychoCondition ?location ?day ?hour ?stressor
WHERE {
    ?context a :Worker . ?context :targets ?worker . ?context :locatedAt ?location .
    ?context :feels ?psychoCondition . ?context :stressedBy ?stressor .
     ?context :hasDayOfWeek ?day . ?context :hasHour ?hour
}
ORDER BY ?worker
"""
#How much time do possible stressors share with the worker during their activities?
CQ2 = """
PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/1/kaire#>
SELECT 
    ?worker ?psychoCondition ?location ?activity ?duration ?stressor ?shared_time
WHERE {
    ?context a :Worker .
    ?context :targets ?worker .
    ?context :feels ?psychoCondition .
    ?context :hasDuration ?duration .
    ?context :hasTsMin ?timestamp .
    ?context :hasTsMax ?tsMax .
    ?context :performs ?activity . 
    ?context :locatedAt ?location .
    ?context :stressedBy ?stressor .
    ?context :stressedByContext ?contextStressor .
    ?contextStressor :hasTsMin ?tsMinStressor .
    ?contextStressor :hasTsMax ?tsMaxStressor .
	BIND ( 
	(IF(?tsMaxStressor < ?tsMax, ?tsMaxStressor - ?timestamp, 
        IF(?tsMaxStressor > ?tsMax, ?tsMax - ?timestamp,0))                 
	     ) AS ?shared_time
	)
}
ORDER BY ?worker
"""
#How often are environmental conditions present in stressful situations?
CQ3 = """
PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/1/kaire#>
SELECT ?location ?workCondition (count(?stressed) AS ?stressedTimes)
WHERE {
    ?context a :Worker .
    ?context :locatedAt ?location .
    ?context :hasEnvContext ?envContext .
    ?envContext :hasCondition ?workCondition
    OPTIONAL {
        ?context :feels :Stressed .
        ?context :targets ?stressed .
    }
}
GROUP BY ?location ?workCondition
ORDER BY ?location
"""
#Who is present in the workgroups in stressful situations?
CQ4 = """
PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/1/kaire#>
SELECT ?workgroup ?worker (count(?env) AS ?stressedTimes)
WHERE {
    ?context a :Worker .
    ?context :hasId ?id .
    ?context :targets ?worker .
    ?context :locatedAt ?workgroup .
    ?context :hasEnvContext ?env .
    ?context :feels :Stressed .
    ?context :targets ?stressed .
}
GROUP BY ?worker ?workgroup
ORDER BY ?workgroup ?id

"""

CQ7 = """
PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/1/kaire#>
SELECT 
   ?id ?stress ?locationId ?activity ?timestamp ?duration ?day ?hour ?hrv_mean ?hrv_sd ?stressorId ?shared_time ?env_cond ?cond
WHERE {
    ?context :hasId ?id . ?context a :Worker . ?context :targets ?worker . ?context :hasLocationId ?locationId .
    ?context :hasDuration ?duration . ?context :hasDayOfWeek ?day . ?context :hasHour ?hour .
    ?context :hasTsMin ?timestamp .	?context :hasTsMax ?tsMax . ?context :performs ?task . 
    ?context :hasHRV ?hrv_mean . ?context :hasHRVsd ?hrv_sd . ?context :hasStressIndex ?stress .
    OPTIONAL {
        ?context :stressedBy ?stressor . ?context :stressedByContext ?contextStressor . ?contextStressor :hasId ?stressorId .
        ?contextStressor :hasTsMin ?tsMinStressor . ?contextStressor :hasTsMax ?tsMaxStressor .
    } .
    BIND( 
        (   
            IF(?tsMaxStressor < ?tsMax && ?tsMinStressor < ?timestamp, ?tsMaxStressor - ?timestamp, 
                IF(?tsMaxStressor > ?tsMax && ?tsMinStressor < ?timestamp, ?tsMax - ?timestamp,
                    IF(?tsMaxStressor < ?tsMax && ?tsMinStressor > ?timestamp, ?tsMaxStressor - ?tsMinStressor, 
                       IF(?tsMaxStressor > ?tsMax && ?tsMinStressor > ?timestamp, ?tsMax - ?tsMinStressor,0))))
        ) AS ?shared_time
    ) .
    BIND (
            IF ( ?task = :WorkTask, 1,
                IF ( ?task = :Meeting, -1,
	   0 )
             ) AS ?activity          
    )  .
    OPTIONAL { ?context :hasEnvContext ?envContext . ?envContext :hasCondition ?cond } .
    BIND ( IF ( BOUND(?cond) , 1, 0) AS ?env_cond ) .
    BIND ( IF ( BOUND(?stressorId),?stressorId,0) AS ?stId )
}
ORDER BY ?id ?timestamp
"""

CQ8 = """
PREFIX : <http://www.semanticweb.org/carlos/ontologies/2022/1/kaire#>
SELECT 
    ?locationId  ?date ?day ?hour ?id ?stress ?shared_time
WHERE {
    ?context :hasId ?id . ?context a :Worker . ?context :targets ?worker . 
    ?context :hasTsMin ?timestamp . ?context :hasTsMax ?tsMax .
    ?context :hasDayOfWeek ?day . ?context :hasHour ?hour .
    ?context :hasStressIndex ?stress . ?context :hasLocationId ?locationId .
    ?context :hasEnvContext ?envContext . ?envContext :hasTsDate ?date .
    ?envContext :hasTsMin ?tsMinEnv . ?envContext :hasTsMax ?tsMaxEnv .	
    BIND ( 
        (   
            IF(?tsMaxEnv < ?tsMax && ?tsMinEnv < ?timestamp, ?tsMaxEnv - ?timestamp, 
                IF(?tsMaxEnv > ?tsMax && ?tsMinEnv < ?timestamp, ?tsMax - ?timestamp,
                    IF(?tsMaxEnv < ?tsMax && ?tsMinEnv > ?timestamp, ?tsMaxEnv - ?tsMinEnv, 
                        IF(?tsMaxEnv > ?tsMax && ?tsMinEnv > ?timestamp, ?tsMax - ?tsMinEnv,0))))
        ) AS ?shared_time
    )
}
ORDER BY ?locationId ?date ?day ?hour
"""