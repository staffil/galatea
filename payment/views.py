from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
import requests
from .models import Payment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from payment.models import Payment,PaymentMethod,PaymentRank,PaymentStats
from django.utils.translation import gettext_lazy as _

class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'payment/payment.html'
    login_url = '/login/'

@login_required
def payment_choice(request):
    payment_rank = PaymentRank.objects.all()

    context = {
        "plans": payment_rank
    }
    return render(request, "payment/payment_choice.html", context)







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

from payment.models import TokenHistory, Token
# 결제 검증
@login_required
def verify_payment(request):
    imp_uid = request.GET.get("imp_uid")
    merchant_uid = request.GET.get("merchant_uid")
    rank_id = int(request.GET.get("rank_id"))

    # 결제 등급 가져오기
    try:
        plan = PaymentRank.objects.get(id=rank_id)
    except PaymentRank.DoesNotExist:
        return JsonResponse({"error": _("잘못된 등급 ID")}, status=400)

    # 아임포트에서 결제 정보 가져오기
    access_token = get_access_token()
    url = f"https://api.iamport.kr/payments/{imp_uid}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    res_json = response.json()

    if res_json["code"] != 0:
        return JsonResponse({"error": _("결제 검증 실패"), "detail": res_json}, status=400)

    payment_data = res_json["response"]
    payment_status = payment_data.get("status")

    # Payment 테이블 생성
    payment = Payment.objects.create(
        user=request.user,
        amount=payment_data["amount"],
        payment_method=PaymentMethod.objects.first(),  # 실제 결제 방식과 매핑 필요
        status=payment_status,
        imp_uid=imp_uid,
        merchant_uid=merchant_uid,
        payment_rank=plan
    )

    # 결제 성공 시 Token 충전
    if payment_status == "paid":
        token, created = Token.objects.get_or_create(user=request.user)
        token.total_token += plan.freetoken  # PaymentRank에 저장된 토큰 수량
        token.payment = payment
        token.save()

        # TokenHistory 기록
        TokenHistory.objects.create(
            user=request.user,
            change_type=TokenHistory.CHARGE,
            amount=plan.freetoken,
            total_voice_generated=0
        )

    if payment_status == "paid":
        payment.customer_uid = payment_data.get("customer_uid")
        payment.save()

    # PaymentStats 갱신
    stats, created = PaymentStats.objects.get_or_create(id=1)  # 단일 통계 레코드
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

from payment.models import PaymentMethod
@login_required
def payment_charge(request):
    if request.method == "POST":
        rank_id = int(request.POST.get("rank_id"))
        plan = PaymentRank.objects.get(id=rank_id)
        payment_method = PaymentMethod.objects.all()

        # 모든 PG사 허용
        available_pgs = ['kakaopay', 'paypaltest', ]
# 'html5_inicis'
        context = {
            "plan": plan,
            "available_pgs": available_pgs,
        }

        return render(request, "payment/payment.html", context)
    else:
        return redirect('payment:payment_choice')


@login_required
def payment_complete(request):
    latest_payment = Payment.objects.filter(user=request.user).order_by('-paid_at').first()
    status = latest_payment.status if latest_payment else "unknown"
    return render(request, "payment/payment_complete.html", {"status": status})

import time
@login_required
def auto_charge(request, rank_id):
    user = request.user
    plan = PaymentRank.objects.get(id=rank_id)
    
    # 가장 최근 카드 토큰 가져오기
    last_payment = Payment.objects.filter(user=user, customer_uid__isnull=False).order_by('-paid_at').first()
    if not last_payment:
        return JsonResponse({"error": _("자동 결제 가능한 카드가 없습니다.")}, status=400)

    # 아임포트 재결제 요청
    data = {
        "merchant_uid": f"auto_{int(time.time())}",
        "customer_uid": last_payment.customer_uid,
        "amount": plan.amount,
        "name": f"자동충전 {plan.name}",
        "buyer_email": user.email,
    }

    access_token = get_access_token()
    url = "https://api.iamport.kr/subscribe/payments/again"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, json=data, headers=headers)
    res_json = response.json()

    if res_json["code"] != 0:
        return JsonResponse({"error": _("자동 결제 실패"), "detail": res_json}, status=400)

    # DB 업데이트
    Payment.objects.create(
        user=user,
        amount=plan.amount,
        status="paid",
        payment_rank=plan,
        customer_uid=last_payment.customer_uid
    )
    return JsonResponse({"message": _("자동 결제 완료")})