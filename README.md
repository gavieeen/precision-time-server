# **PTP/PPS TimeSync Grandmaster using Raspberry Pi-Based System in Distributed Systems and HFT**
[[_TOC_]]
# Objective

Our goal is to investigate the feasibility of using the Raspberry Pi CM4 as a GPS Grandmaster Clock. We aim to achieve microsecond-accurate time synchronization using a u-blox GPS module with PPS capabilities. This enables cost-effective timekeeping for applications such as high-frequency trading (HFT), distributed systems, and scientific instrumentation.

# Background

Precise time synchronization is critical in HFT and similar domains, where timing mismatches can lead to significant inefficiencies or financial losses. Commercial GPS Grandmaster clocks are expensive and complex. This project explores an accessible alternative using off-the-shelf Raspberry Pi hardware and open-source Linux tools.

# Relevance

Our findings will contribute to building more affordable infrastructure for precise time distribution in fields like telecom, finance, and IoT. By using open tools like gpsd and chrony, we hope to create a deployable blueprint for others seeking microsecond accuracy on a budget.

# Demo Video

![Demo Video](./assets/ie421_hft_spring_2025_group_07.mp4)

# Contributors

## Gavin Ebenezer
📸 **Photo**
<div align="center">
  <img src="./assets/GavinProfile.png" alt="Gavin Ebenezer Profile Pic" width="200"/>
</div>

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


## Chetan Boddeti
📸 **Photo**
<div align="center">
  <img src="./assets/ChetanProfile.jpeg" alt="Chetan Boddeti Profile Pic" width="200"/>
</div>

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


## Aryan Sapre
📸 **Photo**
<div align="center">
  <img src="./assets/AryanProfile.JPG" alt="Aryan Sapre" width="200"/>
</div>
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
## Advised by Professor Lariviere


# Hardware

- Raspberry Pi Compute Module 4 (CM4)

- Waveshare CM4 PoE board

- u-blox F9T GPS module (USB connection)

- GNSS antenna (external)

- PPS signal from GPS over USB (or optionally GPIO18)

# Software

- OS: Ubuntu Server 22.04 (64-bit)

- Key packages: gpsd, gpsd-clients, pps-tools, chrony

- Optional: xauth + X11 forwarding (for gpsmon)

# Final Report

For more details, please review our [final_report.md](final_report.md)

# License
[MIT License](LICENSE)

# Project status
Anyone may choose to fork this project or volunteer to step in as a maintainer or owner, allowing this project to keep going. You can also make an explicit request for maintainers.
