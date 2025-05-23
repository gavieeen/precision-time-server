#!/usr/bin/env python3
"""
Script to export GPS data from InfluxDB and create visualizations using matplotlib.
This bypasses Grafana completely for a direct visualization approach.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from influxdb_client import InfluxDBClient
import numpy as np

# InfluxDB connection parameters
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-auth-token"
INFLUXDB_ORG = "ie421"
INFLUXDB_BUCKET = "gps_data"

# Output directory for plots
OUTPUT_DIR = "plots"

def query_data(measurement, field, start_time="2025-05-09T00:00:00Z", end_time="2025-05-14T00:00:00Z"):
    """Query data from InfluxDB and return as a pandas DataFrame."""
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    query_api = client.query_api()
    
    query = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: {start_time}, stop: {end_time})
      |> filter(fn: (r) => r._measurement == "{measurement}")
      |> filter(fn: (r) => r._field == "{field}")
    '''
    
    result = query_api.query_data_frame(query)
    
    if result.empty:
        print(f"No data found for {measurement}.{field}")
        return None
    
    # Convert to DataFrame and process
    df = result
    df['_time'] = pd.to_datetime(df['_time'])
    
    return df

def create_time_series_plot(df, field, title, ylabel, filename):
    """Create a time series plot from DataFrame."""
    if df is None or df.empty:
        print(f"No data to plot for {field}")
        return
    
    plt.figure(figsize=(12, 6))
    
    # Group by source (file) and plot each as a separate line
    for source, group in df.groupby('source'):
        plt.plot(group['_time'], group['_value'], label=f"Source: {source}", marker='o', linestyle='-', alpha=0.7)
    
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    print(f"Saved plot to {os.path.join(OUTPUT_DIR, filename)}")
    plt.close()

def create_map_plot(lat_df, lon_df, title, filename):
    """Create a map plot from latitude and longitude DataFrames."""
    if lat_df is None or lon_df is None or lat_df.empty or lon_df.empty:
        print("No data to plot for map")
        return
    
    # Merge latitude and longitude data
    lat_df = lat_df.rename(columns={'_value': 'latitude'})
    lon_df = lon_df.rename(columns={'_value': 'longitude'})
    
    # Use time as the key for merging
    merged = pd.merge(lat_df, lon_df, on=['_time', 'source', 'device'], how='inner')
    
    if merged.empty:
        print("No matching lat/lon data points found")
        return
    
    plt.figure(figsize=(10, 8))
    
    # Group by source and plot each as a separate track
    for source, group in merged.groupby('source'):
        plt.plot(group['longitude'], group['latitude'], 'o-', label=f"Source: {source}", alpha=0.7)
    
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    print(f"Saved plot to {os.path.join(OUTPUT_DIR, filename)}")
    plt.close()

def create_satellite_count_plot(df, title, filename):
    """Create a bar plot of satellite counts."""
    if df is None or df.empty:
        print("No data to plot for satellite count")
        return
    
    plt.figure(figsize=(12, 6))
    
    # Group by source and time, then plot
    for source, group in df.groupby('source'):
        # Sort by time
        group = group.sort_values('_time')
        times = [t.strftime('%H:%M:%S') for t in group['_time']]
        
        plt.bar(times, group['_value'], label=f"Source: {source}", alpha=0.7)
    
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Number of Satellites')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    print(f"Saved plot to {os.path.join(OUTPUT_DIR, filename)}")
    plt.close()

def create_dop_plot(df_dict, title, filename):
    """Create a plot of DOP (Dilution of Precision) values."""
    if not df_dict or all(df is None or df.empty for df in df_dict.values()):
        print("No data to plot for DOP")
        return
    
    plt.figure(figsize=(12, 6))
    
    # Plot each DOP type
    for dop_type, df in df_dict.items():
        if df is not None and not df.empty:
            # Use the first source we find
            source = df['source'].iloc[0]
            plt.plot(df['_time'], df['_value'], label=f"{dop_type.upper()} (Source: {source})", marker='o', linestyle='-', alpha=0.7)
    
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('DOP Value')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gcf().autofmt_xdate()
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    print(f"Saved plot to {os.path.join(OUTPUT_DIR, filename)}")
    plt.close()

def create_pps_offset_plot(df, title, filename):
    """Create a plot of PPS offset values."""
    if df is None or df.empty:
        print("No data to plot for PPS offset")
        return
    
    plt.figure(figsize=(12, 6))
    
    # Group by source and plot each as a separate line
    for source, group in df.groupby('source'):
        plt.plot(group['_time'], group['_value'], label=f"Source: {source}", marker='o', linestyle='-', alpha=0.7)
    
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Offset (ns)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gcf().autofmt_xdate()
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    print(f"Saved plot to {os.path.join(OUTPUT_DIR, filename)}")
    plt.close()

def main():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Querying data from InfluxDB...")
    
    # Query GPS location data
    lat_df = query_data("gps_location", "latitude")
    lon_df = query_data("gps_location", "longitude")
    alt_df = query_data("gps_location", "altitude")
    
    # Query satellite data
    sat_visible_df = query_data("satellite_info", "satellites_visible")
    sat_used_df = query_data("satellite_info", "satellites_used")
    
    # Query DOP data
    hdop_df = query_data("satellite_info", "hdop")
    vdop_df = query_data("satellite_info", "vdop")
    pdop_df = query_data("satellite_info", "pdop")
    gdop_df = query_data("satellite_info", "gdop")
    
    # Query PPS data
    pps_offset_df = query_data("pps_data", "offset_ns")
    
    print("\nCreating visualizations...")
    
    # Create GPS location plots
    if alt_df is not None and not alt_df.empty:
        create_time_series_plot(alt_df, "altitude", "GPS Altitude Over Time", "Altitude (m)", "altitude_plot.png")
    
    if lat_df is not None and lon_df is not None and not lat_df.empty and not lon_df.empty:
        create_map_plot(lat_df, lon_df, "GPS Position", "gps_map.png")
    
    # Create satellite count plots
    if sat_visible_df is not None and not sat_visible_df.empty:
        create_satellite_count_plot(sat_visible_df, "Visible Satellites", "satellites_visible.png")
    
    if sat_used_df is not None and not sat_used_df.empty:
        create_satellite_count_plot(sat_used_df, "Satellites Used for Positioning", "satellites_used.png")
    
    # Create DOP plot
    dop_dict = {
        "hdop": hdop_df,
        "vdop": vdop_df,
        "pdop": pdop_df,
        "gdop": gdop_df
    }
    create_dop_plot(dop_dict, "Dilution of Precision (DOP) Values", "dop_plot.png")
    
    # Create PPS offset plot
    if pps_offset_df is not None and not pps_offset_df.empty:
        create_pps_offset_plot(pps_offset_df, "PPS Clock Offset", "pps_offset.png")
    
    print("\nVisualization complete! Check the 'plots' directory for the generated images.")

if __name__ == "__main__":
    main()
