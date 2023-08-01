import requests
import json

def statusGDCApi():
    status_endpt = 'https://api.gdc.cancer.gov/status'
    response = requests.get(status_endpt)
    if response.json()["status"] == "OK":
        return True
    else:
        return False