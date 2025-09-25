from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime

class SoilDatabase:
    """Advanced soil type database with thermal property analysis for Pakistani regions"""
    
    def __init__(self):
        self.soil_data = {
            # Punjab Region Soils
            "sandy_loam_punjab": {
                "name": "Sandy Loam (Punjab Plains)",
                "region": "Punjab",
                "soil_type": "Sandy Loam",
                "ph_range": {"min": 7.5, "max": 8.5},
                "organic_matter": {"min": 0.8, "max": 1.5},
                "thermal_properties": {
                    "thermal_conductivity": 1.2,  # W/m·K
                    "specific_heat": 800,         # J/kg·K
                    "bulk_density": 1.45,         # g/cm³
                    "heat_capacity": 1.16,        # MJ/m³·K
                    "thermal_diffusivity": 8.3e-7 # m²/s
                },
                "water_properties": {
                    "field_capacity": 18,         # %
                    "wilting_point": 8,           # %
                    "available_water": 10,        # %
                    "infiltration_rate": "moderate", # 12-25 mm/hr
                    "drainage": "good"
                },
                "agricultural_characteristics": {
                    "suitable_crops": ["Wheat", "Maize", "Cotton", "Sugarcane"],
                    "irrigation_frequency": "medium",
                    "fertilizer_retention": "moderate",
                    "erosion_risk": "low to moderate",
                    "compaction_risk": "low"
                },
                "seasonal_behavior": {
                    "winter": {
                        "temperature_retention": "moderate",
                        "moisture_retention": "good",
                        "frost_risk": "moderate"
                    },
                    "summer": {
                        "heat_stress": "moderate",
                        "water_demand": "high",
                        "cracking_tendency": "low"
                    },
                    "monsoon": {
                        "waterlogging_risk": "low",
                        "nutrient_leaching": "moderate",
                        "surface_runoff": "moderate"
                    }
                },
                "management_recommendations": [
                    "Regular organic matter addition to improve water retention",
                    "Moderate irrigation intervals (7-10 days)",
                    "Deep tillage recommended for root development",
                    "Apply mulch during summer to reduce heat stress"
                ]
            },
            
            "clay_loam_punjab": {
                "name": "Clay Loam (Central Punjab)",
                "region": "Punjab",
                "soil_type": "Clay Loam",
                "ph_range": {"min": 7.8, "max": 8.8},
                "organic_matter": {"min": 1.2, "max": 2.0},
                "thermal_properties": {
                    "thermal_conductivity": 1.8,
                    "specific_heat": 900,
                    "bulk_density": 1.35,
                    "heat_capacity": 1.22,
                    "thermal_diffusivity": 7.2e-7
                },
                "water_properties": {
                    "field_capacity": 32,
                    "wilting_point": 18,
                    "available_water": 14,
                    "infiltration_rate": "slow", # 2-6 mm/hr
                    "drainage": "moderate"
                },
                "agricultural_characteristics": {
                    "suitable_crops": ["Rice", "Wheat", "Sugarcane", "Cotton"],
                    "irrigation_frequency": "low",
                    "fertilizer_retention": "high",
                    "erosion_risk": "low",
                    "compaction_risk": "high"
                },
                "seasonal_behavior": {
                    "winter": {
                        "temperature_retention": "high",
                        "moisture_retention": "excellent",
                        "frost_risk": "low"
                    },
                    "summer": {
                        "heat_stress": "low",
                        "water_demand": "moderate",
                        "cracking_tendency": "high"
                    },
                    "monsoon": {
                        "waterlogging_risk": "high",
                        "nutrient_leaching": "low",
                        "surface_runoff": "low"
                    }
                },
                "management_recommendations": [
                    "Avoid working when soil is wet to prevent compaction",
                    "Install drainage systems to prevent waterlogging",
                    "Use controlled traffic farming methods",
                    "Apply gypsum to improve soil structure"
                ]
            },
            
            # Sindh Region Soils
            "silty_clay_sindh": {
                "name": "Silty Clay (Sindh Delta)",
                "region": "Sindh",
                "soil_type": "Silty Clay",
                "ph_range": {"min": 7.5, "max": 8.8},
                "organic_matter": {"min": 0.5, "max": 1.2},
                "thermal_properties": {
                    "thermal_conductivity": 1.6,
                    "specific_heat": 850,
                    "bulk_density": 1.25,
                    "heat_capacity": 1.06,
                    "thermal_diffusivity": 7.8e-7
                },
                "water_properties": {
                    "field_capacity": 38,
                    "wilting_point": 22,
                    "available_water": 16,
                    "infiltration_rate": "very slow", # 1-3 mm/hr
                    "drainage": "poor"
                },
                "agricultural_characteristics": {
                    "suitable_crops": ["Rice", "Cotton", "Sugarcane"],
                    "irrigation_frequency": "very low",
                    "fertilizer_retention": "very high",
                    "erosion_risk": "very low",
                    "compaction_risk": "very high"
                },
                "seasonal_behavior": {
                    "winter": {
                        "temperature_retention": "very high",
                        "moisture_retention": "excellent",
                        "frost_risk": "very low"
                    },
                    "summer": {
                        "heat_stress": "very low",
                        "water_demand": "low",
                        "cracking_tendency": "very high"
                    },
                    "monsoon": {
                        "waterlogging_risk": "very high",
                        "nutrient_leaching": "very low",
                        "surface_runoff": "very low"
                    }
                },
                "management_recommendations": [
                    "Implement comprehensive drainage systems",
                    "Use raised bed cultivation during monsoon",
                    "Minimize tillage operations",
                    "Apply organic matter to improve structure"
                ]
            },
            
            "sandy_sindh": {
                "name": "Sandy Soil (Thar Desert)",
                "region": "Sindh",
                "soil_type": "Sandy",
                "ph_range": {"min": 7.0, "max": 8.2},
                "organic_matter": {"min": 0.2, "max": 0.8},
                "thermal_properties": {
                    "thermal_conductivity": 0.8,
                    "specific_heat": 750,
                    "bulk_density": 1.55,
                    "heat_capacity": 1.16,
                    "thermal_diffusivity": 9.2e-7
                },
                "water_properties": {
                    "field_capacity": 8,
                    "wilting_point": 3,
                    "available_water": 5,
                    "infiltration_rate": "very fast", # >30 mm/hr
                    "drainage": "excessive"
                },
                "agricultural_characteristics": {
                    "suitable_crops": ["Millet", "Sorghum", "Desert crops"],
                    "irrigation_frequency": "very high",
                    "fertilizer_retention": "poor",
                    "erosion_risk": "very high",
                    "compaction_risk": "very low"
                },
                "seasonal_behavior": {
                    "winter": {
                        "temperature_retention": "poor",
                        "moisture_retention": "poor",
                        "frost_risk": "high"
                    },
                    "summer": {
                        "heat_stress": "very high",
                        "water_demand": "very high",
                        "cracking_tendency": "none"
                    },
                    "monsoon": {
                        "waterlogging_risk": "none",
                        "nutrient_leaching": "very high",
                        "surface_runoff": "high"
                    }
                },
                "management_recommendations": [
                    "Frequent, light irrigation applications",
                    "Use drip irrigation for water conservation",
                    "Apply heavy organic matter and mulching",
                    "Implement windbreaks to reduce erosion"
                ]
            },
            
            # Balochistan Region Soils
            "rocky_balochistan": {
                "name": "Rocky/Calcareous Soil (Balochistan Plateau)",
                "region": "Balochistan",
                "soil_type": "Calcareous/Rocky",
                "ph_range": {"min": 8.0, "max": 9.0},
                "organic_matter": {"min": 0.3, "max": 1.0},
                "thermal_properties": {
                    "thermal_conductivity": 2.2,
                    "specific_heat": 920,
                    "bulk_density": 1.65,
                    "heat_capacity": 1.52,
                    "thermal_diffusivity": 8.9e-7
                },
                "water_properties": {
                    "field_capacity": 15,
                    "wilting_point": 8,
                    "available_water": 7,
                    "infiltration_rate": "fast", # 15-30 mm/hr
                    "drainage": "good to excessive"
                },
                "agricultural_characteristics": {
                    "suitable_crops": ["Wheat", "Barley", "Dates", "Almonds"],
                    "irrigation_frequency": "high",
                    "fertilizer_retention": "poor",
                    "erosion_risk": "high",
                    "compaction_risk": "low"
                },
                "seasonal_behavior": {
                    "winter": {
                        "temperature_retention": "high",
                        "moisture_retention": "moderate",
                        "frost_risk": "high"
                    },
                    "summer": {
                        "heat_stress": "high",
                        "water_demand": "very high",
                        "cracking_tendency": "low"
                    },
                    "monsoon": {
                        "waterlogging_risk": "very low",
                        "nutrient_leaching": "high",
                        "surface_runoff": "very high"
                    }
                },
                "management_recommendations": [
                    "Improve soil depth with organic matter",
                    "Use terracing to prevent erosion",
                    "Install efficient irrigation systems",
                    "Apply sulfur to reduce pH if needed"
                ]
            },
            
            # KPK Region Soils
            "mountainous_kpk": {
                "name": "Mountain Soil (KPK Hills)",
                "region": "Khyber Pakhtunkhwa",
                "soil_type": "Mountain/Forest",
                "ph_range": {"min": 6.5, "max": 7.8},
                "organic_matter": {"min": 2.0, "max": 4.5},
                "thermal_properties": {
                    "thermal_conductivity": 1.4,
                    "specific_heat": 1100,
                    "bulk_density": 1.20,
                    "heat_capacity": 1.32,
                    "thermal_diffusivity": 8.8e-7
                },
                "water_properties": {
                    "field_capacity": 28,
                    "wilting_point": 14,
                    "available_water": 14,
                    "infiltration_rate": "moderate", # 8-15 mm/hr
                    "drainage": "good"
                },
                "agricultural_characteristics": {
                    "suitable_crops": ["Wheat", "Maize", "Potatoes", "Fruits"],
                    "irrigation_frequency": "moderate",
                    "fertilizer_retention": "good",
                    "erosion_risk": "very high",
                    "compaction_risk": "moderate"
                },
                "seasonal_behavior": {
                    "winter": {
                        "temperature_retention": "moderate",
                        "moisture_retention": "good",
                        "frost_risk": "very high"
                    },
                    "summer": {
                        "heat_stress": "low",
                        "water_demand": "moderate",
                        "cracking_tendency": "none"
                    },
                    "monsoon": {
                        "waterlogging_risk": "low",
                        "nutrient_leaching": "moderate",
                        "surface_runoff": "very high"
                    }
                },
                "management_recommendations": [
                    "Implement terracing and contour farming",
                    "Use cover crops to prevent erosion",
                    "Maintain organic matter content",
                    "Install proper drainage systems"
                ]
            }
        }
        
        # Regional soil mapping
        self.regional_mapping = {
            "Punjab_Plains": ["sandy_loam_punjab", "clay_loam_punjab"],
            "Sindh_Plains": ["silty_clay_sindh", "sandy_sindh"],
            "Balochistan_Plateau": ["rocky_balochistan"],
            "Northern_Mountains": ["mountainous_kpk"],
            "Coastal_Areas": ["sandy_sindh", "silty_clay_sindh"]
        }
    
    def get_soil_by_region(self, region: str) -> List[Dict]:
        """Get all soil types for a specific region"""
        soil_codes = self.regional_mapping.get(region, [])
        return [self.soil_data[code] for code in soil_codes if code in self.soil_data]
    
    def get_soil_by_coordinates(self, lat: float, lon: float) -> List[Dict]:
        """Get suitable soil types based on coordinates"""
        from utils import determine_weather_region
        
        region = determine_weather_region(lat, lon)
        return self.get_soil_by_region(region)
    
    def get_soil_thermal_analysis(self, soil_type: str, temperature: float, moisture: float) -> Dict:
        """Analyze soil thermal behavior under specific conditions"""
        if soil_type not in self.soil_data:
            return {"error": "Soil type not found"}
        
        soil = self.soil_data[soil_type]
        thermal_props = soil["thermal_properties"]
        
        # Calculate thermal performance metrics
        thermal_performance = {
            "soil_name": soil["name"],
            "current_conditions": {
                "air_temperature": temperature,
                "soil_moisture": moisture
            },
            "thermal_metrics": {
                "heat_transfer_rate": thermal_props["thermal_conductivity"] * (temperature - 20),
                "temperature_stability": self._calculate_temperature_stability(thermal_props, temperature),
                "moisture_effect": self._calculate_moisture_effect(soil, moisture),
                "root_zone_temperature": self._estimate_root_zone_temp(thermal_props, temperature)
            },
            "agricultural_impact": {
                "seed_germination_suitability": self._assess_germination_conditions(soil, temperature),
                "root_development_conditions": self._assess_root_conditions(soil, temperature, moisture),
                "water_management_needs": self._assess_water_needs(soil, temperature, moisture)
            }
        }
        
        return thermal_performance
    
    def _calculate_temperature_stability(self, thermal_props: Dict, air_temp: float) -> str:
        """Calculate soil temperature stability"""
        thermal_mass = thermal_props["heat_capacity"]
        
        if thermal_mass > 1.3:
            return "Very stable - slow temperature changes"
        elif thermal_mass > 1.1:
            return "Stable - moderate temperature buffering"
        else:
            return "Variable - rapid temperature changes"
    
    def _calculate_moisture_effect(self, soil: Dict, moisture: float) -> Dict:
        """Calculate effect of moisture on soil thermal properties"""
        water_props = soil["water_properties"]
        field_capacity = water_props["field_capacity"]
        
        moisture_ratio = moisture / field_capacity if field_capacity > 0 else 0
        
        return {
            "moisture_status": "Optimal" if 0.6 <= moisture_ratio <= 0.8 else 
                             "Wet" if moisture_ratio > 0.8 else "Dry",
            "thermal_conductivity_modifier": 1 + (moisture_ratio - 0.5) * 0.3,
            "evapotranspiration_effect": "High" if moisture_ratio > 0.7 else 
                                       "Moderate" if moisture_ratio > 0.4 else "Low"
        }
    
    def _estimate_root_zone_temp(self, thermal_props: Dict, air_temp: float) -> float:
        """Estimate root zone temperature based on soil thermal properties"""
        thermal_diffusivity = thermal_props["thermal_diffusivity"]
        
        # Simplified model: soil temperature lags air temperature
        damping_factor = 0.3 + (thermal_diffusivity * 1e6 * 0.1)
        root_zone_temp = 20 + (air_temp - 20) * damping_factor
        
        return round(root_zone_temp, 1)
    
    def _assess_germination_conditions(self, soil: Dict, temperature: float) -> str:
        """Assess soil conditions for seed germination"""
        root_zone_temp = self._estimate_root_zone_temp(soil["thermal_properties"], temperature)
        
        if 15 <= root_zone_temp <= 30:
            return "Excellent"
        elif 10 <= root_zone_temp <= 35:
            return "Good"
        elif 5 <= root_zone_temp <= 40:
            return "Fair"
        else:
            return "Poor"
    
    def _assess_root_conditions(self, soil: Dict, temperature: float, moisture: float) -> str:
        """Assess soil conditions for root development"""
        water_props = soil["water_properties"]
        available_water = water_props["available_water"]
        
        moisture_adequacy = moisture / available_water if available_water > 0 else 0
        temp_suitability = 1.0 if 18 <= temperature <= 28 else 0.7
        
        overall_score = moisture_adequacy * temp_suitability
        
        if overall_score > 0.8:
            return "Excellent"
        elif overall_score > 0.6:
            return "Good"
        elif overall_score > 0.4:
            return "Fair"
        else:
            return "Poor"
    
    def _assess_water_needs(self, soil: Dict, temperature: float, moisture: float) -> Dict:
        """Assess water management needs"""
        water_props = soil["water_properties"]
        
        return {
            "irrigation_urgency": "High" if moisture < water_props["wilting_point"] else
                                 "Medium" if moisture < water_props["field_capacity"] * 0.7 else
                                 "Low",
            "drainage_needs": "High" if water_props["drainage"] == "poor" and moisture > water_props["field_capacity"] else
                             "Medium" if water_props["drainage"] == "moderate" else
                             "Low",
            "recommended_irrigation_method": self._recommend_irrigation_method(soil, temperature)
        }
    
    def _recommend_irrigation_method(self, soil: Dict, temperature: float) -> str:
        """Recommend irrigation method based on soil and climate"""
        water_props = soil["water_properties"]
        infiltration = water_props["infiltration_rate"]
        
        if infiltration == "very fast" or temperature > 35:
            return "Drip irrigation (frequent, small amounts)"
        elif infiltration == "very slow" or water_props["drainage"] == "poor":
            return "Surface irrigation with proper drainage"
        elif temperature > 30:
            return "Sprinkler irrigation (evening hours)"
        else:
            return "Furrow or border irrigation"
    
    def get_crop_soil_compatibility(self, crop_type: str, soil_type: str) -> Dict:
        """Analyze compatibility between crop and soil type"""
        if soil_type not in self.soil_data:
            return {"error": "Soil type not found"}
        
        soil = self.soil_data[soil_type]
        suitable_crops = soil["agricultural_characteristics"]["suitable_crops"]
        
        compatibility = {
            "crop": crop_type,
            "soil": soil["name"],
            "is_suitable": crop_type in suitable_crops,
            "suitability_score": self._calculate_suitability_score(crop_type, soil),
            "recommendations": self._get_crop_soil_recommendations(crop_type, soil)
        }
        
        return compatibility
    
    def _calculate_suitability_score(self, crop_type: str, soil: Dict) -> int:
        """Calculate crop-soil suitability score (0-100)"""
        base_score = 80 if crop_type in soil["agricultural_characteristics"]["suitable_crops"] else 40
        
        # Adjust based on soil characteristics
        adjustments = 0
        
        # pH suitability
        ph_range = soil["ph_range"]
        crop_ph_preferences = {
            "Rice": {"min": 5.5, "max": 7.0},
            "Wheat": {"min": 6.0, "max": 7.5},
            "Cotton": {"min": 5.8, "max": 8.2},
            "Sugarcane": {"min": 6.0, "max": 8.5},
            "Maize": {"min": 6.0, "max": 7.5},
            "Barley": {"min": 6.0, "max": 8.5}
        }
        
        if crop_type in crop_ph_preferences:
            crop_ph = crop_ph_preferences[crop_type]
            if crop_ph["min"] <= ph_range["max"] and crop_ph["max"] >= ph_range["min"]:
                adjustments += 10
            else:
                adjustments -= 15
        
        # Drainage requirements
        drainage = soil["water_properties"]["drainage"]
        if crop_type == "Rice" and drainage in ["poor", "moderate"]:
            adjustments += 15
        elif crop_type in ["Wheat", "Cotton"] and drainage == "good":
            adjustments += 10
        
        return min(100, max(0, base_score + adjustments))
    
    def _get_crop_soil_recommendations(self, crop_type: str, soil: Dict) -> List[str]:
        """Get specific recommendations for crop-soil combination"""
        recommendations = []
        
        # General soil management
        recommendations.extend(soil["management_recommendations"])
        
        # Crop-specific adjustments
        if crop_type == "Rice":
            if soil["water_properties"]["drainage"] != "poor":
                recommendations.append("Consider puddling to create impermeable layer for rice cultivation")
        
        elif crop_type == "Cotton":
            if soil["agricultural_characteristics"]["compaction_risk"] == "high":
                recommendations.append("Use controlled traffic farming to prevent compaction during cotton cultivation")
        
        elif crop_type in ["Wheat", "Barley"]:
            if soil["thermal_properties"]["thermal_conductivity"] < 1.0:
                recommendations.append("Consider spring planting to avoid cold soil conditions")
        
        return recommendations[:6]  # Limit to top 6 recommendations
    
    def get_seasonal_soil_management(self, soil_type: str, season: str) -> Dict:
        """Get seasonal soil management recommendations"""
        if soil_type not in self.soil_data:
            return {"error": "Soil type not found"}
        
        soil = self.soil_data[soil_type]
        seasonal_behavior = soil["seasonal_behavior"]
        
        if season.lower() not in seasonal_behavior:
            return {"error": "Season not found"}
        
        season_data = seasonal_behavior[season.lower()]
        
        return {
            "season": season.title(),
            "soil_name": soil["name"],
            "behavior": season_data,
            "management_priorities": self._get_seasonal_priorities(season_data, season.lower()),
            "risk_factors": self._identify_seasonal_risks(season_data, season.lower()),
            "recommended_practices": self._get_seasonal_practices(soil, season.lower())
        }
    
    def _get_seasonal_priorities(self, season_data: Dict, season: str) -> List[str]:
        """Get management priorities for the season"""
        priorities = []
        
        if season == "winter":
            if season_data.get("frost_risk") in ["high", "very high"]:
                priorities.append("Frost protection measures")
            if season_data.get("moisture_retention") == "excellent":
                priorities.append("Optimize water usage efficiency")
                
        elif season == "summer":
            if season_data.get("heat_stress") in ["high", "very high"]:
                priorities.append("Heat stress mitigation")
            if season_data.get("water_demand") in ["high", "very high"]:
                priorities.append("Intensive irrigation management")
                
        elif season == "monsoon":
            if season_data.get("waterlogging_risk") in ["high", "very high"]:
                priorities.append("Drainage and waterlogging prevention")
            if season_data.get("nutrient_leaching") in ["high", "very high"]:
                priorities.append("Nutrient retention strategies")
        
        return priorities
    
    def _identify_seasonal_risks(self, season_data: Dict, season: str) -> List[str]:
        """Identify seasonal risk factors"""
        risks = []
        
        for risk_type, level in season_data.items():
            if level in ["high", "very high"]:
                risk_name = risk_type.replace("_", " ").title()
                risks.append(f"{risk_name}: {level}")
        
        return risks
    
    def _get_seasonal_practices(self, soil: Dict, season: str) -> List[str]:
        """Get recommended practices for the season"""
        practices = []
        base_recommendations = soil["management_recommendations"]
        
        # Add seasonal-specific practices
        if season == "winter":
            practices.extend([
                "Reduce irrigation frequency",
                "Apply organic mulch for temperature regulation",
                "Plan soil preparation for spring crops"
            ])
        elif season == "summer":
            practices.extend([
                "Increase irrigation frequency",
                "Use reflective mulching",
                "Schedule field operations for cooler hours"
            ])
        elif season == "monsoon":
            practices.extend([
                "Ensure proper field drainage",
                "Avoid heavy machinery operations",
                "Monitor for nutrient deficiencies"
            ])
        
        # Include relevant base recommendations
        practices.extend(base_recommendations[:3])
        
        return practices[:8]  # Limit to 8 practices