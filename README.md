# **PTP/PPS TimeSync Grandmaster using Raspberry Pi-Based System in Distributed Systems and HFT**
[[_TOC_]]
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
💼 **Availability**
- 🎓 **Graduation:** May 2026  
- 💻 **Internships:** Open to **Fall 2025**, **Spring 2026**, and **Summer 2026** roles  
- 🔁 **Full-time:** Open to **full-time positions starting Summer 2026**
- 🌐 **Fields of Interest:** Software Engineering, Quantitative Finance, Trading Infrastructure, Backend Systems
- ☁️ **Summer 2025:** I’ll be joining **Amazon** as a **Software Development Engineer Intern**

---
🔗 **Links**
- [LinkedIn](https://www.linkedin.com/in/gavinebenezer/)
- [GitHub](https://github.com/gavieeen/)
- [GitLab](https://gitlab.engr.illinois.edu/gavinae2)
- [Personal Website](https://gavieeen.github.io/)
- Personal Email: gavinebenezer@gmail.com
- Student Email: gavinae2@illinois.edu

---
📸 **Photo**
<div align="center">
  <img src="./GavinProfile.png" alt="Gavin Ebenezer Profile Pic" width="200"/>
</div>


## Chetan Boddeti
Hi! I’m a Computer Science major at the **University of Illinois at Urbana‐Champaign**, graduating in **May 2026**.  
I am passionate about working on cutting-edge technology that can help us push the fronteir of AI and hardware. I enjoy working with GPU architecture and AI modeling as well as the intersection between HPC and statistics. My specific interests lie in ML, Bayesian Statistics, GPU Programming, and Distributed Systems.

I am also draw into the intersection of Finance and Software engineering and how we can use technology to further our understanding of money as we know it.

---
💼 **Availability**
- 🎓 **Graduation:** May 2026  
- 💻 **Internships:** Open to **Fall 2025**, **Spring 2026**, and **Summer 2026** roles  
- 🔁 **Full-time:** Open to **full-time positions starting Summer 2026**
- 🌐 **Fields of Interest:** Machine Learning, Quantitative Finance, Trading Infrastructure, Embedded Systems
- ☁️ **Summer 2025:** I’ll be joining **AMD** as a **AI Modeling and Software Automation Intern**

---
🔗 **Links**
- [LinkedIn](https://www.linkedin.com/in/chetan-boddeti/)
- [GitHub](https://github.com/Chetanb123/)
- [Personal Website](https://chetanb123.github.io/)
- Personal Email: chetan.boddeti@gmail.com
- Student Email: boddeti2@illinois.edu

---
📸 **Photo**
<div align="center">
  <img src="./ChetanProfile.jpeg" alt="Chetan Boddeti Profile Pic" width="200"/>
</div>


## Aryan Sapre
Hi, I'm Aryan Sapre, a Computer Science and Statistics major at the University of Illinois at Urbana-Champaign, graduating in May 2026. I'm passionate about pushing the bounds of technology and love working at the intersection of hardware and software. My specific interests lie in system programming, operating systems, and embedded systems, where I’m excited to explore how deep technical innovation can create real-world impact.

---
💼 **Availability**
- 🎓 **Graduation:** May 2026  
- 💻 **Internships:** Open to **Fall 2025**, **Spring 2026**, and **Summer 2026** roles  
- 🔁 **Full-time:** Open to **full-time positions starting Summer 2026**
- 🌐 **Fields of Interest:** Software Engineering, Quantitative Finance, Low Latency Software Development, Embedded Systems, Compilers, AI
- ☁️ **Summer 2025:** I’ll be joining **Capital One** as a **Software Engineer Intern**

---
🔗 **Links**
- [LinkedIn](https://www.linkedin.com/in/aryansapre/)
- Student Email: aryanns2@illinois.edu

---
📸 **Photo**
<div align="center">
  <img src="./AryanProfile.JPG" alt="Aryan Sapre" width="200"/>
</div>



**- Advised by Professor Lariviere**


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



# FINAL REPORT
**Executive Summary:**
This project aims to build a low-cost, precision time server using a Raspberry Pi CM4, GNSS receiver, and pulse-per-second (PPS) signal integration. The goal is to achieve sub-microsecond synchronization accuracy for time-sensitive applications, such as high-frequency trading (HFT) and distributed systems. By leveraging GPSD, chrony, and Telegraf for metric reporting, and visualizing with Grafana, the system provides live monitoring of satellite lock, jitter, and PTP clock quality.
Key outcomes include successful PPS signal parsing, live GPS/CPU metric exports, and Prometheus-compatible dashboard panels. The final recommendation is that this architecture is suitable for educational and experimental precision timing, though long-term deployment may benefit from hardware timestamping or grandmaster PTP hardware.

## 1. Introduction
In the world’s most competitive financial markets, *every millisecond is a race*. Traders and algorithms compete in what is known as the “race to zero”—the relentless quest to reduce trading latency to as close to zero as technology allows. In high-frequency trading (HFT), where thousands of orders are executed in the blink of an eye, victory belongs to those who can act fastest and most precisely. Here, time is not just money—it is the very fabric of fairness, opportunity, and success. Yet, in this environment, speed alone is not enough; it is the precision of time synchronization that determines who truly wins the race.

The “race to zero” has made accurate clock synchronization the backbone of modern electronic trading. Every microsecond matters: even the smallest misalignment between system clocks can result in trades being executed out of order, causing financial losses and regulatory complications. As exchanges prioritize orders by both price and the exact time of arrival, precise timekeeping ensures the integrity and transparency of the market.

Precise time synchronization is critical in fields like financial trading, telecommunications, and distributed computing. Commercial Precision Time Protocol (PTP) servers can be costly and complex. This project explores building a compact, affordable alternative using a Raspberry Pi Compute Module 4 (CM4) paired with a u-blox ZED-F9T Global Navigation Satellite System (GNSS) module. The objective is to design, configure, and verify a system capable of delivering precise Coordinated Universal Time (UTC)-synchronized timing signals and monitoring system jitter, satellite visibility, and clock quality. The work is scoped to Linux-based Pulse Per Second (PPS) processing and metric collection, without reliance on hardware timestamping network interface cards (NICs) or field-programmable gate array (FPGA) devices.

The need for such solutions is driven by both technological and regulatory pressures. Regulatory bodies such as the European Union’s Markets in Financial Instruments Directive II (MiFID II), the United States Financial Industry Regulatory Authority (FINRA), and the Securities and Exchange Commission (SEC) mandate strict synchronization requirements—often within microseconds of official standards like Coordinated Universal Time (UTC) or the National Institute of Standards and Technology (NIST). Achieving this level of accuracy requires robust protocols such as Network Time Protocol (NTP) and Precision Time Protocol (PTP), as well as fault-tolerant architectures that use multiple independent and traceable time sources, including Global Positioning System (GPS).

Traditional enterprise-grade time servers can be prohibitively expensive, especially for smaller firms or research and educational environments. Recent advances have demonstrated that affordable, single-board computers like the Raspberry Pi can serve as the foundation for precise time servers. By leveraging GPS receivers and running open-source PTP or NTP services, these systems offer a practical and scalable alternative for achieving high-precision time synchronization.

In this project, we evaluate the use of Raspberry Pi-based servers as Precision Time Protocol (PTP) Grandmaster Clocks, utilizing Global Positioning System (GPS) modules for high-precision timekeeping. Our aim is to demonstrate that small-scale, accessible solutions can meet the stringent timing requirements of high-frequency trading and other time-sensitive applications, lowering barriers to entry and enhancing the robustness of distributed systems infrastructure.

## 2. Background
### 2.1. One Second
The modern definition of a second—9,192,631,770 oscillations of a caesium-133 atom—has been adopted to overcome the inconsistencies in Earth’s rotation, providing a universal, stable reference for global time synchronization.

### 2.2. Clocks and Clock Error
A clock, in this context, is any device that measures and displays time. No physical clock is perfect; all are subject to clock error, which consists of:

- **Drift**: Predictable changes in timekeeping accuracy due to environmental factors such as temperature and aging.
- **Jitter**: Random, unpredictable fluctuations that add noise to the timing signal.
Both drift and jitter are critical considerations when designing systems for precise time synchronization, as they can accumulate and degrade accuracy over time.

### 2.3. Clock Synchronization Protocols
Synchronizing clocks across networked devices is achieved using protocols such as:

- **Network Time Protocol (NTP)**: Operates over the User Datagram Protocol (UDP) and achieves millisecond-level accuracy over the internet, and slightly better on local networks. However, NTP is limited by software latency and cannot guarantee the sub-microsecond precision required for HFT.
- **Precision Time Protocol (PTP)**: Designed for high-precision time synchronization, typically within sub-microsecond accuracy, across local area networks. PTP achieves superior accuracy by hardware timestamping synchronization messages, thereby accounting for device and network latency.
For this project, PTP is the protocol of choice, as it provides the level of precision necessary for applications like HFT, where latency arbitrage and order sequencing depend on extremely accurate timing.

### 2.4. Time Standards and GNSS
The global standard for civil timekeeping is Coordinated Universal Time (UTC), which incorporates leap seconds to remain aligned with Earth’s rotation. The Global Navigation Satellite System (GNSS), and specifically the Global Positioning System (GPS), is a practical means of distributing precise time worldwide. Each GPS satellite is equipped with multiple atomic clocks, broadcasting time signals that allow receivers to synchronize with high accuracy. This makes GNSS an ideal reference for building cost-effective, precise time servers.

### 2.5. Oscillators in Timekeeping
Oscillators generate the stable frequencies required for timekeeping. The most relevant types for this project are:

- **Quartz Oscillator**: Used in most consumer and embedded devices, including the Raspberry Pi. Quartz oscillators are stable and cost-effective but can be affected by temperature and environmental changes.
- **TCXO (Temperature Compensated Crystal Oscillator)**: Improves frequency stability by compensating for temperature variations, suitable for applications requiring moderate precision.
- **OCXO (Oven Controlled Crystal Oscillator)**: Provides even greater stability by maintaining the crystal at a constant temperature, though typically found in higher-end timing equipment.
- **Atomic Clocks**: Atomic clocks use the natural oscillations of atoms to keep extremely precise time. While not directly used in this project, they serve as the ultimate reference for GNSS satellites and national time standards. Common types include caesium and rubidium atomic clocks. Rubidium atomic clocks, for example, are compact, energy-efficient, and offer excellent frequency stability, making them popular in telecommunications, GNSS satellites, and as reference clocks in laboratories. Their main advantages are high accuracy (often within a few nanoseconds per day), long-term reliability, and minimal drift compared to quartz-based oscillators.

### 2.6. Time in Embedded Systems
In embedded systems like the Raspberry Pi, time is maintained by a combination of:

- **System Clock**: Driven by a quartz oscillator, used for general system timing.
- **Pulse Per Second (PPS) Input**: A hardware signal from the GNSS module that provides a precise timing edge each second, allowing the system clock to be disciplined to the GNSS reference.
- **GNSS Receiver**: Provides both time and position data, with the PPS output serving as the high-precision synchronization signal.
By combining the GNSS time reference, PPS input, and PTP protocol, this project achieves sub-microsecond synchronization accuracy suitable for HFT and other demanding applications, without the need for expensive hardware timestamping network interface cards (NICs) or atomic clocks.

### 2.7. Quality Metrics for GNSS Time Synchronization
To evaluate the accuracy and reliability of GNSS-based time synchronization, several parameters and metrics are monitored. Below are the most relevant indicators and what they mean:

#### 2.7.1. Satellite Count
The number of GNSS satellites currently visible to the receiver.
- **Importance**: A higher satellite count generally improves positional and timing accuracy, as the receiver can select the best signals and perform error correction.
- **Typical Values**: 4 is the minimum for a 3D fix; 6 or more is ideal for robust timing.
#### 2.7.2. Satellite Signal Strength (SNR)
Signal-to-noise ratio (SNR) for each satellite, usually measured in decibels (dB-Hz).
- **Importance**: High SNR values indicate strong, reliable signals. Low SNR can result in poor accuracy or loss of lock.
- **Typical Values**: Above 30 dB-Hz is considered good; below 25 dB-Hz may be unreliable.
#### 2.7.3. Satellite Position (Azimuth/Elevation)
The direction (azimuth) and angle above the horizon (elevation) of each satellite.
- **Importance**: Satellites high in the sky (high elevation) are less likely to be obstructed and provide better signals. Distribution across the sky (not all in one direction) improves accuracy.
- **How to View**: Tools like cgps, gpsmon, or gpspipe can display satellite maps and details.
#### 2.7.4. Lock Status (Fix/No Fix)
Indicates whether the receiver has a valid position and time solution.
- **No Fix**: Not enough satellites or poor signal.
- **2D Fix**: Position fixed in latitude/longitude.
- **3D Fix**: Position fixed in latitude, longitude, and altitude.
- **Time Fix**: Sufficient for accurate timing, even if position is ambiguous.
- **Importance**: A 3D or time fix is required for high-precision timing.
#### 2.7.5. PPS Offset and Jitter
The time difference (offset) between the Pulse Per Second (PPS) signal and the system clock, and the variation (jitter) of this offset.
- **Importance**: Low offset and jitter values indicate tight synchronization and stable timing performance.
- **How to View**: Tools like chronyc sourcestats, ppstest, or time_pps_fetch().
#### 2.7.6. Temperature
Some GNSS modules and oscillators report temperature.
- **Importance**: Temperature fluctuations can affect oscillator stability and timing accuracy, especially in quartz-based systems.
- **Monitoring**: Useful for diagnosing drift or instability issues.
#### 2.7.7. CGPS Output
The cgps tool provides a live summary of GNSS status, including:
- **Fix status**
- **Satellite count and signal strengths**
- **Latitude, longitude, altitude**
- **Time and date**
- **Speed, heading (if moving)**
- **Importance**: Offers a comprehensive, real-time view of receiver health and timing quality.
#### 2.7.8. Other Offsets and Delays
- **System Offset**: The difference between the system clock and the reference GNSS time.
- **Root Delay/Dispersion**: Network or hardware delays in the time synchronization path, reported by NTP/PTP/chrony.
- **Importance**: Monitoring these helps identify and correct sources of error in the timing chain.

## 3. Data and Preprocessing
Our data comes directly from GNSS receivers interfaced via GPSD over serial and PPS (Pulse Per Second) GPIO. Metrics of interest include:

* GPS time, satellite count, position accuracy (via `gpspipe` JSON output)
* PPS stability via `/dev/pps0`
* System-level CPU usage and jitter (via Telegraf’s system plugins)

We used GPSD to parse GNSS data and chrony to align the system clock using PPS. The metrics are transformed using a Telegraf exec plugin which parses `gpspipe -w` JSON using `jq` to output Influx-compatible metrics. PPS signals are validated via `ppstest`, `chronyc sourcestats`, and `time_pps_fetch()` output.

These preprocessing steps ensure that raw signal data is aligned, filtered, and transformed for real-time metric export.

---

## 4. Methodology
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

## 5. Implementation
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

## 6. Results and Analysis
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

## 7. Conclusion and Future Work
This project successfully demonstrates a software-defined precision timing server using Raspberry Pi hardware and GNSS PPS signals. Our modular setup with GPSD, chrony, Telegraf, and Grafana provides real-time insights into GPS synchronization and system health.

In future iterations, we recommend:

* Incorporating external OCXO/Rubidium clocks for holdover
* Evaluating MAC timestamping NICs for nanosecond PTP precision
* Automating backup and restore of Grafana dashboards
* Creating alerts for satellite dropout, jitter spikes, or offset drifts

Team Members: (Chetan Boddeti), (Aryan Sapre), (Gavin Ebenezer)





## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.




