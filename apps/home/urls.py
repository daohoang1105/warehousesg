# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('manageform/', views.manageform, name="manageform"),
    path('manage-spare/<str:pk>/', views.managespare, name="manage-spare"),
    path('update-spare/<str:pk>/', views.updateSpare, name="update-spare"),
    path('delete-spare/<str:pk>/', views.deleteSpare, name="delete-spare"),
    path('uploadall/', views.uploadall, name="uploadall"),
    path('manageSparePartOut/', views.manageSparePartOut, name="manageSparePartOut"),
    path('managetable/', views.manageTable, name="manageTable"),
    path('managesparepartouttable/', views.managesparepartouttable, name="managesparepartouttable"),
    path('upload/', views.upload, name="upload"),
    path('request/', views.requestsparepartout, name="requestsparepartout"),
    re_path(r'^.*\.*', views.pages, name='pages'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
