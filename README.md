# Aladdin Lite: IPO Factor Risk Engine

An institutional-grade risk management tool designed to stress-test IPO portfolios. This project replicates the core functionality of BlackRock's Aladdin by moving beyond simple historical tracking into **predictive risk modeling.**

### Core Features:
- **Monte Carlo Simulation:** Uses Geometric Brownian Motion (GBM) to simulate 10,000 market paths for IPO listings.
- **Parametric Risk Metrics:** Calculates **Value at Risk (VaR)** and **Conditional VaR (Expected Shortfall)** to quantify tail risk.
- **Scenario Stress-Testing:** Allows for "Black Swan" event modeling by adjusting volatility parameters.
- **Factor Attribution:** Correlates 'Hype Scores' and 'GMP' against realized Listing Gains.

### Tech Stack:
- **Language:** Python 3.9+
- **Analysis:** NumPy, SciPy, Pandas
- **Dashboard:** Streamlit, Plotly