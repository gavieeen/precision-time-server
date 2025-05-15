import json
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import DateFormatter

def parse_json_file(file_path):
    """Parse a JSON file containing GPS data line by line"""
    try:
        with open(file_path) as f:
            # Try to parse as line-by-line JSON
            try:
                data = [json.loads(line) for line in f if line.strip()]
                if not data:  # If no data was parsed, try as a single JSON object
                    f.seek(0)
                    data = json.load(f)
                    if isinstance(data, dict):
                        data = [data]
            except json.JSONDecodeError:
                # Try as a single JSON object
                f.seek(0)
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]
        return data
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []

def extract_data_from_entries(data):
    """Extract relevant fields from GPS data entries"""
    tpv_data = []
    sky_data = []
    pps_jitter_ns = []

    for entry in data:
        if isinstance(entry, dict):  # Ensure entry is a dictionary
            entry_class = entry.get("class", "")
            
            if entry_class == "TPV" and "lat" in entry and "lon" in entry:
                tpv_data.append({
                    "time": entry.get("time", ""),
                    "lat": entry.get("lat", 0),
                    "lon": entry.get("lon", 0),
                    "alt": entry.get("alt", 0),
                    "eph": entry.get("eph", 0),  # Horizontal position error
                    "epv": entry.get("epv", 0)   # Vertical position error
                })
            elif entry_class == "SKY":
                sky_data.append({
                    "time": entry.get("time", ""),
                    "nSat": entry.get("nSat", 0),
                    "uSat": entry.get("uSat", 0),
                    "hdop": entry.get("hdop", 0),
                    "vdop": entry.get("vdop", 0),
                    "pdop": entry.get("pdop", 0)
                })
            elif entry_class == "PPS":
                jitter = abs(entry.get("clock_nsec", 0) - 0)
                pps_jitter_ns.append({
                    "real_sec": entry.get("real_sec", 0),
                    "jitter_ns": jitter
                })

    # Convert to DataFrames
    df_tpv = pd.DataFrame(tpv_data)
    df_sky = pd.DataFrame(sky_data)
    df_pps = pd.DataFrame(pps_jitter_ns)
    
    # Convert time strings to datetime objects for TPV and SKY data
    if not df_tpv.empty and "time" in df_tpv.columns:
        try:
            df_tpv["datetime"] = pd.to_datetime(df_tpv["time"])
        except:
            print("Could not parse TPV time data")
    
    if not df_sky.empty and "time" in df_sky.columns:
        try:
            df_sky["datetime"] = pd.to_datetime(df_sky["time"])
        except:
            print("Could not parse SKY time data")
    
    return df_tpv, df_sky, df_pps

