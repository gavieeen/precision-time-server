# **group_07_project: PTP/PPS TimeSync Grandmaster using Raspberry Pi-Based System in Distributed Systems and HFT**

# Objective

Our goal is to investigate the feasibility of using the Raspberry Pi CM4 as a GPS Grandmaster Clock. We aim to achieve microsecond-accurate time synchronization using a u-blox GPS module with PPS capabilities. This enables cost-effective timekeeping for applications such as high-frequency trading (HFT), distributed systems, and scientific instrumentation.

# Background

Precise time synchronization is critical in HFT and similar domains, where timing mismatches can lead to significant inefficiencies or financial losses. Commercial GPS Grandmaster clocks are expensive and complex. This project explores an accessible alternative using off-the-shelf Raspberry Pi hardware and open-source Linux tools.

# Relevance

Our findings will contribute to building more affordable infrastructure for precise time distribution in fields like telecom, finance, and IoT. By using open tools like gpsd and chrony, we hope to create a deployable blueprint for others seeking microsecond accuracy on a budget.

# Contributors



## Gavin Ebenezer
Hi! I’m a Computer Science major at the **University of Illinois at Urbana‐Champaign**, graduating in **May 2026**.  
It’s fun to solve problems. That curiosity and persistence have fueled my love for Computer Science, especially in areas like **data structures and algorithms**. I enjoy the mathematical elegance of efficient problem-solving and the creativity involved in building solutions that scale.

I’m especially drawn to the world of **software engineering and finance**, where precision and performance go hand in hand. It's no surprise that the HFT field, where complex algorithms drive trading decisions, inspires me.

---
💼 Availability
- 🎓 **Graduation:** May 2026  
- 💻 **Internships:** Open to **Fall 2025**, **Spring 2026**, and **Summer 2026** roles  
- 🔁 **Full-time:** Open to **full-time positions starting Summer 2026**
- 🌐 **Fields of Interest:** Software Engineering, Quantitative Finance, Trading Infrastructure, Backend Systems
- ☁️ **Summer 2025:** I’ll be joining **Amazon** as a **Software Development Engineer Intern**

