import requests
import json
import csv
def login(url,uid,pwd):
    payload = json.dumps({
        "username": uid,
        "password": pwd
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url+'/auth/login', headers=headers, data=payload)
    JsonData = response.json()
    return JsonData["token"]
url1="https://cloud.apisec.ai"
tk = login(url1,"ApigeeAuto//asif@apisec.ai","bQMyhiUPq")


def OAS_URLs():
    url = url1+"/api/v1/projects"
    with open('/home/ubuntu/Desktop/python_programms/OAS_Specs.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            payload = json.dumps({
                "credsRequired": False,
                "isFileLoad": False,
                "skipAbac": False,
                "manualEpFound": False,
                "localOffSet": -330,
                "apispecType": "openAPISpec",
                "name": row['API_Names'],
                "planType": "ENTERPRISE",
                "openAPISpec": row['Open_API_Spec'],
                "tags": [
                    "API-Automation"
                ]
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+tk,
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            JsonData = response.json()
            #print(JsonData,"<<<<<<<<")
#OAS_URLs()

def getIds(tk):
 num = [0,1]
 prIds = []
 prNames = []
 prEp = 0
 prPb = 0
 for i in num:
   url = url1+"/api/v1/projects?page=" +str(i)+ "&pageSize=100&sort=createdDate&sortType=DESC"
   payload = {}
   headers = {
       'Authorization': 'Bearer ' + tk,
       "Content-Type": "application/json"
   }
   response = requests.request("GET", url, headers=headers, data=payload)
   JsonData = response.json()
   for employee in JsonData["data"]:
      prIds.append(employee["id"])
      prNames.append(employee["name"])
      prEp += (employee["endpointsCount"])
      prPb += (employee["playbooksCount"])
 return prIds,prNames,prEp,prPb
#idl = getIds(tk)

def readFile(name):
    with open('/home/ubuntu/Desktop/python_programms/'+name+'.txt') as f:
        data = f.read()
    js = json.loads(data)
    return js
#idl = readFile('pIDs')

def write(details,name):
    with open('/home/ubuntu/Desktop/python_programms/'+name+'.txt', 'w') as convert_file:
        convert_file.write(json.dumps(details) + '\n')
#write(idl,'pIDs')

def getAPIsRegistered():
    url = url1+"/api/v1/projects/all?page=0&pageSize=25&sort=createdDate&sortType=DESC"
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + tk,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    JsonData = response.json()
    APIsRegistered = JsonData["totalElements"]
    Projects = readFile('pIDs')
    print(len(Projects[0]),"<<<<<<<<")
    if APIsRegistered == len(Projects[0]) :
        print("Total APIs Registered are as Expected")
    else: print("Incorrect Total APIs Registered")
#getAPIsRegistered()

def getEnvByProjectId():
    envIds = []
    num = readFile('pIDs')
    prj = num[0]
    for i in prj:
        url = url1+"/api/v1/envs/projects/"+str(i)+"?page=0&pageSize=100"
        payload = {}
        headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' +tk,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonData = response.json()
        for j in JsonData["data"]:
            envIds.append({i:j["id"]})
    return envIds
#eidl = getEnvByProjectId()

def write1(details,name):
    with open('/home/ubuntu/Desktop/python_programms/'+name+'.txt', 'w') as convert_file:
        convert_file.write(json.dumps(details) + '\n')
#write1(eidl,'eIDs')

def readFile1(name):
    with open('/home/ubuntu/Desktop/python_programms/'+name+'.txt') as f:
        data = f.read()
    js = json.loads(data)
    return js
#eidl = readFile1('eIDs')

def allVulnerabilities():
    activeCount = 0
    Env = readFile1('eIDs')
    for item in Env:
        key, value = list(item.items())[0]
        url = url1+"/api/v1/projects/"+ str(key) +"/auto-suggestions/active?envId="+ str(value) +"&severity=all&page=0&pageSize=100&sort=severity&sortType=ASC"
        payload = ""
        headers = {
            'Authorization': 'Bearer '+tk,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonData = response.json()
        activeCount += (len(JsonData["data"]))
    return activeCount
#idl = allVulnerabilities()

def write2(details,name):
    with open('/home/ubuntu/Desktop/python_programms/'+name+'.txt', 'w') as convert_file:
        convert_file.write(json.dumps(details) + '\n')
#write2(idl,'Vulns')

def readFile2(name):
    with open('/home/ubuntu/Desktop/python_programms/'+name+'.txt') as f:
        data = f.read()
    js = json.loads(data)
    return js
#eidl = readFile2('Vulns')

def getTotalPbEpvulcount():
    count = readFile('pIDs')
    Epoint = count[2]
    Pbook = count[3]
    url = url1+"/api/v1/dashboard/org-stats"
    payload = {}
    headers = {
        'Authorization': 'Bearer ' +tk,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    JsonData = response.json()
    print(JsonData["data"]["totalEndpoints"],"<<<<<<<")
    TotalEp = JsonData["data"]["totalEndpoints"]
    TotalPb = JsonData["data"]["totalPlaybooks"]
    if Epoint == TotalEp :
        print("Expected Endpoints count : " + str(Epoint) +  " & Actual Endpoints count : " + str(TotalEp) + " are Equal")
    else: print("Incorrect Endpoints count")
    if TotalPb == Pbook :
        print("Expected Playbooks count : " + str(Pbook) +  " & Actual Playbooks count : " + str(TotalPb) + " are Equal")
    else: print("Incorrect Playbooks count")
getTotalPbEpvulcount()

'''def passIds():
    num = readFile('pIDs')
    for i in num:
        url =url1+ "/api/v1/test-suites/project-id/" +str(i)+ "?page=0&pageSize=20"
        payload = {}
        headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' + tk,
       "Content-Type": "application/json"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonData = response.json()
        print(JsonData["data"],"<<<<<<")

passIds()
'''

