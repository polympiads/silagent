
import requests

TARGET_URL = "http://192.168.0.5:5000/"

def get_value ():
    response = requests.get( TARGET_URL )
    assert response.status_code == 200

    return response.content
