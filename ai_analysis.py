import json
import os
from typing import Dict, List, Optional
from datetime import datetime

import google.generativeai as genai
from openai import OpenAI


class AgriculturalAnalyzer:
    """AI-powered agricultural analysis using Google Gemini (primary) and OpenAI GPT-5 (fallback)"""

    def __init__(self):
        # Gemini setup
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel("gemini-2.0-flash")
        else:
            self.gemini_model = None

        # OpenAI fallback setup
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None

    def _call_gemini(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Call Gemini API and return raw text response"""
        if not self.gemini_model:
            return None
        try:
            full_prompt = f"{system_prompt}\n\n{user_prompt}\n\nRespond ONLY with a valid JSON object, no markdown, no extra text."
            response = self.gemini_model.generate_content(full_prompt)
            text = response.text.strip()
            # Strip markdown code fences if present
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None

    def _call_openai(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Call OpenAI API and return raw text response"""
        if not self.openai_client:
            return None
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None

    def _call_ai(self, system_prompt: str, user_prompt: str) -> Optional[Dict]:
        """Try Gemini first, fall back to OpenAI, return parsed JSON dict with provider info"""
        raw = self._call_gemini(system_prompt, user_prompt)
        if raw:
            try:
                result = json.loads(raw)
                result['_ai_provider'] = 'Gemini'
                return result
            except json.JSONDecodeError as e:
                print(f"Gemini JSON parse error: {e}")

        raw = self._call_openai(system_prompt, user_prompt)
        if raw:
            try:
                result = json.loads(raw)
                result['_ai_provider'] = 'OpenAI'
                return result
            except json.JSONDecodeError as e:
                print(f"OpenAI JSON parse error: {e}")

        return None

    def analyze_agricultural_conditions(self, weather_data: Dict, crop_type: str, location: str) -> Optional[Dict]:
        """Analyze weather conditions and provide agricultural insights"""
        system_prompt = """You are an expert agricultural consultant with deep knowledge of:
- Pakistani farming conditions and climate patterns
- Crop-specific requirements and vulnerabilities
- Weather impact on agricultural productivity
- Soil management and irrigation practices
- Pest and disease management related to weather conditions

Provide practical, actionable advice for Pakistani farmers. Consider local farming practices,
resource constraints, and the specific challenges of agriculture in Pakistan.

Respond with a JSON object containing:
{
    "risk_level": "LOW/MEDIUM/HIGH",
    "overall_assessment": "brief summary",
    "recommendations": ["list", "of", "actionable", "recommendations"],
    "alerts": ["immediate", "concerns", "if any"],
    "optimal_activities": ["farming", "activities", "to", "prioritize"],
    "irrigation_advice": "specific irrigation recommendations",
    "pest_disease_risk": "assessment of pest/disease risks",
    "harvest_timing": "advice on harvest timing if applicable",
    "soil_management": "soil care recommendations"
}"""

        user_prompt = self._build_analysis_prompt(weather_data, crop_type, location)

        try:
            result = self._call_ai(system_prompt, user_prompt)
            if result:
                result['analysis_timestamp'] = datetime.now().isoformat()
                result['location'] = location
                result['crop_analyzed'] = crop_type
                result['ai_provider'] = result.pop('_ai_provider', 'Unknown')
            return result
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return None

    def _build_analysis_prompt(self, weather_data: Dict, crop_type: str, location: str) -> str:
        """Build comprehensive prompt for AI analysis"""
        prompt = f"Analyze the following agricultural conditions for {crop_type} farming in Pakistan at {location}:\n\nCURRENT WEATHER CONDITIONS:\n"

        if 'current' in weather_data:
            current = weather_data['current']
            prompt += f"""
- Temperature: {current.get('temperature', 'N/A')}°C
- Humidity: {current.get('humidity', 'N/A')}%
- Wind Speed: {current.get('wind_speed', 'N/A')} m/s
- Pressure: {current.get('pressure', 'N/A')} hPa
- Weather Condition: {current.get('weather_condition', 'N/A')}
- Visibility: {current.get('visibility', 'N/A')} km
"""

        if 'forecast' in weather_data:
            prompt += "\n7-DAY FORECAST:\n"
            for i, day in enumerate(weather_data['forecast'][:7]):
                prompt += f"Day {i+1} ({day.get('date', 'N/A')}): "
                prompt += f"Max: {day.get('temp_max', 'N/A')}°C, Min: {day.get('temp_min', 'N/A')}°C, "
                prompt += f"Precipitation: {day.get('precipitation', 'N/A')}mm\n"

        if 'nasa_power' in weather_data and weather_data['nasa_power']:
            nasa_data = weather_data['nasa_power']
            if 'parameters' in nasa_data:
                params = nasa_data['parameters']
                prompt += "\nSOLAR RADIATION & AGRICULTURAL PARAMETERS:\n"

                if 'ALLSKY_SFC_SW_DWN' in params:
                    solar_data = params['ALLSKY_SFC_SW_DWN']
                    if solar_data:
                        recent_solar = list(solar_data.values())[-7:]
                        avg_solar = sum(recent_solar) / len(recent_solar) if recent_solar else 0
                        prompt += f"- Average Solar Radiation (last 7 days): {avg_solar:.2f} kWh/m²/day\n"

                if 'T2M' in params:
                    temp_data = params['T2M']
                    if temp_data:
                        recent_temps = list(temp_data.values())[-7:]
                        avg_temp = sum(recent_temps) / len(recent_temps) if recent_temps else 0
                        prompt += f"- Average Temperature (last 7 days): {avg_temp:.1f}°C\n"

                if 'PRECTOTCORR' in params:
                    precip_data = params['PRECTOTCORR']
                    if precip_data:
                        recent_precip = list(precip_data.values())[-7:]
                        total_precip = sum(recent_precip) if recent_precip else 0
                        prompt += f"- Total Precipitation (last 7 days): {total_precip:.1f}mm\n"

                if 'EVPTRNS' in params:
                    evap_data = params['EVPTRNS']
                    if evap_data:
                        recent_evap = list(evap_data.values())[-7:]
                        avg_evap = sum(recent_evap) / len(recent_evap) if recent_evap else 0
                        prompt += f"- Average Evapotranspiration: {avg_evap:.2f}mm/day\n"

        if 'historical' in weather_data:
            prompt += "\nHISTORICAL CONTEXT (Recent Patterns):\n"
            if 'accuweather' in weather_data['historical'] and weather_data['historical']['accuweather']:
                hist_data = weather_data['historical']['accuweather'].get('historical_data', [])
                if hist_data:
                    avg_temp = sum(day['temperature'] for day in hist_data) / len(hist_data)
                    avg_humidity = sum(day['humidity'] for day in hist_data) / len(hist_data)
                    prompt += f"- Average temperature (last 30 days): {avg_temp:.1f}°C\n"
                    prompt += f"- Average humidity (last 30 days): {avg_humidity:.1f}%\n"

        prompt += f"""
CROP-SPECIFIC ANALYSIS REQUIREMENTS FOR {crop_type.upper()}:
Please consider the following factors specific to {crop_type} cultivation in Pakistan:
- Optimal temperature ranges and climate requirements
- Water requirements and irrigation needs
- Vulnerability to weather extremes (frost, heat waves, storms)
- Growth stage considerations (if applicable to current season)
- Common pests and diseases that are weather-dependent
- Soil moisture requirements
- Harvesting considerations

PAKISTANI AGRICULTURAL CONTEXT:
- Consider monsoon patterns and seasonal variations
- Account for typical farming practices in Pakistan
- Consider water scarcity issues and irrigation challenges
- Factor in typical resource constraints of Pakistani farmers
- Consider crop calendar and seasonal timing

Please provide specific, actionable recommendations that a Pakistani farmer can implement immediately.
Focus on practical solutions that consider local conditions, available resources, and traditional farming practices.
"""
        return prompt

    def analyze_pest_disease_risk(self, weather_data: Dict, crop_type: str) -> Optional[Dict]:
        """Analyze pest and disease risks based on weather conditions"""
        system_prompt = "You are an expert in agricultural pest and disease management with specific knowledge of Pakistani farming conditions."

        user_prompt = f"""Based on the following weather data, assess the pest and disease risks for {crop_type} in Pakistan:

Weather Data: {json.dumps(weather_data, indent=2)}

Provide a JSON response with:
{{
    "high_risk_pests": ["list of pests with high risk"],
    "high_risk_diseases": ["list of diseases with high risk"],
    "preventive_measures": ["specific prevention recommendations"],
    "monitoring_advice": ["what to monitor for"],
    "treatment_recommendations": ["if immediate treatment is needed"]
}}"""

        try:
            return self._call_ai(system_prompt, user_prompt)
        except Exception as e:
            print(f"Error in pest/disease analysis: {e}")
            return None

    def generate_seasonal_advice(self, location: str, crop_type: str, month: int) -> Optional[Dict]:
        """Generate seasonal farming advice"""
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        system_prompt = "You are an expert agricultural consultant specializing in Pakistani farming practices and seasonal crop management."

        user_prompt = f"""Provide seasonal farming advice for {crop_type} cultivation in {location}, Pakistan for the month of {month_names[month-1]}.

Consider:
- Typical weather patterns for this month in Pakistan
- Seasonal farming activities for {crop_type}
- Water management strategies
- Pest and disease prevention for this season
- Soil preparation needs
- Market considerations

Provide a JSON response with:
{{
    "seasonal_activities": ["key activities for this month"],
    "weather_preparation": ["preparations for expected weather"],
    "irrigation_strategy": "water management approach",
    "pest_prevention": ["preventive measures for seasonal pests"],
    "market_timing": "advice on market considerations",
    "general_tips": ["additional seasonal farming tips"]
}}"""

        try:
            return self._call_ai(system_prompt, user_prompt)
        except Exception as e:
            print(f"Error generating seasonal advice: {e}")
            return None
