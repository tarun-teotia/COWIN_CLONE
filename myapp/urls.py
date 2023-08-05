from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('homepage', views.home, name='home'),
    path('slot_check', views.slot, name='slot'),
    path('down_cert', views.cert, name='cert'),
    path('about', views.about, name='about'),
]