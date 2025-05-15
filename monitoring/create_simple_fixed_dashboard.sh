#!/bin/bash

# Create a simplified dashboard with minimal configuration
cat > simple_fixed_dashboard.json << 'EOF'
{
  "dashboard": {
    "id": null,
    "uid": null,
    "title": "Simple Fixed GPS Dashboard",
    "tags": ["gps"],
    "timezone": "browser",
    "schemaVersion": 38,
    "version": 0,
    "refresh": "5s",
    "time": {
      "from": "2025-05-09T00:00:00.000Z",
      "to": "2025-05-13T23:59:59.000Z"
    },
    "panels": [
      {
        "id": 1,
        "gridPos": {
          "h": 8,
          "w": 24,
          "x": 0,
          "y": 0
        },
        "type": "timeseries",
        "title": "Satellites Visible",
        "datasource": {
          "type": "influxdb",
          "uid": "P951FEA4DE68E13C9"
        },
        "targets": [
          {
            "datasource": {
              "type": "influxdb",
              "uid": "P951FEA4DE68E13C9"
            },
            "query": "from(bucket: \"gps_data\")\n  |> range(start: 2025-05-09T00:00:00Z, stop: 2025-05-13T23:59:59Z)\n  |> filter(fn: (r) => r._measurement == \"satellite_info\")\n  |> filter(fn: (r) => r._field == \"satellites_visible\")",
            "refId": "A"
          }
        ]
      }
    ]
  },
  "overwrite": true,
  "message": "Simple fixed dashboard created via API",
  "folderId": 0
}
EOF

# Import the dashboard via API
curl -X POST -H "Content-Type: application/json" -d @simple_fixed_dashboard.json http://admin:admin@localhost:3001/api/dashboards/db

echo -e "\n\nDashboard created! Access it at: http://localhost:3001/dashboards"
