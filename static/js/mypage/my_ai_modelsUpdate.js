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

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken")
            }
        })
        .then(res => {
            if(!res.ok) return res.json().then(err => { throw err });
            return res.json();
        })
        .then(data => {
            if(data.error){
                alert("오류 발생: " + data.error);
            } else {
                alert("AI가 수정되었습니다!");
                window.location.reload();
            }
        })
        .catch(err =>{
            // 서버가 JSON으로 오류 반환하지 않으면 err 자체가 객체가 아닐 수 있음
            alert("통신 오류: " + (err.error || err.message || err));
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
