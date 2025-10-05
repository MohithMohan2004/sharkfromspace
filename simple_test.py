#!/usr/bin/env python3
"""
Simple test script for Sharks from Space API endpoints
"""

import requests
import json
import time

API_BASE = "http://localhost:5000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a single API endpoint"""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.get(url, timeout=10)
        
        print(f"{method} {endpoint} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"{method} {endpoint} - Error: {e}")
        return None

def main():
    """Main test function"""
    print("Sharks from Space - Integration Test")
    print("=" * 50)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Test basic connectivity
    print("\nTesting basic connectivity...")
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            print("Server is running and accessible")
        else:
            print(f"Server returned status {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"Cannot connect to server: {e}")
        print("Make sure the Flask server is running on http://localhost:5000")
        return
    
    # Test tracker page
    print("\nTesting tracker page...")
    response = test_endpoint("/tracker")
    if response and response.status_code == 200:
        print("Tracker page accessible")
    else:
        print("Tracker page not accessible")
    
    # Test API endpoints
    print("\nTesting API endpoints...")
    test_endpoint("/api/data-info")
    test_endpoint("/api/list-heatmaps")
    
    # Test data generation
    print("\nTesting data generation...")
    response = test_endpoint("/api/generate-synthetic-data", "POST")
    if response and response.status_code == 200:
        print("Data generation successful")
        
        # Test heatmap generation
        print("\nTesting heatmap generation...")
        heatmap_params = {
            "grid_res": 0.25,
            "prob_threshold": 0.4,
            "test_size": 0.2,
            "n_est": 200
        }
        response = test_endpoint("/api/generate-heatmap", "POST", heatmap_params)
        if response and response.status_code == 200:
            print("Heatmap generation successful")
        else:
            print("Heatmap generation failed")
    else:
        print("Data generation failed")
    
    print("\n" + "=" * 50)
    print("Integration test complete!")
    print("\nTo test manually:")
    print("1. Open http://localhost:5000/tracker in your browser")
    print("2. Click 'Generate Ocean Data' button")
    print("3. Click 'Generate Heatmap' button")
    print("4. View the interactive shark probability heatmap!")

if __name__ == "__main__":
    main()

