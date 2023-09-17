import requests

status_endpt = 'https://api.gdc.cancer.gov/status'
projects_endpt = 'https://api.gdc.cancer.gov/projects'

def statusGDCApi():
    response = requests.get(status_endpt)
    if response.json()["status"] == "OK":
        return True
    else:
        return False
    
def getProjects():
    try:
        params = {
        "size": "100",
        }
        result = requests.get(projects_endpt, params = params).json()
        return result
    except:
        return None
    
def getProjectsName():
    result = getProjects()
    if result:
        ids = [{"id": e["project_id"], "name": e["name"]} for e in result["data"]["hits"]]
        return ids
    else:
        return None

def getProjectById(project_id):
    response = requests.get(projects_endpt + "/" + project_id).json()['data']
    result = {'primary_site': response}
    return response
