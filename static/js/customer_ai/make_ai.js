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