def plot_gps_data(file_path, all_data=None):
    """Plot GPS data from a single file"""
    print(f"Processing file: {os.path.basename(file_path)}")
    data = parse_json_file(file_path)
    
    if not data:
        print(f"No data found in {file_path}")
        return None
    
    df_tpv, df_sky, df_pps = extract_data_from_entries(data)
    
    # Store data for aggregation if needed
    if all_data is not None:
        all_data["tpv"].append(df_tpv)
        all_data["sky"].append(df_sky)
        all_data["pps"].append(df_pps)
    
    # Skip plotting if any dataframe is empty
    if df_tpv.empty and df_sky.empty and df_pps.empty:
        print(f"No relevant data found in {file_path}")
        return None
    
    # Create a figure with subplots
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle(f"GPS Data Visualization - {os.path.basename(file_path)}", fontsize=16)
    
    # Plot 1: GPS Location (if data exists)
    if not df_tpv.empty and "lon" in df_tpv.columns and "lat" in df_tpv.columns:
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(df_tpv["lon"], df_tpv["lat"], marker="o", linestyle="-", markersize=3)
        ax1.set_title("GPS Location Trace")
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.grid(True)
        
        # Add error bars if available
        if "eph" in df_tpv.columns and df_tpv["eph"].notna().any():
            # Sample every 10th point to avoid cluttering
            sample_idx = np.arange(0, len(df_tpv), 10)
            if len(sample_idx) > 0:
                ax1.errorbar(
                    df_tpv.iloc[sample_idx]["lon"], 
                    df_tpv.iloc[sample_idx]["lat"],
                    xerr=df_tpv.iloc[sample_idx]["eph"] / 111000,  # Approximate conversion to degrees
                    yerr=df_tpv.iloc[sample_idx]["eph"] / 111000,
                    fmt='none', ecolor='r', alpha=0.3
                )
    
    # Plot 2: Satellite Count (if data exists)
    if not df_sky.empty and "nSat" in df_sky.columns and "uSat" in df_sky.columns:
        ax2 = fig.add_subplot(2, 2, 2)
        
        if "datetime" in df_sky.columns:
            ax2.plot(df_sky["datetime"], df_sky["nSat"], label="Total Satellites")
            ax2.plot(df_sky["datetime"], df_sky["uSat"], label="Used Satellites")
            ax2.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        else:
            # If datetime conversion failed, use index
            ax2.plot(df_sky.index, df_sky["nSat"], label="Total Satellites")
            ax2.plot(df_sky.index, df_sky["uSat"], label="Used Satellites")
        
        ax2.set_title("Satellite Count Over Time")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Number of Satellites")
        ax2.legend()
        ax2.grid(True)
    
    # Plot 3: PPS Jitter (if data exists)
    if not df_pps.empty and "jitter_ns" in df_pps.columns:
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(df_pps["real_sec"], df_pps["jitter_ns"])
        ax3.set_title("PPS Jitter Over Time")
        ax3.set_xlabel("Real Time (s)")
        ax3.set_ylabel("Jitter (nanoseconds)")
        ax3.grid(True)
    
    # Plot 4: DOP Values (if data exists)
    if not df_sky.empty and "hdop" in df_sky.columns and "vdop" in df_sky.columns:
        ax4 = fig.add_subplot(2, 2, 4)
        
        if "datetime" in df_sky.columns:
            ax4.plot(df_sky["datetime"], df_sky["hdop"], label="HDOP")
            ax4.plot(df_sky["datetime"], df_sky["vdop"], label="VDOP")
            if "pdop" in df_sky.columns:
                ax4.plot(df_sky["datetime"], df_sky["pdop"], label="PDOP")
            ax4.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        else:
            # If datetime conversion failed, use index
            ax4.plot(df_sky.index, df_sky["hdop"], label="HDOP")
            ax4.plot(df_sky.index, df_sky["vdop"], label="VDOP")
            if "pdop" in df_sky.columns:
                ax4.plot(df_sky.index, df_sky["pdop"], label="PDOP")
        
        ax4.set_title("Dilution of Precision (DOP) Values")
        ax4.set_xlabel("Time")
        ax4.set_ylabel("DOP Value")
        ax4.legend()
        ax4.grid(True)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for the suptitle
    
    return fig

