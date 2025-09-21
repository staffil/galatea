let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let stream;

const baseUrl = window.location.pathname.replace(/\/(chat|vision|novel)\/\d+\/?$/, '');

window.toggleSidebar = function() {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.querySelector('.hamburger');
    sidebar.classList.toggle('active');
    hamburger.classList.toggle('active');
};

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

    document.getElementById("text-input").value = "";

    // AI typing bubble
    const avatarImg = LLM_IMAGE_URL ? 
        `<img src="${LLM_IMAGE_URL}" alt="AI" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">` :
        '🤖';
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

    const formData = new FormData();
    formData.append("text", userText);
    formData.append("llm_id", LLM_ID);

    fetch(`${baseUrl}/generate_response/`, {
        method: "POST",
        body: formData
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => { throw new Error(err.error || "Unknown error"); });
        return res.json();
    })
    .then(data => {
        typingMessage.remove();

        const aiMessage = document.createElement("div");
        aiMessage.className = "message ai";
        const avatarImgAI = LLM_IMAGE_URL ? 
            `<img src="${LLM_IMAGE_URL}" alt="AI" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">` :
            '🤖';
        aiMessage.innerHTML = `
            <div class="message-avatar">${avatarImgAI}</div>
            <div class="message-content">${data.ai_text}</div>
        `;
        messageArea.appendChild(aiMessage);

        if (data.audio_url) {
            const audioElem = document.getElementById("tts-audio");
            audioElem.src = data.audio_url;
            document.getElementById("audio-container").style.display = "block";
            audioElem.play();
        }
        messageArea.scrollTop = messageArea.scrollHeight;
    })
    .catch(error => {
        alert(messages.errorOccurred + error.message);
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

// 링크 복사
document.addEventListener("click", function(e) {
    if (e.target.classList.contains("share-btn")) {
        const link = e.target.getAttribute("data-link");
        navigator.clipboard.writeText(link).then(() => {
            alert(messages.shareCopied);
        });
    }
});