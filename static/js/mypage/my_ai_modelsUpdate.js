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
        fetch(form.action, {
            method:"POST",
            body: FormData,
            headers:{
                "X-CSRFToken": formData.get("csrfmiddlewaretoken")
            }
            
            })
            .then(res => res.json())
            .then(data => {
                if(data.error){
                    alert(data.error)
                }else{
                    ("AI 가 수정되었습니다.");
                }
            }).catch(err =>{
                alert("통신 오류" + err)
            })
        });

        // 음성 선택 기능
        function selectVoiceId(voiceId) {
            const input = document.getElementById('voice_id');
            if (input) {
                input.value = voiceId;
                alert("해당 voice id가 선택되었습니다.");
            }
        }