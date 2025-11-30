#!/usr/bin/env python3
"""
Test script to verify application can start without errors
Run this before deploying to EB
"""
import sys
import os

print("=" * 60)
print("Testing application startup...")
print("=" * 60)

# Test 1: Import application
print("\n1. Testing application import...")
try:
    from application import application, app
    print("✓ Application imported successfully")
except Exception as e:
    print(f"✗ Failed to import application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Check Flask app is created
print("\n2. Checking Flask app...")
try:
    assert application is not None
    assert app is not None
    print(f"✓ Flask app created: {application}")
except Exception as e:
    print(f"✗ Flask app check failed: {e}")
    sys.exit(1)

# Test 3: Check routes
print("\n3. Checking routes...")
try:
    routes = [str(rule) for rule in application.url_map.iter_rules()]
    print(f"✓ Routes registered: {', '.join(routes)}")
    assert '/' in routes
    assert '/health' in routes
    assert '/predict' in routes
except Exception as e:
    print(f"✗ Routes check failed: {e}")
    sys.exit(1)

# Test 4: Test health endpoint
print("\n4. Testing health endpoint...")
try:
    with application.test_client() as client:
        response = client.get('/health')
        print(f"✓ Health endpoint status: {response.status_code}")
        print(f"  Response: {response.get_json()}")
        assert response.status_code == 200
except Exception as e:
    print(f"✗ Health endpoint failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test home page
print("\n5. Testing home page...")
try:
    with application.test_client() as client:
        response = client.get('/')
        print(f"✓ Home page status: {response.status_code}")
        assert response.status_code == 200
        assert b'Student Exam Performance' in response.data
except Exception as e:
    print(f"✗ Home page failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Check artifacts exist
print("\n6. Checking artifacts...")
try:
    assert os.path.exists('artifacts/model.pkl'), "model.pkl not found"
    assert os.path.exists('artifacts/preprocessor.pkl'), "preprocessor.pkl not found"
    print("✓ Model artifacts found")
except Exception as e:
    print(f"✗ Artifacts check failed: {e}")
    sys.exit(1)

# Test 7: Test prediction pipeline import (lazy loaded)
print("\n7. Testing prediction pipeline import...")
try:
    from src.pipeline.predict_pipeline import PredictPipeline, CustomData
    print("✓ Prediction pipeline imports successfully")
except Exception as e:
    print(f"✗ Prediction pipeline import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - Application is ready for deployment")
print("=" * 60)
