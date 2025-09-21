document.addEventListener("DOMContentLoaded", function () {
    const sliders = ["stability", "speed", "style", "temperature"];
    
    sliders.forEach(id => {
        const slider = document.getElementById(id);
        const output = document.getElementById(id + "Value");
        
        if (slider && output) {
            // 초기값 설정
            output.textContent = slider.value;
            
            // 슬라이더 변경 이벤트
            slider.addEventListener('input', function () {
                output.textContent = this.value;
            });
        }
    });

    // 폼 제출 Ajax 처리
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault(); // 기본 제출 막기
            const formData = new FormData(form);

            fetch("{% url 'mypage:my_ai_models_update' %}", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken")
                }
            })
            .then(res => res.json())
            .then(data => {
                if(data.error){
                    alert("오류 발생: " + data.error);
                } else {
                    alert("AI가 수정되었습니다!");
                    window.location.reload(); // 성공 시 새로고침
                }
            });
        });
    }
});

// 음성 선택 기능
function selectVoiceId(voiceId) {
    const input = document.getElementById('voice_id');
    if (input) {
        input.value = voiceId;
        alert("해당 voice id가 선택되었습니다.");
    }
}
