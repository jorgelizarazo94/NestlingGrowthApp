<p align="center">
  <img src="https://github.com/jorgelizarazo94/nestling_app/api/assets/ngapp_log.png" alt="Nestling Growth App" width="200px">
</p>

# 🐣 Nestling Growth App

The **Nestling Growth App** is an interactive web application built with Dash, designed to analyze and visualize bird nestling growth data using multiple biological growth models, including:

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

---

## ⚙️ How to Install & Run

### ✅ Option 1: One-Line Install (recommended)

Just open your terminal (or Anaconda Prompt) and run:

```bash
pip install git+https://github.com/jorgelizarazo94/NestlingGrowthApp.git

```
Then launch the app with:
```
nestling-app

```
It will open on: http://localhost:8050

## Option 2: Install in a Conda Environment (clean setup)

```
conda create -n nestlings python=3.9 -y
conda activate nestlings
pip install git+https://github.com/jorgelizarazo94/NestlingGrowthApp.git
nestling-app
```

## Option 3: Clone the Repo and Run (for development)
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

![Nestling Growth App](https://github.com/jorgelizarazo94/NestlingGrowthApp/blob/master/Nestling_App/api/assets/logo.png)
