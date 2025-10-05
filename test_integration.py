#!/usr/bin/env python3
"""
Test script for Sharks from Space API endpoints
This script tests the frontend-backend integration
"""

import requests
import json
import time
import os

API_BASE = "http://localhost:5000"

def test_api_endpoint(endpoint, method="GET", data=None):
    """Test a single API endpoint"""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.get(url, timeout=10)
        
        print(f"✅ {method} {endpoint} - Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if 'success' in result:
                print(f"   Success: {result['success']}")
                if 'message' in result:
                    print(f"   Message: {result['message']}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return None

def test_frontend_pages():
    """Test that frontend pages are accessible"""
    pages = [
        "/",
        "/about",
        "/nasa", 
        "/tag",
        "/tracker",
        "/contact",
        "/habitat",
        "/types",
        "/migration",
        "/aboutus"
    ]
    
    print("\n🌐 Testing Frontend Pages:")
    for page in pages:
        try:
            response = requests.get(f"{API_BASE}{page}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {page} - Status: {response.status_code}")
            else:
                print(f"❌ {page} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {page} - Error: {e}")

def test_tracker_functionality():
    """Test the complete tracker workflow"""
    print("\n🦈 Testing Tracker Functionality:")
    
    # Step 1: Generate synthetic data
    print("\n1. Generating synthetic ocean data...")
    response = test_api_endpoint("/api/generate-synthetic-data", "POST")
    if not response or response.status_code != 200:
        print("❌ Failed to generate synthetic data")
        return False
    
    # Wait a moment for data generation
    time.sleep(2)
    
    # Step 2: Generate heatmap
    print("\n2. Generating shark probability heatmap...")
    heatmap_params = {
        "grid_res": 0.25,
        "prob_threshold": 0.4,
        "test_size": 0.2,
        "n_est": 200
    }
    response = test_api_endpoint("/api/generate-heatmap", "POST", heatmap_params)
    if not response or response.status_code != 200:
        print("❌ Failed to generate heatmap")
        return False
    
    # Step 3: List available heatmaps
    print("\n3. Listing available heatmaps...")
    response = test_api_endpoint("/api/list-heatmaps")
    if response and response.status_code == 200:
        result = response.json()
        if result.get('success') and result.get('heatmaps'):
            print(f"   Found {len(result['heatmaps'])} heatmap(s)")
            latest_map = result['heatmaps'][0]
            print(f"   Latest: {latest_map}")
            
            # Step 4: Test heatmap serving
            print(f"\n4. Testing heatmap serving: {latest_map}")
            response = test_api_endpoint(f"/api/heatmap/{latest_map}")
            if response and response.status_code == 200:
                print("✅ Heatmap served successfully")
                return True
            else:
                print("❌ Failed to serve heatmap")
                return False
        else:
            print("❌ No heatmaps found")
            return False
    else:
        print("❌ Failed to list heatmaps")
        return False

def main():
    """Main test function"""
    print("Sharks from Space - Frontend-Backend Integration Test")
    print("=" * 60)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test basic connectivity
    print("\n🔗 Testing basic connectivity...")
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            print("Server is running and accessible")
        else:
            print(f"❌ Server returned status {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"Cannot connect to server: {e}")
        print("Make sure the Flask server is running on http://localhost:5000")
        return
    
    # Test API endpoints
    print("\n📊 Testing API Endpoints:")
    test_api_endpoint("/api/data-info")
    test_api_endpoint("/api/list-heatmaps")
    
    # Test frontend pages
    test_frontend_pages()
    
    # Test tracker functionality
    success = test_tracker_functionality()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Frontend-backend integration is working!")
        print("\n📝 Next steps:")
        print("   1. Open http://localhost:5000/tracker in your browser")
        print("   2. Click 'Generate Ocean Data' button")
        print("   3. Click 'Generate Heatmap' button")
        print("   4. View the interactive shark probability heatmap!")
    else:
        print("❌ Some tests failed. Check the server logs for details.")
    
    print("\n🦈 Sharks from Space integration test complete!")

if __name__ == "__main__":
    main()
