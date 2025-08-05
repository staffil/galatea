from django.urls import path
from .views import PaymentView, verify_payment

urlpatterns = [
    path('guest/', PaymentView.as_view(), name='payment'),  # /payment/ → HTML 렌더링
    path('verify_payment/', verify_payment, name='verify_payment'),  # /payment/verify_payment/
]
