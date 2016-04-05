from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^login$',views.userLogin,name="userLogin"),

    url(r'^CreatUser',views.CreatUser,name="CreatUser"),
    url(r'^UserLogin', views.UserLogin, name="UserLogin"),
    url(r'^UpdateUserProfile', views.UpdateUserProfile, name="UpdateUserProfile"),
    url(r'^getUserDetails', views.getUserDetails, name="getUserDetails"),
    url(r'^searchUserByName', views.searchUserByName, name="searchUserByName"),
    url(r'^searchUserByMobileNo', views.searchUserByMobileNo, name="searchUserByMobileNo")

]