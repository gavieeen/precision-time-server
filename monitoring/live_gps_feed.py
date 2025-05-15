#!/usr/bin/env python3
"""
Script to continuously fetch GPS data and store it in InfluxDB for real-time visualization.
This script simulates a live GPS data feed if no actual GPS device is available.
"""
import os
import time
import json
import datetime
import random
import socket
import argparse
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection parameters
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-auth-token"
INFLUXDB_ORG = "ie421"
INFLUXDB_BUCKET = "gps_data"

# Base GPS coordinates (Chicago area)
BASE_LAT = 41.8806
BASE_LON = -87.6439
BASE_ALT = 262.0

def generate_gps_data():
    """Generate simulated GPS data."""
    # Current time
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Simulate small movements
    lat = BASE_LAT + random.uniform(-0.0001, 0.0001)
    lon = BASE_LON + random.uniform(-0.0001, 0.0001)
    alt = BASE_ALT + random.uniform(-0.5, 0.5)
    
    # Simulate satellite data
    satellites_visible = random.randint(25, 30)
    satellites_used = random.randint(8, 15)
    
    # Simulate DOP values
    hdop = 0.8 + random.uniform(-0.1, 0.1)
    vdop = 1.2 + random.uniform(-0.1, 0.1)
    pdop = 1.5 + random.uniform(-0.1, 0.1)
    gdop = 2.0 + random.uniform(-0.2, 0.2)
    
    # Simulate PPS data
    clock_offset_ns = random.uniform(-50, 50)
    
    return {
        "timestamp": timestamp,
        "lat": lat,
        "lon": lon,
        "alt": alt,
        "satellites_visible": satellites_visible,
        "satellites_used": satellites_used,
        "hdop": hdop,
        "vdop": vdop,
        "pdop": pdop,
        "gdop": gdop,
        "clock_offset_ns": clock_offset_ns
    }

def try_connect_to_gpsd():
    """Try to connect to a running gpsd instance."""
    try:
        # Try to connect to gpsd on the default port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect(("localhost", 2947))
        
        # Send the WATCH command to get JSON data
        sock.send(b'?WATCH={"enable":true,"json":true}\n')
        
        print("Successfully connected to gpsd!")
        return sock
    except (socket.error, socket.timeout):
        print("Could not connect to gpsd, will use simulated data")
        return None

def read_from_gpsd(sock):
    """Read data from gpsd socket."""
    try:
        data = sock.recv(4096).decode('utf-8')
        if not data:
            return None
        
        # gpsd may send multiple JSON objects, split by newlines
        json_objects = []
        for line in data.strip().split('\n'):
            try:
                json_obj = json.loads(line)
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                continue
        
        return json_objects
    except (socket.error, socket.timeout):
        print("Error reading from gpsd")
        return None

