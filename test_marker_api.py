#!/usr/bin/env python3
"""
Test script to check which parameters the local Marker API accepts
"""
import requests
import sys
import json

# Marker API URL - adjust based on your setup
# If running in Docker, use the container name or IP
MARKER_URL = "http://marker:8501"  # For Docker network
# MARKER_URL = "http://172.18.0.X:8501"  # Use actual container IP
# MARKER_URL = "http://localhost:8501"  # If exposed to host

import os
# Or get from environment
MARKER_URL = os.getenv("MARKER_SERVER_URL", "http://marker:8501")

if len(sys.argv) > 1:
    MARKER_URL = sys.argv[1]

def test_marker_api():
    print(f"Testing Marker API at {MARKER_URL}")
    
    # First check health
    try:
        health_response = requests.get(f"{MARKER_URL}/health", timeout=5)
        print(f"Health check: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"Health response: {health_response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test with a simple text file
    test_content = b"This is a test document for Marker API."
    
    # Test different parameter combinations
    test_cases = [
        {
            "name": "No parameters",
            "params": {}
        },
        {
            "name": "With output_format",
            "params": {"output_format": "markdown"}
        },
        {
            "name": "With force_ocr",
            "params": {"force_ocr": "true"}
        },
        {
            "name": "With use_llm",
            "params": {"use_llm": "true"}
        },
        {
            "name": "With all parameters",
            "params": {
                "output_format": "markdown",
                "force_ocr": "false",
                "use_llm": "false",
                "skip_cache": "false",
                "langs": "en"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        print(f"Parameters: {test_case['params']}")
        
        try:
            files = {"file": ("test.txt", test_content, "text/plain")}
            
            response = requests.post(
                f"{MARKER_URL}/convert",
                data=test_case['params'],
                files=files,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Success! Response keys: {list(result.keys())}")
                # Print first 200 chars of content if available
                for key in ['markdown', 'text', 'content', 'output']:
                    if key in result and result[key]:
                        print(f"{key}: {str(result[key])[:200]}...")
                        break
            else:
                print(f"Error response: {response.text[:500]}")
                
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    test_marker_api()