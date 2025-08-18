document.addEventListener('DOMContentLoaded', function() {
    const finalCreateBtn = document.getElementById('final-create-btn');
    if (finalCreateBtn) { // 버튼이 존재하는지 확인 (is_result가 True일 때만 존재)
        finalCreateBtn.addEventListener('click', function () {
            // HTML에서 data-voice-create-url 속성을 통해 올바른 URL을 가져옵니다.
            const createVoiceUrl = this.dataset.voiceCreateUrl; // <-- 이 부분이 핵심!
            
            // 만약 <a href> 태그가 버튼 안에 있다면, 기본 동작 방지
            // event.preventDefault(); // 이벤트 객체를 받아야 사용 가능

            const id = this.dataset.id;
            const voiceName = document.getElementById("voice_name").value.trim();

            // CSRF 토큰 가져오는 헬퍼 함수
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

            fetch(createVoiceUrl, { // <-- 여기에 이제 올바른 URL 문자열이 들어갈 것입니다.
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `generated_voice_id=${encodeURIComponent(id)}&voice_name=${encodeURIComponent(voiceName)}`
            })
            .then(res => {
                // HTTP 상태 코드를 확인하여 4xx 또는 5xx 에러인 경우 JSON 파싱을 시도하지 않음
                if (!res.ok) {
                    // 에러 응답이 JSON 형식이 아닐 수 있으므로 텍스트로 읽음
                    return res.text().then(text => { 
                        throw new Error(`Server error: ${res.status} ${res.statusText} - ${text}`);
                    });
                }
                return res.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    alert("최종 목소리 생성 완료! Voice ID: " + data.voice_id);
                    // 성공 시 페이지 이동 (버튼 내 <a href>를 제거했다고 가정)
                    window.location.href = "{% url 'mypage:my_voice' %}"; // 이 부분은 HTML 템플릿에서 직접 렌더링되므로 OK
                } else {
                    alert("오류: " + data.error);
                }
            })
            .catch(error => {
                console.error('Fetch Error:', error);
                alert('요청 처리 중 오류가 발생했습니다. 자세한 내용은 콘솔을 확인해주세요.');
            });
        });
    }


    const retryBtn = document.getElementById("retry-btn");
    if (retryBtn) { // 버튼이 존재하는지 확인 (is_result가 True일 때만 존재)
        retryBtn.addEventListener('click', function () {
            // HTML에서 data-retry-url 속성을 통해 올바른 URL을 가져옵니다.
            const retryUrl = this.dataset.retryUrl; // <-- 이 부분이 핵심!

            if (confirm("다시 만드시겠습니까? 재 생성시 기존의 토큰이 아닌 새로운 토큰이 차감됩니다. 목소리는 마이페이지에 그대로 저장됩니다.")) {
                window.location.href = retryUrl; // <-- 여기에 이제 올바른 URL 문자열이 들어갈 것입니다.
            }
        });
    }
});