                                                            Nestling Growth App

<p align="center">
  <img src="https://raw.githubusercontent.com/jorgelizarazo94/NestlingGrowthApp/master/Nestling_App/api/assets/NGapp_log.png" alt="Nestling Growth App" width="200px">
</p>


Overview

The Nestling Growth App is an interactive web application built with Dash, designed to analyze and visualize bird nestling growth data using multiple biological growth models, including:

Logistic

Gompertz

Richards

Von Bertalanffy

Extreme Value Function (EVF)

This app is ideal for ecologists, ornithologists, and conservation biologists looking to model nestling growth patterns, compare model performance using AIC/BIC, and export results seamlessly.

Features

✔ Upload CSV files with growth data.
✔ Select variables dynamically (e.g., weight, wing, tarsus).
✔ Automatically fit multiple growth models and visualize the best fit.
✔ Export graphs and model results in CSV and PNG formats.
✔ Interactive UI powered by Dash and Plotly.

🛠 Installation & Setup

1️⃣ Clone the repository

    git clone https://github.com/jorgelizarazo94/NestlingGrowthApp.git
    cd NestlingGrowthApp/Nestling_App/api

2️⃣ Install dependencies

    pip install -r requirements.txt

3️⃣ Run the application

    python app.py

Then open http://localhost:8050 in your web browser.

🌎 Live Deployment

You can access the live app here:
[Nestling Growth App (if available)](https://nestling-growth-app.onrender.com)

**Project Structure**

    NestlingGrowthApp
     │── Nestling_App
     │   ├── api
     │   │   ├── assets/ (Images, logo, etc.)
     │   │   ├── app.py (Main Dash app)
     │   │   ├── requirements.txt (Dependencies)
     │   ├── models/
     │       ├── growth_models.py (Growth model functions)
     │── README.md (This file)



Contact:

For questions or contributions, reach out via GitHub Issues or email: jorge.lizarazo.b@gmail.com



![Nestling Growth App](https://github.com/jorgelizarazo94/NestlingGrowthApp/blob/master/Nestling_App/api/assets/Logo.png)
