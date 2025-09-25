import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

from weather_apis import WeatherDataCollector
from ai_analysis import AgriculturalAnalyzer
from sms_service import SMSService
from crop_data import CropDatabase
from data_processor import DataProcessor
from utils import get_pakistan_coordinates, validate_phone_number

# Page configuration
st.set_page_config(
    page_title="AI Agricultural Analysis System",
    page_icon="🌾",
    layout="wide"
)

# Initialize services
@st.cache_resource
def initialize_services():
    weather_collector = WeatherDataCollector()
    ai_analyzer = AgriculturalAnalyzer()
    sms_service = SMSService()
    crop_db = CropDatabase()
    data_processor = DataProcessor()
    
    return weather_collector, ai_analyzer, sms_service, crop_db, data_processor

weather_collector, ai_analyzer, sms_service, crop_db, data_processor = initialize_services()

# Main title
st.title("🌾 AI-Powered Agricultural Analysis System")
st.markdown("### Intelligent Farming Insights for Pakistan")

# Sidebar for inputs
st.sidebar.header("Location & Contact Settings")

# Location input
location_option = st.sidebar.selectbox(
    "Select Location Method",
    ["Major Cities", "Custom Coordinates"]
)

if location_option == "Major Cities":
    city = st.sidebar.selectbox(
        "Select City",
        ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", 
         "Multan", "Peshawar", "Quetta", "Sialkot", "Gujranwala"]
    )
    coordinates = get_pakistan_coordinates(city)
    lat, lon = coordinates[city]
else:
    lat = st.sidebar.number_input("Latitude", value=31.5497, format="%.4f")
    lon = st.sidebar.number_input("Longitude", value=74.3436, format="%.4f")

# Phone number for SMS alerts
phone_number = st.sidebar.text_input(
    "Phone Number (with country code)",
    placeholder="+92XXXXXXXXXX",
    help="Enter phone number in international format"
)

