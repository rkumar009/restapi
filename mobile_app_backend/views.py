
from django.http import HttpResponse

import json
from django.views.decorators.csrf import csrf_exempt
from mobile_app_backend.models import UserProfile, UserContactNumbers, SpamList


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

    try:
        currentUser = UserProfile.objects.get(pk=mobileNo)
    except UserProfile.DoesNotExist:
        currentUser = None
    if (currentUser):
        return HttpResponse(json.dumps({"response":"failed","message":"User Already Exit"}), content_type='application/json')
    else:
        newUser= UserProfile(userName=userName, emailID=emailID, mobileNo=mobileNo, currentCity=currentCity, currentCompany=currentCompany)
        newUser.save()
        return HttpResponse(json.dumps({"response":"success","sessionId":"sessionId"}), content_type='application/json')

# --- this api take user mobile no, password and sessionId and allow user to login into app------------
@csrf_exempt
def UserLogin(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    userpassword = json.loads(request.body.decode('utf-8'))['userPassword']
    # sessionId=json.loads(request.body.decode('utf-8'))['sessionId']
    try:
        currentUser = UserProfile.objects.get(pk=mobileNo)
    except UserProfile.DoesNotExist:
        currentUser = None
    if(currentUser):
        if(currentUser.userPassword==userpassword):
            return HttpResponse(json.dumps({"response":"login-success"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"response": "login-failed"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"response": "user does not exist"}), content_type='application/json')

# this api is used to update user profile----------------

@csrf_exempt
def UpdateUserProfile(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    # sessionId = json.loads(request.body.decode('utf-8'))['sessionId']
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
    # sessionId = json.loads(request.body.decode('utf-8'))['sessionId']
    try:
        currentUser = UserProfile.objects.get(pk=mobileNo)
    except UserProfile.DoesNotExist:
        currentUser = None
    if(currentUser):
        userName = currentUser.userName
        emailID = currentUser.emailID
        currentCity = currentUser.currentCity
        currentCompany = currentUser.currentCompany
        userPassword = currentUser.userPassword
        return HttpResponse(json.dumps({"response":"Success", "user-details":{"userName":userName,"emailId":emailID,"currentCity":currentCity,"currentCompany":currentCompany}}),
        content_type='application/json')
    else:
        return HttpResponse(json.dumps({"response": "Failed", "user-details": "Null"}), content_type='application/json')

@csrf_exempt
def searchUserByName(request):
    seachName = json.loads(request.body.decode('utf-8'))['name']
    # sessionId = json.loads(request.body.decode('utf-8'))['sessionId']

    sameNameUsers=UserProfile.objects.filter(userName=seachName)
    users=[]
    for user in sameNameUsers:
        response_data = {}
        response_data['name'] = user.userName
        response_data['mobileNo'] = user.mobileNo
        users.append(response_data)

    return HttpResponse(json.dumps({"success":True, "user-list":users}),
        content_type='application/json')

#  bonuse requrement ----------------------

@csrf_exempt
def searchUserByMobileNo(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    # sessionId = json.loads(request.body.decode('utf-8'))['sessionId']
    try:
        currentUser = UserProfile.objects.get(pk=mobileNo)
    except UserProfile.DoesNotExist:
        currentUser = None
    if(currentUser):
        try:
            contact = UserContactNumbers.objects.get(pk=mobileNo)
        except UserProfile.DoesNotExist:
            contact = None
        if(contact):
            name = contact.contactName
        else:
            name=currentUser.userName
        return HttpResponse(json.dumps({"success": True, "user-details": {"userName": name}}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({"failed": True, "user-details":"Null"}),content_type='application/json')

@csrf_exempt
def makeMobileNumberSpam(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    userName = json.loads(request.body.decode('utf-8'))['userName']
    try:
        spamuser = SpamList.objects.get(pk=mobileNo)
    except SpamList.DoesNotExist:
        spamuser = None
    if(spamuser):
        spamcount=spamuser.spamCount
        print(spamcount)
        spamcount=spamcount+1
        if(spamcount<10):
            spamstatus="Normal"
        elif (spamcount>10 & spamcount<50):
            spamstatus = "Low Level"
        elif(spamcount>50 & spamcount<200):
            spamstatus = "Medium Level"
        else:
            spamstatus = "High Level"
        print (spamstatus)
        SpamList.objects.filter(contactNumber=mobileNo).update(spamCount=spamcount,spamStatus=spamstatus)
        return HttpResponse(json.dumps({"success": True}), content_type='application/json')
    else:
        newspamuser=SpamList(contactname=userName, contactNumber=mobileNo,spamCount=1)
        newspamuser.save()
        return HttpResponse(json.dumps({"success": True}),content_type='application/json')

@csrf_exempt
def isSapm(request):
    mobileNo = json.loads(request.body.decode('utf-8'))['mobileNumber']
    print (mobileNo)
    # sessionId = json.loads(request.body.decode('utf-8'))['sessionId']
    try:
        spamuser = SpamList.objects.get(pk=mobileNo)
    except SpamList.DoesNotExist:
        spamuser = None
    if(spamuser):
        print (spamuser.spamStatus)
        spamstatus=spamuser.spamStatus
        return HttpResponse(json.dumps({"spam": True,"status":spamstatus}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({"spam": False}),content_type='application/json')
