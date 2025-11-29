#!/usr/bin/env python3
"""
Script để test kết nối backend và các API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend!")
        print("   → Backend không chạy hoặc không accessible")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_cors():
    """Test CORS headers"""
    print("\n🔍 Testing CORS...")
    try:
        response = requests.options(
            f"{BASE_URL}/chat/history",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET"
            },
            timeout=5
        )
        print(f"✅ CORS Preflight Status: {response.status_code}")
        cors_headers = {
            k: v for k, v in response.headers.items() 
            if k.lower().startswith('access-control')
        }
        if cors_headers:
            print(f"✅ CORS Headers: {json.dumps(cors_headers, indent=2)}")
        else:
            print("⚠️  No CORS headers found")
        return True
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_auth_endpoint():
    """Test auth endpoint (without token)"""
    print("\n🔍 Testing /auth/me (should fail without token)...")
    try:
        response = requests.get(f"{BASE_URL}/auth/me", timeout=5)
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly requires authentication")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_chat_history_endpoint():
    """Test chat history endpoint (without token)"""
    print("\n🔍 Testing /chat/history (should fail without token)...")
    try:
        response = requests.get(f"{BASE_URL}/chat/history", timeout=5)
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly requires authentication")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🧪 TESTING BACKEND CONNECTION")
    print("=" * 60)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("CORS", test_cors()))
    results.append(("Auth Endpoint", test_auth_endpoint()))
    results.append(("Chat History Endpoint", test_chat_history_endpoint()))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✅ All tests passed! Backend is working correctly.")
        print("\n💡 If frontend still shows error:")
        print("   1. Check browser console (F12) for detailed errors")
        print("   2. Check if user is logged in (has access_token)")
        print("   3. Try logging out and logging in again")
    else:
        print("\n❌ Some tests failed. Please check backend configuration.")
    
    return all_passed

if __name__ == "__main__":
    main()


