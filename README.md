======================================================================
                  AGROWEATHERSENSE (FASAL GOSHI)
======================================================================

An intelligent, data-driven agricultural analysis system designed for 
Pakistani farming regions. This application integrates multi-source 
meteorological data, soil properties, and AI-powered insights to deliver 
actionable recommendations for crop management.

----------------------------------------------------------------------
FEATURES
----------------------------------------------------------------------
* Multi-Source Weather Integration: Collects real-time meteorological 
  parameters from OpenWeatherMap, Open-Meteo, and NASA POWER (solar 
  radiation and surface parameters).
* Soil & Thermal Analysis: Evaluates soil properties, moisture retention, 
  compaction risks, and root-zone thermal behavior based on local 
  coordinates.
* Seasonal Farming Calendar: Aligned with regional agricultural 
  schedules across Pakistan to optimize planting, irrigation, and 
  harvesting timelines.
* Multi-Crop Analysis: Compares suitability, rotation sequences, and 
  mixed-farming strategies for crops like Wheat, Rice, Cotton, and 
  Sugarcane.
* Automated Alerts: Generates risk evaluations and supports SMS 
  dispatching via Twilio.

----------------------------------------------------------------------
TECH STACK
----------------------------------------------------------------------
* Frontend/UI: Streamlit
* Data Processing: Pandas, NumPy
* Visualizations: Plotly
* APIs & AI: Google Generative AI, OpenAI, REST Weather APIs

----------------------------------------------------------------------
LOCAL INSTALLATION & SETUP
----------------------------------------------------------------------
1. Clone the repository:
   git clone https://github.com/ikramalishba991-debug/AgroWeatherSense-1.git
   cd AgroWeatherSense-1

2. Install the required dependencies:
   pip install -r requirements.txt

3. Run the Streamlit application:
   streamlit run app.py
