#!/bin/bash

# This script tests the live GPS data by querying InfluxDB directly

# InfluxDB parameters
INFLUXDB_URL="http://localhost:8086"
INFLUXDB_TOKEN="my-super-secret-auth-token"
INFLUXDB_ORG="ie421"
INFLUXDB_BUCKET="gps_data"

# Function to query InfluxDB using the Flux query language
query_influxdb() {
    local query="$1"
    
    curl -s -G $INFLUXDB_URL/api/v2/query \
        -H "Authorization: Token $INFLUXDB_TOKEN" \
        -H "Content-Type: application/json" \
        -H "Accept: application/csv" \
        --data-urlencode "org=$INFLUXDB_ORG" \
        --data-urlencode "query=$query"
}

# Query for the latest GPS location data
echo "=== Latest GPS Location Data ==="
query_influxdb "from(bucket: \"$INFLUXDB_BUCKET\")
  |> range(start: -1m)
  |> filter(fn: (r) => r._measurement == \"gps_location\")
  |> filter(fn: (r) => r._field == \"lat\" or r._field == \"lon\" or r._field == \"altitude\")
  |> last()
  |> yield(name: \"last\")"

echo -e "\n=== Latest Satellite Data ==="
query_influxdb "from(bucket: \"$INFLUXDB_BUCKET\")
  |> range(start: -1m)
  |> filter(fn: (r) => r._measurement == \"satellite_info\")
  |> filter(fn: (r) => r._field == \"satellites_visible\" or r._field == \"satellites_used\")
  |> last()
  |> yield(name: \"last\")"

echo -e "\n=== Latest PPS Data ==="
query_influxdb "from(bucket: \"$INFLUXDB_BUCKET\")
  |> range(start: -1m)
  |> filter(fn: (r) => r._measurement == \"pps_data\")
  |> filter(fn: (r) => r._field == \"offset_ns\")
  |> last()
  |> yield(name: \"last\")"

echo -e "\n=== Data Points in the Last Minute ==="
query_influxdb "from(bucket: \"$INFLUXDB_BUCKET\")
  |> range(start: -1m)
  |> count()
  |> yield(name: \"count\")"
