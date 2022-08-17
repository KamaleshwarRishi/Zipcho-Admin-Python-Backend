from django.urls import include, path
from .views import *

urlpatterns = [
    #path("dashboard", dashboard, name= 'dashboard'),
    path("getAllLanguages", getAllLanguages, name= 'getAllLanguages'),
    path("getAllInterests", getAllInterests, name= "getAllInterests"),
    path("getAllGender", getAllGender, name= "getAllGender"),
    path("getAllCategories", getAllCategories, name= "getAllCategories"),
    path("getAllCountries", getAllCountries, name= "getAllCountries"),
    path ("getAllUser", getAllUser, name="getAllUser")
]