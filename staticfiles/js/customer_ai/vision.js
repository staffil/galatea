   const video = document.getElementById('webcam');
        const canvas = document.createElement('canvas');
        const toggleBtn = document.getElementById('toggle-vision-btn');
        const visionResult = document.getElementById('vision-result');
        const ttsAudio = document.getElementById('tts-audio');
        const responseDiv = document.getElementById('response');

        let streaming = false;
        let intervalId = null;
        let isVisionRunning = false;
        let latestVisionResult = '';

        let isProcessingVision = false; // 이미지 분석 중복 방지용
        let isPlayingAudio = false;     // 음성 재생 상태

        // 웹캠 시작
        async function startWebcam() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
                video.srcObject = stream;
                streaming = true;
            } catch (err) {
                alert('웹캠 접근 실패: ' + err);
            }
        }

        // 웹캠 중지
        function stopWebcam() {
            if (video.srcObject) {
                video.srcObject.getTracks().forEach(track => track.stop());
            }
            streaming = false;
        }

        // 이미지 분석 서버 전송 함수
        async function sendFrameToServer() {
            if (!streaming) return;
            if (isProcessingVision) return;
            if (isPlayingAudio) return;  // 음성 재생 중일 때 분석 중단

            isProcessingVision = true;

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);

            canvas.toBlob(async (blob) => {
                if (!blob) {
                    isProcessingVision = false;
                    return;
                }

                const formData = new FormData();
                formData.append('image', blob, 'frame.jpg');

                try {
                    const response = await fetch('/customer_ai/vision_process/', {
                        method: 'POST',
                        body: formData
                    });
                    if (!response.ok) throw new Error('서버 응답 오류');
                    const data = await response.json();
                    visionResult.innerText = '분석 결과: ' + data.result;
                    latestVisionResult = data.result;
                } catch (err) {
                    console.error('Vision error:', err);
                    visionResult.innerText = '분석 오류 발생';
                } finally {
                    isProcessingVision = false;
                }
            }, 'image/jpeg');
        }

        // GPT 응답 요청 (Vision 결과 포함)
        async function sendText(text) {
            if (!text || !text.trim()) return;
            const currentLlmId = "{{ llm_id }}";
          console.log("sendText 호출됨, text:", text);
              console.log("latestVisionResult:", latestVisionResult);

            isPlayingAudio = true;  // 음성 재생 플래그 설정

            const formData = new FormData();
            formData.append('text', text);
            formData.append('vision', latestVisionResult);
            formData.append('llm_id', currentLlmId);


            try {
                const res = await fetch('/customer_ai/generate_response/', {
                    method: 'POST',
                    body: formData,
                });
                if (!res.ok) throw new Error('응답 실패');
                const data = await res.json();

                responseDiv.innerText = 'AI: ' + data.ai_text;
                if (data.audio_url) {
                    ttsAudio.src = data.audio_url + '?t=' + new Date().getTime(); // 캐싱 방지
                    await ttsAudio.play();
                }
            } catch (err) {
                responseDiv.innerText = '응답 중 오류 발생';
                console.error(err);
            }
        }

        // 오디오 재생 종료 시점 플래그 해제
        ttsAudio.addEventListener('ended', () => {
            isPlayingAudio = false;
        });

        // 녹음 및 무음 감지
        async function startRecording() {
            try {
                const micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const mediaRecorder = new MediaRecorder(micStream, { mimeType: 'audio/webm;codecs=opus' });
                let audioChunks = [];

                mediaRecorder.ondataavailable = e => {
                    if (e.data && e.data.size > 0) {
                        audioChunks.push(e.data);
                    }
                };

                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'recorded.webm');

                    try {
                        const response = await fetch('/customer_ai/upload_audio/', {
                            method: 'POST',
                            body: formData,
                        });
                        const data = await response.json();
                        if (response.ok) {
                            console.log('Transcription:', data.text);
                            sendText(data.text);
                        } else {
                            console.error('Error:', data.error);
                        }
                    } catch (err) {
                        console.error('Fetch error:', err);
                    }
                };

                mediaRecorder.start();

                // 예: 5초 후 녹음 중지
                setTimeout(() => {
                    mediaRecorder.stop();
                    micStream.getTracks().forEach(track => track.stop());
                }, 5000);

            } catch (err) {
                console.error('Could not start recording:', err);
            }
        }

        // 비전 모드 토글 버튼 이벤트
        toggleBtn.addEventListener('click', () => {
            if (!isVisionRunning) {
                startVisionMode();
            } else {
                stopVisionMode();
            }
            isVisionRunning = !isVisionRunning;
        });

        // 비전 모드 시작
        async function startVisionMode() {
            if (!streaming) await startWebcam();
            visionResult.innerText = '비전 모드 실행 중...';
            intervalId = setInterval(sendFrameToServer, 1500); // 1.5초마다 프레임 분석
            await startRecording();
            toggleBtn.innerText = '비전 모드 중지';
        }

        // 비전 모드 중지
        function stopVisionMode() {
            clearInterval(intervalId);
            stopWebcam();
            visionResult.innerText = '비전 모드 중지됨';
            toggleBtn.innerText = '비전 모드 시작';
        }

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