# EcoTracker — References

---

## Libraries

| Library | Role | Docs |
|---|---|---|
| **Time** | Measures elapsed training time to calculate energy consumption per run | [docs.python.org](https://docs.python.org/3/library/time.html) |
| **Psutil** | Samples real-time CPU usage to estimate system power draw and CO₂ footprint | [psutil.readthedocs.io](https://psutil.readthedocs.io/stable/) |
| **Threading** | Runs CPU monitoring in the background while model training executes concurrently | [docs.python.org](https://docs.python.org/3/library/threading.html) |
| **Platform** | Detects processor type (IoT edge device vs. server) to select the correct TDP estimate | [docs.python.org](https://docs.python.org/3/library/platform.html) |

---

## Data Sources

### CO₂ Grid Intensity
Egypt-specific and global grid carbon intensity values used to convert energy consumption into CO₂ emissions.
- https://lowcarbonpower.org/region/Egypt
- https://www.researchgate.net/publication/383001672_IMPACT_OF_RENEWABLE_ENERGY_ON_POTENTIAL_GREEN_COMMUNITIES_-CASE_STUDY_MADINATY_EGYPT

### Water Footprint
Thermal and cooling water consumption factors per kWh of electricity used.
- https://www.mdpi.com/1996-1073/11/5/1117

### Electricity Pricing
Egyptian residential and commercial electricity tariffs used to calculate operational cost in EGP.
- https://www.dailynewsegypt.com/2024/01/02/egypt-raises-electricity-prices-by-up-to-26-in-bid-to-curb-subsidies/
- https://www.sciencedirect.com/science/article/pii/S2590140020300290

### Rare-Earth Materials
> **0.012 mg per kWh** — estimated proxy value for hardware material footprint. This is a model assumption; no direct measurement source is available.

### Tree CO₂ Absorption
Average annual CO₂ sequestration per tree (21 kg/year), as commonly cited by the EPA and USDA.
- https://www.epa.gov/
- https://www.usda.gov/

---

## Formulas

### CO₂ Emissions from Data Centres
Methodology for converting energy consumption to carbon emissions in compute environments.
- https://greenexdc.com/why-data-centers-are-affecting-a-carbon-footprint

### Solar Panel Equivalent
Used to express a model's energy footprint in terms of solar watt-peak (Wp), assuming 5.5 peak sun hours per day.
- https://www.makemyhousegreen.com/green-guides/how-to-calculate-solar-panel-output
