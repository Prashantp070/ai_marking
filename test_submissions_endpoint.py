#!/usr/bin/env python3
"""
Test the submissions endpoint after file upload
"""
import requests
import json

print("\n" + "="*70)
print("TESTING SUBMISSIONS ENDPOINT")
print("="*70 + "\n")

# First register a user
print("Step 1: Register User")
reg_response = requests.post("http://127.0.0.1:8000/api/v1/auth/register", json={
    "email": "test_submissions@test.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
})

if reg_response.status_code == 200:
    token = reg_response.json()["access_token"]
    print(f"✅ User registered. Token: {token[:20]}...")
else:
    print(f"❌ Registration failed: {reg_response.status_code}")
    print(reg_response.text)
    exit(1)

# Test getting submissions (should be empty)
print("\nStep 2: Get Submissions (Empty List)")
headers = {"Authorization": f"Bearer {token}"}
subs_response = requests.get("http://127.0.0.1:8000/api/v1/submissions", headers=headers)

if subs_response.status_code == 200:
    data = subs_response.json()
    print(f"✅ Submissions endpoint works")
    print(f"   Response: {json.dumps(data, indent=2)}")
    print(f"   Total: {data.get('total')} submissions")
else:
    print(f"❌ Failed to get submissions: {subs_response.status_code}")
    print(subs_response.text)

print("\n" + "="*70)
print("✅ SUBMISSION ENDPOINT TEST COMPLETE")
print("="*70 + "\n")
