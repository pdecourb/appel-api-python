import time
import requests
import os

"""
#authentification WSO2 à faire dès que dispo
body = {
    'application': 'XOPS-GITLABCI',
    'utilisateur': os.environ["CODE_SOLUTION"],
    'motdepasse': os.environ["USER_PASSWORD"],
    'scope': 'GestionAPI_Gestion',
    'environment': 'Production'
}
authentication = requests.post("https://access.api.cagip.group.gca/securitemontokenapi/1.2/TokenUserAppli/", json=body)
print("status code : ", authentication.status_code)
print("response json : ", authentication.json())
data = info.json()
#indiquer le chemin vers la clé BEARER pour injection dans les requêtes suivantes
BearerToken = data['TOKEN']
"""

#version de l'API Rheia
version = "v0"

#vars ansible
idd = "ILGN"
playbook_url = os.environ["PLAYBOOK_URL"]
playbook_version = os.environ["PLAYBOOK_VERSION"]
playbook_path = "playbook.yml"
inventory_url = os.environ["INVENTORY_URL"]
if inventory_url == "":
  inventory_url = playbook_url
inventory_version = os.environ["INVENTORY_VERSION"]
if inventory_version == "":
  inventory_version = playbook_version
inventory_path = os.environ["INVENTORY_PATH"]
inventory_list = os.environ["INVENTORY_LIST"]
playbook_extra_vars = os.environ["PLAYBOOK_EXTRA_VARS"]
playbook_tags = os.environ["PLAYBOOK_TAGS"]
playbook_skip_tags = os.environ["PLAYBOOK_SKIP_TAGS"]
docker_img_version = os.environ["DOCKER_IMG_VERSION"]
notification_mode = os.environ["NOTIFICATION_MODE"]


print("=================HEALTH request========================")
#request la bonne santé de l'api Rheia
info = requests.get("https://i1-ans8-rheia.hpr.caas.ca-ts.group.gca/api/"+ version +"/info/health")
print("HEALTH status code : ", info.status_code)
print("HEALTH response json : ", info.json())
# Si OK on request le deploy sinon on sort une erreur
if info.status_code == 200:
  body = {
    'idd': idd,
    'playbook_url': playbook_url,
    'playbook_version': playbook_version,
    'playbook_path': playbook_path,
    'inventory_url': inventory_url,
    'inventory_version': inventory_version,
    'inventory_path': inventory_path,
    'inventory_list': inventory_list,
    'playbook_extra_vars': playbook_extra_vars,
    'playbook_tags': playbook_tags,
    'playbook_skip_tags': playbook_skip_tags,
    'docker_img_version': '2.10',
    'notification_mode': notification_mode
  }
  print("=================DEPLOY request========================")
#request le deploy
  deploy = requests.post("https://i1-ans8-rheia.hpr.caas.ca-ts.group.gca/api/"+ version +"/awx/deploy", json=body)
  print("DEPLOY request url : ", deploy.request.url)
  print("DEPLOY request body : ", deploy.request.body)
# Si le deploy est en 200 alors on request le status du job de déploiement sinon on sort une erreur
  if deploy.status_code == 200:
    print("=================DEPLOY request OK========================")
    print("DEPLOY status code : ", deploy.status_code)
    print("DEPLOY response json : ", deploy.json())
    data = deploy.json()
#indiquer le chemin vers la clé job-id
    job_id = data['job_id']
    print("=================STATUS request========================")
#resquest le deploy Status
    statusdeploy =  requests.get("https://i1-ans8-rheia.hpr.caas.ca-ts.group.gca/api/"+ version +"/awx/deploy/" + job_id)
    print("STATUS status code : ", statusdeploy.status_code)
    print("STATUS request url : ", statusdeploy.request.url)
    print("STATUS response json : ", statusdeploy.json())
    data = statusdeploy.json()
#indiquer le chemin vers le status
    status = data['status']
#on va faire une boucle pour attendre le retour fail ou success du deploy
    result = True
    while result:
      if (status == "new" or status == 'pending' or status == "waiting" or status == "running"):
        time.sleep(5)
        print("=================STATUS request LOOP========================")
        statusdeploy =  requests.get("https://i1-ans8-rheia.hpr.caas.ca-ts.group.gca/api/"+ version +"/awx/deploy/" + job_id)
        data = statusdeploy.json()
        status = data['status']
        print("STATUS status code : ", statusdeploy.status_code)
        print("STATUS request url : ", statusdeploy.request.url)
        print("STATUS response : ", status)
  #retour possible successful failed error canceled - https://docs.ansible.com/ansible-tower/3.2.3/html/towerapi/job_list.html
      else:
        print("=================STATUS request reponse => "+ status + "========================")
        print("STATUS response json : ", statusdeploy.json())
        result = False
  else:
    print("=================ERROR DEPLOY request========================")
    print('DEPLOY ERROR - DEPLOY IS INCORRECT')
    print("DEPLOY status code : ", deploy.status_code)
    print("DEPLOY response json : ", deploy.json())
else:
  print("=================ERROR HEALTH request========================")
  print('HEALTH ERROR - RHEIA IS DEAD')
  print("HEALTH status code : ", info.status_code)
  print("HEALTH response json : ", info.json())
