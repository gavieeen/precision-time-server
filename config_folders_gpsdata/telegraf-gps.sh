#!/bin/bash

# Fetch GPS data
DATA=$(gpspipe -w -n 10 | jq -c 'select(.class=="TPV") | {lat: .lat, lon: .lon, alt: .alt, eph: .eph, sep: .sep}' | tail -n 1)

LAT=$(echo "$DATA" | jq -r .lat)
LON=$(echo "$DATA" | jq -r .lon)
ALT=$(echo "$DATA" | jq -r .alt)
EPH=$(echo "$DATA" | jq -r .eph)
SEP=$(echo "$DATA" | jq -r .sep)

# If no data found, don't print empty metrics
if [[ -n "$LAT" && "$LAT" != "null" ]]; then
    echo "gps_status,device=ttyACM0 lat=$LAT,lon=$LON,alt=$ALT,eph=$EPH,sep=$SEP,status=1"
fi

