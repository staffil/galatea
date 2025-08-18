from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from user_auth.models import Faq
from helpdesk.forms import RequestForm
from django.contrib import messages
from user_auth.models import Requests
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.


def faq(request):
    faq_list = Faq.objects.all()
    return render (request, "helpdesk/FAQ.html", {"faq_list": faq_list})
@login_required
def request(request):
    request_list = Requests.objects.all().order_by('-created_at')
    return render(request, "helpdesk/request.html", {'request_list': request_list})

@login_required
def request_write(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            if request.user.is_authenticated:
                req.user = request.user
            req.save()
            messages.success(request, "요청이 정상적으로 제출되었습니다.")
            return redirect('helpdesk:request')
    else:
        form = RequestForm()
    return render(request, "helpdesk/request_write.html", {'form':form})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_auth.models import Requests
from helpdesk.forms import ResponseForm  # response 전용 폼

@login_required
def request_detail(request, pk):
    request_board = get_object_or_404(Requests, id=pk)

    # 비밀글 권한 체크
    if request_board.is_secret and not (request.user.is_superuser or request.user == request_board.user):
        messages.error(request, "이 글에 접근할 권한이 없습니다.")
        return redirect('helpdesk:request')

    if request.user.is_superuser:
        if request.method == 'POST':
            form = ResponseForm(request.POST, instance=request_board)
            if form.is_valid():
                form.save()
                messages.success(request, "응답이 저장되었습니다.")
                return redirect('helpdesk:request_detail', pk=pk)
        else:
            form = ResponseForm(instance=request_board)
    else:
        form = None

    return render(request, 'helpdesk/request_detail.html', {
        'request_list': request_board,
        'response_form': form
    })



def notice(request):
    return render(request, "helpdesk/notice.html")