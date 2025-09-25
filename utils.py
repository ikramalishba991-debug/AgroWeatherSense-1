import re
from typing import Dict, Tuple, Optional

def get_pakistan_coordinates(city: str = None) -> Dict[str, Tuple[float, float]]:
    """
    Get coordinates for major Pakistani cities
    
    Returns:
        Dict mapping city names to (latitude, longitude) tuples
    """
    coordinates = {
        "Karachi": (24.8607, 67.0011),
        "Lahore": (31.5497, 74.3436),
        "Islamabad": (33.6844, 73.0479),
        "Rawalpindi": (33.5651, 73.0169),
        "Faisalabad": (31.4504, 73.1350),
        "Multan": (30.1575, 71.5249),
        "Peshawar": (34.0151, 71.5249),
        "Quetta": (30.1798, 66.9750),
        "Sialkot": (32.4945, 74.5229),
        "Gujranwala": (32.1877, 74.1945),
        "Hyderabad": (25.3960, 68.3578),
        "Bahawalpur": (29.4000, 71.6833),
        "Sargodha": (32.0836, 72.6711),
        "Sukkur": (27.7060, 68.8578),
        "Sheikhupura": (31.7167, 73.9778),
        "Jhang": (31.2681, 72.3317),
        "Rahim Yar Khan": (28.4212, 70.2989),
        "Gujrat": (32.5739, 74.0828),
        "Kasur": (31.1156, 74.4494),
        "Mardan": (34.1989, 72.0450)
    }
    
    if city:
        return coordinates  # Return all coordinates dict
    
    return coordinates

