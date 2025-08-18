from django.urls import path
from payment.views import PaymentView, verify_payment
from payment import views

urlpatterns = [
    path("", views.payment_choice, name= 'chocie'),
    path('pay/', PaymentView.as_view(), name='payment'),  # /payment/ → HTML 렌더링
    path('verify_payment/', verify_payment, name='verify_payment'),  # /payment/verify_payment/
    path('charge/', views.payment_charge, name="payment_charge")
]
