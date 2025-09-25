from typing import Dict, List, Optional

class CropDatabase:
    """Database of crop-specific information for Pakistani agriculture"""
    
    def __init__(self):
        self.crop_data = {
            "Wheat": {
                "optimal_temp_range": {"min": 15, "max": 25},
                "growing_season": "November to April",
                "water_requirements": "Medium to High",
                "frost_sensitivity": "Moderate",
                "heat_sensitivity": "High",
                "soil_ph_range": {"min": 6.0, "max": 7.5},
                "planting_time": "November - December",
                "harvest_time": "April - May",
                "critical_growth_stages": [
                    "Germination (0-15 days)",
                    "Tillering (15-45 days)", 
                    "Stem Elongation (45-75 days)",
                    "Flowering (75-105 days)",
                    "Grain Filling (105-120 days)"
                ],
                "common_pests": [
                    "Aphids", "Army Worm", "Wheat Stem Sawfly", "Hessian Fly"
                ],
                "common_diseases": [
                    "Rust (Yellow, Brown, Black)", "Septoria Leaf Blotch", 
                    "Powdery Mildew", "Fusarium Head Blight"
                ],
                "irrigation_schedule": "Every 15-20 days depending on rainfall",
                "fertilizer_requirements": {
                    "nitrogen": "120-150 kg/ha",
                    "phosphorus": "60-90 kg/ha",
                    "potassium": "60 kg/ha"
                }
            },
            
            "Rice": {
                "optimal_temp_range": {"min": 20, "max": 35},
                "growing_season": "May to November",
                "water_requirements": "Very High",
                "frost_sensitivity": "Very High",
                "heat_sensitivity": "Low",
                "soil_ph_range": {"min": 5.5, "max": 7.0},
                "planting_time": "May - June",
                "harvest_time": "October - November",
                "critical_growth_stages": [
                    "Germination (0-10 days)",
                    "Seedling (10-20 days)",
                    "Tillering (20-45 days)",
                    "Panicle Initiation (45-65 days)",
                    "Flowering (65-95 days)",
                    "Grain Filling (95-120 days)"
                ],
                "common_pests": [
                    "Brown Plant Hopper", "Rice Stem Borer", "Leaf Folder", "Green Leafhopper"
                ],
                "common_diseases": [
                    "Blast", "Bacterial Leaf Blight", "Sheath Blight", "Brown Spot"
                ],
                "irrigation_schedule": "Continuous flooding or alternate wetting/drying",
                "fertilizer_requirements": {
                    "nitrogen": "100-120 kg/ha",
                    "phosphorus": "60 kg/ha",
                    "potassium": "40 kg/ha"
                }
            },
            
            "Cotton": {
                "optimal_temp_range": {"min": 25, "max": 35},
                "growing_season": "April to November",
                "water_requirements": "High",
                "frost_sensitivity": "Very High",
                "heat_sensitivity": "Low to Medium",
                "soil_ph_range": {"min": 5.8, "max": 8.2},
                "planting_time": "April - May",
                "harvest_time": "September - December",
                "critical_growth_stages": [
                    "Germination (0-10 days)",
                    "Squaring (45-65 days)",
                    "Flowering (65-95 days)",
                    "Boll Development (95-130 days)",
                    "Maturity (130-180 days)"
                ],
                "common_pests": [
                    "Bollworm", "Whitefly", "Thrips", "Aphids", "Red Cotton Bug"
                ],
                "common_diseases": [
                    "Cotton Leaf Curl Virus", "Fusarium Wilt", "Root Rot", "Bacterial Blight"
                ],
                "irrigation_schedule": "Every 10-15 days",
                "fertilizer_requirements": {
                    "nitrogen": "150-200 kg/ha",
                    "phosphorus": "75-100 kg/ha",
                    "potassium": "50-75 kg/ha"
                }
            },
            
            "Sugarcane": {
                "optimal_temp_range": {"min": 20, "max": 35},
                "growing_season": "Year-round (18-month crop)",
                "water_requirements": "Very High",
                "frost_sensitivity": "High",
                "heat_sensitivity": "Low",
                "soil_ph_range": {"min": 6.0, "max": 8.5},
                "planting_time": "February - April and September - October",
                "harvest_time": "December - April",
                "critical_growth_stages": [
                    "Germination (0-45 days)",
                    "Tillering (45-120 days)",
                    "Grand Growth (120-270 days)",
                    "Maturation (270-360 days)"
                ],
                "common_pests": [
                    "Top Borer", "Root Borer", "Pyrilla", "White Fly", "Scale Insects"
                ],
                "common_diseases": [
                    "Red Rot", "Smut", "Wilt", "Ring Spot", "Mosaic"
                ],
                "irrigation_schedule": "Every 7-10 days",
                "fertilizer_requirements": {
                    "nitrogen": "200-250 kg/ha",
                    "phosphorus": "100 kg/ha",
                    "potassium": "100 kg/ha"
                }
            },
            
            "Maize": {
                "optimal_temp_range": {"min": 18, "max": 30},
                "growing_season": "Spring: February-June, Autumn: July-November",
                "water_requirements": "Medium to High",
                "frost_sensitivity": "High",
                "heat_sensitivity": "Medium",
                "soil_ph_range": {"min": 6.0, "max": 7.5},
                "planting_time": "February - March (Spring), July - August (Autumn)",
                "harvest_time": "June - July (Spring), November - December (Autumn)",
                "critical_growth_stages": [
                    "Germination (0-10 days)",
                    "Vegetative Growth (10-50 days)",
                    "Tasseling (50-70 days)",
                    "Grain Filling (70-100 days)",
                    "Maturity (100-120 days)"
                ],
                "common_pests": [
                    "Corn Borer", "Fall Army Worm", "Cutworm", "Aphids"
                ],
                "common_diseases": [
                    "Leaf Blight", "Common Rust", "Downy Mildew", "Stalk Rot"
                ],
                "irrigation_schedule": "Every 10-15 days",
                "fertilizer_requirements": {
                    "nitrogen": "120-150 kg/ha",
                    "phosphorus": "80-100 kg/ha",
                    "potassium": "60 kg/ha"
                }
            },
            
            "Barley": {
                "optimal_temp_range": {"min": 12, "max": 22},
                "growing_season": "November to April",
                "water_requirements": "Low to Medium",
                "frost_sensitivity": "Low",
                "heat_sensitivity": "High",
                "soil_ph_range": {"min": 6.0, "max": 8.5},
                "planting_time": "November - December",
                "harvest_time": "March - April",
                "critical_growth_stages": [
                    "Germination (0-15 days)",
                    "Tillering (15-45 days)",
                    "Stem Elongation (45-75 days)",
                    "Heading (75-90 days)",
                    "Grain Filling (90-110 days)"
                ],
                "common_pests": [
                    "Aphids", "Army Worm", "Shoot Fly"
                ],
                "common_diseases": [
                    "Net Blotch", "Powdery Mildew", "Stripe Rust", "Spot Blotch"
                ],
                "irrigation_schedule": "2-3 irrigations throughout season",
                "fertilizer_requirements": {
                    "nitrogen": "80-100 kg/ha",
                    "phosphorus": "60 kg/ha",
                    "potassium": "40 kg/ha"
                }
            },
            
            "Millet": {
                "optimal_temp_range": {"min": 25, "max": 35},
                "growing_season": "May to September",
                "water_requirements": "Low",
                "frost_sensitivity": "High",
                "heat_sensitivity": "Very Low",
                "soil_ph_range": {"min": 5.5, "max": 8.5},
                "planting_time": "May - June",
                "harvest_time": "August - September",
                "critical_growth_stages": [
                    "Germination (0-7 days)",
                    "Vegetative Growth (7-35 days)",
                    "Panicle Initiation (35-55 days)",
                    "Flowering (55-75 days)",
                    "Grain Filling (75-90 days)"
                ],
                "common_pests": [
                    "Shoot Fly", "Stem Borer", "Aphids"
                ],
                "common_diseases": [
                    "Downy Mildew", "Blast", "Rust", "Smut"
                ],
                "irrigation_schedule": "1-2 irrigations if needed",
                "fertilizer_requirements": {
                    "nitrogen": "40-60 kg/ha",
                    "phosphorus": "40 kg/ha",
                    "potassium": "20 kg/ha"
                }
            },
            
            "Sorghum": {
                "optimal_temp_range": {"min": 26, "max": 35},
                "growing_season": "April to October",
                "water_requirements": "Low to Medium",
                "frost_sensitivity": "High",
                "heat_sensitivity": "Very Low",
                "soil_ph_range": {"min": 6.0, "max": 8.5},
                "planting_time": "April - May",
                "harvest_time": "September - October",
                "critical_growth_stages": [
                    "Germination (0-10 days)",
                    "Vegetative Growth (10-45 days)",
                    "Panicle Initiation (45-65 days)",
                    "Flowering (65-85 days)",
                    "Grain Filling (85-110 days)"
                ],
                "common_pests": [
                    "Shoot Fly", "Stem Borer", "Aphids", "Midge"
                ],
                "common_diseases": [
                    "Grain Mold", "Anthracnose", "Rust", "Leaf Blight"
                ],
                "irrigation_schedule": "2-3 irrigations throughout season",
                "fertilizer_requirements": {
                    "nitrogen": "80-100 kg/ha",
                    "phosphorus": "60 kg/ha",
                    "potassium": "40 kg/ha"
                }
            }
        }
    
    def get_crop_info(self, crop_name: str) -> Optional[Dict]:
        """Get comprehensive information about a specific crop"""
        return self.crop_data.get(crop_name, None)
    
    def get_temperature_tolerance(self, crop_name: str, current_temp: float) -> Dict:
        """Check if current temperature is within optimal range for crop"""
        crop_info = self.get_crop_info(crop_name)
        if not crop_info:
            return {"status": "unknown", "message": "Crop information not available"}
        
        temp_range = crop_info["optimal_temp_range"]
        min_temp = temp_range["min"]
        max_temp = temp_range["max"]
        
        if current_temp < min_temp:
            if current_temp < min_temp - 5:
                return {
                    "status": "danger",
                    "message": f"Temperature ({current_temp}°C) is critically low for {crop_name}. Risk of severe damage.",
                    "recommendation": "Implement frost protection measures immediately"
                }
            else:
                return {
                    "status": "warning",
                    "message": f"Temperature ({current_temp}°C) is below optimal range for {crop_name}.",
                    "recommendation": "Monitor closely and consider protective measures"
                }
        elif current_temp > max_temp:
            if current_temp > max_temp + 5:
                return {
                    "status": "danger",
                    "message": f"Temperature ({current_temp}°C) is critically high for {crop_name}. Risk of heat stress.",
                    "recommendation": "Increase irrigation and provide shade if possible"
                }
            else:
                return {
                    "status": "warning",
                    "message": f"Temperature ({current_temp}°C) is above optimal range for {crop_name}.",
                    "recommendation": "Monitor for heat stress and adjust irrigation"
                }
        else:
            return {
                "status": "optimal",
                "message": f"Temperature ({current_temp}°C) is within optimal range for {crop_name}.",
                "recommendation": "Continue current management practices"
            }
    
    def get_seasonal_advice(self, crop_name: str, month: int) -> Dict:
        """Get seasonal farming advice for a specific crop and month"""
        crop_info = self.get_crop_info(crop_name)
        if not crop_info:
            return {"advice": "Crop information not available"}
        
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        current_month = month_names[month - 1]
        planting_time = crop_info["planting_time"]
        harvest_time = crop_info["harvest_time"]
        
        advice = {
            "month": current_month,
            "crop": crop_name,
            "planting_season": planting_time,
            "harvest_season": harvest_time,
            "general_advice": []
        }
        
        # Add month-specific advice based on crop calendar
        if crop_name == "Wheat":
            if month in [11, 12]:  # November, December
                advice["general_advice"] = [
                    "Optimal planting time - prepare fields and sow seeds",
                    "Ensure proper seed bed preparation",
                    "Apply basal fertilizer"
                ]
            elif month in [1, 2, 3]:  # January, February, March
                advice["general_advice"] = [
                    "Monitor for pests and diseases",
                    "Apply top dressing fertilizer",
                    "Irrigate as needed"
                ]
            elif month in [4, 5]:  # April, May
                advice["general_advice"] = [
                    "Harvest time - monitor grain maturity",
                    "Prepare harvesting equipment",
                    "Plan post-harvest storage"
                ]
        
        elif crop_name == "Rice":
            if month in [5, 6]:  # May, June
                advice["general_advice"] = [
                    "Prepare nursery beds",
                    "Transplant seedlings",
                    "Maintain water levels"
                ]
            elif month in [7, 8, 9]:  # July, August, September
                advice["general_advice"] = [
                    "Monitor water levels continuously",
                    "Apply fertilizer as per schedule",
                    "Control weeds and pests"
                ]
            elif month in [10, 11]:  # October, November
                advice["general_advice"] = [
                    "Harvest time - check grain maturity",
                    "Drain fields before harvest",
                    "Dry grains properly"
                ]
        
        elif crop_name == "Cotton":
            if month in [4, 5]:  # April, May
                advice["general_advice"] = [
                    "Optimal planting time",
                    "Prepare cotton beds",
                    "Apply pre-planting fertilizer"
                ]
            elif month in [6, 7, 8]:  # June, July, August
                advice["general_advice"] = [
                    "Monitor for bollworms and other pests",
                    "Apply growth regulators if needed",
                    "Maintain irrigation schedule"
                ]
            elif month in [9, 10, 11, 12]:  # September to December
                advice["general_advice"] = [
                    "Cotton picking season",
                    "Monitor fiber quality",
                    "Plan for multiple pickings"
                ]
        
        # Add more crop-specific monthly advice as needed
        
        return advice
    
    def get_pest_disease_calendar(self, crop_name: str, month: int) -> Dict:
        """Get month-specific pest and disease information"""
        crop_info = self.get_crop_info(crop_name)
        if not crop_info:
            return {"pests": [], "diseases": [], "prevention": []}
        
        # General pest and disease calendar (can be expanded)
        calendar = {
            "pests": crop_info.get("common_pests", []),
            "diseases": crop_info.get("common_diseases", []),
            "prevention": [
                "Regular field monitoring",
                "Maintain field hygiene",
                "Use resistant varieties when available",
                "Follow integrated pest management practices"
            ]
        }
        
        # Add seasonal specific recommendations
        if month in [6, 7, 8, 9]:  # Monsoon months
            calendar["prevention"].extend([
                "Ensure proper drainage to prevent fungal diseases",
                "Increase surveillance for moisture-loving pests",
                "Apply fungicides preventively if needed"
            ])
        elif month in [11, 12, 1, 2]:  # Winter months
            calendar["prevention"].extend([
                "Monitor for aphids and other cool-season pests",
                "Watch for frost damage that can lead to secondary infections"
            ])
        elif month in [4, 5, 10]:  # Pre-monsoon and post-monsoon
            calendar["prevention"].extend([
                "Prepare for seasonal pest transitions",
                "Clean field borders and remove crop residues"
            ])
        
        return calendar
    
    def get_irrigation_schedule(self, crop_name: str, weather_conditions: Dict) -> Dict:
        """Get irrigation recommendations based on crop and weather"""
        crop_info = self.get_crop_info(crop_name)
        if not crop_info:
            return {"schedule": "Information not available"}
        
        base_schedule = crop_info.get("irrigation_schedule", "As needed")
        water_req = crop_info.get("water_requirements", "Medium")
        
        # Adjust based on weather
        current_humidity = weather_conditions.get("humidity", 50)
        recent_precipitation = weather_conditions.get("precipitation", 0)
        temperature = weather_conditions.get("temperature", 25)
        
        recommendations = {
            "base_schedule": base_schedule,
            "water_requirements": water_req,
            "adjustments": []
        }
        
        # Weather-based adjustments
        if recent_precipitation > 10:  # mm
            recommendations["adjustments"].append("Reduce irrigation due to recent rainfall")
        elif recent_precipitation == 0 and current_humidity < 40:
            recommendations["adjustments"].append("Increase irrigation frequency due to low humidity")
        
        if temperature > 35:
            recommendations["adjustments"].append("Increase irrigation frequency due to high temperature")
        elif temperature < 15:
            recommendations["adjustments"].append("Reduce irrigation frequency due to low temperature")
        
        if current_humidity > 80:
            recommendations["adjustments"].append("Monitor for fungal diseases due to high humidity")
        
        return recommendations
