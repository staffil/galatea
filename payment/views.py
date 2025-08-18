from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
import requests
from .models import Payment
from django.shortcuts import render, redirect

# 결제 페이지
class PaymentView(TemplateView):
    template_name = 'payment/payment.html'  # ✅ 앱별 디렉토리 경로


def payment_choice(request):
    return render(request, "payment/payment_choice.html")

# 아임포트 Access Token 발급
def get_access_token():
    url = "https://api.iamport.kr/users/getToken"
    data = {
        "imp_key": settings.IAMPORT_API_KEY,
        "imp_secret": settings.IAMPORT_API_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"토큰 발급 실패: {response.text}")
    return response.json()["response"]["access_token"]

# 결제 검증
def verify_payment(request):
    imp_uid = request.GET.get("imp_uid")
    merchant_uid = request.GET.get("merchant_uid")

    # 디버깅용 출력
    print("IAMPORT_API_KEY:", settings.IAMPORT_API_KEY)
    print("IAMPORT_API_SECRET:", settings.IAMPORT_API_SECRET)
    print("imp_uid:", imp_uid)
    print("merchant_uid:", merchant_uid)

    access_token = get_access_token()
    url = f"https://api.iamport.kr/payments/{imp_uid}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return JsonResponse({"error": "아임포트 서버 오류", "detail": response.text}, status=500)

    res_json = response.json()
    if res_json["code"] == 0:
        payment_data = res_json["response"]
        Payment.objects.create(
            user=request.user,
            amount=payment_data["amount"],
            payment_method=payment_data["pay_method"],
            status=payment_data["status"],
            imp_uid=imp_uid,
            merchant_uid=merchant_uid
        )
        return JsonResponse({"message": "결제 검증 및 저장 성공", "status": payment_data["status"]})
    else:
        return JsonResponse({"error": "결제 검증 실패", "detail": res_json}, status=400)
    

from payment.models import TokenHistory
def payment_charge(request):
    user = request.user
    
    TokenHistory.objects.create(
        user = user,
        change_type = TokenHistory.CHARGE,
        amount= 300
    )
    return redirect('home:main')
