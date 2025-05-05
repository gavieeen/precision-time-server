#!/usr/bin/env python3
import os
import json
import time
import subprocess
import threading
import psutil
import socket
from datetime import datetime
import pytz
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from contextlib import suppress

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ptp-time-server-secret'
socketio = SocketIO(app)

# Global variables to store system status
system_status = {
    'gps': {
        'status': 'Unknown',
        'satellites': 0,
        'fix': False,
        'latitude': 0.0,
        'longitude': 0.0,
        'altitude': 0.0,
        'speed': 0.0,
        'time': '',
        'last_update': 0
    },
    'pps': {
        'status': 'Unknown',
        'offset': 0.0,
        'jitter': 0.0,
        'last_update': 0
    },
    'ptp': {
        'status': 'Unknown',
        'master': '',
        'offset': 0.0,
        'delay': 0.0,
        'last_update': 0
    },
    'system': {
        'hostname': socket.gethostname(),
        'ip': get_ip_address(),
        'uptime': 0,
        'cpu_usage': 0.0,
        'memory_usage': 0.0,
        'disk_usage': 0.0,
        'last_update': 0
    },
    'ntp': {
        'status': 'Unknown',
        'stratum': 0,
        'offset': 0.0,
        'jitter': 0.0,
        'last_update': 0
    }
}

def get_ip_address():
    """Get the primary IP address of the system"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def parse_gps_data(line):
    """Parse a single line of GPS data"""
    with suppress(json.JSONDecodeError):
        data = json.loads(line)
        if data.get('class') == 'TPV':
            system_status['gps']['status'] = 'Active'
            system_status['gps']['fix'] = data.get('mode', 0) >= 2
            system_status['gps']['latitude'] = data.get('lat', 0.0)
            system_status['gps']['longitude'] = data.get('lon', 0.0)
            system_status['gps']['altitude'] = data.get('alt', 0.0)
            system_status['gps']['speed'] = data.get('speed', 0.0)
            if 'time' in data:
                system_status['gps']['time'] = data['time']
        elif data.get('class') == 'SKY':
            satellites = data.get('satellites', [])
            used_sats = sum(sat.get('used', False) for sat in satellites)
            system_status['gps']['satellites'] = used_sats

def update_gps_status():
    """Update GPS status from gpsd"""
    try:
        # Run gpspipe to get GPS data
        process = subprocess.Popen(
            ["gpspipe", "-w", "-n", "5"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=5)
        
        if process.returncode != 0:
            system_status['gps']['status'] = 'Error'
            return
        
        # Parse the JSON output
        lines = stdout.strip().split('\n')
        for line in lines:
            parse_gps_data(line)
        
        system_status['gps']['last_update'] = time.time()
    except Exception as e:
        system_status['gps']['status'] = f'Error: {str(e)}'

def update_pps_status():
    """Update PPS status"""
    try:
        # Check if PPS device exists
        if not os.path.exists('/dev/pps0'):
            system_status['pps']['status'] = 'Not Found'
            return
        
        # Run ppstest to check PPS signal
        process = subprocess.Popen(
            ["sudo", "ppstest", "/dev/pps0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=5)
        
        if "Timestamp" in stdout:
            system_status['pps']['status'] = 'Active'
        else:
            system_status['pps']['status'] = 'Inactive'
        
        # Get PPS statistics from chrony
        process = subprocess.Popen(
            ["chronyc", "sourcestats"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=5)
        
        for line in stdout.strip().split('\n'):
            if "PPS" in line:
                parts = line.split()
                if len(parts) >= 5:
                    system_status['pps']['offset'] = float(parts[4])
                    system_status['pps']['jitter'] = float(parts[5])
        
        system_status['pps']['last_update'] = time.time()
    except Exception as e:
        system_status['pps']['status'] = f'Error: {str(e)}'

def update_ptp_status():
    """Update PTP status"""
    try:
        # Run ptp4l status command
        process = subprocess.Popen(
            ["sudo", "pmc", "-u", "-b", "0", "'get TIME_STATUS_NP'"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        stdout, stderr = process.communicate(timeout=5)
        
        if "master_offset" in stdout:
            system_status['ptp']['status'] = 'Active'
            
            # Parse the output to get master, offset, and delay
            for line in stdout.strip().split('\n'):
                if "master_offset" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        system_status['ptp']['offset'] = float(parts[1])
                elif "mean_path_delay" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        system_status['ptp']['delay'] = float(parts[1])
                elif "gmIdentity" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        system_status['ptp']['master'] = parts[1]
        else:
            system_status['ptp']['status'] = 'Inactive'
        
        system_status['ptp']['last_update'] = time.time()
    except Exception as e:
        system_status['ptp']['status'] = f'Error: {str(e)}'

def update_system_status():
    """Update system status"""
    try:
        # Get uptime
        uptime_seconds = time.time() - psutil.boot_time()
        system_status['system']['uptime'] = int(uptime_seconds)
        
        # Get CPU usage
        system_status['system']['cpu_usage'] = psutil.cpu_percent(interval=1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        system_status['system']['memory_usage'] = memory.percent
        
        # Get disk usage
        disk = psutil.disk_usage('/')
        system_status['system']['disk_usage'] = disk.percent
        
        system_status['system']['last_update'] = time.time()
    except Exception as e:
        print(f"Error updating system status: {e}")

def update_ntp_status():
    """Update NTP/Chrony status"""
    try:
        # Run chronyc tracking to get NTP status
        process = subprocess.Popen(
            ["chronyc", "tracking"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=5)
        
        if "Stratum" in stdout:
            system_status['ntp']['status'] = 'Active'
            
            # Parse the output to get stratum, offset, and jitter
            for line in stdout.strip().split('\n'):
                if "Stratum" in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        system_status['ntp']['stratum'] = int(parts[1].strip())
                elif "Last offset" in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        system_status['ntp']['offset'] = float(parts[1].strip().split()[0])
                elif "RMS offset" in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        system_status['ntp']['jitter'] = float(parts[1].strip().split()[0])
        else:
            system_status['ntp']['status'] = 'Inactive'
        
        system_status['ntp']['last_update'] = time.time()
    except Exception as e:
        system_status['ntp']['status'] = f'Error: {str(e)}'

def background_update():
    """Background thread to update status periodically"""
    while True:
        update_gps_status()
        update_pps_status()
        update_ptp_status()
        update_system_status()
        update_ntp_status()
        
        # Emit updated status to all connected clients
        socketio.emit('status_update', system_status)
        
        # Sleep for 1 second
        time.sleep(1)

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API endpoint to get current status"""
    return jsonify(system_status)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    # Send current status to the newly connected client
    socketio.emit('status_update', system_status, to=request.sid)

if __name__ == '__main__':
    # Start background update thread
    update_thread = threading.Thread(target=background_update)
    update_thread.daemon = True
    update_thread.start()
    
    # Start the Flask app
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
