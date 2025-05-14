import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON file line-by-line
with open("gpt_log_boddeti2.json") as f:
    data = [json.loads(line) for line in f]

# Extract relevant fields
tpv_data = []
sky_data = []
pps_jitter_ns = []

for entry in data:
    if entry["class"] == "TPV" and "lat" in entry:
        tpv_data.append({
            "time": entry["time"],
            "lat": entry["lat"],
            "lon": entry["lon"],
            "alt": entry["alt"]
        })
    elif entry["class"] == "SKY":
        sky_data.append({
            "time": entry["time"],
            "nSat": entry.get("nSat", 0),
            "uSat": entry.get("uSat", 0),
            "hdop": entry.get("hdop"),
            "vdop": entry.get("vdop"),
        })
    elif entry["class"] == "PPS":
        jitter = abs(entry["clock_nsec"] - 0)
        pps_jitter_ns.append({
            "real_sec": entry["real_sec"],
            "jitter_ns": jitter
        })

# Convert to DataFrames
df_tpv = pd.DataFrame(tpv_data)
df_sky = pd.DataFrame(sky_data)
df_pps = pd.DataFrame(pps_jitter_ns)

# Plot 1: GPS Location over time
plt.figure()
plt.plot(df_tpv["lon"], df_tpv["lat"], marker="o", linestyle="-")
plt.title("GPS Location Trace")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.tight_layout()

# Plot 2: Satellite Count
plt.figure()
plt.plot(df_sky["time"], df_sky["nSat"], label="Total Sats")
plt.plot(df_sky["time"], df_sky["uSat"], label="Used Sats")
plt.xticks(rotation=45)
plt.title("Satellite Count Over Time")
plt.xlabel("Time")
plt.ylabel("Satellites")
plt.legend()
plt.tight_layout()

# Plot 3: PPS Jitter
plt.figure()
plt.plot(df_pps["real_sec"], df_pps["jitter_ns"])
plt.title("PPS Jitter Over Time")
plt.xlabel("Real Time (s)")
plt.ylabel("Jitter (nanoseconds)")
plt.grid(True)
plt.tight_layout()

plt.show()
