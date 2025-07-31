# English Documentation

## 🎓 Context

- This repository hosts the implementation developed for my **Undergraduate Thesis (TCC)** in Computer Science.
- The goal was to **design a regional air network and select aircraft types for a new regional airline with a hub in Chapecó (Brazil)** using **Integer Linear Programming model**.

**Full thesis (PDF, in Portuguese):** [`tcc2_leonardo_brancalione.pdf`](tcc2_leonardo_brancalione.pdf)

## 🧩 Overview

- **Language:** Python 3.11
- **Solver:** Gurobi (academic license)
- **Key libs:** `gurobipy`, `pandas`, `numpy`, `openpyxl`
- **Inputs:** `.xlsx` and `.json` files (aircraft specs, airports, demand, fares)
- **Outputs:** `.csv` table of routes, passenger flows, and binary decisions

## 🗂️ Structure

<details>
<summary>Click to expand</summary>

```bash
.
├── main_project/
│   ├── src/
│   │   ├── consts.py
│   │   ├── optimization.py
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── airplane.py
│   │   │   ├── airport.py
│   │   │   ├── model_vars.py
│   │   │   ├── route.py
│   │   │   └── __init__.py
│   │   └── utils/
│   │       ├── file_utils.py
│   │       ├── print_utils.py
│   │       ├── str_utils.py
│   │       ├── utils.py
│   │       └── __init__.py
│   ├── input/
│   │   ├── 2019.xlsx
│   │   ├── 2024.xlsx
│   │   ├── AerodromosPublicos.json
│   │   └── airplanes.xlsx
│   ├── output/
│   ├── requirements.txt
│   └── main.py
└── .gitignore
```
</details>

## 🚀 Quick Start

**1. Clone and enter**
```bash
git clone https://github.com/mactaviish/tcc.git
cd tcc\main_project
```

**2. Environment setup**
```bash
python -m venv .venv
# Windows:
.venv/Scripts/activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Run solver**
```bash
python main.py
```

**4. View results**
```bash
cd output
ls
```
