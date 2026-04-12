# 🌱 EcoTracker — Green AI Analytics

**Nile Delta crop yield prediction · Real-time environmental footprint benchmarking for ML models**

EcoTracker is a Streamlit dashboard that trains multiple machine learning models on simulated Egyptian farm data and measures the environmental cost of each one — CO₂ emissions, water consumption, energy use, rare-earth mineral proxy, and electricity cost — in real time. The goal is to help practitioners make sustainable AI choices without sacrificing the accuracy needed for agricultural decision-making.

---

## Why it exists

Egypt's Digital Agriculture 2030 initiative aims to deploy IoT + AI across 5,000+ Nile Delta farms. At that scale, the choice of ML model is not just a performance question — it is an environmental one. Training a Neural Network instead of a Linear Regression model can mean orders-of-magnitude more CO₂, water, and cost per daily prediction run. EcoTracker makes those trade-offs visible and quantified.

---

## Features

- **Live eco-profiling** — CPU usage is sampled in a background thread during training; energy, CO₂, water, rare-earth, and cost metrics are derived immediately after each model finishes.
- **Six models benchmarked side-by-side** — Linear Regression, Random Forest (10 / 100 / 500 trees), Gradient Boosting, and Neural Network.
- **Egypt-specific constants** — grid CO₂ intensity (0.420 kg/kWh), electricity price (EGP 1.25/kWh), and water footprint (2.3 L/kWh) are grounded in Egyptian data sources.
- **Green Score** — a composite metric that ranks models by their combined environmental footprint.
- **National-scale projection** — extrapolates the experiment footprint to a configurable number of farms and daily prediction frequency.
- **Real-world equivalents** — translates total CO₂ and energy into smartphone charges, LED bulb hours, km driven, and more.
- **Interactive charts** — bar charts, a radar/spider chart across six eco-dimensions, and a full results table, all built with Plotly.
- **Premium dark forest UI** — fully custom Streamlit theme using Syne, DM Mono, and Manrope fonts with a deep-green palette.

---

## Getting started

### Prerequisites

Python 3.9 or later is recommended.

### Install dependencies

```bash
pip install streamlit numpy pandas plotly scikit-learn psutil
```

### Run the app

```bash
streamlit run "EcoTracker - Green_AI_Analytics.py"
```

The app will open in your browser at `http://localhost:8501`.

---

## How to use

1. **Configure the dataset** in the sidebar — set the number of crop sample records (500–20,000), feature dimensions, and sensor noise level.
2. **Select models** to include in the benchmark using the checkboxes.
3. **Set the Egypt deployment scale** — number of active farms and daily predictions per farm.
4. Click **▶ Run experiment**. Models train one by one and eco-metrics are computed live.
5. Explore the results across three chart tabs: **Bar charts**, **Radar chart**, and **Water & Cost**.
6. Read the **Green AI insight** panel at the bottom for a plain-language recommendation.

The **🌿 Auto-select green models** button in the sidebar suggests the most energy-efficient configuration.

---

## Environmental constants used

| Constant | Value | Source |
|---|---|---|
| Egypt grid CO₂ intensity | 0.420 kg/kWh | Low Carbon Power / ResearchGate |
| Global grid CO₂ intensity | 0.357 kg/kWh | Standard global average |
| Water footprint | 2.3 L/kWh (thermal + cooling) | MDPI Energies |
| Rare-earth mineral proxy | 0.012 mg/kWh | Model assumption |
| Egypt electricity price | EGP 1.25/kWh | Daily News Egypt (2024) |
| Cloud compute cost | USD 0.12/kWh | Market estimate |
| Tree CO₂ absorption | 21 kg CO₂/year | EPA / USDA |

---

## Project structure

```
EcoTracker - Green_AI_Analytics.py   # Main Streamlit application
EcoTracker - References.md           # Data sources and formula references
README.md                            # This file
```

---

## Core libraries

| Library | Role |
|---|---|
| `streamlit` | Web dashboard framework |
| `psutil` | CPU and system power monitoring |
| `threading` | Background CPU sampling during model training |
| `time` | High-resolution elapsed-time measurement |
| `platform` | CPU detection for TDP estimation |
| `scikit-learn` | ML models and dataset generation |
| `plotly` | Interactive charts |
| `numpy` / `pandas` | Numerical computation and data handling |

---

## Formulas

**Energy (Wh)**
```
energy_wh = (TDP_watts × cpu_fraction × elapsed_seconds) / 3600 × 1.15
```
A 15% overhead factor accounts for memory, disk, and cooling.

**CO₂ (grams)**
```
co2_g = (energy_wh / 1000) × grid_intensity_kg_per_kwh × 1000
```

**Water (litres)**
```
water_L = (energy_wh / 1000) × 2.3
```

**Green Score** — composite index normalised across CO₂, water, energy, cost, rare-earth, and training time. Higher = greener.

Full formula references are in `EcoTracker - References.md`.

---

## References

See [`EcoTracker - References.md`] for the full list of sources covering CO₂ intensity data, water consumption factors, Egyptian electricity pricing, tree absorption rates, and formula derivations.

---

## Licence

This project was built for research and educational purposes under the Nile Delta Green AI initiative. Please cite the data sources listed in the references file when using the environmental constants in your own work.
