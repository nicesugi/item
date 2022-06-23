from django.urls import path
from item import views

urlpatterns = [
    path('', views.ItemView.as_view()),
    path('order/', views.ItemOrderView.as_view()),
]