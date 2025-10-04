#!/usr/bin/env python3
"""
Test script to verify Sharks from Space installation
"""

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask - OK")
    except ImportError:
        print("❌ Flask - Missing")
        return False
    
    try:
        import pandas
        print("✅ Pandas - OK")
    except ImportError:
        print("❌ Pandas - Missing")
        return False
    
    try:
        import numpy
        print("✅ NumPy - OK")
    except ImportError:
        print("❌ NumPy - Missing")
        return False
    
    try:
        import sklearn
        print("✅ Scikit-learn - OK")
    except ImportError:
        print("❌ Scikit-learn - Missing")
        return False
    
    try:
        import folium
        print("✅ Folium - OK")
    except ImportError:
        print("❌ Folium - Missing")
        return False
    
    try:
        import cartopy
        print("✅ Cartopy - OK")
    except ImportError:
        print("❌ Cartopy - Missing")
        return False
    
    try:
        import shapely
        print("✅ Shapely - OK")
    except ImportError:
        print("❌ Shapely - Missing")
        return False
    
    return True

def test_app_import():
    """Test if the main app can be imported"""
    print("\nTesting app import...")
    try:
        from app import app
        print("✅ App import - OK")
        return True
    except ImportError as e:
        print(f"❌ App import - Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ App import - Error: {e}")
        return False

def main():
    """Main test function"""
    print("🦈 Sharks from Space - Installation Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test app import
    app_ok = test_app_import()
    
    print("\n" + "=" * 40)
    if imports_ok and app_ok:
        print("🎉 All tests passed! Installation is complete.")
        print("🚀 You can now run: python app.py")
        return True
    else:
        print("❌ Some tests failed. Please install missing dependencies:")
        print("   pip install -r sharkfromspace/requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