def process_gpsd_data(json_objects):
    """Process JSON data from gpsd and create data points."""
    data_points = []
    
    for obj in json_objects:
        class_type = obj.get('class')
        
        if class_type == 'TPV':  # Time-Position-Velocity report
            timestamp = obj.get('time')
            if not timestamp:
                continue
                
            # Create a data point for GPS location
            point = Point("gps_location") \
                .tag("source", "live_feed") \
                .tag("device", obj.get('device', 'unknown')) \
                .time(timestamp)
            
            # Add fields if they exist
            for field in ['lat', 'lon', 'altHAE', 'speed', 'climb', 'track']:
                if field in obj and obj[field] is not None:
                    point = point.field(field, obj[field])
            
            data_points.append(point)
            
        elif class_type == 'SKY':  # Satellite information
            timestamp = obj.get('time')
            if not timestamp:
                continue
                
            # Create a data point for satellite metrics
            point = Point("satellite_info") \
                .tag("source", "live_feed") \
                .tag("device", obj.get('device', 'unknown')) \
                .time(timestamp)
            
            # Add DOP values
            for dop_type in ['xdop', 'ydop', 'vdop', 'tdop', 'hdop', 'gdop', 'pdop']:
                if dop_type in obj and obj[dop_type] is not None:
                    point = point.field(dop_type, obj[dop_type])
            
            # Add satellite counts
            if 'nSat' in obj:
                point = point.field("satellites_visible", obj['nSat'])
            if 'uSat' in obj:
                point = point.field("satellites_used", obj['uSat'])
                
            data_points.append(point)
            
        elif class_type == 'PPS':  # Pulse Per Second
            real_sec = obj.get('real_sec')
            real_nsec = obj.get('real_nsec')
            clock_sec = obj.get('clock_sec')
            clock_nsec = obj.get('clock_nsec')
            
            if real_sec is None:
                continue
                
            # Create timestamp from real_sec
            timestamp = datetime.datetime.fromtimestamp(real_sec, tz=datetime.timezone.utc).isoformat()
            
            # Create a data point for PPS
            point = Point("pps_data") \
                .tag("source", "live_feed") \
                .tag("device", obj.get('device', 'unknown')) \
                .time(timestamp)
            
            # Calculate offset between real and clock in nanoseconds
            if real_sec is not None and clock_sec is not None:
                # Calculate offset in nanoseconds
                real_total_ns = real_sec * 1_000_000_000 + (real_nsec or 0)
                clock_total_ns = clock_sec * 1_000_000_000 + (clock_nsec or 0)
                offset_ns = clock_total_ns - real_total_ns
                point = point.field("offset_ns", offset_ns)
            
            data_points.append(point)
    
    return data_points

def create_simulated_data_points():
    """Create simulated data points."""
    data = generate_gps_data()
    timestamp = data["timestamp"]
    
    data_points = []
    
    # GPS location point
    location_point = Point("gps_location") \
        .tag("source", "simulated") \
        .tag("device", "sim_device") \
        .time(timestamp) \
        .field("lat", data["lat"]) \
        .field("lon", data["lon"]) \
        .field("altitude", data["alt"])
    
    data_points.append(location_point)
    
    # Satellite info point
    satellite_point = Point("satellite_info") \
        .tag("source", "simulated") \
        .tag("device", "sim_device") \
        .time(timestamp) \
        .field("satellites_visible", data["satellites_visible"]) \
        .field("satellites_used", data["satellites_used"]) \
        .field("hdop", data["hdop"]) \
        .field("vdop", data["vdop"]) \
        .field("pdop", data["pdop"]) \
        .field("gdop", data["gdop"])
    
    data_points.append(satellite_point)
    
    # PPS data point
    pps_point = Point("pps_data") \
        .tag("source", "simulated") \
        .tag("device", "sim_device") \
        .time(timestamp) \
        .field("offset_ns", data["clock_offset_ns"])
    
    data_points.append(pps_point)
    
    return data_points

def write_to_influxdb(client, data_points):
    """Write data points to InfluxDB."""
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    try:
        write_api.write(bucket=INFLUXDB_BUCKET, record=data_points)
        return True
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Live GPS data feed for Grafana')
    parser.add_argument('--simulate', action='store_true', 
                        help='Force simulation mode even if gpsd is available')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Update interval in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    print("Starting live GPS data feed...")
    
    # Connect to InfluxDB
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    
    # Try to connect to gpsd if not in simulation mode
    gpsd_socket = None
    if not args.simulate:
        gpsd_socket = try_connect_to_gpsd()
    
    try:
        while True:
            data_points = []
            
            if gpsd_socket:
                # Read from gpsd
                json_objects = read_from_gpsd(gpsd_socket)
                if json_objects:
                    data_points = process_gpsd_data(json_objects)
            
            # If no data from gpsd or in simulation mode, generate simulated data
            if not data_points:
                data_points = create_simulated_data_points()
            
            # Write to InfluxDB
            success = write_to_influxdb(client, data_points)
            
            if success:
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Wrote {len(data_points)} data points to InfluxDB")
            
            # Wait for next update
            time.sleep(args.interval)
    
    except KeyboardInterrupt:
        print("\nStopping live GPS data feed...")
    finally:
        if gpsd_socket:
            gpsd_socket.close()
        print("Live GPS data feed stopped")

if __name__ == "__main__":
    main()