def validate_phone_number(phone_number: str) -> bool:
    """
    Validate Pakistani phone number format
    
    Args:
        phone_number: Phone number string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not phone_number:
        return False
    
    # Remove spaces and dashes
    cleaned = re.sub(r'[-\s]', '', phone_number)
    
    # Pakistani phone number patterns
    patterns = [
        r'^\+92[0-9]{10}$',  # International format: +92XXXXXXXXXX
        r'^92[0-9]{10}$',    # International without +: 92XXXXXXXXXX
        r'^0[0-9]{10}$',     # National format: 0XXXXXXXXXX
        r'^3[0-9]{9}$'       # Mobile without leading 0: 3XXXXXXXXX
    ]
    
    return any(re.match(pattern, cleaned) for pattern in patterns)

def format_phone_number(phone_number: str) -> str:
    """
    Format phone number to international format (+92XXXXXXXXXX)
    
    Args:
        phone_number: Input phone number
        
    Returns:
        str: Formatted phone number
    """
    if not phone_number:
        return ""
    
    # Remove spaces and dashes
    cleaned = re.sub(r'[-\s]', '', phone_number)
    
    # Convert to international format
    if cleaned.startswith('+92'):
        return cleaned
    elif cleaned.startswith('92') and len(cleaned) == 12:
        return '+' + cleaned
    elif cleaned.startswith('0') and len(cleaned) == 11:
        return '+92' + cleaned[1:]
    elif cleaned.startswith('3') and len(cleaned) == 10:
        return '+92' + cleaned
    else:
        return phone_number  # Return original if can't format

def get_crop_season_info(crop_type: str, month: int) -> Dict[str, str]:
    """
    Get current season information for a crop
    
    Args:
        crop_type: Type of crop
        month: Current month (1-12)
        
    Returns:
        Dict with season information
    """
    # Pakistani crop calendar
    crop_seasons = {
        "Wheat": {
            "rabi": [11, 12, 1, 2, 3, 4, 5],  # November to May
            "season_type": "rabi"
        },
        "Rice": {
            "kharif": [5, 6, 7, 8, 9, 10, 11],  # May to November
            "season_type": "kharif"
        },
        "Cotton": {
            "kharif": [4, 5, 6, 7, 8, 9, 10, 11, 12],  # April to December
            "season_type": "kharif"
        },
        "Sugarcane": {
            "year_round": list(range(1, 13)),  # Year round
            "season_type": "perennial"
        },
        "Maize": {
            "spring": [2, 3, 4, 5, 6, 7],  # February to July
            "autumn": [7, 8, 9, 10, 11, 12],  # July to December
            "season_type": "dual"
        },
        "Barley": {
            "rabi": [11, 12, 1, 2, 3, 4],  # November to April
            "season_type": "rabi"
        },
        "Millet": {
            "kharif": [5, 6, 7, 8, 9],  # May to September
            "season_type": "kharif"
        },
        "Sorghum": {
            "kharif": [4, 5, 6, 7, 8, 9, 10],  # April to October
            "season_type": "kharif"
        }
    }
    
    crop_info = crop_seasons.get(crop_type, {})
    season_type = crop_info.get("season_type", "unknown")
    
    # Determine current status
    status = "off_season"
    season_name = ""
    
    if season_type == "rabi":
        if month in crop_info.get("rabi", []):
            status = "in_season"
            season_name = "Rabi (Winter) Season"
    elif season_type == "kharif":
        if month in crop_info.get("kharif", []):
            status = "in_season"
            season_name = "Kharif (Summer/Monsoon) Season"
    elif season_type == "perennial":
        status = "in_season"
        season_name = "Year-round cultivation"
    elif season_type == "dual":
        if month in crop_info.get("spring", []):
            status = "in_season"
            season_name = "Spring Season"
        elif month in crop_info.get("autumn", []):
            status = "in_season"
            season_name = "Autumn Season"
    
    return {
        "season_type": season_type,
        "current_season": season_name,
        "status": status,
        "month": month
    }

def calculate_growing_degree_days(max_temp: float, min_temp: float, base_temp: float = 10.0) -> float:
    """
    Calculate Growing Degree Days (GDD) for crop development tracking
    
    Args:
        max_temp: Maximum temperature for the day
        min_temp: Minimum temperature for the day
        base_temp: Base temperature for the crop (default 10°C)
        
    Returns:
        float: Growing degree days
    """
    avg_temp = (max_temp + min_temp) / 2
    gdd = max(0, avg_temp - base_temp)
    return gdd

def assess_frost_risk(min_temp: float, crop_type: str) -> Dict[str, str]:
    """
    Assess frost risk for different crops
    
    Args:
        min_temp: Minimum temperature forecast
        crop_type: Type of crop
        
    Returns:
        Dict with risk assessment
    """
    # Frost sensitivity by crop
    frost_thresholds = {
        "Wheat": {"damage": -2, "kill": -4},
        "Rice": {"damage": 0, "kill": -1},
        "Cotton": {"damage": 2, "kill": 0},
        "Sugarcane": {"damage": -1, "kill": -3},
        "Maize": {"damage": 0, "kill": -2},
        "Barley": {"damage": -3, "kill": -5},
        "Millet": {"damage": 1, "kill": -1},
        "Sorghum": {"damage": 0, "kill": -2}
    }
    
    thresholds = frost_thresholds.get(crop_type, {"damage": 0, "kill": -2})
    
    if min_temp <= thresholds["kill"]:
        return {
            "risk_level": "critical",
            "message": f"Severe frost risk - temperatures may kill {crop_type} plants",
            "action": "Implement immediate frost protection measures"
        }
    elif min_temp <= thresholds["damage"]:
        return {
            "risk_level": "high",
            "message": f"Frost damage likely for {crop_type}",
            "action": "Prepare frost protection - covering, irrigation, or heating"
        }
    elif min_temp <= thresholds["damage"] + 2:
        return {
            "risk_level": "moderate",
            "message": f"Frost possible - monitor {crop_type} closely",
            "action": "Be ready to implement protection measures"
        }
    else:
        return {
            "risk_level": "low",
            "message": "No frost risk expected",
            "action": "Continue normal operations"
        }

def calculate_heat_stress_index(temp: float, humidity: float) -> Dict[str, str]:
    """
    Calculate heat stress index for crops
    
    Args:
        temp: Temperature in Celsius
        humidity: Relative humidity percentage
        
    Returns:
        Dict with heat stress assessment
    """
    # Heat index calculation (simplified)
    if temp <= 26:
        heat_index = temp
    else:
        heat_index = temp + (0.33 * humidity) - 0.7
    
    if heat_index >= 45:
        return {
            "stress_level": "extreme",
            "message": "Extreme heat stress - crop damage likely",
            "recommendation": "Emergency cooling measures needed"
        }
    elif heat_index >= 40:
        return {
            "stress_level": "severe",
            "message": "Severe heat stress conditions",
            "recommendation": "Increase irrigation and provide shade"
        }
    elif heat_index >= 35:
        return {
            "stress_level": "moderate",
            "message": "Moderate heat stress",
            "recommendation": "Monitor crops and adjust irrigation"
        }
    else:
        return {
            "stress_level": "low",
            "message": "Acceptable temperature conditions",
            "recommendation": "Continue normal operations"
        }

def get_pakistan_weather_regions() -> Dict[str, Dict]:
    """
    Get weather regions of Pakistan with characteristics
    
    Returns:
        Dict mapping regions to their characteristics
    """
    return {
        "Northern_Mountains": {
            "provinces": ["Gilgit-Baltistan", "Northern KPK"],
            "characteristics": ["Cold winters", "Moderate summers", "Snow precipitation"],
            "elevation": "High (>1000m)",
            "main_crops": ["Wheat", "Barley", "Potatoes"]
        },
        "Punjab_Plains": {
            "provinces": ["Punjab"],
            "characteristics": ["Hot summers", "Mild winters", "Monsoon rains"],
            "elevation": "Low to moderate (<500m)",
            "main_crops": ["Wheat", "Rice", "Cotton", "Sugarcane"]
        },
        "Sindh_Plains": {
            "provinces": ["Sindh"],
            "characteristics": ["Very hot summers", "Mild winters", "Low rainfall"],
            "elevation": "Low (<200m)",
            "main_crops": ["Rice", "Cotton", "Sugarcane", "Wheat"]
        },
        "Balochistan_Plateau": {
            "provinces": ["Balochistan"],
            "characteristics": ["Extreme temperatures", "Very low rainfall", "Desert climate"],
            "elevation": "Moderate to high (500-2000m)",
            "main_crops": ["Wheat", "Barley", "Dates"]
        },
        "Coastal_Areas": {
            "provinces": ["Coastal Sindh", "Coastal Balochistan"],
            "characteristics": ["Moderate temperatures", "High humidity", "Sea influence"],
            "elevation": "Sea level",
            "main_crops": ["Rice", "Cotton", "Coconut"]
        }
    }

def determine_weather_region(lat: float, lon: float) -> str:
    """
    Determine weather region based on coordinates
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        str: Weather region name
    """
    # Simplified region determination
    if lat > 34:
        return "Northern_Mountains"
    elif lat > 30 and lon > 73:
        return "Punjab_Plains"
    elif lat <= 30 and lon > 68:
        return "Sindh_Plains"
    elif lon <= 68:
        return "Balochistan_Plateau"
    elif lat < 26:
        return "Coastal_Areas"
    else:
        return "Punjab_Plains"  # Default