---
🔗 Links
- [LinkedIn](https://www.linkedin.com/in/gavinebenezer/)
- [GitHub](https://github.com/gavieeen/)
- [GitLab](https://gitlab.engr.illinois.edu/gavinae2)
- [Personal Website](https://gavieeen.github.io/)
- Personal Email: gavinebenezer@gmail.com
- Student Email: gavinae2@illinois.edu

---
📸 Photo
<div align="center">
  <img src="./GavinProfile.png" alt="Gavin Ebenezer Profile Pic" width="200"/>
</div>


## Chetan Boddeti
Hi! I’m a Computer Science major at the **University of Illinois at Urbana‐Champaign**, graduating in **May 2026**.  
I am passionate about working on cutting-edge technology that can help us push the fronteir of AI and hardware. I enjoy working with GPU architecture and AI modeling as well as the intersection between HPC and statistics. My specific interests lie in ML, Bayesian Statistics, GPU Programming, and Distributed Systems.

I am also draw into the intersection of Finance and Software engineering and how we can use technology to further our understanding of money as we know it.

---
💼 Availability
- 🎓 **Graduation:** May 2026  
- 💻 **Internships:** Open to **Fall 2025**, **Spring 2026**, and **Summer 2026** roles  
- 🔁 **Full-time:** Open to **full-time positions starting Summer 2026**
- 🌐 **Fields of Interest:** Machine Learning, Quantitative Finance, Trading Infrastructure, Embedded Systems
- ☁️ **Summer 2025:** I’ll be joining **AMD** as a **AI Modeling and Software Automation Intern**

---
🔗 Links
- [LinkedIn](https://www.linkedin.com/in/chetan-boddeti/)
- [GitHub](https://github.com/Chetanb123/)
- [Personal Website](https://chetanb123.github.io/)
- Personal Email: chetan.boddeti@gmail.com
- Student Email: boddeti2@illinois.edu

---
📸 Photo
<div align="center">
  <img src="./ChetanProfile.jpeg" alt="Chetan Boddeti Profile Pic" width="200"/>
</div>


## Aryan Sapre
Hi, I'm Aryan Sapre, a Computer Science and Statistics major at the University of Illinois at Urbana-Champaign, graduating in May 2026. I'm passionate about pushing the bounds of technology and love working at the intersection of hardware and software. My specific interests lie in system programming, operating systems, and embedded systems, where I’m excited to explore how deep technical innovation can create real-world impact.

Linkedin: https://www.linkedin.com/in/aryansapre/
Email: aryanns2@illinois.edu
---
💼 Availability
- 🎓 **Graduation:** May 2026  
- 💻 **Internships:** Open to **Fall 2025**, **Spring 2026**, and **Summer 2026** roles  
- 🔁 **Full-time:** Open to **full-time positions starting Summer 2026**
- 🌐 **Fields of Interest:** Software Engineering, Quantitative Finance, Low Latency Software Development, Embedded Systems, Compilers, AI
- ☁️ **Summer 2025:** I’ll be joining **Capital One** as a **Software Engineer Intern**

---
📸 Photo
<div align="center">
  <img src="./AryanProfile.JPG" alt="Aryan Sapre" width="200"/>
</div>









**-Advised by Professor Lariviere**



## Hardware

- Raspberry Pi Compute Module 4 (CM4)

- Waveshare CM4 PoE board

- u-blox F9T GPS module (USB connection)

- GNSS antenna (external)

- PPS signal from GPS over USB (or optionally GPIO18)

## Software

- OS: Ubuntu Server 22.04 (64-bit)

- Key packages: gpsd, gpsd-clients, pps-tools, chrony

- Optional: xauth + X11 forwarding (for gpsmon)



# Final Report
**Executive Summary**
This project aims to build a low-cost, precision time server using a Raspberry Pi CM4, GNSS receiver, and pulse-per-second (PPS) signal integration. The goal is to achieve sub-microsecond synchronization accuracy for time-sensitive applications, such as high-frequency trading (HFT) and distributed systems. By leveraging GPSD, chrony, and Telegraf for metric reporting, and visualizing with Grafana, the system provides live monitoring of satellite lock, jitter, and PTP clock quality.
Key outcomes include successful PPS signal parsing, live GPS/CPU metric exports, and Prometheus-compatible dashboard panels. The final recommendation is that this architecture is suitable for educational and experimental precision timing, though long-term deployment may benefit from hardware timestamping or grandmaster PTP hardware.

---

**Introduction**
Precise time synchronization is critical in fields like financial trading, telecommunications, and distributed computing. Commercial PTP (Precision Time Protocol) servers can be costly and complex. This project explores building a compact, affordable alternative using a Raspberry Pi CM4 paired with a u-blox ZED-F9T GNSS module.
The objective is to design, configure, and verify a system capable of delivering precise UTC-synchronized timing signals and monitoring system jitter, satellite visibility, and clock quality. The work is scoped to Linux-based PPS processing and metric collection, without reliance on hardware timestamping NICs or FPGA devices.

---

**Data and Preprocessing**
Our data comes directly from GNSS receivers interfaced via GPSD over serial and PPS (Pulse Per Second) GPIO. Metrics of interest include:

* GPS time, satellite count, position accuracy (via `gpspipe` JSON output)
* PPS stability via `/dev/pps0`
* System-level CPU usage and jitter (via Telegraf’s system plugins)

We used GPSD to parse GNSS data and chrony to align the system clock using PPS. The metrics are transformed using a Telegraf exec plugin which parses `gpspipe -w` JSON using `jq` to output Influx-compatible metrics. PPS signals are validated via `ppstest`, `chronyc sourcestats`, and `time_pps_fetch()` output.

These preprocessing steps ensure that raw signal data is aligned, filtered, and transformed for real-time metric export.

---

**Methodology**
The system’s architecture includes:

* A GNSS receiver with PPS output connected to GPIO18
* GPSD service for GNSS parsing
* Chrony for disciplining the system clock via PPS
* Telegraf for metric ingestion, including a custom GPS exec script
* Prometheus-compatible endpoint for metric scraping

Metrics include:

* `gps_status_lat`, `gps_status_lon`, `gps_status_alt`: Live GNSS coordinates
* `gps_status_sep`, `gps_status_eph`: Satellite precision metrics
* `cpu_usage_user`, `cpu_usage_idle`, `irq`, `iowait`: System load
* `chrony_skew_ppm`, `chrony_rms_offset`, `chrony_jitter`: Clock discipline quality

Grafana dashboards visualize trends and allow remote analysis of satellite visibility, jitter trends, and pulse quality over time.

---

**Implementation**
Technologies used:

* `gpsd`, `chrony`, `ppstest`: low-level GNSS/PPS parsing
* `jq`, `gpspipe`, Bash: custom script metrics extraction
* `Telegraf`: main collector for CPU, PPS, GPS
* `Grafana`: visualization

Key configuration files:

* `/etc/telegraf/telegraf.conf` with `inputs.exec` for GPS parsing
* `telegraf-gps.sh`: Parses `gpspipe -w` JSON and exports metrics
* `/etc/telegraf/telegraf.d/prometheus_output.conf`: Enables Prometheus scraping on port 9273

To run:

1. SSH into the Pi using your key
2. Start GPSD and chrony services
3. Run: `sudo systemctl start telegraf`
4. Visit `localhost:3000` on a port-forwarded browser to view dashboards

All settings are stored in `telegraf-gps-backup.tar.gz` and versioned for reproducibility.

---

**Results and Analysis**
Sample metrics collected:

* `gps_status_lat=41.88`, `lon=-87.64`, `alt=295.2`
* `gps_status_sep=19.97`, `eph=1.13`, `status=1`
* CPU jitter remained below 5% across monitored intervals
* `chronyc tracking` output showed <10us RMS offset from PPS-synced source

Visualizations:

* Grafana panel: Altitude over time (`gps_status_alt`)
* Grafana panel: Satellite visibility (`gps_status_sep`, `eph`)
* Grafana panel: CPU usage and system jitter (`cpu_usage_irq`, `cpu_usage_user`)
* Chrony timing stats overlayed on a dashboard using `exec` plugin

These results confirm stable PPS input, high GNSS fix quality, and usable system clock alignment.

---

**Conclusion and Future Work**
This project successfully demonstrates a software-defined precision timing server using Raspberry Pi hardware and GNSS PPS signals. Our modular setup with GPSD, chrony, Telegraf, and Grafana provides real-time insights into GPS synchronization and system health.

In future iterations, we recommend:

* Incorporating external OCXO/Rubidium clocks for holdover
* Evaluating MAC timestamping NICs for nanosecond PTP precision
* Automating backup and restore of Grafana dashboards
* Creating alerts for satellite dropout, jitter spikes, or offset drifts

Team Members: (Chetan Boddeti), (Aryan Sapre), (Gavin Ebenezer)





## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.




