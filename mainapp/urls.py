
from django.contrib import admin
from django.urls import path
from mainapp import views
 
urlpatterns = [
    path('', views.index, name="todo-mainapp"),
    path('del/<str:item_id>', views.remove, name="del"),
]