import requests
import os
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class WeatherDataCollector:
    """Collects weather data from multiple APIs"""
    
    def __init__(self):
        # API Keys from environment variables
        self.openweather_key = os.getenv("OPENWEATHER_API_KEY", "your_openweather_key")
        self.accuweather_key = os.getenv("ACCUWEATHER_API_KEY", "your_accuweather_key")
        self.nasa_power_key = os.getenv("NASA_POWER_API_KEY", "")  # NASA POWER doesn't require key
        
        # Base URLs
        self.openweather_base = "https://api.openweathermap.org/data/2.5"
        self.nasa_power_base = "https://power.larc.nasa.gov/api/temporal/daily/point"
        self.accuweather_base = "http://dataservice.accuweather.com"
    
    def get_openweather_current(self, lat: float, lon: float) -> Optional[Dict]:
        """Get current weather from OpenWeatherMap"""
        try:
            url = f"{self.openweather_base}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'weather_condition': data['weather'][0]['description'],
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error fetching OpenWeather current data: {e}")
            return None
    
    def get_openweather_forecast(self, lat: float, lon: float) -> Optional[List[Dict]]:
        """Get 7-day forecast from OpenWeatherMap"""
        try:
            url = f"{self.openweather_base}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            forecast_data = []
            for item in data['list'][:35]:  # 7 days * 5 forecasts per day (3-hour intervals)
                forecast_data.append({
                    'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M'),
                    'temp_max': item['main']['temp_max'],
                    'temp_min': item['main']['temp_min'],
                    'humidity': item['main']['humidity'],
                    'precipitation': item.get('rain', {}).get('3h', 0),
                    'weather_condition': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed']
                })
            
            # Group by date and get daily aggregates
            daily_forecast = {}
            for forecast in forecast_data:
                date = forecast['date'][:10]  # Get date part only
                
                if date not in daily_forecast:
                    daily_forecast[date] = {
                        'date': date,
                        'temp_max': forecast['temp_max'],
                        'temp_min': forecast['temp_min'],
                        'precipitation': forecast['precipitation'],
                        'avg_humidity': forecast['humidity'],
                        'avg_wind_speed': forecast['wind_speed'],
                        'conditions': [forecast['weather_condition']]
                    }
                else:
                    daily_forecast[date]['temp_max'] = max(daily_forecast[date]['temp_max'], forecast['temp_max'])
                    daily_forecast[date]['temp_min'] = min(daily_forecast[date]['temp_min'], forecast['temp_min'])
                    daily_forecast[date]['precipitation'] += forecast['precipitation']
                    daily_forecast[date]['conditions'].append(forecast['weather_condition'])
            
            return list(daily_forecast.values())[:7]  # Return 7 days
            
        except Exception as e:
            print(f"Error fetching OpenWeather forecast data: {e}")
            return None
    
    def get_nasa_power_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Get agricultural data from NASA POWER API"""
        try:
            # Get data for the last 30 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            # NASA POWER parameters for agriculture
            parameters = [
                'ALLSKY_SFC_SW_DWN',  # Solar radiation
                'T2M',                # Temperature at 2 meters
                'T2M_MAX',           # Maximum temperature
                'T2M_MIN',           # Minimum temperature
                'PRECTOTCORR',       # Precipitation
                'RH2M',              # Relative humidity
                'WS2M',              # Wind speed
                'EVPTRNS'            # Evapotranspiration
            ]
            
            url = self.nasa_power_base
            params = {
                'latitude': lat,
                'longitude': lon,
                'start': start_date.strftime('%Y%m%d'),
                'end': end_date.strftime('%Y%m%d'),
                'community': 'AG',  # Agricultural community
                'parameters': ','.join(parameters),
                'format': 'JSON'
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching NASA POWER data: {e}")
            return None
    
    def get_accuweather_location_key(self, lat: float, lon: float) -> Optional[str]:
        """Get AccuWeather location key for coordinates"""
        try:
            url = f"{self.accuweather_base}/locations/v1/cities/geoposition/search"
            params = {
                'apikey': self.accuweather_key,
                'q': f"{lat},{lon}"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('Key')
            
        except Exception as e:
            print(f"Error getting AccuWeather location key: {e}")
            return None
    
    def get_accuweather_historical(self, lat: float, lon: float) -> Optional[Dict]:
        """Get historical weather data from AccuWeather"""
        try:
            location_key = self.get_accuweather_location_key(lat, lon)
            if not location_key:
                return None
            
            # Get historical data for the past 30 days
            historical_data = []
            
            for days_back in range(1, 31):  # Last 30 days
                date = datetime.now() - timedelta(days=days_back)
                url = f"{self.accuweather_base}/currentconditions/v1/{location_key}/historical/24"
                params = {
                    'apikey': self.accuweather_key,
                    'details': 'true'
                }
                
                try:
                    response = requests.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        day_data = response.json()
                        if day_data:
                            historical_data.append({
                                'date': date.strftime('%Y-%m-%d'),
                                'temperature': day_data[0].get('Temperature', {}).get('Metric', {}).get('Value', 0),
                                'humidity': day_data[0].get('RelativeHumidity', 0),
                                'wind_speed': day_data[0].get('Wind', {}).get('Speed', {}).get('Metric', {}).get('Value', 0),
                                'condition': day_data[0].get('WeatherText', '')
                            })
                except:
                    continue  # Skip if unable to get data for this day
            
            return {'historical_data': historical_data}
            
        except Exception as e:
            print(f"Error fetching AccuWeather historical data: {e}")
            return None
    
    def collect_all_data(self, lat: float, lon: float) -> Dict:
        """Collect data from all weather APIs"""
        weather_data = {}
        
        print(f"Collecting weather data for coordinates: {lat}, {lon}")
        
        # OpenWeatherMap current weather
        current_weather = self.get_openweather_current(lat, lon)
        if current_weather:
            weather_data['current'] = current_weather
            print("✅ OpenWeatherMap current data collected")
        else:
            print("❌ Failed to collect OpenWeatherMap current data")
        
        # OpenWeatherMap forecast
        forecast_data = self.get_openweather_forecast(lat, lon)
        if forecast_data:
            weather_data['forecast'] = forecast_data
            print("✅ OpenWeatherMap forecast data collected")
        else:
            print("❌ Failed to collect OpenWeatherMap forecast data")
        
        # NASA POWER data
        nasa_data = self.get_nasa_power_data(lat, lon)
        if nasa_data:
            weather_data['nasa_power'] = nasa_data
            print("✅ NASA POWER data collected")
        else:
            print("❌ Failed to collect NASA POWER data")
        
        # AccuWeather historical data
        historical_data = self.get_accuweather_historical(lat, lon)
        if historical_data:
            weather_data['historical'] = historical_data
            print("✅ AccuWeather historical data collected")
        else:
            print("❌ Failed to collect AccuWeather historical data")
        
        return weather_data
    
    def get_historical_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Get comprehensive historical data for pattern analysis"""
        try:
            # Combine NASA POWER and AccuWeather historical data
            nasa_data = self.get_nasa_power_data(lat, lon)
            accuweather_data = self.get_accuweather_historical(lat, lon)
            
            historical_combined = {
                'nasa_power': nasa_data,
                'accuweather': accuweather_data,
                'collection_timestamp': datetime.now().isoformat()
            }
            
            return historical_combined
            
        except Exception as e:
            print(f"Error collecting historical data: {e}")
            return None
