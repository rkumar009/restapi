import datetime
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
import requests
import base64
import sys
import json
from django import forms
import xml.etree.ElementTree as ET
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from mobile_app_backend.models import UserProfile

# --- this api create a new userprofile-------------------
@csrf_exempt
def CreatUser(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    userName = json.loads(request.body.decode('utf-8'))['userName']
    emailID =json.loads(request.body.decode('utf-8'))['emailId']
    currentCity=json.loads(request.body.decode('utf-8'))['currentCity']
    currentCompany = json.loads(request.body.decode('utf-8'))['currentCompany']
    userPassword=json.loads(request.body.decode('utf-8'))['userPassword']

    # -------- create session id and pass into the object of userprofile----------You have to do----
    newUser= UserProfile(userName=userName, emailID=emailID, mobileNo=mobileNo, currentCity=currentCity, currentCompany=currentCompany)
    newUser.save()

    return HttpResponse(json.dumps({"response":"","sessionId":"sessionId"}), content_type='application/json')

# --- this api take user mobile no, password and sessionId and allow user to login into app------------
@csrf_exempt
def UserLogin(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    userPassword = json.loads(request.body.decode('utf-8'))['userPassword']
    sessionId=json.loads(request.body.decode('utf-8'))['sessionId']
    alluser=UserProfile.objects.all();
    currentUser=alluser.get(mobileNo=mobileNo)
    userPassword1=getattr(currentUser, UserProfile.userPassword)
    userSessionId = getattr(currentUser,UserProfile.userSessionId)

    if(userPassword==userPassword1 & sessionId == userSessionId):
        return HttpResponse(json.dumps({"response":"login-success"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"response": "login-failed"}), content_type='application/json')

# this api is used to update user profile----------------

@csrf_exempt
def UpdateUserProfile(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    sessionId = json.loads(request.body.decode('utf-8'))['sessionId']
    userName = json.loads(request.body.decode('utf-8'))['userName']
    emailID = json.loads(request.body.decode('utf-8'))['emailId']
    currentCity = json.loads(request.body.decode('utf-8'))['currentCity']
    currentCompany = json.loads(request.body.decode('utf-8'))['currentCompany']
    userPassword = json.loads(request.body.decode('utf-8'))['userPassword']

    UserProfile.objects.filter(mobileNo=mobileNo).update(userName=userName,emailID=emailID,currentCity=currentCity,currentCompany=currentCompany,userPassword=userPassword)

    # return "profile-update-success" if user profile is updated successfully------------------------------
    return HttpResponse(json.dumps({"response":"profile-update-success"}), content_type='application/json')

# this api is used to get user-profile details which will load on the user profile page on android-app-- and can be update from their

@csrf_exempt
def getUserDetails(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    sessionId = json.loads(request.body.decode('utf-8'))['sessionId']

    alluser = UserProfile.objects.all();
    currentUser = alluser.get(mobileNo=mobileNo)
    userName = getattr(currentUser, UserProfile.userName)
    emailID = getattr(currentUser, UserProfile.emailID)
    currentCity = getattr(currentUser, UserProfile.currentCity)
    currentCompany = getattr(currentUser, UserProfile.currentCompany)
    userPassword = getattr(currentUser, UserProfile.userPassword)

    return HttpResponse(json.dumps({"success":True, "user-details":{"userName":userName,"emailId":emailID,"currentCity":currentCity,"currentCompany":currentCompany}}),
        content_type='application/json')

@csrf_exempt
def searchUserByName(request):
    seachName = json.loads(request.body.decode('utf-8'))['name']
    sessionId = json.loads(request.body.decode('utf-8'))['sessionId']

    alluser = UserProfile.objects.all();
    currentUser=[]
    for user in alluser:
        if getattr(user, UserProfile.userName)==seachName:
            currentUser.append(user)
    return HttpResponse(json.dumps({"success":True, "user-list":currentUser}),
        content_type='application/json')
#  bonuse requrement ----------------------

@csrf_exempt
def searchUserByMobileNo(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNo']
    sessionId = json.loads(request.body.decode('utf-8'))['sessionId']
    alluser = UserProfile.objects.all();
    currentUser=None
    for user in alluser:
        if (getattr(currentUser, UserProfile.mobileNo)==mobileNo):
            currentUser=user
    if(currentUser!=None):
        return HttpResponse(json.dumps({"success":True, "user":currentUser}),
        content_type='application/json')
    else:
        return HttpResponse(json.dumps({"success": False, "user": "null"}),
                            content_type='application/json')

@csrf_exempt
def markMobileNoSpam(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNo']
    sessionId = json.loads(request.body.decode('utf-8'))['sessionId']
    alluser = UserProfile.objects.all();
    currentUser=None
    for user in alluser:
        if (getattr(currentUser, UserProfile.mobileNo)==mobileNo):
            currentUser=user

    if(currentUser!=None):

        return HttpResponse(json.dumps({"success":True, "user":currentUser}),
        content_type='application/json')
    else:
        return HttpResponse(json.dumps({"success": False, "user": "null"}),
                            content_type='application/json')