 let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let stream;

    const baseUrl = window.location.pathname.replace(/\/(chat|vision)\/\d+\/?$/, '');

    window.toggleSidebar= function() {
        const sidebar = document.getElementById('sidebar');
        const hamburger = document.querySelector('.hamburger');
        
        sidebar.classList.toggle('active');
        hamburger.classList.toggle('active');
    }

    window.toggleRecording = function() {
        const recordBtn = document.getElementById("record-btn");
        const recordIcon = document.getElementById("record-icon");
        const recordStatus = document.getElementById("record-status");

        if (!isRecording) {
            navigator.mediaDevices
                .getUserMedia({ audio: true })
                .then((s) => {
                    stream = s;
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];
                    mediaRecorder.start();
                    isRecording = true;

                    recordIcon.className = "fas fa-stop";
                    recordBtn.classList.add("recording");
                    recordStatus.textContent = "{% trans '녹음 중... 다시 누르면 종료됩니다' %}";

                    mediaRecorder.addEventListener("dataavailable", (event) => {
                        audioChunks.push(event.data);
                    });

                    mediaRecorder.addEventListener("stop", () => {
                        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                        const formData = new FormData();
                        formData.append("audio", audioBlob, "recorded.wav");

                        fetch(`${baseUrl}/upload_audio/`, {
                            method: "POST",
                            body: formData,
                        })
                        .then((res) => res.json())
                        .then((data) => {
                            const recognizedText = document.getElementById("recognized-text");
                            recognizedText.textContent = "{% trans '인식된 텍스트: ' %}" + data.text;
                            recognizedText.style.display = "block";
                            setTimeout(() => {
                                recognizedText.style.display = "none";
                            }, 3000);
                            
                            sendText(data.text);

                            if (data.audio_url) {
                                const audioElem = document.getElementById("tts-audio");
                                audioElem.src = data.audio_url;
                                document.getElementById("audio-container").style.display = "block";
                                audioElem.play();
                            }
                        })
                        .catch((error) => {
                            alert("{% trans '오디오 업로드 중 오류가 발생했습니다: ' %}" + error.message);
                        });
                    });
                })
                .catch((err) => {
                    alert("{% trans '마이크 권한을 허용해주세요.' %}");
                    console.error(err);
                });
        } else {
            mediaRecorder.stop();
            isRecording = false;
            recordIcon.className = "fas fa-microphone";
            recordBtn.classList.remove("recording");
            recordStatus.textContent = "{% trans '녹음을 시작하려면 버튼을 누르세요' %}";
            
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        }
    }

window.sendText = function(text) {
    const currentLlmId = LLM_ID;
    const llmImageUrl = LLM_IMAGE_URL;
        const userText = text || document.getElementById("text-input").value;
        
        if (!userText.trim()) return;

        const messageArea = document.getElementById("message-area");

        // 사용자 메시지 추가
        const userMessage = document.createElement("div");
        userMessage.className = "message user";
        userMessage.innerHTML = `
            <div class="message-avatar">👤</div>
            <div class="message-content">${userText}</div>
        `;
        messageArea.appendChild(userMessage);

        // 입력창 초기화
        document.getElementById("text-input").value = "";
        
        // 스크롤을 맨 아래로
        messageArea.scrollTop = messageArea.scrollHeight;

        const formData = new FormData();
        formData.append("text", userText);
        formData.append("llm_id", currentLlmId);

        fetch(`${baseUrl}/generate_response/`, {
            method: "POST",
            body: formData,
        })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => { throw new Error(err.error || "Unknown error"); });
            }
            return res.json();
        })
        .then(data => {
            const aiMessage = document.createElement("div");
            aiMessage.className = "message ai";
            
            const avatarImg = llmImageUrl ? 
                `<img src="${llmImageUrl}" alt="AI" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">` : 
                '🤖';
                
            aiMessage.innerHTML = `
                <div class="message-avatar">${avatarImg}</div>
                <div class="message-content">${data.ai_text}</div>
            `;
            messageArea.appendChild(aiMessage);

            if(data.audio_url){
                const audioElem = document.getElementById("tts-audio");
                audioElem.src = data.audio_url;
                document.getElementById("audio-container").style.display = "block";
                audioElem.play();
            }

            // 스크롤을 맨 아래로
            messageArea.scrollTop = messageArea.scrollHeight;
        })
        .catch(error => {
            alert("{% trans '오류 발생: ' %}" + error.message);
        });
    }

    // 모바일에서 사이드바 외부 클릭 시 닫기
    document.addEventListener('click', (e) => {
        const sidebar = document.getElementById('sidebar');
        const hamburger = document.querySelector('.hamburger');
        
        if (window.innerWidth <= 1024 && sidebar.classList.contains('active')) {
            if (!sidebar.contains(e.target) && !hamburger.contains(e.target)) {
                sidebar.classList.remove('active');
                hamburger.classList.remove('active');
            }
        }
    });

    // 화면 크기 변경 시 사이드바 상태 리셋
    window.addEventListener('resize', () => {
        const sidebar = document.getElementById('sidebar');
        const hamburger = document.querySelector('.hamburger');
        
        if (window.innerWidth > 1024) {
            sidebar.classList.remove('active');
            hamburger.classList.remove('active');
        }
    });

    // 링크 복사하기
document.addEventListener("click", function(e) {
    if (e.target.classList.contains("share-btn")) {
        const link = e.target.getAttribute("data-link");
        navigator.clipboard.writeText(link).then(() => {
            alert("링크가 복사되었습니다!");
        });
    }
});