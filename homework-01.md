Homework for 1/27/2025

# Question 1:

> docker run -it --entrypoint=bash python:3.12.8
Once inside the bash entrypoint:
> pip --version
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)

# Question 2. Understanding Docker networking and docker-compose
Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

it'd be postgres:5432 because the container name is going to be the name found by te dockerized pgadmin, not localhost.


Some scratch...

docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="some user" \
    -e PGADMIN_DEFAULT_PASSWORD="some pass" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4

docker network create pg-network

docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v C:/Users/alecr/ny_taxi_main:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg_database \
    postgres:17


URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

docker build -t taxi_ingest:v007 .

URL="https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

docker run -it \
    --network=pg-network \
    taxi_ingest:v007 \
        --user=root \
        --password=root \
        --host=pg_database \
        --port=5432 \
        --db=ny_taxi \
        --tb=zones \
        --url=${URL}


##### Start of homework

# Question 3:

SELECT 
  COUNT(1) AS total_trips,
  CASE 
    WHEN gtt.trip_distance <= 1 THEN 'less than 1 mile'
    WHEN gtt.trip_distance > 1 AND gtt.trip_distance <= 3 THEN '1 to 3 miles'
    WHEN gtt.trip_distance > 3 AND gtt.trip_distance <= 7 THEN '3 to 7 miles'
    WHEN gtt.trip_distance > 7 AND gtt.trip_distance <= 10 THEN '7 to 10 miles'
	WHEN gtt.trip_distance > 10 THEN '10+ miles'
  END AS trip_distance_group
FROM green_taxi_trips gtt
WHERE (CAST(gtt.lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-11-01')
  AND (CAST(gtt.lpep_dropoff_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-11-01')
GROUP BY 
  CASE 
    WHEN gtt.trip_distance <= 1 THEN 'less than 1 mile'
    WHEN gtt.trip_distance > 1 AND gtt.trip_distance <= 3 THEN '1 to 3 miles'
    WHEN gtt.trip_distance > 3 AND gtt.trip_distance <= 7 THEN '3 to 7 miles'
    WHEN gtt.trip_distance > 7 AND gtt.trip_distance <= 10 THEN '7 to 10 miles'
	WHEN gtt.trip_distance > 10 THEN '10+ miles'
END;

# Question 4:

SELECT MAX(gtt.trip_distance), CAST(gtt.lpep_pickup_datetime AS DATE) as pickup_time from green_taxi_trips gtt
GROUP BY pickup_time
ORDER BY 1 DESC
LIMIT 1;

# Question 5:

SELECT z."Zone", SUM(gtt.total_amount) as total_amount_in_zone FROM green_taxi_trips gtt
JOIN zones z
ON gtt."PULocationID" = z."LocationID"
WHERE CAST(gtt.lpep_pickup_datetime as date) = '2019-10-18'
GROUP BY "Zone"
ORDER BY total_amount_in_zone DESC
limit 3;

# Question 6:

SELECT 
    zdropoff."Zone", 
    gtt.tip_amount AS Tip
FROM 
    green_taxi_trips gtt
JOIN 
    zones zpickup ON gtt."PULocationID" = zpickup."LocationID"
JOIN 
    zones zdropoff ON gtt."DOLocationID" = zdropoff."LocationID"
WHERE 
    zpickup."Zone" = 'East Harlem North'
    AND CAST(gtt.lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31'
ORDER BY 
    gtt.tip_amount DESC
LIMIT 1;
