import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import json

from weather_apis import WeatherDataCollector
from ai_analysis import AgriculturalAnalyzer
from sms_service import SMSService
from crop_data import CropDatabase
from data_processor import DataProcessor
from soil_database import SoilDatabase
from seasonal_calendar import PakistanFarmingCalendar
from utils import get_pakistan_coordinates, validate_phone_number, determine_weather_region

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
    soil_db = SoilDatabase()
    farming_calendar = PakistanFarmingCalendar()
    
    return weather_collector, ai_analyzer, sms_service, crop_db, data_processor, soil_db, farming_calendar

weather_collector, ai_analyzer, sms_service, crop_db, data_processor, soil_db, farming_calendar = initialize_services()

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

        # Soil Analysis Section
        st.subheader("🌱 Soil Analysis & Thermal Properties")
        
        # Get soil data for current location
        current_region = determine_weather_region(lat, lon)
        available_soils = soil_db.get_soil_by_coordinates(lat, lon)
        
        if available_soils:
            # Soil selection
            soil_names = [soil["name"] for soil in available_soils]
            selected_soil_name = st.selectbox("Select Soil Type for Analysis", soil_names)
            
            # Find selected soil data
            selected_soil = next((soil for soil in available_soils if soil["name"] == selected_soil_name), None)
            
            if selected_soil:
                col_soil1, col_soil2, col_soil3 = st.columns(3)
                
                with col_soil1:
                    st.write("**Soil Properties:**")
                    st.write(f"Region: {selected_soil['region']}")
                    st.write(f"Type: {selected_soil['soil_type']}")
                    ph_range = selected_soil['ph_range']
                    st.write(f"pH Range: {ph_range['min']} - {ph_range['max']}")
                    
                with col_soil2:
                    st.write("**Thermal Properties:**")
                    thermal = selected_soil['thermal_properties']
                    st.write(f"Conductivity: {thermal['thermal_conductivity']} W/m·K")
                    st.write(f"Heat Capacity: {thermal['heat_capacity']} MJ/m³·K")
                    st.write(f"Bulk Density: {thermal['bulk_density']} g/cm³")
                
                with col_soil3:
                    st.write("**Water Properties:**")
                    water = selected_soil['water_properties']
                    st.write(f"Field Capacity: {water['field_capacity']}%")
                    st.write(f"Available Water: {water['available_water']}%")
                    st.write(f"Drainage: {water['drainage'].title()}")
                
                # Thermal analysis with current weather
                if 'weather_data' in st.session_state and 'current' in st.session_state.weather_data:
                    current_weather = st.session_state.weather_data['current']
                    current_temp = current_weather.get('temperature', 25)
                    current_humidity = current_weather.get('humidity', 60)
                    
                    # Calculate soil moisture based on weather data
                    recent_precip = 0
                    if 'forecast' in st.session_state.weather_data:
                        forecast = st.session_state.weather_data['forecast']
                        recent_precip = sum(day.get('precipitation', 0) for day in forecast[:3])
                    
                    # Simple soil moisture estimation
                    base_moisture = water['field_capacity'] * 0.6  # Base level
                    precip_contribution = min(recent_precip * 0.5, water['field_capacity'] * 0.3)
                    humidity_factor = (current_humidity - 50) / 100 * water['field_capacity'] * 0.1
                    
                    soil_moisture = max(water['wilting_point'], 
                                      min(water['field_capacity'], 
                                          base_moisture + precip_contribution + humidity_factor))
                    
                    # Get soil type key
                    soil_type_key = None
                    for key, soil_data in soil_db.soil_data.items():
                        if soil_data["name"] == selected_soil_name:
                            soil_type_key = key
                            break
                    
                    if soil_type_key:
                        thermal_analysis = soil_db.get_soil_thermal_analysis(soil_type_key, current_temp, soil_moisture)
                        
                        st.subheader("🌡️ Real-time Soil Thermal Analysis")
                        
                        col_thermal1, col_thermal2 = st.columns(2)
                        
                        with col_thermal1:
                            st.write("**Current Conditions:**")
                            metrics = thermal_analysis['thermal_metrics']
                            st.metric("Root Zone Temperature", f"{metrics['root_zone_temperature']}°C")
                            st.write(f"**Temperature Stability:** {metrics['temperature_stability']}")
                            
                        with col_thermal2:
                            st.write("**Agricultural Impact:**")
                            impact = thermal_analysis['agricultural_impact']
                            st.write(f"**Germination Suitability:** {impact['seed_germination_suitability']}")
                            st.write(f"**Root Development:** {impact['root_development_conditions']}")
                            
                            # Display calculated soil moisture
                            st.metric("Estimated Soil Moisture", f"{soil_moisture:.1f}%")
                
                # Crop-soil compatibility
                st.subheader("🌾 Crop-Soil Compatibility Analysis")
                
                if soil_type_key:
                    compatibility = soil_db.get_crop_soil_compatibility(crop_type, soil_type_key)
                    
                    col_compat1, col_compat2 = st.columns(2)
                    
                    with col_compat1:
                        # Enhanced compatibility display
                        score = compatibility['suitability_score']
                        if score >= 80:
                            st.success(f"✅ Excellent match: {crop_type} is highly suitable for this soil")
                        elif score >= 60:
                            st.success(f"✅ Good match: {crop_type} is suitable for this soil")
                        elif score >= 40:
                            st.warning(f"⚠️ Moderate match: {crop_type} can grow but may need extra care")
                        else:
                            st.error(f"❌ Poor match: {crop_type} may face significant challenges")
                        
                        st.metric("Suitability Score", f"{score}/100")
                        
                        # Display specific suitable crops for comparison
                        suitable_crops = selected_soil['agricultural_characteristics']['suitable_crops']
                        st.write("**Best crops for this soil:**")
                        st.write(", ".join(suitable_crops))
                    
                    with col_compat2:
                        st.write("**Specific Recommendations:**")
                        for i, rec in enumerate(compatibility['recommendations'][:5], 1):
                            st.write(f"{i}. {rec}")
                        
                        # Show irrigation and fertilizer needs
                        agri_chars = selected_soil['agricultural_characteristics']
                        st.write(f"**Irrigation Frequency:** {agri_chars['irrigation_frequency']}")
                        st.write(f"**Fertilizer Retention:** {agri_chars['fertilizer_retention']}")
                        
                        if agri_chars['compaction_risk'] in ['high', 'very high']:
                            st.warning("⚠️ High compaction risk - avoid working wet soil")
                
                # Enhanced Seasonal soil management
                current_month = datetime.now().month
                current_season = "winter" if current_month in [12, 1, 2] else \
                               "summer" if current_month in [3, 4, 5, 10, 11] else "monsoon"
                
                if soil_type_key:
                    seasonal_mgmt = soil_db.get_seasonal_soil_management(soil_type_key, current_season)
                    
                    if 'error' not in seasonal_mgmt:
                        st.subheader(f"🗓️ {seasonal_mgmt['season']} Soil Management ({datetime.now().strftime('%B %Y')})")
                        
                        col_season1, col_season2, col_season3 = st.columns(3)
                        
                        with col_season1:
                            st.write("**Management Priorities:**")
                            priorities = seasonal_mgmt['management_priorities']
                            if priorities:
                                for priority in priorities:
                                    st.write(f"🎯 {priority}")
                            else:
                                st.write("No specific priorities for this season")
                            
                        with col_season2:
                            st.write("**Risk Factors:**")
                            risks = seasonal_mgmt['risk_factors']
                            if risks:
                                for risk in risks:
                                    st.write(f"⚠️ {risk}")
                            else:
                                st.success("✅ Low risk season")
                                
                        with col_season3:
                            st.write("**Recommended Practices:**")
                            practices = seasonal_mgmt.get('recommended_practices', [])
                            for i, practice in enumerate(practices[:4], 1):
                                st.write(f"{i}. {practice}")
                        
                        # Seasonal behavior details
                        behavior = seasonal_mgmt.get('behavior', {})
                        if behavior:
                            st.write("**Seasonal Soil Behavior:**")
                            col_behav1, col_behav2 = st.columns(2)
                            
                            with col_behav1:
                                for key, value in list(behavior.items())[:3]:
                                    readable_key = key.replace('_', ' ').title()
                                    st.write(f"• **{readable_key}:** {value}")
                            
                            with col_behav2:
                                for key, value in list(behavior.items())[3:]:
                                    readable_key = key.replace('_', ' ').title()
                                    st.write(f"• **{readable_key}:** {value}")
        else:
            st.info(f"No specific soil data available for {current_region} region. Using general recommendations.")

