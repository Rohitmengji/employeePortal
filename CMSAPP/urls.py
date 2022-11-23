from django.contrib import admin
from django.urls import path
from CMSAPP import views
from . import views

urlpatterns = [
    path("userregister/",views.userregistercode),
    path("login/",views.login),
    path("",views.login),
    
    ## 
    path("uploadfile/",views.UploadFilecode),
    path("adminhome/",views.adminhome),
    path("adminviewusers/",views.registerdisplayCode),
    path("adminviewfiles/",views.uploaddisplayCode),
    path("checkduplicate/",views.checkduplicate),

    path("viewusers/",views.viewusers),
    path("myfriends/",views.myfriends),
    path("usermessages/",views.usermessages),
    path("acceptedrequest/",views.acceptedrequest),
    path("userhome/",views.userhome),




]
