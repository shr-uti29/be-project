from django.urls import path, include
from django.contrib import admin
from dcease import views

urlpatterns = [
path('', views.index, name='dcease'),
path('submit',views.submit,name = 'submit')
]
