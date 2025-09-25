import os
from typing import Optional
from twilio.rest import Client

class SMSService:
    """SMS notification service using Twilio"""
    
    def __init__(self):
        # Twilio credentials from environment variables
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER", "your_twilio_number")
        
        # Initialize Twilio client
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_alert(self, to_number: str, message: str) -> bool:
        """
        Send SMS alert to specified phone number
        
        Args:
            to_number: Phone number in international format (+92XXXXXXXXXX)
            message: Alert message to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            # Send SMS
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            print(f"SMS sent successfully. SID: {message_obj.sid}")
            return True
            
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
    
    def send_weather_alert(self, to_number: str, location: str, weather_data: dict, risk_level: str) -> bool:
        """
        Send formatted weather alert
        
        Args:
            to_number: Phone number to send alert to
            location: Location information
            weather_data: Current weather data
            risk_level: Risk assessment (LOW/MEDIUM/HIGH)
            
        Returns:
            bool: Success status
        """
        try:
            # Format weather alert message
            current = weather_data.get('current', {})
            temp = current.get('temperature', 'N/A')
            humidity = current.get('humidity', 'N/A')
            condition = current.get('weather_condition', 'N/A')
            
            risk_emoji = "🟢" if risk_level == "LOW" else "🟡" if risk_level == "MEDIUM" else "🔴"
            
            message = f"""🌾 AGRICULTURAL WEATHER ALERT
📍 Location: {location}
{risk_emoji} Risk Level: {risk_level}

🌡️ Current Conditions:
• Temperature: {temp}°C
• Humidity: {humidity}%
• Condition: {condition}

⚠️ This is an automated alert from AI Agricultural Analysis System.
"""
            
            return self.send_alert(to_number, message)
            
        except Exception as e:
            print(f"Error sending weather alert: {e}")
            return False
    
    def send_crop_recommendation(self, to_number: str, crop_type: str, recommendations: list, alerts: list) -> bool:
        """
        Send crop-specific recommendations via SMS
        
        Args:
            to_number: Phone number to send to
            crop_type: Type of crop
            recommendations: List of recommendations
            alerts: List of alerts
            
        Returns:
            bool: Success status
        """
        try:
            message = f"🌾 {crop_type.upper()} FARMING ALERT\n\n"
            
            if alerts:
                message += "🚨 IMMEDIATE ALERTS:\n"
                for i, alert in enumerate(alerts[:3], 1):  # Limit to 3 alerts for SMS
                    message += f"{i}. {alert}\n"
                message += "\n"
            
            if recommendations:
                message += "💡 RECOMMENDATIONS:\n"
                for i, rec in enumerate(recommendations[:3], 1):  # Limit to 3 recommendations
                    message += f"{i}. {rec}\n"
            
            message += f"\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            message += "\n🤖 AI Agricultural Analysis System"
            
            return self.send_alert(to_number, message)
            
        except Exception as e:
            print(f"Error sending crop recommendation: {e}")
            return False
    
    def send_irrigation_alert(self, to_number: str, location: str, irrigation_advice: str, urgency: str = "MEDIUM") -> bool:
        """
        Send irrigation-specific alert
        
        Args:
            to_number: Phone number to send to
            location: Farm location
            irrigation_advice: Specific irrigation recommendations
            urgency: Alert urgency level
            
        Returns:
            bool: Success status
        """
        try:
            urgency_emoji = "🔴" if urgency == "HIGH" else "🟡" if urgency == "MEDIUM" else "🟢"
            
            message = f"""💧 IRRIGATION ALERT {urgency_emoji}
📍 {location}
⚡ Urgency: {urgency}

🚰 IRRIGATION ADVICE:
{irrigation_advice}

📱 For detailed analysis, check the AI Agricultural System dashboard.
"""
            
            return self.send_alert(to_number, message)
            
        except Exception as e:
            print(f"Error sending irrigation alert: {e}")
            return False
    
    def send_pest_disease_alert(self, to_number: str, crop_type: str, risks: dict) -> bool:
        """
        Send pest and disease risk alert
        
        Args:
            to_number: Phone number to send to
            crop_type: Type of crop
            risks: Dictionary containing pest/disease risk information
            
        Returns:
            bool: Success status
        """
        try:
            message = f"🐛 PEST & DISEASE ALERT - {crop_type.upper()}\n\n"
            
            high_risk_pests = risks.get('high_risk_pests', [])
            high_risk_diseases = risks.get('high_risk_diseases', [])
            preventive_measures = risks.get('preventive_measures', [])
            
            if high_risk_pests:
                message += "🐛 HIGH RISK PESTS:\n"
                for pest in high_risk_pests[:3]:
                    message += f"• {pest}\n"
                message += "\n"
            
            if high_risk_diseases:
                message += "🦠 HIGH RISK DISEASES:\n"
                for disease in high_risk_diseases[:3]:
                    message += f"• {disease}\n"
                message += "\n"
            
            if preventive_measures:
                message += "🛡️ PREVENTION:\n"
                for measure in preventive_measures[:2]:
                    message += f"• {measure}\n"
            
            message += "\n🔍 Monitor your crops closely and take preventive action."
            
            return self.send_alert(to_number, message)
            
        except Exception as e:
            print(f"Error sending pest/disease alert: {e}")
            return False
    
    def send_harvest_timing_alert(self, to_number: str, crop_type: str, harvest_advice: str, timing: str) -> bool:
        """
        Send harvest timing alert
        
        Args:
            to_number: Phone number to send to
            crop_type: Type of crop
            harvest_advice: Specific harvest recommendations
            timing: Recommended timing
            
        Returns:
            bool: Success status
        """
        try:
            message = f"""🌾 HARVEST TIMING ALERT
🌱 Crop: {crop_type.upper()}
⏰ Timing: {timing}

📋 HARVEST ADVICE:
{harvest_advice}

🌤️ Weather conditions have been analyzed for optimal harvest timing.
"""
            
            return self.send_alert(to_number, message)
            
        except Exception as e:
            print(f"Error sending harvest timing alert: {e}")
            return False

# Import datetime for timestamp
from datetime import datetime
