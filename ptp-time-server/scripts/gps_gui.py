#!/usr/bin/env python3
"""
Simple GUI to interact with GPS data from the PTP time server
using pygpsclient library.
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

def main():
    """Launch a simple GUI to interact with PyGPSClient"""
    print("Starting GPS GUI Launcher...")
    
    # Create the main application window
    root = tk.Tk()
    root.title("PTP Time Server GPS Monitor")
    root.geometry("400x300")
    
    # Set up the frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Add a title label
    title_label = ttk.Label(
        main_frame,
        text="PTP Time Server GPS Interface",
        font=("Helvetica", 16)
    )
    title_label.pack(pady=20)
    
    # Add description
    desc_label = ttk.Label(
        main_frame,
        text="Launch PyGPSClient to interact with GPS data",
        wraplength=350
    )
    desc_label.pack(pady=10)
    
    # Add a button to launch the full pygpsclient GUI
    launch_button = ttk.Button(
        main_frame, 
        text="Launch PyGPSClient GUI",
        command=launch_pygpsclient_gui,
        width=25
    )
    launch_button.pack(pady=20)
    
    # Add a button to check GPSD status
    status_button = ttk.Button(
        main_frame, 
        text="Check GPSD Status",
        command=check_gpsd_status,
        width=25
    )
    status_button.pack(pady=10)
    
    # Start the main loop
    root.mainloop()

def launch_pygpsclient_gui():
    """Launch the full PyGPSClient GUI"""
    try:
        # Use subprocess to launch pygpsclient as a separate process
        subprocess.Popen([sys.executable, "-m", "pygpsclient"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch PyGPSClient GUI: {str(e)}")

def check_gpsd_status():
    """Check if GPSD is running and show status"""
    try:
        # This will work on Linux systems with systemd
        result = subprocess.run(["systemctl", "status", "gpsd"], 
                               capture_output=True, text=True)
        status_window = tk.Toplevel()
        status_window.title("GPSD Status")
        status_window.geometry("500x400")
        
        status_text = tk.Text(status_window, wrap=tk.WORD)
        status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if result.returncode == 0:
            status_text.insert(tk.END, "GPSD is running\n\n")
        else:
            status_text.insert(tk.END, "GPSD may not be running\n\n")
        
        status_text.insert(tk.END, result.stdout)
        status_text.config(state=tk.DISABLED)
    except Exception as e:
        # If the command fails (e.g., on macOS or if systemctl is not available)
        messagebox.showinfo("GPSD Status", 
                           "Could not check GPSD status using systemctl.\n\n"
                           "If you're running on the Raspberry Pi:\n"
                           "1. Make sure GPSD is installed and running\n"
                           "2. Check if GPS device is connected to /dev/ttyACM0\n"
                           "3. Verify GPSD configuration in /etc/default/gpsd")

if __name__ == "__main__":
    main()
