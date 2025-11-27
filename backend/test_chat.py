"""
Script để test tính năng chat
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_chat():
    """Test chat endpoint"""
    print("=" * 50)
    print("🧪 Testing Chat Feature")
    print("=" * 50)
    
    # Step 1: Login
    print("\n1️⃣  Testing login...")
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        token = response.json()["access_token"]
        print(f"✅ Login successful, token: {token[:20]}...")
    except Exception as e:
        print(f"❌ Login error: {e}")
        print("   Hint: Make sure backend is running and user exists")
        return False
    
    # Step 2: Send chat message
    print("\n2️⃣  Testing send message...")
    headers = {"Authorization": f"Bearer {token}"}
    chat_data = {
        "message": "xin chào",
        "jlpt_level": "N5"
    }
    
    try:
        print(f"   Sending message: '{chat_data['message']}'")
        response = requests.post(
            f"{BASE_URL}/chat/message",
            json=chat_data,
            headers=headers,
            timeout=15
        )
        
        if response.status_code != 200:
            print(f"❌ Send message failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        result = response.json()
        print(f"✅ Message sent successfully")
        print(f"   Answer: {result.get('answer', '')[:100]}...")
        print(f"   Response time: {result.get('response_time', 0):.2f}s")
        return True
        
    except requests.exceptions.Timeout:
        print(f"❌ Request timeout (>15s)")
        print("   Hint: Ollama might be slow or not responding")
        return False
    except Exception as e:
        print(f"❌ Send message error: {e}")
        return False
    
    # Step 3: Get chat history
    print("\n3️⃣  Testing get chat history...")
    try:
        response = requests.get(
            f"{BASE_URL}/chat/history?limit=10",
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Get history failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        history = response.json()
        print(f"✅ Chat history retrieved: {len(history)} messages")
        
        if len(history) > 0:
            latest = history[0]
            print(f"   Latest message: {latest.get('question', '')[:50]}...")
            print(f"   Latest answer: {latest.get('answer', '')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Get history error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🚀 Starting Chat Test")
    print("=" * 50)
    print(f"Backend URL: {BASE_URL}")
    print("Make sure:")
    print("  1. Backend is running (uvicorn)")
    print("  2. Database is connected")
    print("  3. Ollama is running (if using Ollama)")
    print("  4. Test user exists (email: test@example.com, password: test123)")
    print("=" * 50)
    
    result = test_chat()
    
    print("\n" + "=" * 50)
    if result:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")
    print("=" * 50)



















