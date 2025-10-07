import requests

url = "http://127.0.0.1:8000/blog/"

# Step 1: Register user (or use existing)
user_payload = {"name": "Test", "email": "test@example.com", "password": "password123"}
requests.post("http://127.0.0.1:8000/user/", json=user_payload)

# Step 2: Login to get JWT
login_payload = {"username": "test@example.com", "password": "password123"}
login_resp = requests.post("http://127.0.0.1:8000/login", data=login_payload)
token = login_resp.json()["access_token"]

# Step 3: Create 20 MB blog
big_body = "A" * (20 * 1024 * 1024)
payload = {"title": "Large Blog Test", "body": big_body}

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)
try:
    print(response.json())
except:
    print(response.text)
