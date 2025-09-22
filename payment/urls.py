from django.urls import path
from payment.views import PaymentView, verify_payment, verify_payment_v2
from payment import views

urlpatterns = [
    path("", views.payment_choice, name= 'chocie'),
    path('pay/', PaymentView.as_view(), name='payment'),  
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('verify_payment_v2/', verify_payment_v2, name='verify_payment_v2'),
    path('charge/', views.payment_charge, name="payment_charge"),
    path('payment_detail/', views.payment_detail, name="payment_detail"),
]
