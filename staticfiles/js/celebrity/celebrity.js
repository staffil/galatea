
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

                        recordStatus.textContent = "⏹ 녹음 종료";

  

                        mediaRecorder.addEventListener("dataavailable", (event) => {

                            audioChunks.push(event.data);

                        });

  

                        mediaRecorder.addEventListener("stop", () => {

                            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });

                            const formData = new FormData();

                            formData.append("audio", audioBlob, "recorded.wav");

  

                            fetch("/celebrity/celebrity_audio/", {

                                method: "POST",

                                body: formData,

                            })

                                .then((res) => res.json())

                                .then((data) => {

                                    document.getElementById("recognized-text").textContent = "인식된 텍스트: " + data.text;

                                    sendText(data.text);

                                });

  

                            // 마이크 스트림 해제

                            stream.getTracks().forEach((track) => track.stop());

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

                recordStatus.textContent = "🎙 녹음 시작";

            }

        }

  

        function sendText(text = null) {

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

  

            const formData = new FormData();

            formData.append("text", userText);

            const pathParts = window.location.pathname.split('/');

            const celebrityId = pathParts[2];

  

            fetch(`/celebrity/celebrity_response/${celebrityId}/`, {

                method: "POST",

                body: formData,

            })

                .then((res) => res.json())

                .then((data) => {

                    // AI 메시지 추가

                    const aiMessage = document.createElement("div");

                    aiMessage.className = "ai-message";

                    aiMessage.textContent = data.ai_text + " (emotion: " + data.emotion + ")";

                    messageArea.appendChild(aiMessage);

                    // 오디오 설정

                    document.getElementById("tts-audio").src = data.audio_url;

  

                    // 텍스트 입력창으로 스크롤

                    setTimeout(() => {

                        const textInput = document.getElementById("text-input");

                        textInput.scrollIntoView({

                            behavior: 'smooth',

                            block: 'center'

                        });

                    }, 100);

                })

                .catch((error) => {

                    console.error("Error:", error);

                    alert("오류가 발생했습니다.");

                });

        }