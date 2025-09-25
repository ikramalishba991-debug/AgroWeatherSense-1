"""
Seasonal Farming Calendar for Pakistani Agricultural Practices
Provides region-specific planting and harvest schedules for major crops
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import calendar

class PakistanFarmingCalendar:
    def __init__(self):
        """Initialize the Pakistani farming calendar system"""
        
        # Define the three main seasons in Pakistan
        self.seasons = {
            'kharif': {  # Summer/Monsoon crops (April-October)
                'months': [4, 5, 6, 7, 8, 9, 10],
                'description': 'Summer/Monsoon season crops',
                'weather_dependency': 'monsoon_rainfall'
            },
            'rabi': {  # Winter crops (November-April)
                'months': [11, 12, 1, 2, 3, 4],
                'description': 'Winter season crops',
                'weather_dependency': 'winter_temperature'
            },
            'zaid': {  # Spring crops (March-June)
                'months': [3, 4, 5, 6],
                'description': 'Spring season crops',
                'weather_dependency': 'hot_weather'
            }
        }
        
        # Regional variations in Pakistan
        self.regions = {
            'Punjab_Plains': {
                'climate_zone': 'semi_arid',
                'irrigation': 'canal_tubewell',
                'soil_type': 'alluvial'
            },
            'Sindh_Plains': {
                'climate_zone': 'arid',
                'irrigation': 'canal_tubewell',
                'soil_type': 'alluvial'
            },
            'KPK_Mountainous': {
                'climate_zone': 'temperate',
                'irrigation': 'rain_fed',
                'soil_type': 'mountain'
            },
            'Balochistan_Arid': {
                'climate_zone': 'arid',
                'irrigation': 'limited',
                'soil_type': 'desert'
            },
            'Punjab_Pothohar': {
                'climate_zone': 'semi_arid',
                'irrigation': 'rain_fed',
                'soil_type': 'clay'
            },
            'Gilgit_Baltistan': {
                'climate_zone': 'cold_temperate',
                'irrigation': 'glacier_fed',
                'soil_type': 'mountain'
            }
        }
        
        # Comprehensive crop calendar for Pakistani agriculture
        self.crop_calendar = {
            'wheat': {
                'season': 'rabi',
                'regional_schedules': {
                    'Punjab_Plains': {
                        'sowing': {'start_month': 11, 'end_month': 12, 'optimal_weeks': [46, 47, 48, 49]},
                        'harvesting': {'start_month': 4, 'end_month': 5, 'optimal_weeks': [16, 17, 18, 19]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 2, 'critical_factors': ['soil_moisture', 'temperature']},
                            'tillering': {'weeks_after_sowing': 8, 'critical_factors': ['irrigation', 'fertilizer']},
                            'stem_elongation': {'weeks_after_sowing': 12, 'critical_factors': ['water_stress_avoid']},
                            'grain_filling': {'weeks_after_sowing': 18, 'critical_factors': ['hot_winds_protection']}
                        }
                    },
                    'Sindh_Plains': {
                        'sowing': {'start_month': 11, 'end_month': 12, 'optimal_weeks': [47, 48, 49, 50]},
                        'harvesting': {'start_month': 4, 'end_month': 5, 'optimal_weeks': [15, 16, 17, 18]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 2, 'critical_factors': ['soil_moisture', 'salinity_control']},
                            'tillering': {'weeks_after_sowing': 8, 'critical_factors': ['irrigation', 'fertilizer']},
                            'stem_elongation': {'weeks_after_sowing': 12, 'critical_factors': ['water_management']},
                            'grain_filling': {'weeks_after_sowing': 18, 'critical_factors': ['heat_stress_management']}
                        }
                    },
                    'KPK_Mountainous': {
                        'sowing': {'start_month': 10, 'end_month': 11, 'optimal_weeks': [42, 43, 44, 45]},
                        'harvesting': {'start_month': 5, 'end_month': 6, 'optimal_weeks': [20, 21, 22, 23]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 3, 'critical_factors': ['frost_protection', 'soil_preparation']},
                            'tillering': {'weeks_after_sowing': 10, 'critical_factors': ['spring_irrigation']},
                            'stem_elongation': {'weeks_after_sowing': 15, 'critical_factors': ['disease_management']},
                            'grain_filling': {'weeks_after_sowing': 22, 'critical_factors': ['rain_protection']}
                        }
                    }
                },
                'variety_recommendations': {
                    'early': ['Faisalabad-2008', 'Punjab-2011'],
                    'medium': ['Shafaq-2006', 'Lasani-2008'],
                    'late': ['Inquilab-91', 'Pak-81']
                }
            },
            
            'rice': {
                'season': 'kharif',
                'regional_schedules': {
                    'Punjab_Plains': {
                        'nursery': {'start_month': 4, 'end_month': 5, 'optimal_weeks': [16, 17, 18, 19]},
                        'transplanting': {'start_month': 6, 'end_month': 7, 'optimal_weeks': [24, 25, 26, 27]},
                        'harvesting': {'start_month': 10, 'end_month': 11, 'optimal_weeks': [40, 41, 42, 43]},
                        'growth_stages': {
                            'seedling': {'weeks_after_sowing': 4, 'critical_factors': ['water_level', 'pest_control']},
                            'tillering': {'weeks_after_sowing': 8, 'critical_factors': ['nitrogen_application', 'weed_control']},
                            'panicle_initiation': {'weeks_after_sowing': 12, 'critical_factors': ['water_stress_avoid']},
                            'grain_filling': {'weeks_after_sowing': 16, 'critical_factors': ['stem_borer_control']}
                        }
                    },
                    'Sindh_Plains': {
                        'nursery': {'start_month': 5, 'end_month': 6, 'optimal_weeks': [18, 19, 20, 21]},
                        'transplanting': {'start_month': 7, 'end_month': 8, 'optimal_weeks': [27, 28, 29, 30]},
                        'harvesting': {'start_month': 11, 'end_month': 12, 'optimal_weeks': [44, 45, 46, 47]},
                        'growth_stages': {
                            'seedling': {'weeks_after_sowing': 4, 'critical_factors': ['salinity_tolerance', 'pest_control']},
                            'tillering': {'weeks_after_sowing': 8, 'critical_factors': ['fertilizer_management']},
                            'panicle_initiation': {'weeks_after_sowing': 12, 'critical_factors': ['heat_tolerance']},
                            'grain_filling': {'weeks_after_sowing': 16, 'critical_factors': ['lodging_prevention']}
                        }
                    }
                },
                'variety_recommendations': {
                    'basmati': ['Super Basmati', 'Basmati 385', 'Basmati 2000'],
                    'coarse': ['IRRI-6', 'KS-282', 'Shaheen Basmati'],
                    'hybrid': ['Guard-1', 'Surjeet-1']
                }
            },
            
            'cotton': {
                'season': 'kharif',
                'regional_schedules': {
                    'Punjab_Plains': {
                        'sowing': {'start_month': 4, 'end_month': 6, 'optimal_weeks': [17, 18, 19, 20, 21, 22]},
                        'picking': {'start_month': 9, 'end_month': 12, 'optimal_weeks': [36, 40, 44, 48]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 2, 'critical_factors': ['soil_temperature', 'moisture']},
                            'squaring': {'weeks_after_sowing': 8, 'critical_factors': ['thrips_control', 'fertilizer']},
                            'flowering': {'weeks_after_sowing': 12, 'critical_factors': ['bollworm_control']},
                            'boll_development': {'weeks_after_sowing': 16, 'critical_factors': ['pink_bollworm_control']}
                        }
                    },
                    'Sindh_Plains': {
                        'sowing': {'start_month': 5, 'end_month': 6, 'optimal_weeks': [18, 19, 20, 21, 22, 23]},
                        'picking': {'start_month': 10, 'end_month': 1, 'optimal_weeks': [40, 44, 48, 52]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 2, 'critical_factors': ['heat_tolerance', 'soil_salinity']},
                            'squaring': {'weeks_after_sowing': 8, 'critical_factors': ['pest_management']},
                            'flowering': {'weeks_after_sowing': 12, 'critical_factors': ['water_stress_management']},
                            'boll_development': {'weeks_after_sowing': 16, 'critical_factors': ['late_season_pests']}
                        }
                    }
                },
                'variety_recommendations': {
                    'bt_varieties': ['Bt-121', 'IUB-222', 'FH-142'],
                    'conventional': ['CIM-573', 'MNH-886', 'VH-289'],
                    'early_maturing': ['CIM-448', 'NIAB-78']
                }
            },
            
            'sugarcane': {
                'season': 'both',  # Perennial crop
                'regional_schedules': {
                    'Punjab_Plains': {
                        'autumn_planting': {'start_month': 9, 'end_month': 11, 'optimal_weeks': [37, 38, 39, 40, 41, 42]},
                        'spring_planting': {'start_month': 2, 'end_month': 4, 'optimal_weeks': [8, 9, 10, 11, 12, 13]},
                        'harvesting': {'start_month': 11, 'end_month': 4, 'optimal_weeks': [46, 47, 48, 49, 50, 14, 15, 16]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 4, 'critical_factors': ['soil_moisture', 'temperature']},
                            'tillering': {'weeks_after_sowing': 12, 'critical_factors': ['irrigation', 'fertilizer']},
                            'grand_growth': {'weeks_after_sowing': 24, 'critical_factors': ['borers_control']},
                            'maturity': {'weeks_after_sowing': 48, 'critical_factors': ['sucrose_content']}
                        }
                    },
                    'Sindh_Plains': {
                        'autumn_planting': {'start_month': 10, 'end_month': 12, 'optimal_weeks': [40, 41, 42, 43, 44, 45]},
                        'spring_planting': {'start_month': 2, 'end_month': 3, 'optimal_weeks': [6, 7, 8, 9, 10, 11]},
                        'harvesting': {'start_month': 12, 'end_month': 4, 'optimal_weeks': [48, 49, 50, 51, 52, 14, 15]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 4, 'critical_factors': ['salinity_tolerance']},
                            'tillering': {'weeks_after_sowing': 12, 'critical_factors': ['water_management']},
                            'grand_growth': {'weeks_after_sowing': 24, 'critical_factors': ['heat_stress']},
                            'maturity': {'weeks_after_sowing': 48, 'critical_factors': ['harvest_timing']}
                        }
                    }
                },
                'variety_recommendations': {
                    'high_yielding': ['CPF-246', 'HSF-240', 'CPF-243'],
                    'disease_resistant': ['CPF-251', 'S-2003-US-127'],
                    'ratoon_suitable': ['CP-77-400', 'CPF-237']
                }
            },
            
            'maize': {
                'season': 'both',  # Spring and autumn
                'regional_schedules': {
                    'Punjab_Plains': {
                        'spring_sowing': {'start_month': 2, 'end_month': 3, 'optimal_weeks': [6, 7, 8, 9, 10]},
                        'autumn_sowing': {'start_month': 7, 'end_month': 8, 'optimal_weeks': [28, 29, 30, 31, 32]},
                        'spring_harvesting': {'start_month': 6, 'end_month': 7, 'optimal_weeks': [22, 23, 24, 25]},
                        'autumn_harvesting': {'start_month': 11, 'end_month': 12, 'optimal_weeks': [44, 45, 46, 47]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 1, 'critical_factors': ['soil_temperature', 'moisture']},
                            'knee_high': {'weeks_after_sowing': 6, 'critical_factors': ['stem_borer_control']},
                            'tasseling': {'weeks_after_sowing': 10, 'critical_factors': ['irrigation_critical']},
                            'grain_filling': {'weeks_after_sowing': 14, 'critical_factors': ['drought_stress']}
                        }
                    },
                    'KPK_Mountainous': {
                        'spring_sowing': {'start_month': 4, 'end_month': 5, 'optimal_weeks': [14, 15, 16, 17, 18]},
                        'spring_harvesting': {'start_month': 9, 'end_month': 10, 'optimal_weeks': [36, 37, 38, 39]},
                        'growth_stages': {
                            'germination': {'weeks_after_sowing': 2, 'critical_factors': ['frost_protection']},
                            'knee_high': {'weeks_after_sowing': 8, 'critical_factors': ['disease_control']},
                            'tasseling': {'weeks_after_sowing': 12, 'critical_factors': ['rain_fed_management']},
                            'grain_filling': {'weeks_after_sowing': 16, 'critical_factors': ['early_frost_protection']}
                        }
                    }
                },
                'variety_recommendations': {
                    'spring': ['Agaiti-2002', 'EV-1098', 'Sahiwal-2002'],
                    'autumn': ['Agaiti-2002', 'Pearl', 'Pak-Afghan'],
                    'high_yielding': ['YH-1898', 'YH-5427', 'FH-810']
                }
            },
            
            'mango': {
                'season': 'perennial',
                'regional_schedules': {
                    'Punjab_Plains': {
                        'flowering': {'start_month': 1, 'end_month': 3, 'optimal_weeks': [2, 3, 4, 5, 6, 7, 8, 9]},
                        'fruit_development': {'start_month': 3, 'end_month': 6, 'optimal_weeks': [10, 11, 12, 13, 14, 15, 16]},
                        'harvesting': {'start_month': 5, 'end_month': 8, 'optimal_weeks': [18, 19, 20, 21, 22, 23, 24, 25]},
                        'growth_stages': {
                            'flowering': {'weeks_after_flowering': 0, 'critical_factors': ['pollination', 'disease_control']},
                            'fruit_set': {'weeks_after_flowering': 4, 'critical_factors': ['fruit_drop_control']},
                            'fruit_development': {'weeks_after_flowering': 8, 'critical_factors': ['irrigation', 'pest_control']},
                            'maturity': {'weeks_after_flowering': 16, 'critical_factors': ['harvest_timing']}
                        }
                    },
                    'Sindh_Plains': {
                        'flowering': {'start_month': 12, 'end_month': 2, 'optimal_weeks': [50, 51, 52, 1, 2, 3, 4, 5]},
                        'fruit_development': {'start_month': 2, 'end_month': 5, 'optimal_weeks': [6, 7, 8, 9, 10, 11, 12]},
                        'harvesting': {'start_month': 4, 'end_month': 7, 'optimal_weeks': [14, 15, 16, 17, 18, 19, 20]},
                        'growth_stages': {
                            'flowering': {'weeks_after_flowering': 0, 'critical_factors': ['heat_protection', 'irrigation']},
                            'fruit_set': {'weeks_after_flowering': 4, 'critical_factors': ['wind_protection']},
                            'fruit_development': {'weeks_after_flowering': 8, 'critical_factors': ['water_stress_management']},
                            'maturity': {'weeks_after_flowering': 16, 'critical_factors': ['early_harvest']}
                        }
                    }
                },
                'variety_recommendations': {
                    'early': ['Anwar Ratol', 'Dosehri', 'Saroli'],
                    'mid_season': ['Chaunsa', 'Langra', 'Fajri'],
                    'late': ['Sindhri', 'Neelum', 'Samar Bahisht']
                }
            },
            
            'onion': {
                'season': 'rabi',
                'regional_schedules': {
                    'Punjab_Plains': {
                        'nursery': {'start_month': 9, 'end_month': 10, 'optimal_weeks': [36, 37, 38, 39, 40]},
                        'transplanting': {'start_month': 11, 'end_month': 12, 'optimal_weeks': [44, 45, 46, 47, 48]},
                        'harvesting': {'start_month': 4, 'end_month': 5, 'optimal_weeks': [16, 17, 18, 19, 20]},
                        'growth_stages': {
                            'establishment': {'weeks_after_transplanting': 2, 'critical_factors': ['irrigation', 'weeding']},
                            'bulb_initiation': {'weeks_after_transplanting': 8, 'critical_factors': ['nitrogen_control']},
                            'bulb_development': {'weeks_after_transplanting': 12, 'critical_factors': ['water_management']},
                            'maturity': {'weeks_after_transplanting': 18, 'critical_factors': ['curing_preparation']}
                        }
                    },
                    'Sindh_Plains': {
                        'nursery': {'start_month': 8, 'end_month': 9, 'optimal_weeks': [32, 33, 34, 35, 36]},
                        'transplanting': {'start_month': 10, 'end_month': 11, 'optimal_weeks': [40, 41, 42, 43, 44]},
                        'harvesting': {'start_month': 3, 'end_month': 4, 'optimal_weeks': [12, 13, 14, 15, 16]},
                        'growth_stages': {
                            'establishment': {'weeks_after_transplanting': 2, 'critical_factors': ['heat_protection']},
                            'bulb_initiation': {'weeks_after_transplanting': 8, 'critical_factors': ['salinity_management']},
                            'bulb_development': {'weeks_after_transplanting': 12, 'critical_factors': ['thrips_control']},
                            'maturity': {'weeks_after_transplanting': 18, 'critical_factors': ['market_timing']}
                        }
                    }
                },
                'variety_recommendations': {
                    'red': ['Nasarpuri', 'Desi Red', 'Red Swat'],
                    'white': ['White Swat', 'Phulkara'],
                    'yellow': ['TG-1', 'Surkh-1']
                }
            }
        }
        
        # Critical farming periods requiring special attention
        self.critical_periods = {
            'wheat_sowing': {
                'period': 'November 15 - December 15',
                'regions': ['Punjab_Plains', 'Sindh_Plains'],
                'critical_factors': ['soil_preparation', 'seed_quality', 'irrigation_scheduling'],
                'weather_requirements': ['temperature_15_25C', 'soil_moisture_adequate']
            },
            'rice_transplanting': {
                'period': 'June 15 - July 15',
                'regions': ['Punjab_Plains', 'Sindh_Plains'],
                'critical_factors': ['water_availability', 'seedling_quality', 'pest_control'],
                'weather_requirements': ['monsoon_arrival', 'temperature_25_35C']
            },
            'cotton_sowing': {
                'period': 'April 15 - May 15',
                'regions': ['Punjab_Plains', 'Sindh_Plains'],
                'critical_factors': ['soil_temperature', 'irrigation', 'pest_monitoring'],
                'weather_requirements': ['temperature_above_20C', 'no_late_frost']
            },
            'mango_flowering': {
                'period': 'January 1 - March 31',
                'regions': ['Punjab_Plains', 'Sindh_Plains'],
                'critical_factors': ['pollination', 'disease_prevention', 'irrigation_management'],
                'weather_requirements': ['dry_weather', 'temperature_15_25C']
            }
        }
    
    def get_current_season(self, current_month: int) -> str:
        """Determine current agricultural season based on month"""
        if current_month in [11, 12, 1, 2, 3, 4]:
            return 'rabi'
        elif current_month in [4, 5, 6, 7, 8, 9, 10]:
            return 'kharif'
        elif current_month in [3, 4, 5, 6]:
            return 'zaid'
        else:
            return 'transition'
    
    def get_crop_schedule(self, crop: str, region: str) -> Dict:
        """Get detailed schedule for a specific crop in a region"""
        if crop not in self.crop_calendar:
            return {'error': f'Crop {crop} not found in calendar'}
        
        crop_data = self.crop_calendar[crop]
        
        if region not in crop_data.get('regional_schedules', {}):
            # Find the closest region or use a default
            available_regions = list(crop_data['regional_schedules'].keys())
            if not available_regions:
                return {'error': f'No regional data available for {crop}'}
            
            # Use first available region as fallback
            fallback_region = available_regions[0]
            schedule = crop_data['regional_schedules'][fallback_region].copy()
            schedule['note'] = f'Using {fallback_region} schedule as reference for {region}'
        else:
            schedule = crop_data['regional_schedules'][region]
        
        return {
            'crop': crop,
            'region': region,
            'season': crop_data['season'],
            'schedule': schedule,
            'varieties': crop_data.get('variety_recommendations', {}),
            'current_month_activity': self._get_current_activity(crop, region, datetime.now().month)
        }
    
    def _get_current_activity(self, crop: str, region: str, current_month: int) -> Dict:
        """Determine what farming activity should be happening now"""
        if crop not in self.crop_calendar:
            return {'activity': 'unknown', 'description': 'Crop not in calendar'}
        
        crop_data = self.crop_calendar[crop]
        regional_schedule = crop_data['regional_schedules'].get(region, {})
        
        activities = []
        
        # Check all schedule items for current month
        for activity_name, activity_data in regional_schedule.items():
            if 'start_month' in activity_data and 'end_month' in activity_data:
                start_month = activity_data['start_month']
                end_month = activity_data['end_month']
                
                # Handle year-wrap scenarios
                if start_month <= end_month:
                    if start_month <= current_month <= end_month:
                        activities.append({
                            'activity': activity_name,
                            'timing': f"Month {current_month}",
                            'optimal_weeks': activity_data.get('optimal_weeks', []),
                            'description': f"{activity_name.replace('_', ' ').title()} period for {crop}"
                        })
                else:  # Wraps around year (e.g., Nov-Apr)
                    if current_month >= start_month or current_month <= end_month:
                        activities.append({
                            'activity': activity_name,
                            'timing': f"Month {current_month}",
                            'optimal_weeks': activity_data.get('optimal_weeks', []),
                            'description': f"{activity_name.replace('_', ' ').title()} period for {crop}"
                        })
        
        if not activities:
            return {
                'activity': 'maintenance',
                'description': f'General farm maintenance period for {crop}',
                'recommendations': ['Monitor for pests and diseases', 'Maintain irrigation systems', 'Plan for next season']
            }
        
        return {
            'current_activities': activities,
            'recommendations': self._get_activity_recommendations(crop, activities)
        }
    
    def _get_activity_recommendations(self, crop: str, activities: List[Dict]) -> List[str]:
        """Get specific recommendations based on current activities"""
        recommendations = []
        
        for activity in activities:
            activity_name = activity['activity']
            
            if 'sowing' in activity_name or 'planting' in activity_name:
                recommendations.extend([
                    f"Ensure soil preparation is complete for {crop}",
                    "Check weather forecast for optimal sowing window",
                    "Verify seed quality and treatment",
                    "Prepare irrigation system"
                ])
            elif 'transplanting' in activity_name:
                recommendations.extend([
                    f"Prepare transplanting field for {crop}",
                    "Ensure adequate water supply",
                    "Monitor seedling health",
                    "Plan pest control measures"
                ])
            elif 'harvesting' in activity_name or 'picking' in activity_name:
                recommendations.extend([
                    f"Monitor {crop} maturity indicators",
                    "Prepare harvesting equipment",
                    "Arrange labor and storage",
                    "Check market prices for optimal selling time"
                ])
            elif 'flowering' in activity_name:
                recommendations.extend([
                    f"Monitor {crop} flowering progress",
                    "Ensure pollination conditions",
                    "Control pests and diseases",
                    "Manage irrigation carefully"
                ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def get_regional_calendar(self, region: str, month: Optional[int] = None) -> Dict:
        """Get all crop activities for a region in a specific month"""
        if month is None:
            month = datetime.now().month
        
        month_name = calendar.month_name[month]
        regional_activities = {
            'region': region,
            'month': month_name,
            'current_season': self.get_current_season(month),
            'crop_activities': {},
            'critical_periods': [],
            'regional_characteristics': self.regions.get(region, {})
        }
        
        # Get activities for each crop
        for crop in self.crop_calendar.keys():
            activity = self._get_current_activity(crop, region, month)
            if activity.get('current_activities') or activity.get('activity') != 'maintenance':
                regional_activities['crop_activities'][crop] = activity
        
        # Check for critical periods
        for period_name, period_data in self.critical_periods.items():
            if region in period_data['regions']:
                # Simple check if current month falls in critical period
                # This could be enhanced with exact date parsing
                if month in self._extract_months_from_period(period_data['period']):
                    regional_activities['critical_periods'].append({
                        'name': period_name,
                        'period': period_data['period'],
                        'critical_factors': period_data['critical_factors'],
                        'weather_requirements': period_data['weather_requirements']
                    })
        
        return regional_activities
    
    def _extract_months_from_period(self, period_string: str) -> List[int]:
        """Extract month numbers from period string (basic implementation)"""
        # This is a simplified implementation
        # In practice, you'd want more sophisticated date parsing
        month_map = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        
        months = []
        for month_name, month_num in month_map.items():
            if month_name.lower() in period_string.lower():
                months.append(month_num)
        
        return months
    
    def get_seasonal_recommendations(self, region: str, current_weather: Dict) -> Dict:
        """Get seasonal farming recommendations based on current weather"""
        current_month = datetime.now().month
        current_season = self.get_current_season(current_month)
        
        recommendations = {
            'season': current_season,
            'region': region,
            'month': calendar.month_name[current_month],
            'weather_analysis': {},
            'farming_recommendations': [],
            'priority_crops': [],
            'irrigation_advice': [],
            'pest_disease_alerts': []
        }
        
        # Analyze current weather conditions
        temp = current_weather.get('temperature', 0)
        humidity = current_weather.get('humidity', 0)
        precipitation = current_weather.get('precipitation', 0)
        
        recommendations['weather_analysis'] = {
            'temperature_status': self._assess_temperature(temp, current_season),
            'humidity_status': self._assess_humidity(humidity, current_season),
            'precipitation_status': self._assess_precipitation(precipitation, current_season)
        }
        
        # Season-specific recommendations
        if current_season == 'rabi':
            recommendations['farming_recommendations'].extend([
                "Monitor wheat and other rabi crops for disease",
                "Ensure adequate irrigation for winter crops",
                "Prepare for spring harvest activities",
                "Plan summer crop preparations"
            ])
            recommendations['priority_crops'] = ['wheat', 'onion', 'peas', 'mustard']
            
        elif current_season == 'kharif':
            recommendations['farming_recommendations'].extend([
                "Monitor rice and cotton for pests",
                "Ensure drainage in fields during monsoon",
                "Prepare for autumn harvest",
                "Plan winter crop preparations"
            ])
            recommendations['priority_crops'] = ['rice', 'cotton', 'sugarcane', 'maize']
            
        elif current_season == 'zaid':
            recommendations['farming_recommendations'].extend([
                "Focus on water management for spring crops",
                "Monitor for heat stress in crops",
                "Prepare summer irrigation schedules",
                "Plan monsoon crop activities"
            ])
            recommendations['priority_crops'] = ['maize', 'fodder', 'vegetables']
        
        # Weather-specific advice
        if temp > 35:
            recommendations['irrigation_advice'].append("Increase irrigation frequency due to high temperature")
        elif temp < 5:
            recommendations['farming_recommendations'].append("Protect crops from frost damage")
        
        if humidity > 80:
            recommendations['pest_disease_alerts'].append("High humidity - monitor for fungal diseases")
        elif humidity < 30:
            recommendations['irrigation_advice'].append("Low humidity - ensure adequate soil moisture")
        
        if precipitation > 50:
            recommendations['farming_recommendations'].append("Ensure field drainage to prevent waterlogging")
        elif precipitation < 5:
            recommendations['irrigation_advice'].append("Low rainfall - plan supplemental irrigation")
        
        return recommendations
    
    def _assess_temperature(self, temp: float, season: str) -> str:
        """Assess if temperature is optimal for the season"""
        if season == 'rabi':
            if 15 <= temp <= 25:
                return "Optimal for rabi crops"
            elif temp > 25:
                return "High for rabi season - may stress winter crops"
            else:
                return "Low temperature - monitor for frost risk"
        elif season == 'kharif':
            if 25 <= temp <= 35:
                return "Optimal for kharif crops"
            elif temp > 35:
                return "High temperature - ensure adequate irrigation"
            else:
                return "Cool for kharif season"
        else:
            return "Transitional temperature"
    
    def _assess_humidity(self, humidity: float, season: str) -> str:
        """Assess humidity levels for farming"""
        if humidity > 80:
            return "High humidity - disease risk elevated"
        elif humidity < 30:
            return "Low humidity - increase irrigation attention"
        elif 50 <= humidity <= 70:
            return "Optimal humidity for most crops"
        else:
            return "Moderate humidity levels"
    
    def _assess_precipitation(self, precipitation: float, season: str) -> str:
        """Assess precipitation for seasonal farming"""
        if season == 'kharif' and precipitation > 100:
            return "Heavy monsoon - ensure field drainage"
        elif season == 'rabi' and precipitation > 50:
            return "Unexpected high rainfall for rabi season"
        elif precipitation < 10:
            return "Low precipitation - irrigation planning needed"
        else:
            return "Adequate precipitation levels"
    
    def get_crop_calendar_summary(self) -> Dict:
        """Get a summary of all crops and their seasons"""
        summary = {
            'total_crops': len(self.crop_calendar),
            'by_season': {'rabi': [], 'kharif': [], 'both': [], 'perennial': []},
            'critical_periods_count': len(self.critical_periods),
            'regions_covered': list(self.regions.keys())
        }
        
        for crop, data in self.crop_calendar.items():
            season = data['season']
            if season in summary['by_season']:
                summary['by_season'][season].append(crop)
            else:
                summary['by_season']['other'] = summary['by_season'].get('other', [])
                summary['by_season']['other'].append(crop)
        
        return summary