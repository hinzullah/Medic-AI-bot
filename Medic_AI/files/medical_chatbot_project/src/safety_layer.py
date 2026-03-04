"""
Safety Layer - Emergency detection and warnings
"""


class MedicalSafetyLayer:
    """Safety checks for medical chatbot"""
    
    EMERGENCY_KEYWORDS = [
        "chest pain", "difficulty breathing", "can't breathe",
        "severe bleeding", "unconscious", "seizure",
        "heart attack", "stroke", "suicide",
        "overdose", "severe allergic reaction"
    ]
    
    HIGH_RISK_KEYWORDS = [
        "pregnant", "pregnancy", "baby", "infant",
        "severe pain", "high fever", "blood in",
        "can't move", "vision loss"
    ]
    
    @staticmethod
    def check_emergency(message: str) -> tuple:
        """
        Check if message contains emergency keywords
        Returns: (is_emergency: bool, message: str)
        """
        message_lower = message.lower()
        
        for keyword in MedicalSafetyLayer.EMERGENCY_KEYWORDS:
            if keyword in message_lower:
                emergency_msg = f"""
🚨 EMERGENCY DETECTED 🚨

Your message mentions: "{keyword}"

This may require IMMEDIATE medical attention.

ACTION REQUIRED NOW:
1. Call emergency services immediately:
   - US: 911
   - UK: 999  
   - EU: 112
2. Do not wait for online advice
3. Seek in-person medical care NOW

This is a critical situation requiring professional help.
"""
                return True, emergency_msg
        
        return False, ""
    
    @staticmethod
    def check_high_risk(message: str) -> tuple:
        """
        Check for high-risk situations
        Returns: (is_high_risk: bool, warning: str)
        """
        message_lower = message.lower()
        
        for keyword in MedicalSafetyLayer.HIGH_RISK_KEYWORDS:
            if keyword in message_lower:
                warning = f"""
⚠️ HIGH-RISK SITUATION DETECTED ⚠️

Your question involves: "{keyword}"

IMPORTANT:
- This requires professional medical evaluation
- Online information is not sufficient
- Contact your doctor or healthcare provider
- Visit urgent care if needed

I can provide general information, but you MUST seek professional care.
"""
                return True, warning
        
        return False, ""
    
    @staticmethod
    def add_disclaimer(response: str) -> str:
        """Add medical disclaimer"""
        disclaimer = """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ MEDICAL DISCLAIMER:
This is educational information only, not medical advice.
Always consult qualified healthcare professionals.
Never delay seeking medical care based on online information.
In emergencies, call your local emergency number.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return response + disclaimer


class SafeChatbotWrapper:
    """Wrap any chatbot with safety checks"""
    
    def __init__(self, base_chatbot):
        self.chatbot = base_chatbot
        self.safety = MedicalSafetyLayer()
    
    def chat(self, message: str) -> str:
        """Chat with safety checks"""
        
        # Emergency check
        is_emergency, emergency_msg = self.safety.check_emergency(message)
        if is_emergency:
            return emergency_msg
        
        # High risk check
        is_high_risk, warning = self.safety.check_high_risk(message)
        
        # Get chatbot response
        response = self.chatbot.chat(message)
        
        # Add warnings
        if is_high_risk:
            response = warning + "\n\n" + response
        
        # Add disclaimer
        response = self.safety.add_disclaimer(response)
        
        return response
    
    def reset(self):
        """Reset chatbot state"""
        if hasattr(self.chatbot, 'reset'):
            self.chatbot.reset()


# Testing
if __name__ == "__main__":
    # Test emergency detection
    safety = MedicalSafetyLayer()
    
    test_messages = [
        "I have chest pain",
        "My baby has a fever",
        "What causes headaches?"
    ]
    
    for msg in test_messages:
        print(f"\nTesting: '{msg}'")
        is_emergency, emerg_msg = safety.check_emergency(msg)
        is_high_risk, risk_msg = safety.check_high_risk(msg)
        
        if is_emergency:
            print("🚨 EMERGENCY DETECTED")
        elif is_high_risk:
            print("⚠️ HIGH RISK")
        else:
            print("✅ Normal query")
