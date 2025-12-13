
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_server():
    # 1. Create Session
    print("Creating session...")
    resp = requests.post(f"{BASE_URL}/session", json={"customer_id": "CUST001"})
    if resp.status_code != 200:
        print(f"Failed to create session: {resp.text}")
        return
    
    data = resp.json()
    session_id = data["session_id"]
    user_id = "cust001"
    print(f"Session ID: {session_id}")
    
    # 2. Chat 1
    print("\nSending: I want a personal loan")
    resp = requests.post(f"{BASE_URL}/chat", json={
        "session_id": session_id,
        "user_id": user_id,
        "message": "I want a personal loan"
    })
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
    
    # 3. Chat 2
    print("\nSending: For home renovation")
    resp = requests.post(f"{BASE_URL}/chat", json={
        "session_id": session_id,
        "user_id": user_id,
        "message": "For home renovation"
    })
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

if __name__ == "__main__":
    test_server()