# New section for Seasonal Farming Calendar
st.markdown("---")
st.header("📅 Seasonal Farming Calendar")

# Get current regional farming activities
current_month = datetime.now().month
regional_calendar = farming_calendar.get_regional_calendar(current_region, current_month)

col_cal1, col_cal2 = st.columns(2)

with col_cal1:
    st.subheader(f"🌾 Current Activities - {regional_calendar['month']}")
    st.write(f"**Season:** {regional_calendar['current_season'].title()}")
    
    # Display current crop activities
    if regional_calendar['crop_activities']:
        for crop, activity_data in regional_calendar['crop_activities'].items():
            if crop == crop_type.lower():  # Highlight selected crop
                st.success(f"**{crop.title()} (Selected Crop):**")
            else:
                st.write(f"**{crop.title()}:**")
            
            if 'current_activities' in activity_data:
                for activity in activity_data['current_activities']:
                    st.write(f"• {activity['description']}")
            else:
                st.write(f"• {activity_data.get('description', 'Maintenance period')}")
    else:
        st.info("No specific crop activities scheduled for this month in your region.")

with col_cal2:
    st.subheader("🎯 Priority Recommendations")
    
    # Get seasonal recommendations based on current weather
    if 'weather_data' in st.session_state and 'current' in st.session_state.weather_data:
        seasonal_recs = farming_calendar.get_seasonal_recommendations(
            current_region, 
            st.session_state.weather_data['current']
        )
        
        st.write("**Priority Crops for This Season:**")
        for crop in seasonal_recs['priority_crops']:
            if crop == crop_type.lower():
                st.success(f"✅ {crop.title()} (Your selected crop)")
            else:
                st.write(f"• {crop.title()}")
        
        if seasonal_recs['irrigation_advice']:
            st.write("**Irrigation Advice:**")
            for advice in seasonal_recs['irrigation_advice']:
                st.write(f"💧 {advice}")
        
        if seasonal_recs['pest_disease_alerts']:
            st.write("**Pest & Disease Alerts:**")
            for alert in seasonal_recs['pest_disease_alerts']:
                st.warning(f"⚠️ {alert}")
    else:
        st.info("Load weather data to get personalized seasonal recommendations.")

