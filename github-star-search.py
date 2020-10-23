#!/usr/bin/python3

from github import Github,UnknownObjectException
import requests,sys,json,bs4,time
from pathlib import Path
import os,re

home = str(Path.home())
data_path = os.path.join(home,'.github-star-search')
pattern = str(sys.argv[1])

api_token = "xxxxxxxxxx"
headers = {'Authorization': 'token %s' % api_token}
topic_headers = {'Accept': 'application/vnd.github.mercy-preview+json','Authorization':'token xxxxxxxxxxx'}

all_repos = []
all_json_results = []

def Update_Data():
    print("[+] UPDATING")
    g = Github(str(api_token))
    stared = g.get_user().get_starred()
    for repo in stared:
        full_name = repo.full_name
        try:
            if full_name not in all_repos:
                print(repo.url)
                all_repos.append(full_name)
                repo = g.get_repo(full_name)
                description = str(repo.description)
                url = repo.url
                raw_content = ""
                contents = repo.get_contents("")
                if contents:
                    for each_c in contents:
                        if each_c.path.endswith('.md') or each_c.path.endswith('.rst'):
                            raw_content += str(each_c.decoded_content)
                data = {"description":description,"readme":raw_content,"url":url,"name":str(full_name)}
                all_json_results.append(data)
        except Exception as e:
            print("[EXCEPTION] : ",e,full_name)
            
    if all_json_results:
        with open(os.path.join(data_path,'data.json'),'w') as f:
            json.dump(all_json_results, f)
        f.close()

if pattern == "update":
    Update_Data()

if not os.path.exists(data_path):
    os.makedirs(data_path)
    Update_Data()
else:
    if not os.path.exists(os.path.join(data_path,'data.json')):
        Update_Data()

with open(os.path.join(data_path,'data.json')) as f:
    all_json_results = json.load(f)
f.close()
    
for i in all_json_results:
    url = i['url']
    all_data = i['readme'] + i['description'] + i['url'] + i['name']
    if re.search(pattern,all_data,re.I):
        print(url.replace('https://api.github.com/repos','https://github.com'))
