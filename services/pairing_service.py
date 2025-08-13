import requests

API_URL = "http://localhost:8080/api/kiosks/pair"

def pair_device(code):
    try:
        response = requests.post(API_URL, json={"code": code})

        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None
