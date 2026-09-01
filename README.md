> ⚠️ **Disclaimer:** This software is a research and educational prototype. Its outputs must not be interpreted as engineering design, regulatory assessment, reservoir certification, or operational advice. Model assumptions require calibration against site-specific field data.

# 🌍 BECCS Integrated Systems Simulator
**Python Framework | License: MIT Academic Domain**

An open-source, object-oriented desktop research simulator designed for analyzing **Bioenergy with Carbon Capture and Storage (BECCS)** value chains. This framework bridges *Ecosphere* biomass kinetics, *Technosphere* capture efficiency, and *Geosphere* carbon sequestration mechanisms (Saline Aquifers, Depleted Reservoirs, and Basalt In-situ Mineralization) using a rigorous systems-thinking methodology.

---

## 🖥️ Application Dashboard & KPI Panel
![BECCS Simulator Dashboard v1.2](image.png)
*Real-time dynamic visualization of cumulative mobile and mineralized CO₂ trajectories with interactive multi-parameter crosshairs and a comprehensive KPI mass-balance panel.*

---

## 🔬 Scientific Core & Systems Modeling
The simulator decomposes the net negative-emission lifecycle into three coupled dynamic sub-systems, ensuring full accountability for efficiency losses across the CCUS chain.

### 🧮 Mass Balance Chain
| ⚙️ Stage | 📊 Metric Name | Example Value (Mt CO₂) | 📝 Notes |
| :--- | :--- | :--- | :--- |
| **Capture 🏭** | Gross Captured CO₂ | 990.0 | Post-plant capture efficiency |
| **Transport 🚰** | Transported CO₂ | 988.0 | Pipeline losses (~0.2% typical) |
| **Injection 💉** | Injected CO₂ | 970.0 | Wellhead & pump leakage |
| **Storage 🪨** | Net Stored CO₂ | 950.0 | Mobile + Mineralized minus formation leakage |
| **Credit 🌿** | Net GGR Removal | 902.5 | Factoring in LCA emissions (Net Negative) |

### 📐 Systems Modeling Definitions & Formulas
The core variables are governed by the following constraints and lifecycle equations:

*   **Gross Captured ($C_g$)**: 
    $$C_g = B_m \times 1.5 \times \eta_{cap}$$ 
    *(where $B_m$ is biomass mass, $1.5$ is stoichiometric conversion, $\eta_{cap}$ is capture efficiency)*
*   **Transported ($T_m$)**: 
    $$T_m = C_g \times (1 - \lambda_{trans})$$
*   **Injected ($I_m$)**: 
    $$I_m = T_m \times (1 - \lambda_{inj})$$
*   **Cumulative Leakage ($L_c$)**: 
    $$L_c = \sum_{t=0}^{n} (Pool_{t} \times \lambda_{form})$$ 
    *(where $\lambda_{form}$ is specific to Basalt, Aquifer, or Depleted Reservoir)*
*   **Mineralized ($M_m$)**: 
    $$M_m = \sum_{t=0}^{n} (Pool_{t} \times \gamma_{min})$$
*   **Net Stored ($S_{net}$)**: 
    $$S_{net} = I_m - L_c$$
*   **Net GGR ($R_{net}$)**: 
    $$R_{net} = S_{net} \times \eta_{LCA}$$

---

## 🗺️ Research & Development Roadmap
- [ ] **Wellbore Integrity Modeling 🛢️**: Add physics for casing pressure and micro-annulus leakage probabilities.
- [ ] **Cost Curve Integration 📉**: Techno-economic analysis (LCOE & Cost per ton of CO₂ removed).
- [ ] **Real-world Data Support 📂**: Import site-specific permeability and porosity log data (LAS files).
- [ ] **Mobile Export 📱**: Buildozer deployment for Android devices (via Kivy/Flutter integrations).
