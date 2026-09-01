> ⚠️ **Disclaimer:** This software is a research and educational prototype. Its outputs must not be interpreted as engineering design, regulatory assessment, reservoir certification, or operational advice. Model assumptions require calibration against site-specific field data.

# 🌍 BECCS Integrated Systems Simulator Pro (v1.4)
**Python Framework | Object-Oriented Architecture | License: MIT Academic Domain**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-PyQt5%20%7C%20PyQtGraph-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg?logo=sqlite)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Domain](https://img.shields.io/badge/Domain-CCUS%20%2F%20BECCS%20Systems-purple.svg)](#)

An open-source, object-oriented desktop research simulator designed for analyzing **Bioenergy with Carbon Capture and Storage (BECCS)** value chains. This framework bridges *Ecosphere* biomass kinetics, *Technosphere* capture efficiency, and *Geosphere* carbon sequestration mechanisms (Saline Aquifers, Depleted Reservoirs, and Basalt In-situ Mineralization) using a rigorous systems-thinking methodology.

---

## 🖥️ Application Dashboard & Visualization
<img width="1366" height="680" alt="BECCS Simulator Dashboard v1.4" src="https://github.com/user-attachments/assets/5c914ec5-8b95-49f0-863c-917a6654ae31" />
<img width="1366" height="682" alt="BECCS Simulator Trajectory Analysis" src="https://github.com/user-attachments/assets/ab6c0828-cdbb-4c3d-8bf5-13ca9a74dd11" />

*Real-time dynamic visualization of cumulative gross, injected, mobile, and mineralized CO₂ trajectories with interactive multi-parameter crosshairs and a comprehensive KPI mass-balance panel.*

---

## ✨ Key Features (v1.4)
* **Subsurface Trapping Dynamics:** Accurate behavioral modeling for 3 distinct geological hosts (*Basalt In-situ Mineralization / CarbFix*, *Saline Aquifers*, *Depleted Hydrocarbon Reservoirs*).
* **Multi-Scale Units:** Dynamic toggle between **Tons**, **kTons ($10^3\text{ Tons}$)**, and **MTons ($10^6\text{ Tons}$)** with synchronized metric conversions.
* **Interactive Live Crosshairs (+):** High-frequency cursor tracking with real-time inspection tooltip over mass-balance curves (`PyQtGraph`).
* **Relational Storage Engine:** Integrated SQLite3 persistence (`beccs_records.db`) with historical scenario management.
* **Automated Reporting:** Instant high-resolution vector PDF generation and Excel-compatible CSV exports.
* **Security & Auditing:** Role-based UI lock/unlock and interactive real-time execution logger.

---

## 🔬 Scientific Core & Systems Modeling
The simulator decomposes the net negative-emission lifecycle into coupled dynamic sub-systems, ensuring full accountability for mass losses and phase changes across the CCUS chain.

### 🧮 Mass Balance Chain Architecture
| ⚙️ Stage | 📊 Metric Name | Unit Scaling | 📝 Scientific Description |
| :--- | :--- | :--- | :--- |
| **Capture 🏭** | Gross Captured CO₂ | Tons / kTons / MTons | Biomass conversion scaled by plant capture efficiency ($\eta_{cap}$) |
| **Transport 🚰** | Transported CO₂ | Tons / kTons / MTons | Gross mass minus pipeline & compression transmission losses ($\sim 1.5\%$) |
| **Injection 💉** | Injected CO₂ | Tons / kTons / MTons | Wellhead throughput constrained by geological storage capacity ($Cap_{max}$) |
| **Storage 🪨** | Net Stored CO₂ | Tons / kTons / MTons | Injected mass minus formation leakage ($L_c$) over reservoir lifetime |
| **Mineralization 💎** | In-situ Mineralized CO₂ | Tons / kTons / MTons | Rapid permanent carbonate precipitation (e.g., Basaltic host rocks) |
| **Credit 🌿** | Net GGR Removal | Tons / kTons / MTons | Net geological balance factoring upstream & transport lifecycle penalties |

### 📐 Systems Modeling Definitions & Mathematical Formulations
The lifecycle variables are constrained by the following equations:

* **Gross Captured ($C_g$)**:
  $$C_g(t) = B_m \times \eta_{cap} \times t$$
  *(where $B_m$ is annual biomass mass, $\eta_{cap}$ is capture efficiency, and $t$ is duration in years)*

* **Transported ($T_m$)**:
  $$T_m(t) = C_g(t) \times (1 - \lambda_{trans})$$
  *(where $\lambda_{trans} = 0.015$ accounting for line losses and compression slips)*

* **Injected ($I_m$)**:
  $$I_m(t) = \min\left(T_m(t), Cap_{max}\right)$$
  *(where $Cap_{max}$ represents site-specific geological pore volume limit)*

* **Cumulative Formation Leakage ($L_c$)**:
  $$L_c(t) = I_m(t) \times \left(1 - e^{-\lambda_{form} \cdot t}\right)$$
  *(with empirical leakage factors: $\lambda_{\text{Aquifer}} = 0.004$, $\lambda_{\text{Depleted}} = 0.0015$, $\lambda_{\text{Basalt}} \approx 0.0001$)*

* **In-situ Mineralization ($M_m$)**:
  $$M_m(t) = \left(I_m(t) - L_c(t)\right) \times \gamma_{max} \times \left(1 - e^{-k_{min} \cdot t}\right)$$
  *(where Basalt achieves $\gamma_{max} = 85\%$ fast-kinetics precipitation via CarbFix pathways)*

* **Net Geological Storage ($S_{net}$)** & **Net Carbon Removal ($R_{net}$)**:
  $$S_{net}(t) = I_m(t) - L_c(t)$$
  $$R_{net}(t) = S_{net}(t) - \left(C_g(t) \times \lambda_{trans}\right)$$

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
Ensure you have Python 3.9+ installed:
```bash
git clone https://github.com/parvizt/BECCS-Systems-Simulator.git
cd BECCS-Systems-Simulator

**### 2. Install Dependencies
**

pip install -r requirements.txt
(Dependencies: PyQt5, pyqtgraph, numpy)

**### 3. Run Simulator
**
python beccs_simulator.py
🔑 Default Admin Password: admin (Click Unlock on top-right to activate control inputs).

**📁 Repository Structure
**
text
├── beccs_simulator.py       # Main Application & GUI Architecture (PyQt5 + PyQtGraph)
├── beccs_records.db         # SQLite Scenario Database (auto-generated)
├── requirements.txt         # Project Dependencies
├── LICENSE                  # MIT License
└── README.md                # Project Documentation & Theoretical Formulations

**🗺️ Research & Development Roadmap**
[ ] Wellbore Integrity Modeling 🛢️: Add physics for casing pressure degradation and micro-annulus leakage probabilities.
[ ] Techno-Economic Integration 📉: Dynamic Levelized Cost of CO₂ Removal (LCOE & CAPEX/OPEX curve estimation).
[ ] Subsurface LAS Import 📂: Direct ingestion of site-specific well logs (porosity and permeability profiles).
[ ] Mobile Deployment 📱: Cross-platform Kivy/Flutter deployment via WSL for Android devices.
👨‍💻 Author & Attribution
Developed with a systems-thinking approach for CCUS and subsurface engineering.

Platform: AiBrothersTools.ir
Domain: Geological Carbon Storage & Energy Transition Systems