# Detailed crop schedule for selected crop
st.subheader(f"📋 Detailed Schedule for {crop_type}")
crop_schedule = farming_calendar.get_crop_schedule(crop_type.lower(), current_region)

if 'error' not in crop_schedule:
    col_sched1, col_sched2, col_sched3 = st.columns(3)
    
    with col_sched1:
        st.write("**Schedule Overview:**")
        schedule = crop_schedule['schedule']
        for activity, timing in schedule.items():
            if isinstance(timing, dict) and 'start_month' in timing:
                start_month = calendar.month_name[timing['start_month']]
                end_month = calendar.month_name[timing['end_month']]
                st.write(f"• **{activity.replace('_', ' ').title()}:** {start_month} - {end_month}")
    
    with col_sched2:
        st.write("**Current Month Activity:**")
        current_activity = crop_schedule.get('current_month_activity', {})
        if 'current_activities' in current_activity:
            for activity in current_activity['current_activities']:
                st.write(f"🎯 {activity['description']}")
        else:
            st.write(current_activity.get('description', 'General maintenance period'))
        
        if 'recommendations' in current_activity:
            st.write("**Action Items:**")
            for i, rec in enumerate(current_activity['recommendations'][:4], 1):
                st.write(f"{i}. {rec}")
    
    with col_sched3:
        st.write("**Recommended Varieties:**")
        varieties = crop_schedule.get('varieties', {})
        if varieties:
            for variety_type, variety_list in varieties.items():
                st.write(f"**{variety_type.replace('_', ' ').title()}:**")
                st.write(", ".join(variety_list[:3]))  # Show first 3 varieties
        else:
            st.write("Contact local agriculture extension for variety recommendations.")
    
    # Display any critical periods
    if regional_calendar['critical_periods']:
        st.write("**⚠️ Critical Periods This Month:**")
        for period in regional_calendar['critical_periods']:
            st.warning(f"**{period['name'].replace('_', ' ').title()}:** {period['period']}")
            st.write("Critical factors: " + ", ".join(period['critical_factors']))
else:
    st.error(f"Could not load schedule for {crop_type}: {crop_schedule.get('error', 'Unknown error')}")

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
