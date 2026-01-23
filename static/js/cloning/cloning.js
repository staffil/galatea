const consentVoice = document.getElementById('consentVoice');
const consentThird = document.getElementById('consentThird');
const consentShare = document.getElementById('consentShare');
const agreeBtn = document.getElementById('agreeBtn');
const consentSection = document.getElementById('consentSection');
const cloningUI = document.getElementById('cloningUI');

const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const audioPlayback = document.getElementById('audioPlayback');
const generateSampleBtn = document.getElementById('generateSampleBtn');
const retryBtn = document.getElementById('retryBtn');
const saveBtn = document.getElementById('saveBtn');
const voiceNameInput = document.getElementById('voiceName');
const sampleTextInput = document.getElementById('sampleText');
const messageDiv = document.getElementById('message');

let mediaRecorder;
let audioChunks = [];
let recordedBlob = null;
let savedVoiceId = null;

// 1️⃣ 동의 후 UI 활성화
agreeBtn.onclick = async () => {
    if(!consentVoice.checked || !consentThird.checked || !consentShare.checked){
        alert("모든 동의 항목에 체크해야 합니다.");
        return;
    }

    // 서버에 체크박스만 저장
    try {
        const res = await fetch("{% url 'cloning:save_consent' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                consent_voice: consentVoice.checked,
                consent_third: consentThird.checked,
                consent_share: consentShare.checked
            })
        });
        const data = await res.json();
        if(data.status === 'success'){
            consentSection.style.display = 'none';
            cloningUI.style.display = 'block';
        } else {
            alert("동의 저장에 실패했습니다: " + data.error);
        }
    } catch(e){
        alert("서버 오류가 발생했습니다.");
    }
}

// CSRF token 가져오기 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// 2️⃣ 녹음/샘플/저장 기능 (기존 코드 그대로)
function showMessage(text, color = 'red') {
    messageDiv.style.color = color;
    messageDiv.textContent = text;
}

// 녹음 시작
recordBtn.onclick = async () => {
    showMessage('');
    audioChunks = [];
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        recordBtn.disabled = true;
        stopBtn.disabled = false;

        mediaRecorder.ondataavailable = e => {
            audioChunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
            recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
            audioPlayback.src = URL.createObjectURL(recordedBlob);
            generateSampleBtn.disabled = false;
            retryBtn.disabled = false;
            saveBtn.disabled = true;
            savedVoiceId = null;
        };
    } catch(err) {
        showMessage('마이크 접근 권한을 허용해주세요.');
    }
};

// 녹음 중지
stopBtn.onclick = () => {
    mediaRecorder.stop();
    recordBtn.disabled = false;
    stopBtn.disabled = true;
};

// 샘플 생성
generateSampleBtn.onclick = async () => {
    showMessage('');
    const voiceName = voiceNameInput.value.trim();
    const sampleText = sampleTextInput.value.trim();

    if (!voiceName) { alert('목소리 이름을 입력하세요.'); return; }
    if (!sampleText || sampleText.length < 130) { alert('샘플 텍스트를 130자 이상 입력하세요.'); return; }
    if (!recordedBlob) { alert('녹음된 음성이 없습니다.'); return; }

    generateSampleBtn.disabled = true;
    showMessage('샘플 생성 중입니다. 잠시만 기다려주세요...', 'blue');

    const formData = new FormData();
    formData.append('voice_name', voiceName);
    formData.append('sample_text', sampleText);
    formData.append('audio', recordedBlob, 'recorded.webm');

    try {
        const res = await fetch("{% url 'cloning:voice_cloning_sample' %}", {
            method: 'POST',
            body: formData,
            credentials: 'include',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
        });
        const data = await res.json();

        if (data.status === 'success') {
            audioPlayback.src = data.sample_url;
            savedVoiceId = data.voice_id;
            saveBtn.disabled = false;
            showMessage('샘플 생성 완료! 목소리를 확인하세요.', 'green');
        } else {
            showMessage('오류: ' + data.error);
        }
    } catch (e) {
        showMessage('서버 오류가 발생했습니다.');
    } finally {
        generateSampleBtn.disabled = false;
    }
};

// 다시 만들기
retryBtn.onclick = () => {
    recordedBlob = null;
    savedVoiceId = null;
    audioPlayback.src = '';
    sampleTextInput.value = '';
    voiceNameInput.value = '';
    generateSampleBtn.disabled = true;
    retryBtn.disabled = true;
    saveBtn.disabled = true;
    showMessage('');
};

// 저장
saveBtn.onclick = async () => {
    showMessage('');
    if (!savedVoiceId) { alert('저장할 목소리가 없습니다.'); return; }
    const voiceName = voiceNameInput.value.trim();
    if (!voiceName) { alert('목소리 이름을 입력하세요.'); return; }

    try {
        const res = await fetch("{% url 'cloning:voice_cloning_save' %}", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            credentials: 'include',
            body: JSON.stringify({ voice_id: savedVoiceId, voice_name: voiceName }),
        });
        const data = await res.json();
        if (data.status === 'success') {
            alert('목소리가 성공적으로 저장되었습니다!');
            window.location.href = '/mypage/my_voice/';
        } else {
            showMessage('저장 오류: ' + data.error);
        }
    } catch (e) {
        showMessage('서버 오류가 발생했습니다.');
    }
};

// CSRF token 가져오기
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}