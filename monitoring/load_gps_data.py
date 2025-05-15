#!/usr/bin/env python3
"""
Script to load GPS data into InfluxDB for visualization with Grafana.
"""
import os
import glob
import json
import datetime
import argparse
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection parameters
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-auth-token"
INFLUXDB_ORG = "ie421"
INFLUXDB_BUCKET = "gps_data"

def parse_gps_log(file_path):
    """Parse GPS log file and return data points."""
    data_points = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    # Each line is a JSON object
                    data = json.loads(line)
                    
                    # Check if this is a PPS (Pulse Per Second) record
                    if data.get('class') == 'PPS':
                        # Extract timestamp from real_sec and real_nsec
                        real_sec = data.get('real_sec')
                        real_nsec = data.get('real_nsec')
                        clock_sec = data.get('clock_sec')
                        clock_nsec = data.get('clock_nsec')
                        precision = data.get('precision')
                        
                        if real_sec is None:
                            continue
                            
                        # Create timestamp from real_sec
                        timestamp = datetime.datetime.fromtimestamp(real_sec, tz=datetime.timezone.utc).isoformat()
                        
                        # Create a data point for PPS
                        point = Point("pps_data") \
                            .tag("source", os.path.basename(file_path)) \
                            .tag("device", data.get('device', 'unknown')) \
                            .time(timestamp)
                        
                        # Calculate offset between real and clock in nanoseconds
                        if real_sec is not None and clock_sec is not None:
                            # Calculate offset in nanoseconds
                            real_total_ns = real_sec * 1_000_000_000 + (real_nsec or 0)
                            clock_total_ns = clock_sec * 1_000_000_000 + (clock_nsec or 0)
                            offset_ns = clock_total_ns - real_total_ns
                            point = point.field("offset_ns", offset_ns)
                        
                        # Add other PPS fields
                        if precision is not None:
                            point = point.field("precision", precision)
                        if real_nsec is not None:
                            point = point.field("real_nsec", real_nsec)
                        if clock_nsec is not None:
                            point = point.field("clock_nsec", clock_nsec)
                            
                        data_points.append(point)
                    
                    # Check if this is a TPV (Time-Position-Velocity) record
                    elif data.get('class') == 'TPV':
                        # Extract timestamp
                        timestamp = data.get('time')
                        if not timestamp:
                            continue
                            
                        # Extract GPS data
                        latitude = data.get('lat')
                        longitude = data.get('lon')
                        altitude = data.get('altHAE')  # Height above ellipsoid
                        speed = data.get('speed')
                        climb = data.get('climb')
                        track = data.get('track')  # Direction of movement
                        
                        # Create a data point
                        point = Point("gps_location") \
                            .tag("source", os.path.basename(file_path)) \
                            .tag("device", data.get('device', 'unknown')) \
                            .time(timestamp)
                        
                        # Add fields if they exist
                        if latitude is not None:
                            point = point.field("latitude", latitude)
                        if longitude is not None:
                            point = point.field("longitude", longitude)
                        if altitude is not None:
                            point = point.field("altitude", altitude)
                        if speed is not None:
                            point = point.field("speed", speed)
                        if climb is not None:
                            point = point.field("climb", climb)
                        if track is not None:
                            point = point.field("track", track)
                            
                        # Add additional fields that might be useful
                        for field in ['ept', 'epx', 'epy', 'epv', 'mode', 'leapseconds']:
                            if field in data and data[field] is not None:
                                point = point.field(field, data[field])
                                
                        data_points.append(point)
                    
                    # Check if this is a SKY record (satellite information)
                    elif data.get('class') == 'SKY':
                        timestamp = data.get('time')
                        if not timestamp:
                            continue
                            
                        # Create a data point for satellite metrics
                        point = Point("satellite_info") \
                            .tag("source", os.path.basename(file_path)) \
                            .tag("device", data.get('device', 'unknown')) \
                            .time(timestamp)
                        
                        # Add DOP (Dilution of Precision) values
                        for dop_type in ['xdop', 'ydop', 'vdop', 'tdop', 'hdop', 'gdop', 'pdop']:
                            if dop_type in data and data[dop_type] is not None:
                                point = point.field(dop_type, data[dop_type])
                        
                        # Add satellite counts
                        if 'nSat' in data:
                            point = point.field("satellites_visible", data['nSat'])
                        if 'uSat' in data:
                            point = point.field("satellites_used", data['uSat'])
                            
                        data_points.append(point)
                        
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON in {file_path}: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line in {file_path}: {e}")
                    continue
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    
    return data_points

def load_data_to_influxdb(data_points):
    """Load data points into InfluxDB."""
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        try:
            write_api.write(bucket=INFLUXDB_BUCKET, record=data_points)
            print(f"Successfully loaded {len(data_points)} data points to InfluxDB")
        except Exception as e:
            print(f"Error writing to InfluxDB: {e}")

def main():
    parser = argparse.ArgumentParser(description='Load GPS data into InfluxDB')
    parser.add_argument('--log-dir', type=str, default='../gps-logs/json-files',
                        help='Directory containing GPS log files')
    parser.add_argument('--pattern', type=str, default='*.json',
                        help='Pattern to match log files')
    parser.add_argument('--file', type=str, 
                        help='Process a specific file instead of using pattern')
    
    args = parser.parse_args()
    
    # Find all matching log files
    if args.file:
        log_files = [args.file]
        if not os.path.exists(args.file):
            print(f"File not found: {args.file}")
            return
    elif not (log_files := glob.glob(os.path.join(args.log_dir, args.pattern))):
        print(f"No log files found matching pattern {args.pattern} in {args.log_dir}")
        return
    
    print(f"Found {len(log_files)} log files")
    
    # Process each log file
    total_points = 0
    for log_file in log_files:
        print(f"Processing {log_file}...")
        data_points = parse_gps_log(log_file)
        
        if data_points:
            print(f"  Found {len(data_points)} data points")
            load_data_to_influxdb(data_points)
            total_points += len(data_points)
        else:
            print(f"  No valid data points found in {log_file}")
    
    print(f"Total data points loaded: {total_points}")
    print("You can now access Grafana at http://localhost:3001 to create dashboards")
    print("Username: admin, Password: admin")

if __name__ == "__main__":
    main()