# Crop selection
crop_type = st.sidebar.selectbox(
    "Select Crop Type",
    ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize", "Barley", "Millet", "Sorghum"]
)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Weather Data Dashboard")
    
    # Data collection section
    if st.button("🔄 Collect Latest Weather Data", type="primary"):
        with st.spinner("Collecting weather data from multiple sources..."):
            try:
                # Collect weather data
                weather_data = weather_collector.collect_all_data(lat, lon)
                
                if weather_data:
                    st.session_state.weather_data = weather_data
                    st.success("✅ Weather data collected successfully!")
                else:
                    st.error("❌ Failed to collect weather data. Please check your API keys.")
                    
            except Exception as e:
                st.error(f"❌ Error collecting data: {str(e)}")

    # Display weather data if available
    if 'weather_data' in st.session_state:
        weather_data = st.session_state.weather_data
        
        # Current weather display
        st.subheader("🌤️ Current Weather Conditions")
        
        if 'current' in weather_data:
            current = weather_data['current']
            
            col_temp, col_humid, col_wind, col_pressure = st.columns(4)
            
            with col_temp:
                st.metric("Temperature", f"{current.get('temperature', 'N/A')}°C")
            with col_humid:
                st.metric("Humidity", f"{current.get('humidity', 'N/A')}%")
            with col_wind:
                st.metric("Wind Speed", f"{current.get('wind_speed', 'N/A')} m/s")
            with col_pressure:
                st.metric("Pressure", f"{current.get('pressure', 'N/A')} hPa")
        
        # Forecast visualization
        if 'forecast' in weather_data:
            st.subheader("📈 7-Day Weather Forecast")
            
            forecast_df = pd.DataFrame(weather_data['forecast'])
            
            if not forecast_df.empty:
                # Temperature chart
                fig_temp = px.line(
                    forecast_df, 
                    x='date', 
                    y=['temp_max', 'temp_min'],
                    title="Temperature Forecast",
                    labels={'value': 'Temperature (°C)', 'date': 'Date'}
                )
                st.plotly_chart(fig_temp, use_container_width=True)
                
                # Precipitation chart
                if 'precipitation' in forecast_df.columns:
                    fig_precip = px.bar(
                        forecast_df,
                        x='date',
                        y='precipitation',
                        title="Precipitation Forecast",
                        labels={'precipitation': 'Precipitation (mm)', 'date': 'Date'}
                    )
                    st.plotly_chart(fig_precip, use_container_width=True)

        # NASA POWER data visualization
        if 'nasa_power' in weather_data:
            st.subheader("☀️ Solar Radiation & Agricultural Parameters")
            
            nasa_data = weather_data['nasa_power']
            if nasa_data and 'parameters' in nasa_data:
                params = nasa_data['parameters']
                
                col_solar, col_temp_range = st.columns(2)
                
                with col_solar:
                    if 'ALLSKY_SFC_SW_DWN' in params:
                        solar_data = params['ALLSKY_SFC_SW_DWN']
                        if solar_data:
                            recent_solar = list(solar_data.values())[-7:]  # Last 7 days
                            dates = list(solar_data.keys())[-7:]
                            
                            fig_solar = px.line(
                                x=dates,
                                y=recent_solar,
                                title="Solar Radiation (kWh/m²/day)",
                                labels={'x': 'Date', 'y': 'Solar Radiation'}
                            )
                            st.plotly_chart(fig_solar, use_container_width=True)

        # Open-Meteo data (Pakistani local weather)
        if 'open_meteo' in weather_data:
            st.subheader("🇵🇰 Pakistani Local Weather Data (Open-Meteo)")
            
            meteo_data = weather_data['open_meteo']
            
            col_meteo1, col_meteo2 = st.columns(2)
            
            with col_meteo1:
                if 'current' in meteo_data:
                    current_meteo = meteo_data['current']
                    st.metric("Local Temperature", f"{current_meteo.get('temperature', 'N/A')}°C")
                    st.metric("Wind Speed", f"{current_meteo.get('wind_speed', 'N/A')} km/h")
            
            with col_meteo2:
                if 'daily_forecast' in meteo_data:
                    daily = meteo_data['daily_forecast']
                    if ('temperature_2m_max' in daily and daily['temperature_2m_max'] and 
                        len(daily['temperature_2m_max']) > 0):
                        temps = [t for t in daily['temperature_2m_max'][:7] if t is not None]
                        if temps:
                            avg_max_temp = sum(temps) / len(temps)
                            st.metric("7-day Avg Max Temp", f"{avg_max_temp:.1f}°C")
                    
                    if ('precipitation_sum' in daily and daily['precipitation_sum'] and 
                        len(daily['precipitation_sum']) > 0):
                        precip = [p for p in daily['precipitation_sum'][:7] if p is not None]
                        if precip:
                            total_precip = sum(precip)
                            st.metric("7-day Total Rain", f"{total_precip:.1f}mm")

        # Pakistan Meteorological Department data
        if 'pmd' in weather_data:
            st.subheader("🏛️ Pakistan Meteorological Department")
            
            pmd_data = weather_data['pmd']
            
            col_pmd1, col_pmd2 = st.columns(2)
            
            with col_pmd1:
                st.write(f"**Nearest PMD Station:** {pmd_data.get('nearest_station', 'N/A')}")
                if 'station_info' in pmd_data:
                    station_info = pmd_data['station_info']
                    coords = station_info.get('coordinates', (0, 0))
                    st.write(f"**Station Coordinates:** {coords[0]:.4f}, {coords[1]:.4f}")
            
            with col_pmd2:
                status = pmd_data.get('status', 'unknown')
                if status == 'unavailable':
                    st.warning("⚠️ PMD API Currently Unavailable")
                    st.info(pmd_data.get('note', 'PMD data integration planned for future updates.'))
                else:
                    st.info("ℹ️ Using comprehensive alternative weather sources")

with col2:
    st.header("🤖 AI Analysis")
    
    # AI Analysis section
    if st.button("🧠 Generate AI Insights", type="secondary"):
        if 'weather_data' in st.session_state:
            with st.spinner("Analyzing data with AI..."):
                try:
                    # Get crop information
                    crop_info = crop_db.get_crop_info(crop_type)
                    
                    # Process data for AI analysis
                    processed_data = data_processor.prepare_for_analysis(
                        st.session_state.weather_data, 
                        crop_info,
                        lat,
                        lon
                    )
                    
                    # Generate AI insights
                    insights = ai_analyzer.analyze_agricultural_conditions(
                        processed_data,
                        crop_type,
                        f"Lat: {lat}, Lon: {lon}"
                    )
                    
                    if insights:
                        st.session_state.ai_insights = insights
                        st.success("✅ AI analysis completed!")
                    else:
                        st.error("❌ Failed to generate AI insights.")
                        
                except Exception as e:
                    st.error(f"❌ Error in AI analysis: {str(e)}")
        else:
            st.warning("⚠️ Please collect weather data first.")
    
    # Display AI insights
    if 'ai_insights' in st.session_state:
        insights = st.session_state.ai_insights
        
        st.subheader("📋 Agricultural Recommendations")
        
        # Risk level indicator
        if 'risk_level' in insights:
            risk_level = insights['risk_level'].upper()
            if risk_level == 'LOW':
                st.success(f"🟢 Risk Level: {risk_level}")
            elif risk_level == 'MEDIUM':
                st.warning(f"🟡 Risk Level: {risk_level}")
            else:
                st.error(f"🔴 Risk Level: {risk_level}")
        
        # Recommendations
        if 'recommendations' in insights:
            for i, rec in enumerate(insights['recommendations'], 1):
                st.write(f"**{i}.** {rec}")
        
        # Alerts
        if 'alerts' in insights and insights['alerts']:
            st.subheader("⚠️ Active Alerts")
            for alert in insights['alerts']:
                st.warning(f"🚨 {alert}")

