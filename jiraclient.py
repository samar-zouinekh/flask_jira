from flask import request, Flask, jsonify
import json
import csv
import requests
from requests.auth import HTTPBasicAuth
import xlrd 
import re
import os
from pymongo import MongoClient
from jira import JIRA
import urllib3
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from time import time

jiraServer = "https://primainternship.atlassian.net"
jiraUser = "zouinekhsamar97@gmail.com"
jiraPass = "BX2uroYD0625Vhrenm0U0D86"
global jira
global project_name
try:
    jira = JIRA(basic_auth=(jiraUser, jiraPass),options={'server': jiraServer})
    project_name="WM3D"
except Exception as e:
    print('unable to connect to jira server\n', 'Error : '+str(e))
app = Flask(__name__)
@app.route('/project')
def get_all_projects():
    global project

    try:
        res = {}
        affichage=[]
        projects = jira.projects()
        for project in projects:
            res={"key": str(project.key)  , "id":str(project.id),
                 "name": str(project.name),"projectTypeKey": str(project.projectTypeKey)
                 
                 }
            affichage.append(res)
        return (json.dumps(affichage))
    except Exception as e:
        print('unable to get projects \n', 'Error : '+str(e))
        return ("error")

@app.route('/issue')
def get_all_issues():

    
    res = {}
    affichage=[]
    projects = jira.projects()


    for i in range(len(projects)):
        print (i)
        
        size = 100
        initial = 0
        start= initial*size
        issues = jira.search_issues('project='+str(projects[i]),  start,size)
        
        initial += 1
        for issue in issues:
            
            res={"Key": str(issue),
                 "IssueType": str(issue.fields.issuetype.name),
                 "Status":str (issue.fields.status.name),
                 "Summary":str (issue.fields.summary),
                 "Created": str(issue.fields.created),
                 "Lables":str(issue.fields.labels),
                 "Priority":str (issue.fields.priority),
                 "Components":str ( issue.fields.components),
                 "Creator":str ( issue.fields.creator),
                 "Summary": str (issue.fields.duedate),
                 "Duedate":str ( issue.fields.duedate),
                 "ResolutionDate":str ( issue.fields.resolutiondate),
                 "Description":str ( issue.fields.description)}
            affichage.append(res)
    return(json.dumps(affichage))    


@app.route('/createIssue',methods = ['POST'])
def createIssue():
    if request.method == 'POST':
      res={"status": "error"}  
      if 'project'  in request.form : 
          project = request.form['project']
          summary = request.form['summary']
          description = request.form['description']
          issuetype = request.form['issuetype']
          '''new_issue = jira.create_issue(project='PM', summary='New issue from jira-python',
                                  description='Look into this one', issuetype={'name': 'Bug'})'''
          new_issue = jira.create_issue(project=str(project), summary=summary,
                                  description="desc", issuetype={'name': str(issuetype)})

          res={"status": "created"}
      else :
         res={"status": "NOTE created"}
    return(json.dumps(res))


@app.route('/updateissue',methods = ['POST'])
def updateissue():
    if request.method == 'POST':
      res={"status": "POST"}  
      if 'issuekey'  in request.form : 
          key = request.form['issuekey']
          summary = request.form['summary']
          description = request.form['description']       
          issue = jira.issue(key)
          issue.update(summary=summary, description=description)
          res={"status": "updated"}
      else :
         res={"status": "not updated"}
    return(json.dumps(res))  

@app.route('/deleteissue/<key_issue>')
def deleteIssue(key_issue):     
    issue = jira.issue(str(key_issue))
    issue.delete()
    res={"status": "deleted"}
    return(json.dumps(res))  


@app.route('/getIssuesByProject/<project_name>')
def getIssue(project_name):

    size = 100
    initial = 0
    res = {}
    affichage=[]
    while True:
        start= initial*size
        issues = jira.search_issues('project='+str(project_name),  start,size)
        if len(issues) == 0:
            break
        initial += 1
        for issue in issues:
             res={"Key": str(issue),
                     "IssueType": str(issue.fields.issuetype.name),
                     "Status":str (issue.fields.status.name),
                     "Summary":str(issue.fields.summary),
                     "Created": str(issue.fields.created),
                     "Lables":str(issue.fields.labels),
                     "Priority":str (issue.fields.priority),
                     "Components":str ( issue.fields.components),
                     "Creator":str ( issue.fields.creator),
                     "Summary": str (issue.fields.duedate),
                     "Duedate":str ( issue.fields.duedate),
                     "ResolutionDate":str ( issue.fields.resolutiondate),
                     "Description":str ( issue.fields.description)
                     }
             affichage.append(res)
    return (json.dumps(affichage)) 


@app.route('/getsprintbyid/<idboard>')
def getSprintById(idboard):
    sprints = jira.sprints(idboard)
    res = {}
    affichage=[]
    for sprint in sprints :
        print (sprint.id)
        res={"id": str(sprint.id),
                     "Sprint name": str(sprint.name)}
        
        affichage.append(res)
    return (json.dumps(affichage))    


@app.route('/getprojectbyid/<idproject>')
def getProjectById(idproject):
    project = jira.project(idproject)
    res={"key": str(project.key),
                 "name": str(project.name),"projectTypeKey": str(project.projectTypeKey)
                 }
    return (json.dumps(res))  
@app.route('/createproject',methods = ['POST'])
def createIssue():
    if request.method == 'POST':
      res={"status": "error"}  
      if 'projkey'  in request.form : 
          projkey = request.form['projkey']
          projname = request.form['projname']
          projtype = request.form['projtype']
          jira.create_project(projkey, projname, jiraUser, projtype)

          res={"status": "created"}
      else :
         res={"status": "NOTE created"}
    return(json.dumps(res)) 
@app.route('/updateproject',methods = ['POST'])
def updateproject():
    if request.method == 'POST':
      res={"status": "POST"}  
      if 'projkey'  in request.form : 
          key = request.form['projkey']
          name = request.form['projname']
          projtype = request.form['projtype']       
          project = jira.project(key)
          project.update(name=name, ptype=projtype)
          res={"status": "updated"}
      else :
         res={"status": "not updated"}
    return(json.dumps(res)) 

if __name__ == "__main__":
    app.run()