def plot_aggregate_data(all_data):
    """Plot aggregate statistics from all files"""
    # Combine all dataframes
    combined_tpv = pd.concat(all_data["tpv"]) if all_data["tpv"] else pd.DataFrame()
    combined_sky = pd.concat(all_data["sky"]) if all_data["sky"] else pd.DataFrame()
    combined_pps = pd.concat(all_data["pps"]) if all_data["pps"] else pd.DataFrame()
    
    if combined_tpv.empty and combined_sky.empty and combined_pps.empty:
        print("No data available for aggregate plots")
        return None
    
    # Create a figure with subplots for aggregate data
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle("Aggregate GPS Data Visualization", fontsize=16)
    
    # Plot 1: Satellite Usage Statistics
    if not combined_sky.empty and "nSat" in combined_sky.columns and "uSat" in combined_sky.columns:
        ax1 = fig.add_subplot(2, 2, 1)
        
        # Calculate satellite usage ratio
        if not combined_sky["nSat"].empty and (combined_sky["nSat"] > 0).any():
            combined_sky["usage_ratio"] = combined_sky["uSat"] / combined_sky["nSat"]
            
            # Create histogram of satellite usage ratio
            ax1.hist(combined_sky["usage_ratio"], bins=20, alpha=0.7)
            ax1.set_title("Satellite Usage Ratio Distribution")
            ax1.set_xlabel("Ratio of Used to Total Satellites")
            ax1.set_ylabel("Frequency")
            ax1.grid(True)
            
            # Add mean and median lines
            mean_ratio = combined_sky["usage_ratio"].mean()
            median_ratio = combined_sky["usage_ratio"].median()
            ax1.axvline(mean_ratio, color='r', linestyle='--', label=f'Mean: {mean_ratio:.2f}')
            ax1.axvline(median_ratio, color='g', linestyle='-.', label=f'Median: {median_ratio:.2f}')
            ax1.legend()
    
    # Plot 2: PPS Jitter Statistics
    if not combined_pps.empty and "jitter_ns" in combined_pps.columns:
        ax2 = fig.add_subplot(2, 2, 2)
        
        # Create histogram of jitter values
        ax2.hist(combined_pps["jitter_ns"], bins=30, alpha=0.7)
        ax2.set_title("PPS Jitter Distribution")
        ax2.set_xlabel("Jitter (nanoseconds)")
        ax2.set_ylabel("Frequency")
        ax2.grid(True)
        
        # Add mean and median lines
        mean_jitter = combined_pps["jitter_ns"].mean()
        median_jitter = combined_pps["jitter_ns"].median()
        ax2.axvline(mean_jitter, color='r', linestyle='--', label=f'Mean: {mean_jitter:.2f}')
        ax2.axvline(median_jitter, color='g', linestyle='-.', label=f'Median: {median_jitter:.2f}')
        ax2.legend()
    
    # Plot 3: DOP Values Box Plot
    if not combined_sky.empty:
        dop_columns = [col for col in ["hdop", "vdop", "pdop"] if col in combined_sky.columns]
        if dop_columns:
            ax3 = fig.add_subplot(2, 2, 3)
            combined_sky[dop_columns].boxplot(ax=ax3)
            ax3.set_title("DOP Values Distribution")
            ax3.set_ylabel("DOP Value")
            ax3.grid(True)
            
            # Add a table with statistics
            stats_data = []
            for col in dop_columns:
                stats_data.append([
                    col.upper(),
                    f"{combined_sky[col].mean():.2f}",
                    f"{combined_sky[col].median():.2f}",
                    f"{combined_sky[col].min():.2f}",
                    f"{combined_sky[col].max():.2f}"
                ])
            
            ax3.table(
                cellText=stats_data,
                colLabels=["Metric", "Mean", "Median", "Min", "Max"],
                loc="bottom",
                bbox=[0.0, -0.5, 1.0, 0.3]
            )
            ax3.set_xlabel("")  # Remove x-label as table provides context
    
    # Plot 4: Position Error Statistics
    if not combined_tpv.empty:
        error_columns = [col for col in ["eph", "epv"] if col in combined_tpv.columns]
        if error_columns:
            ax4 = fig.add_subplot(2, 2, 4)
            
            for col in error_columns:
                if combined_tpv[col].notna().any():
                    label = "Horizontal Error" if col == "eph" else "Vertical Error"
                    ax4.hist(combined_tpv[col], bins=20, alpha=0.5, label=label)
            
            ax4.set_title("Position Error Distribution")
            ax4.set_xlabel("Error (meters)")
            ax4.set_ylabel("Frequency")
            ax4.legend()
            ax4.grid(True)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for the suptitle
    
    return fig

