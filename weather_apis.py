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
        self.open_meteo_base = "https://api.open-meteo.com/v1"
        self.pmd_base = "https://pmd.css.net.pk"
    
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
        
        # Open-Meteo data (free, reliable Pakistani weather data)
        open_meteo_data = self.get_open_meteo_data(lat, lon)
        if open_meteo_data:
            weather_data['open_meteo'] = open_meteo_data
            print("✅ Open-Meteo data collected")
        else:
            print("❌ Failed to collect Open-Meteo data")
        
        # Pakistan Meteorological Department data
        pmd_data = self.get_pmd_data(lat, lon)
        if pmd_data:
            weather_data['pmd'] = pmd_data
            print("✅ Pakistan Meteorological Department data collected")
        else:
            print("❌ Failed to collect PMD data (using alternative sources)")
        
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
    
    def get_open_meteo_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Get weather data from Open-Meteo API (free, no API key required)"""
        try:
            url = f"{self.open_meteo_base}/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current_weather': True,
                'hourly': 'temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m,pressure_msl',
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max',
                'timezone': 'Asia/Karachi',
                'forecast_days': 7
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Process current weather
            current = data.get('current_weather', {})
            hourly = data.get('hourly', {})
            daily = data.get('daily', {})
            
            processed_data = {
                'current': {
                    'temperature': current.get('temperature', 0),
                    'wind_speed': current.get('windspeed', 0),
                    'wind_direction': current.get('winddirection', 0),
                    'weather_code': current.get('weathercode', 0),
                    'timestamp': current.get('time', datetime.now().isoformat())
                },
                'hourly_data': hourly,
                'daily_forecast': daily,
                'source': 'Open-Meteo'
            }
            
            return processed_data
            
        except Exception as e:
            print(f"Error fetching Open-Meteo data: {e}")
            return None
    
    def get_pmd_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Get weather data from Pakistan Meteorological Department
        
        Note: PMD currently does not provide a public API. This function identifies
        the nearest PMD station and provides infrastructure for future integration
        when PMD data becomes programmatically accessible.
        """
        try:
            # Find nearest PMD station based on coordinates
            nearest_city = self._find_nearest_pmd_station(lat, lon)
            
            # PMD data structure for future implementation
            pmd_data = {
                'nearest_station': nearest_city,
                'source': 'Pakistan Meteorological Department',
                'status': 'unavailable',
                'note': 'PMD does not currently provide public API access. Using alternative weather sources.',
                'station_info': {
                    'city': nearest_city,
                    'coordinates': self._get_pmd_station_coordinates(nearest_city)
                }
            }
            
            # For now, return station information only
            # Future implementation would parse actual PMD data when available
            return pmd_data
            
        except Exception as e:
            print(f"Error accessing PMD station data: {e}")
            return None
    
    def _get_pmd_station_coordinates(self, station_city: str) -> tuple:
        """Get coordinates for PMD station city"""
        pmd_stations = {
            'Karachi': (24.8607, 67.0011),
            'Lahore': (31.5204, 74.3587),
            'Islamabad': (33.6844, 73.0479),
            'Peshawar': (34.0151, 71.5249),
            'Quetta': (30.1798, 66.9750),
            'Multan': (30.1575, 71.5249),
            'Faisalabad': (31.4504, 73.1350),
            'Rawalpindi': (33.5651, 73.0169),
            'Hyderabad': (25.3960, 68.3578),
            'Sialkot': (32.4945, 74.5229),
            'Sukkur': (27.7060, 68.8578),
            'Jacobabad': (28.2819, 68.4372),
            'Nawabshah': (26.2442, 68.4100)
        }
        return pmd_stations.get(station_city, (24.8607, 67.0011))
    
    def _find_nearest_pmd_station(self, lat: float, lon: float) -> str:
        """Find nearest PMD weather station city"""
        # Major PMD weather stations in Pakistan
        pmd_stations = {
            'Karachi': (24.8607, 67.0011),
            'Lahore': (31.5204, 74.3587),
            'Islamabad': (33.6844, 73.0479),
            'Peshawar': (34.0151, 71.5249),
            'Quetta': (30.1798, 66.9750),
            'Multan': (30.1575, 71.5249),
            'Faisalabad': (31.4504, 73.1350),
            'Rawalpindi': (33.5651, 73.0169),
            'Hyderabad': (25.3960, 68.3578),
            'Sialkot': (32.4945, 74.5229),
            'Sukkur': (27.7060, 68.8578),
            'Jacobabad': (28.2819, 68.4372),
            'Nawabshah': (26.2442, 68.4100)
        }
        
        min_distance = float('inf')
        nearest_city = 'Karachi'
        
        for city, (city_lat, city_lon) in pmd_stations.items():
            # Calculate simple distance (Euclidean)
            distance = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_city = city
        
        return nearest_city
