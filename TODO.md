**System Setup and Optimization**


1. Try both:

-*PPS via GPIO18

- PPS via CM4 MAC pin
- Compare which one gives better timing performance.

2. IRQ Steering and CPU Isolation

- Use watch -d -n1 'cat /proc/interrupts'

- Steer all non-important IRQs to core 0

- Dedicate clean cores for:

    - PPS GPIO18 IRQ

    - PTP/chronyd

- Use isolcpus and set CPU affinity (manual scheduling)
-------------------------------------- (Aryan)
3. Tickless Kernel 

- Enable and verify tickless kernel (CONFIG_NO_HZ_FULL or similar)

^ going to take too long and need to recompile kernal
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


4. Assign Chrony/PTP Threads

- Use htop tree view

- Assign critical thread(s) to dedicated core(s)


**PPS, GPS, and Clock Configuration**


5. Configure EVKF9T GPS Module

- Enable L5 band

- (Maybe) disable GLONASS

- Reset to known good config on Pi reboot (coordinating with Group 30)

6. Baud Rate and Logging

- Increase USB baud rate to avoid overflow

- Use gpspipe -w for logging

- Instrument once-per-second logging (CPU temps, jitter, etc.)

7. Use ubxtool to:

- Enable detailed satellite logs

- Log signal strength, satellite usage, PPS jitter, etc.

8. Log and Store GPS Performance Data

- Write satellite info and timing quality into a database

- Possibly reuse prior teams’ CesiumJS GUI for visualization


**PTP and Client-Server Timing**

9. PTP Time Input

- Ensure the PTP daemon uses PPS GPIO or MAC pin input

10. Compare PPS vs PTP Outputs

- Measure distribution between RPi PTP client's MAC time and PRS10 PPS

- Optionally: feed client PPS into EVKF9T for timestamping

11. Evaluate Packet Size Effects

- Test PTP sync quality for small vs large packets (64 vs 1500 bytes)

12. Web GUI + Grafana Setup

- Show:

    - Satellite info

    - PTP quality

    - CPU/jitter metrics

- Possibly integrate CesiumJS + Grafana

- Visualize signal strength and satellite usage

**Post-Processing & Precision Improvements**


13. Download/post-process GNSS data

- Use correction services to determine exact location

- Upload back to improve lock and fix speed

14. Almanac Saving

- Learn how to periodically save/load GPS almanac to improve lock speed

15. Test SNMP + IPMI Compatibility

- Determine if devices can expose stats over SNMP/IPMI

- Enables Prometheus/Grafana monitoring




**PROFESSOR TODO (Prof. Lariviere)** 


1. Buy Battery for RTC

2. Provide PRS10 Configuration Tool (Code)

3. Instrument Logging

- Provide code for logging PPS jitter, CPU temp, etc.

4. Wire Hardware Connections

- GPS PPS → PRS10 in

- PRS10 PPS → Timecard splitter → RPi GPIO18 + MAC pin

- PRS10 PPS → GPS EXTINT (timestamp incoming PPS)

5. Provide PRS10 Access

- RS232 serial connection to Waveshare PoE board

- Allow querying of temperature, clock data

6. Commit All Documentation

- EVKF9T Manual

- F9T-10 Integration Guide

- GPS L5 Enable Guide

7. Setup Secondary Raspberry Pi as PTP Client

8. Add 2nd USB Ethernet Adapters to Devices

- Separate SSH from PTP traffic

9. Setup Oscilloscope for PPS Comparison

- PRS10 PPS vs. RPi PTP-recovered PPS

10. Wire Rubidium Clock’s 10 MHz to SiLabs Clock Generator

- Explore non-Windows or I2C/SPI interface

- Professor to wire + students to find control path

11. Investigate Phase Comparison Features in SiLabs

- Compare multiple 10 MHz sources (rubidium, GPS, OCXO, etc.)

12. Setup SNMP Stats Server

- Possibly add IPMI compatibility

13. Provision Remote VM with Storage for DB

