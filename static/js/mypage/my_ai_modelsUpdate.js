document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // 기본 제출 막기

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken") // Django CSRF
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("오류 발생: " + data.error); // 에러 팝업
            } else {
                alert("AI 설정이 수정되었습니다!");
                window.location.reload(); // 성공 시 페이지 갱신
            }
        })
        .catch(err => {
            alert("서버 통신 오류: " + err);
        });
    });
});

        // 음성 선택 기능
        function selectVoiceId(voiceId) {
            const input = document.getElementById('voice_id');
            if (input) {
                input.value = voiceId;
                alert("해당 voice id가 선택되었습니다.");
            }
        }