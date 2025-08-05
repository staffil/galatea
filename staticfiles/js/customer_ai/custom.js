        let mediaRecorder;
        let audioChunks = [];
        let isRecording = false;
        let stream;

        function toggleRecording() {
            const recordBtn = document.getElementById("record-btn");
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

                        recordBtn.querySelector(".record-icon").textContent = "⏹";
                        recordBtn.classList.add("recording");
                        recordBtn.parentElement.classList.add("recording");
                        recordStatus.textContent = "녹음 중... 다시 누르면 종료됩니다";

                        mediaRecorder.addEventListener("dataavailable", (event) => {
                            audioChunks.push(event.data);
                        });

                        mediaRecorder.addEventListener("stop", () => {
                            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                            const formData = new FormData();
                            formData.append("audio", audioBlob, "recorded.wav");

                            // 실제 환경에서는 이 부분을 활성화하세요
                          
                            fetch("/customer_ai/upload_audio/", {
                                method: "POST",
                                body: formData,
                            })
                                .then((res) => res.json())
                                .then((data) => {
                                    document.getElementById("recognized-text").textContent = "인식된 텍스트: " + data.text;
                                    sendText(data.text);
                                });
                         

                        });
                    })
                    .catch((err) => {
                        alert("마이크 권한을 허용해주세요.");
                        console.error(err);
                    });
            } else {
                mediaRecorder.stop();
                isRecording = false;
                recordBtn.querySelector(".record-icon").textContent = "🎤";
                recordBtn.classList.remove("recording");
                recordBtn.parentElement.classList.remove("recording");
                recordStatus.textContent = "녹음을 시작하려면 버튼을 누르세요";
            }
        }

        function sendText(text = null) {
            const currentLlmId = "{{ llm_id }}";
            const userText = text || document.getElementById("text-input").value;
            if (!userText.trim()) return;

            const messageArea = document.getElementById("message-area");
            
            // 사용자 메시지 추가
            const userMessage = document.createElement("div");
            userMessage.className = "user-message";
            userMessage.textContent = userText;
            messageArea.appendChild(userMessage);

            // 입력창 초기화
            document.getElementById("text-input").value = "";

            // 메시지 추가 후 텍스트 입력창으로 부드럽게 스크롤
            setTimeout(() => {
                const textInput = document.getElementById("text-input");
                textInput.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }, 100);

            const formData = new FormData();
            formData.append("text", userText);
            formData.append("llm_id", currentLlmId);

          
            fetch("/customer_ai/generate_response/", {
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
                aiMessage.className = "ai-message";
                aiMessage.textContent = data.ai_text + " (emotion: " + data.emotion + ")";
                messageArea.appendChild(aiMessage);

                document.getElementById("tts-audio").src = data.audio_url;
                document.getElementById("audio-container").style.display = "block";

                // AI 응답 후에도 텍스트 입력창으로 스크롤
                setTimeout(() => {
                    const textInput = document.getElementById("text-input");
                    textInput.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }, 100);
            })
            .catch(error => {
                alert("오류 발생: " + error.message);
            });

          

            setTimeout(() => {
                const aiMessage = document.createElement("div");
              
                messageArea.appendChild(aiMessage);
                
                // 텍스트 입력창으로 스크롤 이동
                setTimeout(() => {
                    const textInput = document.getElementById("text-input");
                    textInput.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }, 100);
            }, 1000);
        }