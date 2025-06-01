"""
Test script to verify registration and authentication functionality
"""
import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_registration_and_login():
    """Test user registration and login functionality"""
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test data
    test_username = f"testuser_{int(time.time())}"
    test_password = "testpassword123"
    
    print(f"Testing with username: {test_username}")
    
    # Test 1: Register a new user
    print("\n=== Testing Registration ===")
    register_data = {
        'username': test_username,
        'password': test_password
    }
    
    try:
        response = session.post(f"{BASE_URL}/register", data=register_data)
        print(f"Registration response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Registration form submitted successfully")
            if "註冊成功" in response.text or response.url.endswith('/login'):
                print("✅ Registration appears successful")
            else:
                print("❌ Registration may have failed")
        else:
            print(f"❌ Registration failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Test 2: Login with the registered user
    print("\n=== Testing Login ===")
    login_data = {
        'username': test_username,
        'password': test_password
    }
    
    try:
        response = session.post(f"{BASE_URL}/login", data=login_data)
        print(f"Login response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login form submitted successfully")
            if response.url.endswith('/') or 'username' in response.text:
                print("✅ Login appears successful")
                return True
            else:
                print("❌ Login may have failed")
                print("Response URL:", response.url)
        else:
            print(f"❌ Login failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    return False

def test_duplicate_registration():
    """Test that duplicate registration is prevented"""
    print("\n=== Testing Duplicate Registration Prevention ===")
    session = requests.Session()
    
    test_username = "duplicate_test_user"
    test_password = "testpassword123"
    
    register_data = {
        'username': test_username,
        'password': test_password
    }
    
    # Register first time
    try:
        response1 = session.post(f"{BASE_URL}/register", data=register_data)
        print(f"First registration status: {response1.status_code}")
        
        # Register second time (should fail)
        response2 = session.post(f"{BASE_URL}/register", data=register_data)
        print(f"Second registration status: {response2.status_code}")
        
        if "已存在" in response2.text or "失敗" in response2.text:
            print("✅ Duplicate registration properly prevented")
            return True
        else:
            print("❌ Duplicate registration was not prevented")
            return False
            
    except Exception as e:
        print(f"❌ Duplicate registration test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Starting Authentication Tests")
    print("================================")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Run tests
    auth_test_passed = test_registration_and_login()
    duplicate_test_passed = test_duplicate_registration()
    
    print("\n" + "="*50)
    print("📊 Test Results:")
    print(f"Registration & Login: {'✅ PASSED' if auth_test_passed else '❌ FAILED'}")
    print(f"Duplicate Prevention: {'✅ PASSED' if duplicate_test_passed else '❌ FAILED'}")
    
    if auth_test_passed and duplicate_test_passed:
        print("\n🎉 All tests passed! Authentication system is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the authentication implementation.")
