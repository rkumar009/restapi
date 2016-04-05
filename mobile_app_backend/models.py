from django.contrib import admin
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    userName=models.CharField(max_length=50, blank=False)
    emailID=models.CharField(max_length=50, blank=False, unique=True)
    mobileNo = models.CharField(primary_key=True,max_length=10, blank=False, unique=True)
    currentCity = models.CharField(max_length=100, blank=True)
    currentCompany = models.CharField(max_length=100, blank=True)
    userPassword=models.CharField(max_length=100, blank=False)
    userSessionId=models.CharField(max_length=100, blank=True)

class UserAdmin(admin.ModelAdmin):
    list_display = ('userName', 'mobileNo')
    search_fields = ['userName', 'mobileNo']
    def userName(self,obj):
        return obj.UserProfile.userName
    def mobileNo(self,obj):
        return obj.UserProfile.mobileNo

admin.site.register(UserProfile,UserAdmin)

class UserContactNumbers(models.Model):
    contactName=models.CharField(max_length=50, blank=False)
    mobileNo = models.CharField(primary_key=True,max_length=10, blank=False, unique=True)

class UserContactNumberAdmin(admin.ModelAdmin):
    list_display = ('contactName', 'mobileNo')
    search_fields = ['contactName', 'mobileNo']
    def userName(self,obj):
        return obj.UserProfile.userName
    def mobileNo(self,obj):
        return obj.UserProfile.mobileNo

admin.site.register(UserContactNumbers,UserContactNumberAdmin)

class SpamList(models.Model):
    contactname=models.CharField(max_length=50, blank=False)
    contactNumber = models.CharField(primary_key=True,max_length=10, blank=False, unique=True)
    spamCount=models.IntegerField(blank=True,default=0)
    spamStatus=models.CharField(max_length=10, default="Normal")

class SpamListAdmin(admin.ModelAdmin):
    list_display = ('contactname', 'contactNumber')
    search_fields = ['contactNumber', 'contactNumber']
    def contactname(self,obj):
        return obj.SpamList.contactname
    def contactNumber(self,obj):
        return obj.SpamList.contactNumber

admin.site.register(SpamList,SpamListAdmin)