def create_combined_visualization(all_data, individual_data_figures):
    """Create a single figure containing all visualizations"""
    if not individual_data_figures:
        print("No data to visualize")
        return
    
    # Calculate total number of rows needed
    # 4 rows for aggregate data + 4 rows for each individual file
    total_files = len(individual_data_figures)
    total_rows = 4 + (4 * total_files)
    
    # Create a large figure to hold all plots
    plt.figure(figsize=(15, 5 * total_rows // 4))
    
    # Current row counter
    current_row = 1
    
    # First, add the aggregate data at the top
    plt.figtext(0.5, 1 - (0.5 / total_rows), "AGGREGATE GPS DATA VISUALIZATION", 
                ha="center", va="center", fontsize=16, fontweight="bold")
    
    # Create aggregate plots first
    try:
        combined_tpv = pd.concat(all_data["tpv"]) if all_data["tpv"] else pd.DataFrame()
        combined_sky = pd.concat(all_data["sky"]) if all_data["sky"] else pd.DataFrame()
        combined_pps = pd.concat(all_data["pps"]) if all_data["pps"] else pd.DataFrame()
        
        # Plot 1: Satellite Usage Statistics
        if not combined_sky.empty and "nSat" in combined_sky.columns and "uSat" in combined_sky.columns:
            plt.subplot(total_rows // 4, 4, current_row)
            if not combined_sky["nSat"].empty and (combined_sky["nSat"] > 0).any():
                combined_sky["usage_ratio"] = combined_sky["uSat"] / combined_sky["nSat"]
                plt.hist(combined_sky["usage_ratio"], bins=20, alpha=0.7)
                plt.title("Satellite Usage Ratio Distribution")
                plt.xlabel("Ratio of Used to Total Satellites")
                plt.ylabel("Frequency")
                plt.grid(True)
                mean_ratio = combined_sky["usage_ratio"].mean()
                median_ratio = combined_sky["usage_ratio"].median()
                plt.axvline(mean_ratio, color='r', linestyle='--', label=f'Mean: {mean_ratio:.2f}')
                plt.axvline(median_ratio, color='g', linestyle='-.', label=f'Median: {median_ratio:.2f}')
                plt.legend()
        
        # Plot 2: PPS Jitter Statistics
        current_row += 1
        if not combined_pps.empty and "jitter_ns" in combined_pps.columns:
            plt.subplot(total_rows // 4, 4, current_row)
            plt.hist(combined_pps["jitter_ns"], bins=30, alpha=0.7)
            plt.title("PPS Jitter Distribution")
            plt.xlabel("Jitter (nanoseconds)")
            plt.ylabel("Frequency")
            plt.grid(True)
            mean_jitter = combined_pps["jitter_ns"].mean()
            median_jitter = combined_pps["jitter_ns"].median()
            plt.axvline(mean_jitter, color='r', linestyle='--', label=f'Mean: {mean_jitter:.2f}')
            plt.axvline(median_jitter, color='g', linestyle='-.', label=f'Median: {median_jitter:.2f}')
            plt.legend()
        
        # Plot 3: DOP Values Box Plot
        current_row += 1
        if not combined_sky.empty:
            dop_columns = [col for col in ["hdop", "vdop", "pdop"] if col in combined_sky.columns]
            if dop_columns:
                plt.subplot(total_rows // 4, 4, current_row)
                combined_sky[dop_columns].boxplot()
                plt.title("DOP Values Distribution")
                plt.ylabel("DOP Value")
                plt.grid(True)
        
        # Plot 4: Position Error Statistics
        current_row += 1
        if not combined_tpv.empty:
            error_columns = [col for col in ["eph", "epv"] if col in combined_tpv.columns]
            if error_columns:
                plt.subplot(total_rows // 4, 4, current_row)
                for col in error_columns:
                    if combined_tpv[col].notna().any():
                        label = "Horizontal Error" if col == "eph" else "Vertical Error"
                        plt.hist(combined_tpv[col], bins=20, alpha=0.5, label=label)
                plt.title("Position Error Distribution")
                plt.xlabel("Error (meters)")
                plt.ylabel("Frequency")
                plt.legend()
                plt.grid(True)
    
    except Exception as e:
        print(f"Error creating aggregate plots: {e}")
    
    # Now add individual file plots
    for i, (file_path, fig) in enumerate(individual_data_figures):
        current_row += 1
        
        # Add a title for this log file
        file_name = os.path.basename(file_path)
        plt.figtext(0.5, 1 - ((current_row + 0.5) / total_rows), 
                    f"LOG FILE: {file_name}", 
                    ha="center", va="center", fontsize=14, fontweight="bold")
        
        # Extract the axes from the figure
        for j, ax in enumerate(fig.get_axes()):
            # Get the data and properties from the original axis
            lines = ax.get_lines()
            title = ax.get_title()
            xlabel = ax.get_xlabel()
            ylabel = ax.get_ylabel()
            legend = ax.get_legend()
            
            # Always enable grid for consistency
            grid_visible = True
            
            # Create a new subplot in the combined figure
            new_ax = plt.subplot(total_rows // 4, 4, current_row + j)
            
            # Copy over the data and properties
            for line in lines:
                new_ax.plot(line.get_xdata(), line.get_ydata(), 
                           color=line.get_color(), 
                           linestyle=line.get_linestyle(), 
                           marker=line.get_marker(),
                           markersize=line.get_markersize())
            
            new_ax.set_title(title)
            new_ax.set_xlabel(xlabel)
            new_ax.set_ylabel(ylabel)
            if grid_visible:
                new_ax.grid(True)
            
            # Copy legend if it exists
            if legend is not None:
                handles, labels = ax.get_legend_handles_labels()
                if handles and labels:
                    new_ax.legend(handles, labels)
            
            # Handle error bars if present
            for collection in ax.collections:
                if hasattr(collection, 'get_segments'):
                    # This is likely an error bar or line collection
                    try:
                        new_collection = plt.matplotlib.collections.LineCollection(
                            collection.get_segments(),
                            colors=collection.get_colors(),
                            linewidths=collection.get_linewidths()
                        )
                        new_ax.add_collection(new_collection)
                    except:
                        # Skip if we can't copy the collection
                        pass
        
        current_row += 3  # Move to the next set of plots (4 plots per file)
    
    plt.tight_layout()
    return plt.gcf()

def main():
    """Main function to process all JSON files and create visualizations"""
    print("GPS Data Visualization Tool")
    print("---------------------------")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all JSON files in the current directory and subdirectories
    json_files = []
    for ext in ["*.json"]:
        json_files.extend(glob.glob(os.path.join(script_dir, ext)))
        json_files.extend(glob.glob(os.path.join(script_dir, "**", ext), recursive=True))
    
    # Remove duplicates and sort
    json_files = sorted(list(set(json_files)))
    
    if not json_files:
        print("No JSON files found in the current directory or subdirectories.")
        return
    
    print(f"Found {len(json_files)} JSON files.")
    
    # Initialize data storage for aggregation
    all_data = {
        "tpv": [],
        "sky": [],
        "pps": []
    }
    
    # First create and display aggregate plots
    try:
        # Process each file to collect data without displaying
        for file_path in json_files:
            try:
                data = parse_json_file(file_path)
                if data:
                    print(f"Processing file: {os.path.basename(file_path)}")
                    df_tpv, df_sky, df_pps = extract_data_from_entries(data)
                    all_data["tpv"].append(df_tpv)
                    all_data["sky"].append(df_sky)
                    all_data["pps"].append(df_pps)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Create and display aggregate plots first
        agg_fig = plot_aggregate_data(all_data)
        if agg_fig:
            plt.figure(agg_fig.number)
            plt.show()
    except Exception as e:
        print(f"Error creating aggregate plots: {e}")
    
    # Now process and display individual file plots
    for file_path in json_files:
        try:
            fig = plot_gps_data(file_path)
            if fig:
                plt.figure(fig.number)
                plt.show()
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print("Visualization complete.")

if __name__ == "__main__":
    main()
