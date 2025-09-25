import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

class DataProcessor:
    """Process and analyze weather data for agricultural insights"""
    
    def __init__(self):
        self.historical_window = 30  # days for historical analysis
    
    def prepare_for_analysis(self, weather_data: Dict, crop_info: Dict, lat: float, lon: float) -> Dict:
        """
        Prepare weather data for AI analysis
        
        Args:
            weather_data: Raw weather data from APIs
            crop_info: Crop-specific information
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dict: Processed data ready for AI analysis
        """
        processed_data = {
            "location": {"latitude": lat, "longitude": lon},
            "crop_information": crop_info,
            "analysis_timestamp": datetime.now().isoformat(),
            "weather_summary": {},
            "risk_indicators": {},
            "trends": {}
        }
        
        # Process current weather
        if 'current' in weather_data:
            current = weather_data['current']
            processed_data["weather_summary"]["current"] = self._process_current_weather(current)
        
        # Process forecast data
        if 'forecast' in weather_data:
            forecast = weather_data['forecast']
            processed_data["weather_summary"]["forecast"] = self._process_forecast(forecast)
            processed_data["trends"]["forecast_trends"] = self._analyze_forecast_trends(forecast)
        
        # Process NASA POWER data
        if 'nasa_power' in weather_data:
            nasa_data = weather_data['nasa_power']
            processed_data["weather_summary"]["nasa_power"] = self._process_nasa_power(nasa_data)
        
        # Process historical data
        if 'historical' in weather_data:
            historical = weather_data['historical']
            processed_data["weather_summary"]["historical"] = self._process_historical(historical)
        
        # Calculate risk indicators
        processed_data["risk_indicators"] = self._calculate_risk_indicators(
            processed_data["weather_summary"], 
            crop_info
        )
        
        return processed_data
    
    def _process_current_weather(self, current_data: Dict) -> Dict:
        """Process current weather data"""
        return {
            "temperature": current_data.get('temperature', 0),
            "humidity": current_data.get('humidity', 0),
            "wind_speed": current_data.get('wind_speed', 0),
            "pressure": current_data.get('pressure', 0),
            "condition": current_data.get('weather_condition', ''),
            "visibility": current_data.get('visibility', 0)
        }
    
    def _process_forecast(self, forecast_data: List[Dict]) -> Dict:
        """Process forecast data and calculate statistics"""
        if not forecast_data:
            return {}
        
        temps_max = [day.get('temp_max', 0) for day in forecast_data]
        temps_min = [day.get('temp_min', 0) for day in forecast_data]
        precipitation = [day.get('precipitation', 0) for day in forecast_data]
        humidity = [day.get('avg_humidity', 0) for day in forecast_data]
        
        return {
            "temperature_range": {
                "max_forecasted": max(temps_max) if temps_max else 0,
                "min_forecasted": min(temps_min) if temps_min else 0,
                "avg_max": np.mean(temps_max) if temps_max else 0,
                "avg_min": np.mean(temps_min) if temps_min else 0
            },
            "precipitation_forecast": {
                "total_expected": sum(precipitation),
                "max_daily": max(precipitation) if precipitation else 0,
                "days_with_rain": len([p for p in precipitation if p > 0]),
                "avg_daily": np.mean(precipitation) if precipitation else 0
            },
            "humidity_forecast": {
                "avg_humidity": np.mean(humidity) if humidity else 0,
                "max_humidity": max(humidity) if humidity else 0,
                "min_humidity": min(humidity) if humidity else 0
            }
        }
    
    def _process_nasa_power(self, nasa_data: Dict) -> Dict:
        """Process NASA POWER agricultural data"""
        if not nasa_data or 'parameters' not in nasa_data:
            return {}
        
        params = nasa_data['parameters']
        processed = {}
        
        # Process solar radiation data
        if 'ALLSKY_SFC_SW_DWN' in params:
            solar_data = params['ALLSKY_SFC_SW_DWN']
            if solar_data:
                values = list(solar_data.values())
                processed['solar_radiation'] = {
                    'recent_avg': np.mean(values[-7:]) if len(values) >= 7 else np.mean(values),
                    'monthly_avg': np.mean(values),
                    'trend': self._calculate_trend(values[-14:]) if len(values) >= 14 else 'stable'
                }
        
        # Process temperature data
        if 'T2M' in params:
            temp_data = params['T2M']
            if temp_data:
                values = list(temp_data.values())
                processed['temperature_nasa'] = {
                    'recent_avg': np.mean(values[-7:]) if len(values) >= 7 else np.mean(values),
                    'monthly_avg': np.mean(values),
                    'max_temp': max(values),
                    'min_temp': min(values)
                }
        
        # Process precipitation data
        if 'PRECTOTCORR' in params:
            precip_data = params['PRECTOTCORR']
            if precip_data:
                values = list(precip_data.values())
                processed['precipitation_nasa'] = {
                    'recent_total': sum(values[-7:]) if len(values) >= 7 else sum(values),
                    'monthly_total': sum(values),
                    'max_daily': max(values),
                    'wet_days': len([v for v in values if v > 1.0])
                }
        
        # Process evapotranspiration
        if 'EVPTRNS' in params:
            evap_data = params['EVPTRNS']
            if evap_data:
                values = list(evap_data.values())
                processed['evapotranspiration'] = {
                    'recent_avg': np.mean(values[-7:]) if len(values) >= 7 else np.mean(values),
                    'monthly_avg': np.mean(values),
                    'trend': self._calculate_trend(values[-14:]) if len(values) >= 14 else 'stable'
                }
        
        return processed
    
    def _process_historical(self, historical_data: Dict) -> Dict:
        """Process historical weather data"""
        processed = {}
        
        # Process AccuWeather historical data
        if 'accuweather' in historical_data and historical_data['accuweather']:
            acc_data = historical_data['accuweather'].get('historical_data', [])
            if acc_data:
                temps = [day['temperature'] for day in acc_data if 'temperature' in day]
                humidity = [day['humidity'] for day in acc_data if 'humidity' in day]
                
                processed['accuweather_historical'] = {
                    'avg_temperature': np.mean(temps) if temps else 0,
                    'temp_range': {'max': max(temps), 'min': min(temps)} if temps else {'max': 0, 'min': 0},
                    'avg_humidity': np.mean(humidity) if humidity else 0,
                    'data_points': len(acc_data)
                }
        
        return processed
    
    def _analyze_forecast_trends(self, forecast_data: List[Dict]) -> Dict:
        """Analyze trends in forecast data"""
        if not forecast_data:
            return {}
        
        # Temperature trend
        temps_max = [day.get('temp_max', 0) for day in forecast_data]
        temps_min = [day.get('temp_min', 0) for day in forecast_data]
        
        temp_trend = self._calculate_trend(temps_max)
        
        # Precipitation pattern
        precipitation = [day.get('precipitation', 0) for day in forecast_data]
        wet_days = len([p for p in precipitation if p > 0])
        
        return {
            'temperature_trend': temp_trend,
            'precipitation_pattern': {
                'wet_days_forecast': wet_days,
                'total_precipitation': sum(precipitation),
                'heaviest_day': max(precipitation) if precipitation else 0
            },
            'weather_stability': self._assess_weather_stability(forecast_data)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a series of values"""
        if len(values) < 3:
            return 'stable'
        
        # Simple linear trend
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.5:
            return 'increasing'
        elif slope < -0.5:
            return 'decreasing'
        else:
            return 'stable'
    
    def _assess_weather_stability(self, forecast_data: List[Dict]) -> str:
        """Assess overall weather stability"""
        if not forecast_data:
            return 'unknown'
        
        # Calculate temperature variance
        temps = [day.get('temp_max', 0) for day in forecast_data]
        temp_variance = np.var(temps) if temps else 0
        
        # Calculate precipitation variability
        precip = [day.get('precipitation', 0) for day in forecast_data]
        precip_days = len([p for p in precip if p > 0])
        
        if temp_variance < 9:  # Low temperature variance
            if precip_days <= 2:
                return 'stable'
            else:
                return 'moderately_stable'
        else:
            return 'unstable'
    
    def _calculate_risk_indicators(self, weather_summary: Dict, crop_info: Dict) -> Dict:
        """Calculate various risk indicators for agricultural analysis"""
        risks = {
            'temperature_risk': 'low',
            'water_stress_risk': 'low',
            'disease_risk': 'low',
            'pest_risk': 'low',
            'overall_risk': 'low'
        }
        
        if not crop_info:
            return risks
        
        current_weather = weather_summary.get('current', {})
        forecast = weather_summary.get('forecast', {})
        
        # Temperature risk assessment
        if current_weather.get('temperature'):
            temp = current_weather['temperature']
            optimal_range = crop_info.get('optimal_temp_range', {})
            min_temp = optimal_range.get('min', 0)
            max_temp = optimal_range.get('max', 40)
            
            if temp < min_temp - 5 or temp > max_temp + 5:
                risks['temperature_risk'] = 'high'
            elif temp < min_temp or temp > max_temp:
                risks['temperature_risk'] = 'medium'
        
        # Water stress risk
        if forecast.get('precipitation_forecast'):
            precip = forecast['precipitation_forecast']
            if precip['total_expected'] < 5 and current_weather.get('humidity', 100) < 40:
                risks['water_stress_risk'] = 'high'
            elif precip['total_expected'] < 15:
                risks['water_stress_risk'] = 'medium'
        
        # Disease risk (high humidity + moderate temperature)
        current_humidity = current_weather.get('humidity', 0)
        if current_humidity > 80 and 20 <= current_weather.get('temperature', 0) <= 30:
            risks['disease_risk'] = 'high'
        elif current_humidity > 70:
            risks['disease_risk'] = 'medium'
        
        # Overall risk assessment
        risk_levels = list(risks.values())
        if 'high' in risk_levels:
            risks['overall_risk'] = 'high'
        elif 'medium' in risk_levels:
            risks['overall_risk'] = 'medium'
        
        return risks
    
    def analyze_historical_patterns(self, historical_data: Dict, crop_type: str) -> Optional[Dict]:
        """Analyze historical weather patterns for insights"""
        try:
            patterns = {
                'seasonal_trends': [],
                'risk_periods': [],
                'monthly_averages': [],
                'anomalies': []
            }
            
            # Process NASA POWER historical data
            if 'nasa_power' in historical_data and historical_data['nasa_power']:
                nasa_data = historical_data['nasa_power']
                if 'parameters' in nasa_data:
                    params = nasa_data['parameters']
                    
                    # Analyze temperature patterns
                    if 'T2M' in params:
                        temp_data = params['T2M']
                        monthly_temps = self._aggregate_by_month(temp_data)
                        patterns['monthly_averages'] = monthly_temps
                        patterns['seasonal_trends'].extend(self._identify_seasonal_trends(monthly_temps, 'temperature'))
                    
                    # Analyze precipitation patterns
                    if 'PRECTOTCORR' in params:
                        precip_data = params['PRECTOTCORR']
                        monthly_precip = self._aggregate_by_month(precip_data)
                        patterns['seasonal_trends'].extend(self._identify_seasonal_trends(monthly_precip, 'precipitation'))
            
            # Identify risk periods based on crop type
            patterns['risk_periods'] = self._identify_risk_periods(crop_type, patterns.get('monthly_averages', []))
            
            return patterns
            
        except Exception as e:
            print(f"Error analyzing historical patterns: {e}")
            return None
    
    def _aggregate_by_month(self, time_series_data: Dict) -> List[Dict]:
        """Aggregate time series data by month"""
        if not time_series_data:
            return []
        
        monthly_data = {}
        
        for date_str, value in time_series_data.items():
            try:
                date = datetime.strptime(date_str, '%Y%m%d')
                month_key = date.strftime('%B')
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = []
                monthly_data[month_key].append(value)
            except:
                continue
        
        # Calculate monthly averages
        monthly_averages = []
        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        
        for month in month_order:
            if month in monthly_data and monthly_data[month]:
                avg_value = np.mean(monthly_data[month])
                monthly_averages.append({
                    'month': month,
                    'temperature': avg_value if 'T2M' in str(monthly_data) else None,
                    'precipitation': avg_value if 'PREC' in str(monthly_data) else None,
                    'value': avg_value
                })
        
        return monthly_averages
    
    def _identify_seasonal_trends(self, monthly_data: List[Dict], data_type: str) -> List[str]:
        """Identify seasonal trends from monthly data"""
        trends = []
        
        if len(monthly_data) < 6:
            return trends
        
        values = [month['value'] for month in monthly_data]
        
        # Find peak and low periods
        max_idx = values.index(max(values))
        min_idx = values.index(min(values))
        
        peak_month = monthly_data[max_idx]['month']
        low_month = monthly_data[min_idx]['month']
        
        if data_type == 'temperature':
            trends.append(f"Highest temperatures typically occur in {peak_month}")
            trends.append(f"Lowest temperatures typically occur in {low_month}")
        elif data_type == 'precipitation':
            trends.append(f"Peak rainfall season is {peak_month}")
            trends.append(f"Driest period is typically {low_month}")
        
        return trends
    
    def _identify_risk_periods(self, crop_type: str, monthly_data: List[Dict]) -> List[str]:
        """Identify historical risk periods for specific crops"""
        risk_periods = []
        
        # General risk periods based on crop type and Pakistani climate
        if crop_type in ['Wheat', 'Barley']:
            risk_periods.extend([
                "Late February to March: Risk of heat stress during grain filling",
                "December to January: Frost risk during germination",
                "March to April: Hot winds (loo) can damage crops"
            ])
        elif crop_type == 'Rice':
            risk_periods.extend([
                "June to July: Flooding risk during monsoon",
                "September to October: Late monsoon can delay harvest",
                "May: High temperatures can stress seedlings"
            ])
        elif crop_type == 'Cotton':
            risk_periods.extend([
                "July to August: Peak bollworm season",
                "September: Heavy rains can damage open bolls",
                "June: Heat waves can cause flower drop"
            ])
        elif crop_type in ['Sugarcane']:
            risk_periods.extend([
                "March to April: Water stress before monsoon",
                "August to September: Waterlogging during heavy monsoon",
                "December to January: Frost damage risk"
            ])
        
        return risk_periods
