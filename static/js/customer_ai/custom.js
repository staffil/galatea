let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let stream;

const baseUrl = window.location.pathname.replace(/\/(chat|vision|novel)\/\d+\/?$/, '');

// 오디오 폴링을 위한 전역 변수들
let audioCheckIntervals = new Map(); // conversation_id별 인터벌 저장

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

// 오디오 상태 확인 함수
function checkAudioStatus(conversationId, messageElement, maxAttempts = 100) {
    let attempts = 0;
    
    // 상태 표시 요소 생성/업데이트
    let statusElement = messageElement.querySelector('.audio-status');
    if (!statusElement) {
        statusElement = document.createElement('div');
        statusElement.className = 'audio-status';
        statusElement.style.cssText = 'font-size: 0.8em; color: #666; margin-top: 5px; font-style: italic;';
        messageElement.querySelector('.message-content').appendChild(statusElement);
    }
    statusElement.textContent = '🎵 음성 생성 중...';

    const checkInterval = setInterval(() => {
        attempts++;
        
        fetch(`${baseUrl}/check_audio_status/?conversation_id=${conversationId}`)
            .then(res => res.json())
            .then(data => {
                if (data.ready && data.audio_url) {
                    // 오디오 준비 완료
                    clearInterval(checkInterval);
                    audioCheckIntervals.delete(conversationId);
                    
                    // 상태 업데이트
                    statusElement.textContent = '🔊 음성 재생';
                    statusElement.style.color = '#2ecc71';
                    
                    // 오디오 재생
                    playAudio(data.audio_url, statusElement);
                    
                } else if (attempts >= maxAttempts) {
                    // 최대 시도 횟수 초과 (20초 후 포기)
                    clearInterval(checkInterval);
                    audioCheckIntervals.delete(conversationId);
                    
                    statusElement.textContent = '⚠️ 음성 생성 시간 초과';
                    statusElement.style.color = '#e74c3c';
                }
            })
            .catch(error => {
                console.error('오디오 상태 확인 오류:', error);
                
                if (attempts >= maxAttempts) {
                    clearInterval(checkInterval);
                    audioCheckIntervals.delete(conversationId);
                    
                    statusElement.textContent = '⚠️ 음성 생성 실패';
                    statusElement.style.color = '#e74c3c';
                }
            });
    }, 500); // 0.5초마다 확인
    
    // 인터벌 저장 (필요시 취소할 수 있도록)
    audioCheckIntervals.set(conversationId, checkInterval);
}

// 오디오 재생 함수
function playAudio(audioUrl, statusElement) {
    const audioElem = document.getElementById("tts-audio");
    audioElem.src = audioUrl;
    document.getElementById("audio-container").style.display = "block";
    
    // 재생 이벤트 리스너
    audioElem.onplay = () => {
        if (statusElement) {
            statusElement.textContent = '▶️ 재생 중...';
            statusElement.style.color = '#3498db';
        }
    };
    
    audioElem.onended = () => {
        if (statusElement) {
            statusElement.textContent = '✓ 재생 완료';
            statusElement.style.color = '#95a5a6';
            // 3초 후 상태 메시지 숨김
            setTimeout(() => {
                if (statusElement) {
                    statusElement.style.display = 'none';
                }
            }, 3000);
        }
    };
    
    audioElem.onerror = () => {
        if (statusElement) {
            statusElement.textContent = '⚠️ 재생 실패';
            statusElement.style.color = '#e74c3c';
        }
    };
    
    // 오디오 재생 시작
    audioElem.play().catch(error => {
        console.error('오디오 재생 실패:', error);
        if (statusElement) {
            statusElement.textContent = '⚠️ 재생 실패';
            statusElement.style.color = '#e74c3c';
        }
    });
}

// 사이드바 토글 함수
window.toggleSidebar = function() {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.querySelector('.hamburger');
    sidebar.classList.toggle('active');
    hamburger.classList.toggle('active');
};

// 녹음 토글 함수 (수정됨 - 새로운 방식 적용)
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

                    // 새로운 방식으로 텍스트 전송 (오디오는 폴링으로 처리)
                    sendText(data.text);
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

// 텍스트 전송 함수 (완전히 수정됨 - 새로운 방식 적용)
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

    // 서버로 요청 전송 (새로운 방식)
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
        const messageId = 'ai-message-' + Date.now();
        aiMessage.innerHTML = `
            <div class="message-avatar">${avatarImg}</div>
            <div class="message-content" id="${messageId}">
                <div class="message-text"></div>
            </div>
        `;
        messageArea.appendChild(aiMessage);

        // 스크롤 위치 조정
        messageArea.scrollTop = messageArea.scrollHeight;

        // 타이핑 효과로 AI 응답 표시
        const responseDiv = aiMessage.querySelector('.message-text');
        typewriterEffect(responseDiv, data.ai_text, 25);

        // 백그라운드에서 오디오 상태 확인 시작
        if (data.conversation_id) {
            setTimeout(() => {
                checkAudioStatus(data.conversation_id, aiMessage);
            }, 1000); // 1초 후 오디오 확인 시작 (타이핑 효과 시작 후)
        } else {
            // conversation_id가 없으면 기존 방식으로 폴백
            if (data.audio_url) {
                setTimeout(() => {
                    const audioElem = document.getElementById("tts-audio");
                    audioElem.src = data.audio_url;
                    document.getElementById("audio-container").style.display = "block";
                    audioElem.play();
                }, 300);
            }
        }

        // 스크롤을 끝까지 유지
        const scrollInterval = setInterval(() => {
            messageArea.scrollTop = messageArea.scrollHeight;
        }, 50);

        // 타이핑이 끝나면 스크롤 업데이트 중단
        setTimeout(() => {
            clearInterval(scrollInterval);
        }, data.ai_text.length * 25 + 500);

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

// 페이지 언로드 시 모든 오디오 확인 인터벌 정리
window.addEventListener('beforeunload', () => {
    audioCheckIntervals.forEach((interval, conversationId) => {
        clearInterval(interval);
    });
    audioCheckIntervals.clear();
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
    
    console.log('Voice Chat UI initialized with fast text response and background audio generation');
});