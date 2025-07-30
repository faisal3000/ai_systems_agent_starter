import requests

resp = requests.post(
    "http://127.0.0.1:8000/auth/login",
    data={
      "username": "f.khann@gmail.com",
      "password": "Passw0rd!"
    },
)
print(resp.status_code, resp.text)
