document.addEventListener("DOMContentLoaded", function() {
    const sliders = ["temperature", 'stability', 'style', 'speed'];

    sliders.forEach(id => {
        const slider = document.getElementById(id);
        const output = document.getElementById(id + "Value");
        if (slider && output) {
            output.textContent = slider.value; 
            slider.addEventListener('input', function() {
                output.textContent = this.value;
            });
        }
    });
});

function check(){
    return confirm(messages.aiGenerateConfirm);
}

function selectVoiceId(voiceId){
    const input = document.getElementById('voice_id');
    if(input){
        input.value = voiceId;
        alert(messages.voiceSelected);
    }
}

// 쿠키에서 CSRF 토큰 읽기 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.getElementById("auto_prompt").addEventListener("click", function(){
    const userPromptInput  = document.getElementById('prompt').value.trim()

    if (!userPromptInput){
        alert(messages.promptRequired);
        return;
    }

    fetch(AUTO_PROMPT_URL, {
        method :"POST",
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body : JSON.stringify({prompt:userPromptInput})
    })
    .then(res => res.json())
    .then(data =>{
        if (data.status == 'success'){
            document.getElementById("prompt").value = data.refine_data;
            alert(messages.promptRefined);
        } else {
            alert(messages.promptError);
        }
    })
    .catch(err => {
        console.error(err);
        alert(messages.serverError);
    })
});

document.addEventListener("DOMContentLoaded", function() {
    // 슬라이더 값 표시
    const sliders = ["temperature", "stability", "style", "speed"];
    sliders.forEach(id => {
        const slider = document.getElementById(id);
        const output = document.getElementById(id + "Value");
        if (slider && output) {
            output.textContent = slider.value;
            slider.addEventListener("input", function() {
                output.textContent = this.value;
            });
        }
    });

    // 폼 제출 전에 유효성 검사
    const form = document.querySelector("form");
    form.addEventListener("submit", function(e) {
        const prompt = document.getElementById("prompt").value.trim();
        const voiceId = document.getElementById("voice_id").value.trim();

        if (!prompt) {
            alert(messages.promptRequired);
            e.preventDefault(); // 폼 제출 막기
            return false;
        }

        if (!voiceId) {
            alert(messages.voiceSelectRequired);
            e.preventDefault(); // 폼 제출 막기
            return false;
        }
    });
});

// 선택 버튼 클릭 시 voice_id 입력
function selectVoiceId(voiceId){
    const input = document.getElementById('voice_id');
    if(input){
        input.value = voiceId;
        alert(messages.voiceSelected);
    }
}