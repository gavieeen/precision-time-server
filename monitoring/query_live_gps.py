#!/usr/bin/env python3
"""
Script to query and display live GPS data from InfluxDB
"""
import datetime
from influxdb_client import InfluxDBClient
from tabulate import tabulate

# InfluxDB connection parameters
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-auth-token"
INFLUXDB_ORG = "ie421"
INFLUXDB_BUCKET = "gps_data"

def query_influxdb(query):
    """Execute a Flux query against InfluxDB"""
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    query_api = client.query_api()
    
    try:
        result = query_api.query(query=query)
        return result
    except Exception as e:
        print(f"Error querying InfluxDB: {e}")
        return None
    finally:
        client.close()

def format_results(tables):
    """Format query results into a readable table"""
    if not tables:
        return "No data found"
    
    all_rows = []
    headers = []
    
    for table in tables:
        for record in table.records:
            row = {}
            for key, value in record.values.items():
                if key not in ["result", "table", "_start", "_stop"]:
                    row[key] = value
            
            # Get timestamp
            if "_time" in row:
                row["time"] = row["_time"].strftime("%Y-%m-%d %H:%M:%S")
                del row["_time"]
            
            all_rows.append(row)
            
            # Get headers from first row
            if not headers and row:
                headers = list(row.keys())
    
    if not all_rows:
        return "No data found"
    
    # Convert to list of lists for tabulate
    table_data = []
    for row in all_rows:
        table_row = []
        for header in headers:
            table_row.append(row.get(header, ""))
        table_data.append(table_row)
    
    return tabulate(table_data, headers=headers, tablefmt="grid")

def main():
    print(f"Querying InfluxDB at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Query GPS location data
    print("\n=== Latest GPS Location Data ===")
    query = f"""
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -1m)
      |> filter(fn: (r) => r._measurement == "gps_location")
      |> last()
    """
    results = query_influxdb(query)
    print(format_results(results))
    
    # Query satellite data
    print("\n=== Latest Satellite Data ===")
    query = f"""
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -1m)
      |> filter(fn: (r) => r._measurement == "satellite_info")
      |> last()
    """
    results = query_influxdb(query)
    print(format_results(results))
    
    # Query PPS data
    print("\n=== Latest PPS Data ===")
    query = f"""
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -1m)
      |> filter(fn: (r) => r._measurement == "pps_data")
      |> last()
    """
    results = query_influxdb(query)
    print(format_results(results))
    
    # Count data points in the last minute
    print("\n=== Data Points in the Last Minute ===")
    query = f"""
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -1m)
      |> count()
    """
    results = query_influxdb(query)
    print(format_results(results))

if __name__ == "__main__":
    main()
