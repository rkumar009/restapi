from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^login$',views.userLogin,name="userLogin"),

    url(r'^CreatUser',views.CreatUser,name="CreatUser")

]