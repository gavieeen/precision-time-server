#!/bin/bash

# Create a dashboard that embeds the pre-generated plot images
cat > image_dashboard.json << 'EOF'
{
  "dashboard": {
    "id": null,
    "uid": null,
    "title": "GPS Data Visualizations",
    "tags": ["gps"],
    "timezone": "browser",
    "schemaVersion": 38,
    "version": 0,
    "refresh": "5s",
    "time": {
      "from": "now-6h",
      "to": "now"
    },
    "panels": [
      {
        "id": 1,
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 0
        },
        "type": "text",
        "title": "PPS Clock Offset",
        "options": {
          "mode": "html",
          "content": "<img src=\"/public/img/pps_offset.png\" width=\"100%\" />"
        }
      },
      {
        "id": 2,
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 0
        },
        "type": "text",
        "title": "GPS Map",
        "options": {
          "mode": "html",
          "content": "<img src=\"/public/img/gps_map.png\" width=\"100%\" />"
        }
      },
      {
        "id": 3,
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 8
        },
        "type": "text",
        "title": "Satellites Visible",
        "options": {
          "mode": "html",
          "content": "<img src=\"/public/img/satellites_visible.png\" width=\"100%\" />"
        }
      },
      {
        "id": 4,
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 8
        },
        "type": "text",
        "title": "Satellites Used",
        "options": {
          "mode": "html",
          "content": "<img src=\"/public/img/satellites_used.png\" width=\"100%\" />"
        }
      },
      {
        "id": 5,
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 16
        },
        "type": "text",
        "title": "Altitude Plot",
        "options": {
          "mode": "html",
          "content": "<img src=\"/public/img/altitude_plot.png\" width=\"100%\" />"
        }
      },
      {
        "id": 6,
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 16
        },
        "type": "text",
        "title": "DOP Plot",
        "options": {
          "mode": "html",
          "content": "<img src=\"/public/img/dop_plot.png\" width=\"100%\" />"
        }
      }
    ]
  },
  "overwrite": true,
  "message": "Image dashboard created via API",
  "folderId": 0
}
EOF

# Copy the plot images to Grafana's public directory
docker cp plots/pps_offset.png grafana:/usr/share/grafana/public/img/
docker cp plots/gps_map.png grafana:/usr/share/grafana/public/img/
docker cp plots/satellites_visible.png grafana:/usr/share/grafana/public/img/
docker cp plots/satellites_used.png grafana:/usr/share/grafana/public/img/
docker cp plots/altitude_plot.png grafana:/usr/share/grafana/public/img/
docker cp plots/dop_plot.png grafana:/usr/share/grafana/public/img/

# Import the dashboard via API
curl -X POST -H "Content-Type: application/json" -d @image_dashboard.json http://admin:admin@localhost:3001/api/dashboards/db

echo -e "\n\nDashboard created! Access it at: http://localhost:3001/dashboards"
