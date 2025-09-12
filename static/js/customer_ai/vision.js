const baseUrl = window.location.pathname.replace(/\/(chat|vision)\/\d+\/?$/, '');

const video = document.getElementById('webcam');
const canvas = document.createElement('canvas');
const toggleBtn = document.getElementById('toggle-vision-btn');
const visionResult = document.getElementById('vision-result');
const ttsAudio = document.getElementById('tts-audio');
const responseDiv = document.getElementById('response');
const recognizedText = document.getElementById('recognized-text');
const recognizedTextDisplay = document.getElementById('recognized-text-display');

let streaming = false;
let intervalId = null;
let isVisionRunning = false;
let latestVisionResult = '';

let isProcessingVision = false;
let isPlayingAudio = false;

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.querySelector('.hamburger');
    
    sidebar.classList.toggle('active');
    hamburger.classList.toggle('active');
}

// 웹캠 시작
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        video.classList.add('active');
        streaming = true;
        visionResult.textContent = "{% trans '웹캠이 시작되었습니다' %}";
        visionResult.className = "vision-status active";
    } catch (err) {
        alert("{% trans '웹캠 접근 실패: ' %}" + err);
        visionResult.textContent = "{% trans '웹캠 접근 실패' %}";
        visionResult.className = "vision-status";
    }
}

// 웹캠 중지
function stopWebcam() {
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
    }
    video.classList.remove('active');
    streaming = false;
}

// 이미지 분석 서버 전송 함수
async function sendFrameToServer() {
    if (!streaming) return;
    if (isProcessingVision) return;
    if (isPlayingAudio) return;

    isProcessingVision = true;
    visionResult.textContent = "{% trans '이미지 분석 중...' %}";
    visionResult.className = "vision-status processing";

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
            const response = await fetch(`${baseUrl}/vision_process/`, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) throw new Error("{% trans '서버 응답 오류' %}");
            const data = await response.json();
            visionResult.textContent = "{% trans '분석 완료: ' %}" + data.result;
            visionResult.className = "vision-status active";
            latestVisionResult = data.result;
        } catch (err) {
            console.error('Vision error:', err);
            visionResult.textContent = "{% trans '분석 오류 발생' %}";
            visionResult.className = "vision-status";
        } finally {
            isProcessingVision = false;
        }
    }, 'image/jpeg');
}

// GPT 응답 요청
async function sendText(text) {
    if (!text || !text.trim()) return;
const currentLlmId = LLM_ID;
    
    isPlayingAudio = true;
    responseDiv.textContent = "{% trans 'AI가 응답을 생성 중...' %}";

    const formData = new FormData();
    formData.append('text', text);
    formData.append('vision', latestVisionResult);
    formData.append('llm_id', currentLlmId);

    try {
        const res = await fetch(`${baseUrl}/generate_response/`, {
            method: 'POST',
            body: formData,
        });
        if (!res.ok) throw new Error('응답 실패');
        const data = await res.json();

        responseDiv.textContent = data.ai_text;
        if (data.audio_url) {
            ttsAudio.src = data.audio_url + '?t=' + new Date().getTime();
            document.getElementById('audio-container').style.display = 'block';
            await ttsAudio.play();
        }
    } catch (err) {
        responseDiv.textContent = '응답 중 오류 발생: ' + err.message;
        console.error(err);
    }
}

// 오디오 재생 종료 시점 플래그 해제
ttsAudio.addEventListener('ended', () => {
    isPlayingAudio = false;
});

// 비전 모드 토글
toggleBtn.addEventListener('click', () => {
    if (!isVisionRunning) {
        startVisionMode();
    } else {
        stopVisionMode();
    }
});

// 비전 모드 시작
async function startVisionMode() {
    if (!streaming) await startWebcam();
    
    isVisionRunning = true;
    intervalId = setInterval(sendFrameToServer, 1500);
    
    toggleBtn.innerHTML = '<i class="fas fa-stop"></i> {% trans "비전 모드 중지" %}';
    toggleBtn.classList.add('active');
    
    visionResult.textContent = "{% trans '비전 모드 실행 중...' %}";
    visionResult.className = "vision-status processing";
}

// 비전 모드 중지
function stopVisionMode() {
    clearInterval(intervalId);
    stopWebcam();
    isVisionRunning = false;
    
    toggleBtn.innerHTML = '<i class="fas fa-play"></i> {% trans "비전 모드 시작" %}';
    toggleBtn.classList.remove('active');
    
    visionResult.textContent = "{% trans '비전 모드 중지됨' %}";
    visionResult.className = "vision-status";
}

// 녹음 관련
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let stream;

function toggleRecording() {
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
                        recognizedText.textContent = "{% trans '인식된 텍스트: ' %}" + data.text;
                        recognizedTextDisplay.textContent = "{% trans '인식된 텍스트: ' %}" + data.text;
                        recognizedTextDisplay.style.display = "block";
                        
                        setTimeout(() => {
                            recognizedTextDisplay.style.display = "none";
                        }, 3000);
                        
                        sendText(data.text);
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

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 초기 상태 설정
    visionResult.textContent = "{% trans '비전 모드 준비 중...' %}";
    recognizedText.textContent = "{% trans '음성 인식 대기 중...' %}";
    responseDiv.textContent = "{% trans 'AI 응답 대기 중...' %}";
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