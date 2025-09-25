"""
Multi-Crop Analysis System
Supports simultaneous analysis of different agricultural products for comparison and planning
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json

class MultiCropAnalyzer:
    def __init__(self, crop_db, soil_db, farming_calendar):
        """Initialize multi-crop analyzer with dependencies"""
        self.crop_db = crop_db
        self.soil_db = soil_db
        self.farming_calendar = farming_calendar
        
        # Crop rotation compatibility matrix
        self.rotation_compatibility = {
            'wheat': {
                'excellent': ['cotton', 'rice', 'sugarcane'],
                'good': ['maize', 'onion'],
                'fair': ['mango'],
                'poor': ['wheat']  # Avoid continuous wheat
            },
            'cotton': {
                'excellent': ['wheat', 'onion'],
                'good': ['maize', 'sugarcane'],
                'fair': ['rice'],
                'poor': ['cotton', 'mango']
            },
            'rice': {
                'excellent': ['wheat', 'onion'],
                'good': ['cotton', 'maize'],
                'fair': ['sugarcane'],
                'poor': ['rice', 'mango']
            },
            'maize': {
                'excellent': ['wheat', 'cotton', 'onion'],
                'good': ['rice', 'sugarcane'],
                'fair': ['mango'],
                'poor': ['maize']
            },
            'sugarcane': {
                'excellent': [],  # Perennial crop
                'good': ['wheat', 'cotton'],
                'fair': ['rice', 'maize'],
                'poor': ['onion', 'mango']
            },
            'mango': {
                'excellent': [],  # Perennial orchard crop
                'good': [],
                'fair': ['wheat', 'cotton', 'rice', 'maize'],
                'poor': ['onion', 'sugarcane']
            },
            'onion': {
                'excellent': ['wheat', 'cotton', 'rice', 'maize'],
                'good': [],
                'fair': [],
                'poor': ['onion', 'sugarcane', 'mango']
            }
        }
        
        # Economic scoring factors
        self.economic_factors = {
            'market_demand': {
                'wheat': 95,  # Staple food, high demand
                'rice': 90,   # Staple food, export potential
                'cotton': 85, # Textile industry, variable prices
                'sugarcane': 80, # Sugar industry demand
                'maize': 75,  # Animal feed, poultry
                'mango': 88,  # Export fruit, seasonal
                'onion': 82   # Daily vegetable, storage issues
            },
            'price_stability': {
                'wheat': 85,  # Government support, stable
                'rice': 80,   # Export dependent
                'cotton': 60, # Highly volatile
                'sugarcane': 90, # Contract farming
                'maize': 70,  # Feed demand stable
                'mango': 65,  # Weather/season dependent
                'onion': 50   # Highly volatile
            },
            'input_cost': {  # Lower is better (inverted for scoring)
                'wheat': 30,  # Moderate input costs
                'rice': 45,   # High water, labor costs
                'cotton': 55, # High pesticide, fertilizer
                'sugarcane': 40, # High initial, then low
                'maize': 25,  # Lower input requirements
                'mango': 35,  # Initial high, then moderate
                'onion': 40   # Moderate inputs
            },
            'labor_intensity': {  # Lower is better (inverted for scoring)
                'wheat': 25,  # Mechanized, low labor
                'rice': 50,   # High labor for transplanting
                'cotton': 45, # Manual picking intensive
                'sugarcane': 35, # Seasonal labor peaks
                'maize': 20,  # Highly mechanized
                'mango': 30,  # Seasonal pruning, harvesting
                'onion': 40   # Manual transplanting, harvesting
            }
        }
        
        # Risk assessment factors
        self.risk_factors = {
            'weather_sensitivity': {
                'wheat': 60,  # Moderate, some heat tolerance
                'rice': 40,   # Monsoon dependent
                'cotton': 50, # Heat tolerant, pest issues
                'sugarcane': 70, # Hardy crop
                'maize': 45,  # Drought sensitive
                'mango': 30,  # Weather dependent flowering
                'onion': 55   # Moderate weather tolerance
            },
            'pest_disease_risk': {
                'wheat': 70,  # Moderate disease pressure
                'rice': 60,   # Stem borer, blast issues
                'cotton': 30, # High bollworm pressure
                'sugarcane': 75, # Generally hardy
                'maize': 65,  # Stem borer issues
                'mango': 50,  # Seasonal pest issues
                'onion': 60   # Thrips, disease issues
            },
            'market_risk': {
                'wheat': 80,  # Government procurement
                'rice': 75,   # Export opportunities
                'cotton': 40, # Price volatility
                'sugarcane': 85, # Contract system
                'maize': 70,  # Steady feed demand
                'mango': 50,  # Export dependent
                'onion': 35   # High price volatility
            }
        }
    
    def analyze_multiple_crops(self, crops: List[str], region: str, weather_data: Dict, 
                              analysis_type: str = 'comparative') -> Dict:
        """Analyze multiple crops simultaneously for comparison"""
        
        if len(crops) < 2:
            return {'error': 'At least 2 crops required for multi-crop analysis'}
        
        results = {
            'analysis_type': analysis_type,
            'crops_analyzed': crops,
            'region': region,
            'analysis_date': datetime.now().isoformat(),
            'individual_analyses': {},
            'comparative_analysis': {},
            'recommendations': {}
        }
        
        # Individual crop analyses
        for crop in crops:
            results['individual_analyses'][crop] = self._analyze_single_crop(
                crop, region, weather_data
            )
        
        # Comparative analysis
        if analysis_type in ['comparative', 'all']:
            results['comparative_analysis'] = self._perform_comparative_analysis(
                crops, results['individual_analyses'], region, weather_data
            )
        
        # Rotation analysis
        if analysis_type in ['rotation', 'all'] and len(crops) <= 4:
            results['rotation_analysis'] = self._analyze_crop_rotation(
                crops, region, weather_data
            )
        
        # Mixed farming analysis
        if analysis_type in ['mixed', 'all'] and len(crops) <= 3:
            results['mixed_farming'] = self._analyze_mixed_farming(
                crops, region, weather_data
            )
        
        # Generate recommendations
        results['recommendations'] = self._generate_multi_crop_recommendations(
            crops, results['individual_analyses'], results['comparative_analysis']
        )
        
        return results
    
    def _analyze_single_crop(self, crop: str, region: str, weather_data: Dict) -> Dict:
        """Perform detailed analysis for a single crop"""
        analysis = {
            'crop': crop,
            'region': region,
            'basic_info': {},
            'suitability_scores': {},
            'economic_analysis': {},
            'risk_assessment': {},
            'timing_analysis': {}
        }
        
        # Get basic crop information
        crop_info = self.crop_db.get_crop_info(crop)
        if crop_info:
            analysis['basic_info'] = {
                'optimal_temp_range': crop_info.get('optimal_temperature', {}),
                'growth_period': crop_info.get('growth_stages', {}),
                'water_requirements': crop_info.get('water_requirements', 'moderate'),
                'soil_preferences': crop_info.get('soil_requirements', {})
            }
        
        # Soil-crop compatibility
        if region in self.soil_db.regional_mapping:
            soil_compatibility = self.soil_db.get_crop_soil_compatibility(crop, region)
            analysis['suitability_scores']['soil'] = soil_compatibility.get('suitability_score', 50)
        else:
            analysis['suitability_scores']['soil'] = 60  # Default moderate score
        
        # Weather suitability
        current_weather = weather_data.get('current', {})
        if current_weather:
            weather_score = self._calculate_weather_suitability(crop, current_weather)
            analysis['suitability_scores']['weather'] = weather_score
        
        # Economic analysis
        analysis['economic_analysis'] = {
            'market_demand_score': self.economic_factors['market_demand'].get(crop, 60),
            'price_stability_score': self.economic_factors['price_stability'].get(crop, 50),
            'input_cost_score': 100 - self.economic_factors['input_cost'].get(crop, 50),  # Inverted
            'labor_requirement_score': 100 - self.economic_factors['labor_intensity'].get(crop, 50)  # Inverted
        }
        
        # Risk assessment
        analysis['risk_assessment'] = {
            'weather_risk_score': self.risk_factors['weather_sensitivity'].get(crop, 50),
            'pest_disease_score': self.risk_factors['pest_disease_risk'].get(crop, 50),
            'market_risk_score': self.risk_factors['market_risk'].get(crop, 50)
        }
        
        # Timing analysis using farming calendar
        crop_schedule = self.farming_calendar.get_crop_schedule(crop, region)
        if 'error' not in crop_schedule:
            analysis['timing_analysis'] = {
                'season': crop_schedule.get('season', 'unknown'),
                'current_activity': crop_schedule.get('current_month_activity', {}),
                'schedule_summary': self._summarize_crop_schedule(crop_schedule.get('schedule', {}))
            }
        
        # Calculate overall suitability score
        analysis['overall_suitability'] = self._calculate_overall_suitability(analysis)
        
        return analysis
    
    def _calculate_weather_suitability(self, crop: str, current_weather: Dict) -> float:
        """Calculate how suitable current weather is for the crop"""
        score = 50  # Base score
        
        temp = current_weather.get('temperature', 25)
        humidity = current_weather.get('humidity', 60)
        precipitation = current_weather.get('precipitation', 0)
        
        # Get crop optimal temperature range
        crop_info = self.crop_db.get_crop_info(crop)
        if crop_info and 'optimal_temperature' in crop_info:
            temp_range = crop_info['optimal_temperature']
            min_temp = temp_range.get('min', 15)
            max_temp = temp_range.get('max', 35)
            
            if min_temp <= temp <= max_temp:
                score += 30  # Optimal temperature
            elif abs(temp - min_temp) <= 5 or abs(temp - max_temp) <= 5:
                score += 15  # Near optimal
            elif temp < min_temp - 10 or temp > max_temp + 10:
                score -= 20  # Poor temperature
        
        # Humidity assessment (crop-specific)
        if crop in ['rice', 'sugarcane'] and humidity > 70:
            score += 10  # High humidity crops
        elif crop in ['wheat', 'onion'] and 40 <= humidity <= 70:
            score += 10  # Moderate humidity crops
        elif crop in ['cotton', 'maize'] and humidity < 80:
            score += 5   # Heat tolerant crops
        
        # Precipitation assessment
        if crop == 'rice' and precipitation > 10:
            score += 15  # Rice needs water
        elif crop in ['wheat', 'cotton'] and 2 <= precipitation <= 10:
            score += 10  # Moderate water needs
        elif precipitation > 30:
            score -= 10  # Excessive rain can harm most crops
        
        return max(0, min(100, score))
    
    def _calculate_overall_suitability(self, analysis: Dict) -> float:
        """Calculate overall suitability score for a crop"""
        weights = {
            'soil': 0.25,
            'weather': 0.20,
            'economic': 0.30,
            'risk': 0.25
        }
        
        soil_score = analysis['suitability_scores'].get('soil', 50)
        weather_score = analysis['suitability_scores'].get('weather', 50)
        
        # Economic score (average of economic factors)
        econ_analysis = analysis['economic_analysis']
        economic_score = sum(econ_analysis.values()) / len(econ_analysis) if econ_analysis else 50
        
        # Risk score (average, higher is better)
        risk_analysis = analysis['risk_assessment']
        risk_score = sum(risk_analysis.values()) / len(risk_analysis) if risk_analysis else 50
        
        overall = (
            soil_score * weights['soil'] +
            weather_score * weights['weather'] +
            economic_score * weights['economic'] +
            risk_score * weights['risk']
        )
        
        return round(overall, 1)
    
    def _summarize_crop_schedule(self, schedule: Dict) -> Dict:
        """Summarize crop schedule for analysis"""
        summary = {}
        
        for activity, timing in schedule.items():
            if isinstance(timing, dict) and 'start_month' in timing:
                start_month = timing['start_month']
                end_month = timing['end_month']
                summary[activity] = {
                    'start_month': start_month,
                    'end_month': end_month,
                    'duration_months': self._calculate_duration_months(start_month, end_month)
                }
        
        return summary
    
    def _calculate_duration_months(self, start_month: int, end_month: int) -> int:
        """Calculate duration in months handling year wrap"""
        if start_month <= end_month:
            return end_month - start_month + 1
        else:
            return (12 - start_month + 1) + end_month
    
    def _perform_comparative_analysis(self, crops: List[str], individual_analyses: Dict, 
                                    region: str, weather_data: Dict) -> Dict:
        """Compare multiple crops across various dimensions"""
        comparison = {
            'ranking': {},
            'strengths_weaknesses': {},
            'profitability_comparison': {},
            'resource_comparison': {},
            'timing_comparison': {}
        }
        
        # Overall ranking by suitability
        crop_scores = {}
        for crop in crops:
            if crop in individual_analyses:
                crop_scores[crop] = individual_analyses[crop].get('overall_suitability', 0)
        
        sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
        comparison['ranking'] = {
            'by_suitability': sorted_crops,
            'recommendations': self._generate_ranking_recommendations(sorted_crops)
        }
        
        # Strengths and weaknesses comparison
        for crop in crops:
            if crop in individual_analyses:
                analysis = individual_analyses[crop]
                comparison['strengths_weaknesses'][crop] = self._identify_crop_strengths_weaknesses(
                    crop, analysis
                )
        
        # Profitability comparison
        comparison['profitability_comparison'] = self._compare_profitability(crops, individual_analyses)
        
        # Resource requirements comparison
        comparison['resource_comparison'] = self._compare_resource_requirements(crops, individual_analyses)
        
        # Timing comparison
        comparison['timing_comparison'] = self._compare_timing_requirements(crops, individual_analyses)
        
        return comparison
    
    def _identify_crop_strengths_weaknesses(self, crop: str, analysis: Dict) -> Dict:
        """Identify strengths and weaknesses of a crop"""
        strengths = []
        weaknesses = []
        
        # Soil suitability
        soil_score = analysis['suitability_scores'].get('soil', 50)
        if soil_score >= 75:
            strengths.append(f"Excellent soil compatibility ({soil_score}%)")
        elif soil_score <= 40:
            weaknesses.append(f"Poor soil compatibility ({soil_score}%)")
        
        # Economic factors
        econ = analysis['economic_analysis']
        if econ.get('market_demand_score', 0) >= 85:
            strengths.append("High market demand")
        if econ.get('price_stability_score', 0) >= 80:
            strengths.append("Stable pricing")
        if econ.get('input_cost_score', 0) >= 70:
            strengths.append("Low input costs")
        if econ.get('labor_requirement_score', 0) >= 70:
            strengths.append("Low labor requirements")
        
        # Risk factors
        risk = analysis['risk_assessment']
        if risk.get('weather_risk_score', 0) >= 70:
            strengths.append("Weather resilient")
        if risk.get('pest_disease_score', 0) >= 70:
            strengths.append("Pest/disease resistant")
        if risk.get('market_risk_score', 0) >= 75:
            strengths.append("Market stability")
        
        # Identify weaknesses (opposite conditions)
        if econ.get('market_demand_score', 0) <= 60:
            weaknesses.append("Limited market demand")
        if econ.get('price_stability_score', 0) <= 50:
            weaknesses.append("Price volatility")
        if risk.get('weather_risk_score', 0) <= 45:
            weaknesses.append("Weather sensitive")
        if risk.get('pest_disease_score', 0) <= 45:
            weaknesses.append("High pest/disease pressure")
        
        return {'strengths': strengths, 'weaknesses': weaknesses}
    
    def _compare_profitability(self, crops: List[str], individual_analyses: Dict) -> Dict:
        """Compare profitability potential across crops"""
        profitability = {}
        
        for crop in crops:
            if crop in individual_analyses:
                econ = individual_analyses[crop]['economic_analysis']
                
                # Calculate profitability score
                profit_score = (
                    econ.get('market_demand_score', 50) * 0.3 +
                    econ.get('price_stability_score', 50) * 0.2 +
                    econ.get('input_cost_score', 50) * 0.3 +
                    econ.get('labor_requirement_score', 50) * 0.2
                )
                
                profitability[crop] = {
                    'profit_score': round(profit_score, 1),
                    'market_demand': econ.get('market_demand_score', 50),
                    'price_stability': econ.get('price_stability_score', 50),
                    'cost_efficiency': econ.get('input_cost_score', 50),
                    'labor_efficiency': econ.get('labor_requirement_score', 50)
                }
        
        # Rank by profitability
        ranked = sorted(profitability.items(), key=lambda x: x[1]['profit_score'], reverse=True)
        
        return {
            'individual_scores': profitability,
            'ranking': ranked,
            'most_profitable': ranked[0] if ranked else None,
            'profit_leader_advantage': ranked[0][1]['profit_score'] - ranked[1][1]['profit_score'] if len(ranked) > 1 else 0
        }
    
    def _compare_resource_requirements(self, crops: List[str], individual_analyses: Dict) -> Dict:
        """Compare resource requirements across crops"""
        resource_comparison = {
            'water_requirements': {},
            'labor_intensity': {},
            'land_utilization': {},
            'input_costs': {}
        }
        
        for crop in crops:
            if crop in individual_analyses:
                analysis = individual_analyses[crop]
                econ = analysis['economic_analysis']
                basic_info = analysis['basic_info']
                
                # Water requirements
                water_req = basic_info.get('water_requirements', 'moderate')
                resource_comparison['water_requirements'][crop] = water_req
                
                # Labor intensity (lower score means higher intensity)
                labor_score = econ.get('labor_requirement_score', 50)
                if labor_score >= 70:
                    resource_comparison['labor_intensity'][crop] = 'low'
                elif labor_score >= 50:
                    resource_comparison['labor_intensity'][crop] = 'moderate'
                else:
                    resource_comparison['labor_intensity'][crop] = 'high'
                
                # Input costs (higher score means lower costs)
                cost_score = econ.get('input_cost_score', 50)
                if cost_score >= 70:
                    resource_comparison['input_costs'][crop] = 'low'
                elif cost_score >= 50:
                    resource_comparison['input_costs'][crop] = 'moderate'
                else:
                    resource_comparison['input_costs'][crop] = 'high'
        
        return resource_comparison
    
    def _compare_timing_requirements(self, crops: List[str], individual_analyses: Dict) -> Dict:
        """Compare timing and scheduling requirements"""
        timing_comparison = {
            'seasonal_distribution': {},
            'conflict_analysis': {},
            'complementary_crops': []
        }
        
        seasonal_crops = {'rabi': [], 'kharif': [], 'both': [], 'perennial': []}
        
        for crop in crops:
            if crop in individual_analyses:
                timing = individual_analyses[crop].get('timing_analysis', {})
                season = timing.get('season', 'unknown')
                
                if season in seasonal_crops:
                    seasonal_crops[season].append(crop)
                else:
                    seasonal_crops['unknown'] = seasonal_crops.get('unknown', [])
                    seasonal_crops['unknown'].append(crop)
        
        timing_comparison['seasonal_distribution'] = seasonal_crops
        
        # Identify potential conflicts (same season crops)
        conflicts = []
        for season, season_crops in seasonal_crops.items():
            if len(season_crops) > 1 and season != 'both':
                conflicts.append({
                    'season': season,
                    'conflicting_crops': season_crops,
                    'conflict_level': 'high' if season in ['rabi', 'kharif'] else 'moderate'
                })
        
        timing_comparison['conflict_analysis'] = conflicts
        
        # Identify complementary crops (different seasons)
        if seasonal_crops['rabi'] and seasonal_crops['kharif']:
            timing_comparison['complementary_crops'] = {
                'rabi_kharif_rotation': {
                    'rabi_crops': seasonal_crops['rabi'],
                    'kharif_crops': seasonal_crops['kharif'],
                    'rotation_potential': 'excellent'
                }
            }
        
        return timing_comparison
    
    def _analyze_crop_rotation(self, crops: List[str], region: str, weather_data: Dict) -> Dict:
        """Analyze crop rotation possibilities and benefits"""
        if len(crops) < 2:
            return {'error': 'At least 2 crops required for rotation analysis'}
        
        rotation_analysis = {
            'compatibility_matrix': {},
            'rotation_sequences': [],
            'benefits_analysis': {},
            'recommended_rotations': []
        }
        
        # Build compatibility matrix
        for crop1 in crops:
            rotation_analysis['compatibility_matrix'][crop1] = {}
            for crop2 in crops:
                if crop1 != crop2:
                    compatibility = self._get_rotation_compatibility(crop1, crop2)
                    rotation_analysis['compatibility_matrix'][crop1][crop2] = compatibility
        
        # Generate possible rotation sequences
        rotation_sequences = self._generate_rotation_sequences(crops)
        rotation_analysis['rotation_sequences'] = rotation_sequences
        
        # Analyze benefits of each rotation
        for sequence in rotation_sequences:
            benefits = self._analyze_rotation_benefits(sequence, region)
            rotation_analysis['benefits_analysis']['-'.join(sequence)] = benefits
        
        # Recommend best rotations
        rotation_analysis['recommended_rotations'] = self._recommend_best_rotations(
            rotation_analysis['benefits_analysis']
        )
        
        return rotation_analysis
    
    def _get_rotation_compatibility(self, crop1: str, crop2: str) -> Dict:
        """Get compatibility rating for crop rotation"""
        compatibility_data = self.rotation_compatibility.get(crop1, {})
        
        for level, compatible_crops in compatibility_data.items():
            if crop2 in compatible_crops:
                return {
                    'level': level,
                    'score': {'excellent': 90, 'good': 75, 'fair': 60, 'poor': 30}.get(level, 50),
                    'reason': self._get_compatibility_reason(crop1, crop2, level)
                }
        
        return {
            'level': 'unknown',
            'score': 50,
            'reason': 'No specific compatibility data available'
        }
    
    def _get_compatibility_reason(self, crop1: str, crop2: str, level: str) -> str:
        """Get reason for compatibility rating"""
        reasons = {
            'excellent': f"{crop2} provides excellent soil benefits after {crop1}",
            'good': f"{crop2} is a good choice after {crop1} with some benefits",
            'fair': f"{crop2} can follow {crop1} but with limited benefits",
            'poor': f"{crop2} not recommended after {crop1} due to potential issues"
        }
        return reasons.get(level, "Standard rotation compatibility")
    
    def _generate_rotation_sequences(self, crops: List[str]) -> List[List[str]]:
        """Generate possible rotation sequences"""
        from itertools import permutations
        
        sequences = []
        
        # 2-crop rotations
        for perm in permutations(crops, 2):
            sequences.append(list(perm))
        
        # 3-crop rotations (if enough crops)
        if len(crops) >= 3:
            for perm in permutations(crops, 3):
                sequences.append(list(perm))
        
        return sequences[:10]  # Limit to top 10 sequences
    
    def _analyze_rotation_benefits(self, sequence: List[str], region: str) -> Dict:
        """Analyze benefits of a specific rotation sequence"""
        benefits = {
            'soil_health_score': 0,
            'pest_disease_control': 0,
            'economic_benefits': 0,
            'resource_efficiency': 0,
            'overall_score': 0,
            'specific_benefits': []
        }
        
        # Calculate rotation benefits
        compatibility_scores = []
        for i in range(len(sequence) - 1):
            crop1, crop2 = sequence[i], sequence[i + 1]
            compat = self._get_rotation_compatibility(crop1, crop2)
            compatibility_scores.append(compat['score'])
        
        # Average compatibility score
        if compatibility_scores:
            benefits['soil_health_score'] = sum(compatibility_scores) / len(compatibility_scores)
        
        # Pest and disease control benefits
        if len(set(sequence)) == len(sequence):  # All different crops
            benefits['pest_disease_control'] = 80
            benefits['specific_benefits'].append("Breaks pest and disease cycles")
        else:
            benefits['pest_disease_control'] = 40
        
        # Economic diversity benefits
        profit_variance = self._calculate_profit_variance(sequence)
        benefits['economic_benefits'] = max(0, 100 - profit_variance)
        
        # Resource efficiency
        resource_efficiency = self._calculate_resource_efficiency(sequence)
        benefits['resource_efficiency'] = resource_efficiency
        
        # Overall score
        benefits['overall_score'] = (
            benefits['soil_health_score'] * 0.3 +
            benefits['pest_disease_control'] * 0.25 +
            benefits['economic_benefits'] * 0.25 +
            benefits['resource_efficiency'] * 0.2
        )
        
        return benefits
    
    def _calculate_profit_variance(self, sequence: List[str]) -> float:
        """Calculate profit variance in rotation (lower is better for risk)"""
        # Simplified calculation based on price stability
        price_stabilities = []
        for crop in sequence:
            stability = self.economic_factors['price_stability'].get(crop, 50)
            price_stabilities.append(stability)
        
        if len(price_stabilities) <= 1:
            return 0
        
        # Calculate variance
        mean_stability = sum(price_stabilities) / len(price_stabilities)
        variance = sum((x - mean_stability) ** 2 for x in price_stabilities) / len(price_stabilities)
        
        return min(100, variance)  # Cap at 100
    
    def _calculate_resource_efficiency(self, sequence: List[str]) -> float:
        """Calculate resource efficiency of rotation"""
        # Check for complementary resource usage
        efficiency_score = 50  # Base score
        
        # Different seasons use land efficiently
        seasons = set()
        for crop in sequence:
            crop_schedule = self.farming_calendar.get_crop_schedule(crop, 'Punjab_Plains')  # Default region
            if 'error' not in crop_schedule:
                seasons.add(crop_schedule.get('season', 'unknown'))
        
        if len(seasons) > 1:
            efficiency_score += 20  # Bonus for seasonal diversity
        
        # Different water requirements
        water_reqs = set()
        for crop in sequence:
            crop_info = self.crop_db.get_crop_info(crop)
            if crop_info:
                water_req = crop_info.get('water_requirements', 'moderate')
                water_reqs.add(water_req)
        
        if len(water_reqs) > 1:
            efficiency_score += 15  # Bonus for water diversity
        
        return min(100, efficiency_score)
    
    def _recommend_best_rotations(self, benefits_analysis: Dict) -> List[Dict]:
        """Recommend the best rotation sequences"""
        if not benefits_analysis:
            return []
        
        # Sort by overall score
        sorted_rotations = sorted(
            benefits_analysis.items(),
            key=lambda x: x[1]['overall_score'],
            reverse=True
        )
        
        recommendations = []
        for rotation_name, benefits in sorted_rotations[:3]:  # Top 3
            recommendations.append({
                'sequence': rotation_name.split('-'),
                'overall_score': benefits['overall_score'],
                'key_benefits': benefits['specific_benefits'],
                'recommendation_level': self._get_recommendation_level(benefits['overall_score'])
            })
        
        return recommendations
    
    def _get_recommendation_level(self, score: float) -> str:
        """Get recommendation level based on score"""
        if score >= 80:
            return 'highly_recommended'
        elif score >= 65:
            return 'recommended'
        elif score >= 50:
            return 'acceptable'
        else:
            return 'not_recommended'
    
    def _analyze_mixed_farming(self, crops: List[str], region: str, weather_data: Dict) -> Dict:
        """Analyze mixed farming possibilities"""
        mixed_analysis = {
            'compatibility_assessment': {},
            'space_utilization': {},
            'resource_sharing': {},
            'risk_diversification': {},
            'recommended_combinations': []
        }
        
        # Assess compatibility for mixed farming
        for i, crop1 in enumerate(crops):
            for crop2 in crops[i+1:]:
                compatibility = self._assess_mixed_farming_compatibility(crop1, crop2)
                mixed_analysis['compatibility_assessment'][f"{crop1}-{crop2}"] = compatibility
        
        # Analyze space utilization
        mixed_analysis['space_utilization'] = self._analyze_space_utilization(crops)
        
        # Resource sharing analysis
        mixed_analysis['resource_sharing'] = self._analyze_resource_sharing(crops)
        
        # Risk diversification
        mixed_analysis['risk_diversification'] = self._analyze_risk_diversification(crops)
        
        # Generate recommendations
        mixed_analysis['recommended_combinations'] = self._recommend_mixed_combinations(
            mixed_analysis['compatibility_assessment']
        )
        
        return mixed_analysis
    
    def _assess_mixed_farming_compatibility(self, crop1: str, crop2: str) -> Dict:
        """Assess if two crops can be grown together"""
        compatibility = {
            'spatial_compatibility': 50,
            'resource_compatibility': 50,
            'growth_compatibility': 50,
            'overall_compatibility': 50,
            'benefits': [],
            'challenges': []
        }
        
        # Spatial compatibility (tree crops vs field crops)
        if crop1 == 'mango' or crop2 == 'mango':
            if crop1 != crop2:  # One is mango, other is not
                compatibility['spatial_compatibility'] = 70
                compatibility['benefits'].append("Orchard intercropping possible")
            else:
                compatibility['spatial_compatibility'] = 30
                compatibility['challenges'].append("Both are tree crops")
        
        # Different growth heights/patterns
        height_crops = {'mango': 'tree', 'sugarcane': 'tall', 'wheat': 'short', 
                       'rice': 'medium', 'cotton': 'medium', 'maize': 'tall', 'onion': 'short'}
        
        height1 = height_crops.get(crop1, 'medium')
        height2 = height_crops.get(crop2, 'medium')
        
        if height1 != height2:
            compatibility['spatial_compatibility'] += 15
            compatibility['benefits'].append("Different growth heights complement each other")
        
        # Resource compatibility
        crop1_info = self.crop_db.get_crop_info(crop1)
        crop2_info = self.crop_db.get_crop_info(crop2)
        
        if crop1_info and crop2_info:
            water1 = crop1_info.get('water_requirements', 'moderate')
            water2 = crop2_info.get('water_requirements', 'moderate')
            
            if water1 == water2:
                compatibility['resource_compatibility'] = 70
                compatibility['benefits'].append("Similar water requirements")
            else:
                compatibility['resource_compatibility'] = 40
                compatibility['challenges'].append("Different water needs")
        
        # Calculate overall compatibility
        compatibility['overall_compatibility'] = (
            compatibility['spatial_compatibility'] * 0.4 +
            compatibility['resource_compatibility'] * 0.4 +
            compatibility['growth_compatibility'] * 0.2
        )
        
        return compatibility
    
    def _analyze_space_utilization(self, crops: List[str]) -> Dict:
        """Analyze space utilization in mixed farming"""
        utilization = {
            'vertical_space_usage': {},
            'horizontal_space_efficiency': 0,
            'recommendations': []
        }
        
        # Categorize crops by space usage
        space_categories = {
            'ground_cover': ['onion', 'wheat'],
            'medium_height': ['rice', 'cotton'],
            'tall_crops': ['maize', 'sugarcane'],
            'tree_layer': ['mango']
        }
        
        crop_layers = {}
        for crop in crops:
            for layer, layer_crops in space_categories.items():
                if crop in layer_crops:
                    crop_layers[crop] = layer
                    break
        
        utilization['vertical_space_usage'] = crop_layers
        
        # Calculate efficiency
        unique_layers = len(set(crop_layers.values()))
        utilization['horizontal_space_efficiency'] = min(100, unique_layers * 25)
        
        if unique_layers > 1:
            utilization['recommendations'].append("Good vertical space utilization possible")
        
        return utilization
    
    def _analyze_resource_sharing(self, crops: List[str]) -> Dict:
        """Analyze resource sharing potential in mixed farming"""
        sharing = {
            'water_efficiency': 0,
            'nutrient_complementarity': 0,
            'pest_control_benefits': 0,
            'overall_resource_efficiency': 0
        }
        
        # Water efficiency
        water_reqs = []
        for crop in crops:
            crop_info = self.crop_db.get_crop_info(crop)
            if crop_info:
                water_req = crop_info.get('water_requirements', 'moderate')
                water_reqs.append(water_req)
        
        if len(set(water_reqs)) == 1:  # All same water requirements
            sharing['water_efficiency'] = 80
        else:
            sharing['water_efficiency'] = 40
        
        # Pest control benefits (diversity)
        sharing['pest_control_benefits'] = min(100, len(crops) * 20)
        
        # Overall efficiency
        sharing['overall_resource_efficiency'] = (
            sharing['water_efficiency'] * 0.4 +
            sharing['nutrient_complementarity'] * 0.3 +
            sharing['pest_control_benefits'] * 0.3
        )
        
        return sharing
    
    def _analyze_risk_diversification(self, crops: List[str]) -> Dict:
        """Analyze risk diversification in mixed farming"""
        diversification = {
            'market_risk_reduction': 0,
            'weather_risk_distribution': 0,
            'pest_disease_risk_reduction': 0,
            'overall_risk_mitigation': 0
        }
        
        # Market risk reduction (different price patterns)
        price_stabilities = []
        for crop in crops:
            stability = self.economic_factors['price_stability'].get(crop, 50)
            price_stabilities.append(stability)
        
        if price_stabilities:
            diversification['market_risk_reduction'] = sum(price_stabilities) / len(price_stabilities)
        
        # Weather risk distribution
        weather_sensitivities = []
        for crop in crops:
            sensitivity = self.risk_factors['weather_sensitivity'].get(crop, 50)
            weather_sensitivities.append(sensitivity)
        
        if weather_sensitivities:
            diversification['weather_risk_distribution'] = sum(weather_sensitivities) / len(weather_sensitivities)
        
        # Pest/disease risk reduction (diversity effect)
        diversification['pest_disease_risk_reduction'] = min(100, len(crops) * 25)
        
        # Overall risk mitigation
        diversification['overall_risk_mitigation'] = (
            diversification['market_risk_reduction'] * 0.4 +
            diversification['weather_risk_distribution'] * 0.3 +
            diversification['pest_disease_risk_reduction'] * 0.3
        )
        
        return diversification
    
    def _recommend_mixed_combinations(self, compatibility_assessment: Dict) -> List[Dict]:
        """Recommend best mixed farming combinations"""
        recommendations = []
        
        for combination, assessment in compatibility_assessment.items():
            if assessment['overall_compatibility'] >= 60:  # Good compatibility threshold
                recommendations.append({
                    'combination': combination.split('-'),
                    'compatibility_score': assessment['overall_compatibility'],
                    'key_benefits': assessment['benefits'],
                    'potential_challenges': assessment['challenges'],
                    'recommendation_level': self._get_recommendation_level(assessment['overall_compatibility'])
                })
        
        # Sort by compatibility score
        recommendations.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _generate_multi_crop_recommendations(self, crops: List[str], individual_analyses: Dict, 
                                           comparative_analysis: Dict) -> Dict:
        """Generate comprehensive recommendations for multi-crop analysis"""
        recommendations = {
            'primary_recommendation': {},
            'alternative_strategies': [],
            'optimization_suggestions': [],
            'risk_mitigation': [],
            'next_steps': []
        }
        
        # Primary recommendation based on highest overall suitability
        if comparative_analysis and 'ranking' in comparative_analysis:
            ranking = comparative_analysis['ranking'].get('by_suitability', [])
            if ranking:
                best_crop, best_score = ranking[0]
                recommendations['primary_recommendation'] = {
                    'recommended_crop': best_crop,
                    'suitability_score': best_score,
                    'reason': f"{best_crop} shows highest overall suitability ({best_score}%) for current conditions",
                    'key_advantages': individual_analyses[best_crop]['economic_analysis'] if best_crop in individual_analyses else {}
                }
        
        # Alternative strategies
        if len(crops) >= 2:
            recommendations['alternative_strategies'].extend([
                "Consider crop rotation to optimize soil health and reduce pest pressure",
                "Evaluate mixed farming opportunities for risk diversification",
                "Plan seasonal crop sequencing for year-round productivity"
            ])
        
        # Optimization suggestions
        for crop in crops:
            if crop in individual_analyses:
                analysis = individual_analyses[crop]
                strengths_weaknesses = comparative_analysis.get('strengths_weaknesses', {}).get(crop, {})
                
                if strengths_weaknesses.get('weaknesses'):
                    for weakness in strengths_weaknesses['weaknesses'][:2]:  # Top 2 weaknesses
                        recommendations['optimization_suggestions'].append(
                            f"For {crop}: Address {weakness} through targeted management practices"
                        )
        
        # Risk mitigation
        recommendations['risk_mitigation'].extend([
            "Diversify crop portfolio to reduce market risk exposure",
            "Implement integrated pest management for sustainable production",
            "Monitor weather patterns for optimal timing decisions",
            "Consider crop insurance for high-value crops"
        ])
        
        # Next steps
        recommendations['next_steps'].extend([
            "Conduct detailed soil testing for optimal crop selection",
            "Consult local agricultural extension services for variety recommendations",
            "Develop detailed crop calendar with critical activity timelines",
            "Plan irrigation and input procurement schedules"
        ])
        
        return recommendations
    
    def generate_multi_crop_summary(self, analysis_results: Dict) -> Dict:
        """Generate a concise summary of multi-crop analysis"""
        summary = {
            'analysis_overview': {},
            'key_findings': [],
            'top_recommendations': [],
            'decision_matrix': {}
        }
        
        # Analysis overview
        summary['analysis_overview'] = {
            'crops_analyzed': len(analysis_results.get('crops_analyzed', [])),
            'analysis_type': analysis_results.get('analysis_type', 'comparative'),
            'region': analysis_results.get('region', 'unknown'),
            'analysis_date': analysis_results.get('analysis_date', datetime.now().isoformat())
        }
        
        # Key findings
        if 'comparative_analysis' in analysis_results:
            comp_analysis = analysis_results['comparative_analysis']
            
            # Best crop
            ranking = comp_analysis.get('ranking', {}).get('by_suitability', [])
            if ranking:
                best_crop, best_score = ranking[0]
                summary['key_findings'].append(f"{best_crop.title()} is the most suitable crop ({best_score}% suitability)")
            
            # Profitability leader
            profit_comparison = comp_analysis.get('profitability_comparison', {})
            most_profitable = profit_comparison.get('most_profitable')
            if most_profitable:
                crop, data = most_profitable
                summary['key_findings'].append(f"{crop.title()} shows highest profitability potential ({data['profit_score']:.1f}%)")
        
        # Top recommendations
        if 'recommendations' in analysis_results:
            recs = analysis_results['recommendations']
            primary_rec = recs.get('primary_recommendation', {})
            if primary_rec:
                summary['top_recommendations'].append(
                    f"Primary: Focus on {primary_rec.get('recommended_crop', 'N/A')}"
                )
            
            # Add alternative strategies
            alt_strategies = recs.get('alternative_strategies', [])
            summary['top_recommendations'].extend(alt_strategies[:2])  # Top 2 alternatives
        
        # Decision matrix (simplified)
        if 'individual_analyses' in analysis_results:
            for crop, analysis in analysis_results['individual_analyses'].items():
                summary['decision_matrix'][crop] = {
                    'overall_suitability': analysis.get('overall_suitability', 0),
                    'economic_score': sum(analysis.get('economic_analysis', {}).values()) / 4,  # Average of 4 factors
                    'risk_level': 100 - sum(analysis.get('risk_assessment', {}).values()) / 3  # Lower is better
                }
        
        return summary