# services/video_api.py
import requests
import os

API_URL = "http://localhost:8080/api/videos/store"

def store_video(file_path, kiosk_id):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'video/mp4')}
            data = {'kiosk_id': kiosk_id}
            response = requests.post(API_URL, files=files, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en store_video: {response.status_code}")
            print("Respuesta del servidor:", response.text)
            return None
    except Exception as e:
        print("Error:", e)
        return None
