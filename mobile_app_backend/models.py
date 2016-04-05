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
    list_display = ('userName','','creationTime')
    search_fields = ['userName', 'mobileNo']
    def userName(self,obj):
        return obj.UserProfile.userName
    def mobileNo(self,obj):
        return obj.UserProfile.mobileNo