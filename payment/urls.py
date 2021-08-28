from django.django.urls import path
from . import views


app_name = 'payment'


urlpatterns = [
    path('process/', views.PaymentProcessView.as_view(), name='process')
    
]