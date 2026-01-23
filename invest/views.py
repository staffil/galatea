

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def invest_code(request):
    user = request.user
    # 유저 referral_code는 save()에서 자동 생성되므로 바로 사용 가능
    invite_link = f"{request.scheme}://{request.get_host()}/register/?ref={user.referral_code}"

    context = {
        "referral_code": user.referral_code,
        "invite_link": invite_link
    }

    return render(request, "invest/invest.html", context)
