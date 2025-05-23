#!/usr/bin/env python3
"""
Debug script to directly query InfluxDB and display results.
This bypasses Grafana to help diagnose data issues.
"""
import sys
from influxdb_client import InfluxDBClient
from tabulate import tabulate

# InfluxDB connection parameters
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-auth-token"
INFLUXDB_ORG = "ie421"
INFLUXDB_BUCKET = "gps_data"

def main():
    print("Connecting to InfluxDB...")
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    query_api = client.query_api()
    
    # Get list of measurements
    print("\nQuerying available measurements...")
    query = f'''
    import "influxdata/influxdb/schema"
    schema.measurements(bucket: "{INFLUXDB_BUCKET}")
    '''
    try:
        result = query_api.query(query)
        if not result:
            print("No measurements found in the database!")
            return
        
        measurements = [record.values.get("_value") for table in result for record in table.records]
        print(f"Found {len(measurements)} measurements: {', '.join(measurements)}")
        
        # For each measurement, get a sample of data
        for measurement in measurements:
            print(f"\n=== Sample data from measurement: {measurement} ===")
            query = f'''
            from(bucket: "{INFLUXDB_BUCKET}")
              |> range(start: -30d)
              |> filter(fn: (r) => r._measurement == "{measurement}")
              |> limit(n: 5)
            '''
            
            try:
                result = query_api.query(query)
                if not result:
                    print(f"No data found in measurement {measurement}")
                    continue
                
                # Format the results as a table
                headers = ["Time", "Field", "Value", "Tags"]
                rows = []
                
                for table in result:
                    for record in table.records:
                        # Extract tags excluding standard ones
                        tags = {k: v for k, v in record.values.items() 
                               if k not in ["_time", "_value", "_field", "_measurement", "_start", "_stop"]}
                        
                        rows.append([
                            record.get_time().isoformat(),
                            record.get_field(),
                            record.get_value(),
                            str(tags)
                        ])
                
                print(tabulate(rows, headers=headers, tablefmt="grid"))
                print(f"Total records: {len(rows)}")
                
            except Exception as e:
                print(f"Error querying measurement {measurement}: {e}")
    
    except Exception as e:
        print(f"Error querying measurements: {e}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
