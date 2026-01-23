from django import forms
from user_auth.models import Requests

class RequestForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['title', 'content', 'is_secret']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '제목을 입력하세요'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': '요청 내용을 입력하세요'}),
            'is_secret': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'is_secret': '비밀글로 작성',
        }


from django import forms
from user_auth.models import Requests

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['response']  # content는 안 바뀌도록
        widgets = {
            'response': forms.Textarea(attrs={'rows':4, 'placeholder':'관리자 응답 작성'})
        }


from django import forms
from customer_ai.models import Prompt

class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        # fields = ['prompt_title', 'prompt', 'prompt_type']
        fields = ['prompt_title', 'prompt']
