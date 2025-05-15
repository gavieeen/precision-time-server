# GPS Data Monitoring with Grafana and InfluxDB

This directory contains the setup for monitoring and visualizing GPS data using Grafana and InfluxDB.

## Setup Instructions

### 1. Start the Monitoring Stack

```bash
cd monitoring
docker-compose up -d
```

This will start both InfluxDB and Grafana containers.

### 2. Access Grafana

Open your browser and navigate to:
- http://localhost:3001

Login credentials:
- Username: admin
- Password: admin

### 3. Load GPS Data into InfluxDB

Before you can visualize your GPS data, you need to load it into InfluxDB. Use the provided Python script:

```bash
# Install required dependencies
pip install influxdb-client

# Run the script to load data
python load_gps_data.py --log-dir ../gps-logs --pattern "*.csv"
```

Adjust the `--log-dir` and `--pattern` parameters to match your GPS log files.

### 4. Create Dashboards

Once your data is loaded into InfluxDB, you can create dashboards in Grafana:

1. In Grafana, click on "Create" (+ icon) and select "Dashboard"
2. Add a new panel
3. Select "InfluxDB" as the data source
4. Use Flux query language to query your GPS data
5. Customize your visualization as needed

Example Flux query for GPS data:

```
from(bucket: "gps_data")
  |> range(start: -1d)
  |> filter(fn: (r) => r._measurement == "gps_location")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
```

## Configuration Files

- `docker-compose.yml`: Defines the services (InfluxDB and Grafana)
- `grafana/provisioning/datasources/influxdb.yml`: Configures the InfluxDB data source
- `grafana/provisioning/dashboards/dashboards.yml`: Configures dashboard provisioning
- `load_gps_data.py`: Script to load GPS data into InfluxDB

## Notes

- The InfluxDB admin token is set to `my-super-secret-auth-token` (you should change this in production)
- Data is persisted in Docker volumes (`influxdb-data` and `grafana-data`)
- You may need to adjust the data parsing logic in `load_gps_data.py` to match your specific GPS log format
