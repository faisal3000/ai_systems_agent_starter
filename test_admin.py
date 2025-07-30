# test_admin.py
import requests

# 1) Log in and grab token
res = requests.post(
    "http://127.0.0.1:8000/auth/login",
    data={"username": "f.khann@gmail.com", "password": "Passw0rd!"},
)
print("Login:", res.status_code, res.json())
token = res.json().get("access_token")

# 2) Call the admin/users endpoint
res2 = requests.get(
    "http://127.0.0.1:8000/admin/users",
    headers={"Authorization": f"Bearer {token}"},
)
print("Admin /users:", res2.status_code, res2.json())
