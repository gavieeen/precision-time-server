# PTP Time Server GUI

This is a web-based GUI for monitoring the PTP time server with GPS and PPS synchronization. It provides real-time status information about the GPS, PPS, PTP, and system performance.

## Features

- Real-time monitoring of GPS status (satellites, position, time)
- PPS signal monitoring (status, offset, jitter)
- PTP status monitoring (master, offset, delay)
- NTP/Chrony status monitoring (stratum, offset, jitter)
- System resource monitoring (CPU, memory, disk usage)
- Responsive web interface accessible from any device

## Installation

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Make sure the following services are running on your Raspberry Pi:
   - gpsd
   - chrony
   - ptp4l
   - phc2sys

## Running the GUI

To start the GUI server, run:

```bash
python app.py
```

This will start a web server on port 8080. You can access the dashboard by opening a web browser and navigating to:

```
http://[raspberry-pi-ip]:8080
```

Replace `[raspberry-pi-ip]` with the IP address of your Raspberry Pi.

## Ansible Integration

To deploy this GUI as part of your Ansible playbook, add the following tasks to your Ansible role:

```yaml
- name: Create GUI directory
  file:
    path: /opt/ptp-time-server-gui
    state: directory
    mode: '0755'
  become: yes

- name: Copy GUI files
  copy:
    src: "{{ item }}"
    dest: /opt/ptp-time-server-gui/
    mode: '0644'
  with_items:
    - gui/app.py
    - gui/requirements.txt
  become: yes

- name: Create templates directory
  file:
    path: /opt/ptp-time-server-gui/templates
    state: directory
    mode: '0755'
  become: yes

- name: Copy template files
  copy:
    src: gui/templates/index.html
    dest: /opt/ptp-time-server-gui/templates/
    mode: '0644'
  become: yes

- name: Install GUI dependencies
  pip:
    requirements: /opt/ptp-time-server-gui/requirements.txt
  become: yes

- name: Create systemd service for GUI
  template:
    src: ptp-gui.service.j2
    dest: /etc/systemd/system/ptp-gui.service
    owner: root
    group: root
    mode: '0644'
  become: yes
  notify: reload systemd

- name: Enable and start GUI service
  systemd:
    name: ptp-gui
    enabled: yes
    state: started
  become: yes
```

You'll also need to create a systemd service template file `ptp-gui.service.j2` in your templates directory.

## Troubleshooting

If you encounter issues with the GUI:

1. Check that all required services are running:
   ```bash
   systemctl status gpsd chrony ptp4l phc2sys
   ```

2. Verify that the GPS device is properly connected and recognized:
   ```bash
   ls -l /dev/ttyACM0
   ```

3. Check that the PPS signal is being detected:
   ```bash
   ls -l /dev/pps0
   ```

4. Check the logs for any errors:
   ```bash
   journalctl -u ptp-gui -f
   ```

## X11 Forwarding (Optional)

If you want to run the GUI directly on the Raspberry Pi and forward it to your local machine, you can use X11 forwarding:

1. On macOS, install XQuartz:
   ```bash
   brew install --cask xquartz
   ```

2. Connect to the Raspberry Pi with X11 forwarding enabled:
   ```bash
   ssh -X username@raspberry-pi-ip
   ```

3. Run a web browser on the Raspberry Pi:
   ```bash
   firefox http://localhost:8080
   ```

This will display the Firefox window from the Raspberry Pi on your local machine.
