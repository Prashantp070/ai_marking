import requests
import json

# Login as existing user
email = 'tempuser@example.com'
password = 'password123'

resp = requests.post('http://127.0.0.1:8000/api/v1/auth/login', json={
    'email': email,
    'password': password
})

print(f'Login Status: {resp.status_code}')
if resp.status_code == 200:
    data = resp.json()
    token = data.get('access_token')
    print(f'Got token for {email}')
    
    # Test submissions endpoint
    resp2 = requests.get('http://127.0.0.1:8000/api/v1/submissions', 
                        headers={'Authorization': f'Bearer {token}'})
    print(f'Submissions Status: {resp2.status_code}')
    print('Submissions:')
    print(json.dumps(resp2.json(), indent=2))
else:
    print(f'Login failed: {resp.json()}')