# SMS Alert section
st.header("📱 SMS Alert System")

col_sms1, col_sms2 = st.columns(2)

with col_sms1:
    if st.button("📤 Send Current Analysis via SMS"):
        if phone_number and validate_phone_number(phone_number):
            if 'ai_insights' in st.session_state:
                with st.spinner("Sending SMS..."):
                    try:
                        # Format message
                        insights = st.session_state.ai_insights
                        message = f"🌾 Agricultural Alert for {crop_type}\n"
                        message += f"📍 Location: {lat:.2f}, {lon:.2f}\n"
                        message += f"⚠️ Risk: {insights.get('risk_level', 'Unknown')}\n"
                        
                        if 'alerts' in insights and insights['alerts']:
                            message += "🚨 Alerts:\n"
                            for alert in insights['alerts'][:2]:  # Limit to 2 alerts for SMS
                                message += f"• {alert}\n"
                        
                        if 'recommendations' in insights:
                            message += "💡 Top Recommendation:\n"
                            message += f"• {insights['recommendations'][0]}\n"
                        
                        message += f"\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                        
                        # Send SMS
                        sms_service.send_alert(phone_number, message)
                        st.success("✅ SMS sent successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Failed to send SMS: {str(e)}")
            else:
                st.warning("⚠️ No analysis data available. Please generate AI insights first.")
        else:
            st.error("❌ Please enter a valid phone number in international format.")

with col_sms2:
    # Auto-alert settings
    st.subheader("🔔 Auto-Alert Settings")
    
    auto_alerts = st.checkbox("Enable automatic alerts")
    
    if auto_alerts:
        alert_conditions = st.multiselect(
            "Send alerts for:",
            ["High Risk Conditions", "Frost Warning", "Heat Wave", "Heavy Rain", "Drought Risk"]
        )
        
        if alert_conditions:
            st.info("🔄 Auto-alerts configured. System will monitor conditions.")

# Historical Analysis section
st.header("📈 Historical Pattern Analysis")

if st.button("📊 Analyze Historical Patterns"):
    with st.spinner("Analyzing historical patterns..."):
        try:
            # Get historical data
            historical_data = weather_collector.get_historical_data(lat, lon)
            
            if historical_data:
                # Process historical data
                patterns = data_processor.analyze_historical_patterns(
                    historical_data, 
                    crop_type
                )
                
                if patterns:
                    st.subheader("🔍 Historical Insights")
                    
                    # Display patterns
                    if 'seasonal_trends' in patterns:
                        st.write("**Seasonal Trends:**")
                        for trend in patterns['seasonal_trends']:
                            st.write(f"• {trend}")
                    
                    if 'risk_periods' in patterns:
                        st.write("**Historical Risk Periods:**")
                        for period in patterns['risk_periods']:
                            st.write(f"• {period}")
                    
                    # Visualization of historical data
                    if 'monthly_averages' in patterns:
                        monthly_df = pd.DataFrame(patterns['monthly_averages'])
                        
                        if not monthly_df.empty:
                            fig_historical = px.bar(
                                monthly_df,
                                x='month',
                                y='temperature',
                                title="Historical Monthly Temperature Averages",
                                labels={'temperature': 'Temperature (°C)', 'month': 'Month'}
                            )
                            st.plotly_chart(fig_historical, use_container_width=True)
                
            else:
                st.warning("⚠️ No historical data available for this location.")
                
        except Exception as e:
            st.error(f"❌ Error analyzing historical patterns: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "**🌾 AI Agricultural Analysis System** | "
    "Powered by OpenWeatherMap, NASA POWER, AccuWeather, Open-Meteo & PMD APIs | "
    "AI Analysis by OpenAI GPT-5 | SMS Alerts by Twilio"
)
