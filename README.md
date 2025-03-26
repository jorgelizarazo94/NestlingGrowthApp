                                                            Nestling Growth App
<p align="center">
  <img src="https://github.com/jorgelizarazo94/NestlingGrowthApp/blob/master/Nestling_App/api/assets/NGapp_log.png" alt="Nestling Growth App" width="200px">
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

## Features

✔ Upload CSV files with growth data  
✔ Select variables dynamically (e.g., weight, wing, tarsus)  
✔ Automatically fit multiple growth models and visualize the best fit  
✔ Export graphs and model results in CSV and PNG formats  
✔ Interactive UI powered by Dash and Plotly  
✔ Dual-tab layout for:
- **Weight Analysis**
- **Wing & Tarsus Analysis**

---

## Installation & Setup

### Option 1: Run Manually (Development Mode)

```bash
git clone https://github.com/jorgelizarazo94/NestlingGrowthApp.git
cd NestlingGrowthApp
pip install -r Nestling_App/api/requirements.txt
python Nestling_App/api/app.py

```

# Option 2: Install as a Python Package (from setup.py)

This lets you run the app from the command line using nestling-app

```bash
git clone https://github.com/jorgelizarazo94/NestlingGrowthApp.git
cd NestlingGrowthApp
pip install .
```
Then launch the app with:

```bash
nestling-app
```

# 🌐 Live Deployment

You can access the live app here:
[Nestling Growth App (if available)](https://nestling-growth-app.onrender.com)

# 📁 Project Structure

```
NestlingGrowthApp/
│
├── Nestling_App/
│   ├── api/
│   │   ├── app.py                # Main Dash app
│   │   ├── assets/               # Images and logo
│   │   ├── requirements.txt      # All dependencies
│   ├── models/
│   │   └── growth_models.py      # Growth model definitions
│   ├── components/
│   └── setup.py                 # Setup for pip installation
├── README.md
```

# **Contact**
For questions, suggestions or collaborations, feel free to:
Email: jorge.lizarazo.b@gmail.com
Open an issue: GitHub Issues


![Nestling Growth App](https://github.com/jorgelizarazo94/NestlingGrowthApp/blob/master/Nestling_App/api/assets/Logo.png)