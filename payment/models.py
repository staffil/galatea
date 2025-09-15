from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
import requests
from payment.models import Payment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from payment.models import Payment, PaymentMethod, PaymentRank, PaymentStats, TokenHistory, Token
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import time

# PG사 매핑
PG_MAPPING = {
    "card": "KG",        # 카드 결제는 KG로 매핑
    "kakao": "KakaoPay",
    "paypal": "PayPal",
    # 필요한 PG사 추가 가능
}

class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'payment/payment.html'
    login_url = '/login/'

@login_required
def payment_choice(request):
    payment_rank = PaymentRank.objects.all()
    context = {"plans": payment_rank}
    return render(request, "payment/payment_choice.html", context)

# 아임포트 Access Token 발급
def get_access_token():
    url = "https://api.iamport.kr/users/getToken"
    data = {"imp_key": settings.IAMPORT_API_KEY, "imp_secret": settings.IAMPORT_API_SECRET}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"토큰 발급 실패: {response.text}")
    return response.json()["response"]["access_token"]

@login_required
def verify_payment(request):
    try:
        imp_uid = request.GET.get("imp_uid")
        merchant_uid = request.GET.get("merchant_uid")
        rank_id = int(request.GET.get("rank_id"))

        plan = PaymentRank.objects.get(id=rank_id)
        if plan.freetoken is None:
            plan.freetoken = 0

        access_token = get_access_token()
        url = f"https://api.iamport.kr/payments/{imp_uid}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        res_json = response.json()

        if res_json.get("code") != 0 or "response" not in res_json:
            return JsonResponse({"error": _("결제 검증 실패"), "detail": res_json}, status=400)

        payment_data = res_json["response"]
        payment_status = payment_data.get("status")
        pay_method_code = payment_data.get("pay_method")
        
        # PG사 매핑
        pay_method_name = PG_MAPPING.get(pay_method_code.lower(), pay_method_code)
        payment_method = PaymentMethod.objects.filter(name__iexact=pay_method_name).first()
        if not payment_method:
            return JsonResponse({"error": f"등록되지 않은 결제수단: {pay_method_code}"}, status=400)

        # Payment 객체 생성
        payment = Payment.objects.create(
            user=request.user,
            amount=payment_data.get("amount", 0),
            payment_method=payment_method,
            status=payment_status,
            imp_uid=imp_uid,
            merchant_uid=merchant_uid,
            payment_rank=plan,
            customer_uid=payment_data.get("customer_uid", "")
        )

        # 결제 성공 시 Token 충전
        if payment_status == "paid":
            token, _ = Token.objects.get_or_create(user=request.user)
            token.total_token += Decimal(plan.freetoken)
            token.payment = payment
            token.save()

            TokenHistory.objects.create(
                user=request.user,
                change_type=TokenHistory.CHARGE,
                amount=plan.freetoken,
                total_voice_generated=0
            )

        # PaymentStats 갱신
        stats, _ = PaymentStats.objects.get_or_create(id=1)
        stats.total_payments += 1
        if payment_status == "paid":
            stats.success_count += 1
        elif payment_status == "failed":
            stats.failure_count += 1
        elif payment_status == "ready":
            stats.pending_count += 1
        elif payment_status == "cancelled":
            stats.refunded_count += 1
        stats.save()

        return JsonResponse({"message": _("결제 처리 완료"), "status": payment_status})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def payment_charge(request):
    if request.method == "POST":
        rank_id = int(request.POST.get("rank_id"))
        plan = PaymentRank.objects.get(id=rank_id)
        available_pgs = PaymentMethod.objects.filter(is_active=True)
        context = {"plan": plan, "available_pgs": available_pgs}
        return render(request, "payment/payment.html", context)
    else:
        return redirect('payment:payment_choice')

@login_required
def payment_complete(request):
    latest_payment = Payment.objects.filter(user=request.user).order_by('-paid_at').first()
    status = latest_payment.status if latest_payment else "unknown"
    return render(request, "payment/payment_complete.html", {"status": status})

@login_required
def auto_charge(request, rank_id):
    try:
        user = request.user
        plan = PaymentRank.objects.get(id=rank_id)
        if plan.freetoken is None:
            plan.freetoken = 0

        last_payment = Payment.objects.filter(user=user, customer_uid__isnull=False).order_by('-paid_at').first()
        if not last_payment:
            return JsonResponse({"error": _("자동 결제 가능한 카드가 없습니다.")}, status=400)

        data = {
            "merchant_uid": f"auto_{int(time.time())}",
            "customer_uid": last_payment.customer_uid,
            "amount": plan.price,
            "name": f"자동충전 {plan.rankname}",
            "buyer_email": user.email,
        }

        access_token = get_access_token()
        url = "https://api.iamport.kr/subscribe/payments/again"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(url, json=data, headers=headers)
        res_json = response.json()

        if res_json.get("code") != 0 or "response" not in res_json:
            return JsonResponse({"error": _("자동 결제 실패"), "detail": res_json}, status=400)

        payment_data = res_json["response"]
        payment_status = payment_data.get("status")
        pay_method_code = payment_data.get("pay_method")
        pay_method_name = PG_MAPPING.get(pay_method_code.lower(), pay_method_code)
        payment_method = PaymentMethod.objects.filter(name__iexact=pay_method_name).first()

        Payment.objects.create(
            user=user,
            amount=plan.price,
            status=payment_status,
            payment_rank=plan,
            customer_uid=last_payment.customer_uid,
            payment_method=payment_method
        )

        return JsonResponse({"message": _("자동 결제 완료"), "status": payment_status})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
