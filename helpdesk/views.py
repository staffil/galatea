from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from user_auth.models import Faq
from helpdesk.forms import RequestForm
from django.contrib import messages
from user_auth.models import Requests
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.translation import gettext_lazy as _

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
            messages.success(request, _("요청이 정상적으로 제출되었습니다."))
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
        messages.error(request, _("이 글에 접근할 권한이 없습니다."))
        return redirect('helpdesk:request')

    if request.user.is_superuser:
        if request.method == 'POST':
            form = ResponseForm(request.POST, instance=request_board)
            if form.is_valid():
                form.save()
                messages.success(request, _("응답이 저장되었습니다."))
                return redirect('helpdesk:request_detail', pk=pk)
        else:
            form = ResponseForm(instance=request_board)
    else:
        form = None

    return render(request, 'helpdesk/request_detail.html', {
        'request_list': request_board,
        'response_form': form
    })

@login_required
def request_delete(request, pk):
    request_form = get_object_or_404(Requests, id = pk)
    if request.user != request_form.user:
        messages.error(request, _("수정 권한이 없습니다."))
        return redirect('helpdesk:request', pk=pk)
    request_form.delete()
    messages.success(request, _("요청사항이 삭제 되었습니다"))
    return redirect("helpdesk:request")


from user_auth.models import Notice

def notice(request):
    notice = Notice.objects.order_by("-created_at")

    context= {
        "notice_list" : notice
    }


    return render(request, "helpdesk/notice.html", context)


def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    context= {
        "notice": notice
    }


    return render (request,"helpdesk/notice_detail.html", context)

from customer_ai.models import Prompt
@login_required
def prompt_share(request):
    prompt = Prompt.objects.order_by("-created_at")
    context = {
        "prompt_list": prompt
    }

    return render(request, "helpdesk/prompt_share.html", context)

from helpdesk.forms import PromptForm

@login_required
def prompt_share_write(request):
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt_instance = form.save(commit=False)
            prompt_instance.user = request.user
            prompt_instance.save()
            return redirect('helpdesk:prompt_share')
    else:  # GET 요청 시
        form = PromptForm()

    # POST 실패(is_valid=False)도 여기서 처리
    return render(request, "helpdesk/prompt_share_write.html", {"form": form})

@login_required
def prompt_share_detail(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)

    context = {
        "prompt": prompt
    }
    return render(request, "helpdesk/prompt_share_detail.html", context)


@login_required
def prompt_share_delete(request, prompt_id):
    prompt = get_object_or_404(Prompt ,id=prompt_id)

    if request.user != prompt.user:
        messages.error(request, _("삭제 권한이 없습니다."))
        return redirect('helpdesk:prompt_share_detail', prompt_id=prompt.id)
    prompt.delete()
    messages.success(request, _("프롬프트가 삭제 되었습니다."))
    return redirect("helpdesk:prompt_share")


@login_required
def prompt_share_update(request, prompt_id):
    prompt = get_object_or_404(Prompt, id= prompt_id)

    if request.user != prompt.user:
        messages.error(request, _("수정 권한이 없습니다."))
        return redirect('helpdesk:prompt_share_detail', prompt_id=prompt.id)
    
    if request.method =="POST":
        form = PromptForm(request.POST , instance=prompt)
        if form.is_valid():
            form.save()
            messages.success(request, _("프롬프트가 수정되었습니다."))
            return redirect('helpdesk:prompt_share_detail', prompt_id=prompt.id)
        
    else:
        form = PromptForm(instance=prompt)

    return render(request, "helpdesk/prompt_share_update.html", {"form": form, "prompt": prompt})