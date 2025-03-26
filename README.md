<p align="center">
    <img src="https://raw.githubusercontent.com/jorgelizarazo94/NestlingGrowthApp/7a9916a809009ea6359db6b8e02645db32c0a28d/nestling_app/api/assets/ngapp_log.png" alt="Nestling Growth App" width="200px">
</p>

# 🐣 Nestling Growth App

The Nestling Growth App is a web-based tool designed for ornithologists, ecologists, and researchers working on nestling development. It allows users to visualize and model growth metrics such as weight, wing, and tarsus length using classic biological growth functions.
- Logistic  
- Gompertz  
- Richards  
- Von Bertalanffy  
- Extreme Value Function (EVF)  

This app is ideal for ecologists, ornithologists, and conservation biologists looking to model nestling growth patterns, compare model performance using AIC/BIC, and export results seamlessly.

---

## ✨ Features

✔ Upload CSV files with growth data  
✔ Select variables dynamically (e.g., weight, wing, tarsus)  
✔ Automatically fit multiple growth models and visualize the best fit  
✔ Export graphs and model results in CSV and PNG formats  
✔ Interactive UI powered by Dash and Plotly  
✔ Dual-tab layout:
- **Weight Analysis**
- **Wing & Tarsus Analysis**

## Input Format
The uploaded CSV should contain at least:
A day column (e.g., Day, Age, Month)
At least one of:
- Weight
- Wing
- Tarsus

## Output
Graphs with observed and fitted curves
A table comparing models by:
- PNG graphs ready for publishing 300dpi
- AIC/BIC
- Parameters
- Growth rate k
- Inflection point T
- ΔAIC

## Examples

You can access to the folder:
[data](https://github.com/jorgelizarazo94/NestlingGrowthApp/tree/16d2ace118ba1caaf614fd3fb4572b6ded4d18ea/nestling_app/data)
In order to have some previous data to test and learn from.

---
# 📦 Installation

You can install the app globally via pip:

```bash
pip install nestling-growth-app
```
Once installed, run it with:
```
nestling-app
```

### ✅ Option 2: One-Line Install (recommended)

Just open your terminal (or Anaconda Prompt) and run:

```bash
pip install git+https://github.com/jorgelizarazo94/NestlingGrowthApp.git

```
Then launch the app with:
```
nestling-app

```
It will open on: http://localhost:8050

## Option 3: Install in a Conda Environment (clean setup)

```
conda create -n nestlings python=3.9 -y
conda activate nestlings
pip install git+https://github.com/jorgelizarazo94/NestlingGrowthApp.git
nestling-app
```

## Option 4: Clone the Repo and Run (for development)
```
git clone https://github.com/jorgelizarazo94/NestlingGrowthApp.git
cd NestlingGrowthApp
pip install -e .
nestling-app

```

# 🌐 Live Deployment
If deployed on Render you can access the live app here::
[Nestling Growth App (if available)](https://nestling-growth-app.onrender.com)


# 📁 Project Structure
```
NestlingGrowthApp/
│
├── Nestling_App/
│   ├── api/
│   │   ├── app.py              # Main Dash app
│   │   ├── assets/             # Images and logo
│   │   ├── __init__.py
│   ├── models/
│   │   └── growth_models.py    # Growth model definitions
│   ├── setup.py                # Installer file for pip
├── requirements.txt
├── README.md
```

# **Contact**
For questions, suggestions or collaborations, feel free to:
Email: jorge.lizarazo.b@gmail.com
Open an issue: GitHub Issues



![Nestling Growth App](https://raw.githubusercontent.com/jorgelizarazo94/NestlingGrowthApp/7a9916a809009ea6359db6b8e02645db32c0a28d/nestling_app/api/assets/logo.png)
