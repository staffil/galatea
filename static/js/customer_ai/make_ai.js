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
            return confirm("이대로 AI를 생성하시겠습니까?") 
        }
        function selectVoiceId(voiceId){
            const input = document.getElementById('voice_id');
            if(input){
                input.value = voiceId;
                alert("해당 voice id 가 선택되었습니다.")
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
                        alert("{% trans '프롬프트을 입력해 주세요' %}")
                        return;
                    }
                    fetch("{% url 'auto_prompt' %}", {
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
                            document.getElementById("prompt").value = data.refine_data
                        alert("{% trans '프롬프트가 좀 더 구체화 되었습니다.'%}");
                        }else {
                            alert("{% trans '프롬프트 생성 중 오류가 발생했습니다.'%}")
                        }


                    })
                    .catch(err => {
                        console.error(err);
                        alert("서버 요청중 오류 발생")
                    })
                })


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
            alert("프롬프트를 입력해 주세요.");
            e.preventDefault(); // 폼 제출 막기
            return false;
        }

        if (!voiceId) {
            alert("목소리를 선택해 주세요.");
            e.preventDefault(); // 폼 제출 막기
            return false;
        }

        // 최종 확인
        if (!confirm("이대로 AI를 생성하시겠습니까?")) {
            e.preventDefault();
            return false;
        }
    });
});

// 선택 버튼 클릭 시 voice_id 입력
function selectVoiceId(voiceId){
    const input = document.getElementById('voice_id');
    if(input){
        input.value = voiceId;
        alert("해당 voice id 가 선택되었습니다.");
    }
}
