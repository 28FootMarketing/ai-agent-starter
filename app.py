import requests
import os
import json
from typing import Dict, Any

def send_to_ghl(data: Dict[str, Any]) -> bool:
    """
    Send data to GoHighLevel webhook
    """
    try:
        # Get webhook URL from environment variables
        webhook_url = os.getenv("GHL_WEBHOOK_URL")
        
        if not webhook_url:
            print("Warning: GHL_WEBHOOK_URL not found in environment variables")
            return False
        
        # Prepare payload
        payload = {
            "timestamp": str(pd.Timestamp.now()),
            "source": "AI_Recruiting_Assistant",
            **data
        }
        
        # Send POST request
        response = requests.post(
            webhook_url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AI-Recruiting-Assistant/1.0"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("Successfully sent data to GHL")
            return True
        else:
            print(f"Failed to send data to GHL: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error sending to GHL: {str(e)}")
        return False
