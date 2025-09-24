let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let stream;

const baseUrl = window.location.pathname.replace(/\/(chat|vision|novel)\/\d+\/?$/, '');

// 타이핑 효과 함수
function typewriterEffect(element, text, speed = 30) {
    element.textContent = '';
    let i = 0;
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            // 문장 부호에서는 조금 더 긴 간격
            const currentChar = text.charAt(i - 1);
            const delay = (currentChar === '.' || currentChar === '!' || currentChar === '?') ? speed * 3 : speed;
            setTimeout(type, delay);
        }
    }
    type();
}

// 사이드바 토글 함수
window.toggleSidebar = function() {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.querySelector('.hamburger');
    sidebar.classList.toggle('active');
    hamburger.classList.toggle('active');
};

// 녹음 토글 함수
window.toggleRecording = function() {
    const recordBtn = document.getElementById("record-btn");
    const recordIcon = document.getElementById("record-icon");
    const recordStatus = document.getElementById("record-status");

    if (!isRecording) {
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then((s) => {
            stream = s;
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            mediaRecorder.start();
            isRecording = true;

            recordIcon.className = "fas fa-stop";
            recordBtn.classList.add("recording");
            recordStatus.textContent = messages.recordingInProgress;

            mediaRecorder.addEventListener("dataavailable", (event) => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                const formData = new FormData();
                formData.append("audio", audioBlob, "recorded.wav");

                fetch(`${baseUrl}/upload_audio/`, {
                    method: "POST",
                    body: formData
                })
                .then(res => res.json())
                .then(data => {
                    const recognizedText = document.getElementById("recognized-text");
                    recognizedText.textContent = messages.recognizedText + data.text;
                    recognizedText.style.display = "block";
                    setTimeout(() => { recognizedText.style.display = "none"; }, 3000);

                    sendText(data.text);

                    if (data.audio_url) {
                        const audioElem = document.getElementById("tts-audio");
                        audioElem.src = data.audio_url;
                        document.getElementById("audio-container").style.display = "block";
                        audioElem.play();
                    }
                })
                .catch((error) => {
                    alert(messages.audioUploadError + error.message);
                });
            });
        })
        .catch((err) => {
            alert(messages.micPermission);
            console.error(err);
        });
    } else {
        mediaRecorder.stop();
        isRecording = false;
        recordIcon.className = "fas fa-microphone";
        recordBtn.classList.remove("recording");
        recordStatus.textContent = messages.recordingStart;

        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    }
};

// 텍스트 전송 함수 (타이핑 효과 적용)
window.sendText = function(text) {
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

    // 입력창 비우기
    document.getElementById("text-input").value = "";

    // AI 아바타 이미지 설정
    const avatarImg = LLM_IMAGE_URL ? 
        `<img src="${LLM_IMAGE_URL}" alt="AI" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">` :
        '🤖';

    // AI typing bubble 추가
    const typingMessage = document.createElement("div");
    typingMessage.className = "message ai typing";
    typingMessage.innerHTML = `
        <div class="message-avatar">${avatarImg}</div>
        <div class="message-content">
            <div class="typing-bubbles"><span></span><span></span><span></span></div>
        </div>
    `;
    messageArea.appendChild(typingMessage);
    messageArea.scrollTop = messageArea.scrollHeight;

    // FormData 준비
    const formData = new FormData();
    formData.append("text", userText);
    formData.append("llm_id", LLM_ID);

    // 서버로 요청 전송
    fetch(`${baseUrl}/generate_response/`, {
        method: "POST",
        body: formData
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => { throw new Error(err.error || "Unknown error"); });
        return res.json();
    })
    .then(data => {
        // typing bubble 제거
        typingMessage.remove();

        // AI 응답 메시지 생성 (빈 content로 시작)
        const aiMessage = document.createElement("div");
        aiMessage.className = "message ai";
        const messageId = 'ai-message-' + Date.now(); // 고유 ID 생성
        aiMessage.innerHTML = `
            <div class="message-avatar">${avatarImg}</div>
            <div class="message-content" id="${messageId}"></div>
        `;
        messageArea.appendChild(aiMessage);

        // 스크롤 위치 조정
        messageArea.scrollTop = messageArea.scrollHeight;

        // 타이핑 효과로 AI 응답 표시
        const responseDiv = document.getElementById(messageId);
        typewriterEffect(responseDiv, data.ai_text, 25); // 25ms 간격으로 타이핑

        // 오디오가 있으면 타이핑과 동시에 재생 시작
        if (data.audio_url) {
            // 타이핑 시작과 거의 동시에 오디오 재생
            setTimeout(() => {
                const audioElem = document.getElementById("tts-audio");
                audioElem.src = data.audio_url;
                document.getElementById("audio-container").style.display = "block";
                audioElem.play();
            }, 300); // 300ms 후 오디오 재생 (자연스러운 타이밍)
        }

        // 스크롤을 끝까지 유지
        const scrollInterval = setInterval(() => {
            messageArea.scrollTop = messageArea.scrollHeight;
        }, 50);

        // 타이핑이 끝나면 스크롤 업데이트 중단
        setTimeout(() => {
            clearInterval(scrollInterval);
        }, data.ai_text.length * 25 + 500); // 타이핑 시간 + 여유시간
    })
    .catch(error => {
        // 에러 발생 시 typing bubble 제거
        if (typingMessage.parentNode) {
            typingMessage.remove();
        }
        
        // 에러 메시지 표시
        const errorMessage = document.createElement("div");
        errorMessage.className = "message ai";
        errorMessage.innerHTML = `
            <div class="message-avatar">⚠️</div>
            <div class="message-content" style="color: #e74c3c;">
                ${messages.errorOccurred} ${error.message}
            </div>
        `;
        messageArea.appendChild(errorMessage);
        messageArea.scrollTop = messageArea.scrollHeight;
        
        console.error('Error:', error);
    });
};

// 사이드바 외부 클릭 시 닫기
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

// 링크 복사 기능
document.addEventListener("click", function(e) {
    if (e.target.classList.contains("share-btn")) {
        const link = e.target.getAttribute("data-link");
        navigator.clipboard.writeText(link).then(() => {
            alert(messages.shareCopied);
        });
    }
});

// 페이지 로드 완료 후 초기화
document.addEventListener('DOMContentLoaded', function() {
    // 텍스트 입력창에 포커스
    const textInput = document.getElementById('text-input');
    if (textInput) {
        textInput.focus();
    }
    
    // 엔터키 이벤트 리스너 추가 (중복 방지)
    textInput?.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendText();
        }
    });
    
    console.log('Voice Chat UI initialized with typing effect');
});