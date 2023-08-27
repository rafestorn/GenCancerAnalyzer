import requests

status_endpt = 'https://api.gdc.cancer.gov/status'
projects_endpt = 'https://api.gdc.cancer.gov/projects'

def statusGDCApi():
    response = requests.get(status_endpt)
    if response.json()["status"] == "OK":
        return True
    else:
        return False
    
def getProjectsName():
    params = {
    "size": "100",
    }
    result = requests.get(projects_endpt, params = params).json()
    ids = [{"id": e["project_id"], "name": e["name"]} for e in result["data"]["hits"]]
    return ids