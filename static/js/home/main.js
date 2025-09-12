// ===== 공통 유틸 =====
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ===== 모달 =====
window.openModal = function(llm_id) {
    const modalHTML = `
    <div id="llm-modal">
        <div class="modal-overlay" onclick="closeModal()"></div>
        <div class="modal-content">
            <button class="close-btn" onclick="closeModal()">X</button>
            <div id="llm-container" class="llm-container"></div>
        </div>
    </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    document.body.style.overflow = "hidden";
    document.documentElement.style.overflow = "hidden";

fetch(`/${window.LANGUAGE_CODE}/intro/${llm_id}`)

        .then(response => response.text())
        .then(html => {
            document.getElementById('llm-container').innerHTML = html;
        });
};

function closeModal() {
    const modal = document.getElementById('llm-modal');
    if (modal) modal.remove();
    document.body.style.overflow = "auto";
    document.documentElement.style.overflow = "auto";
}

// ===== 사이드바 토글 =====
const toggleBtn = document.getElementById('sidebar-toggle');
const sidebarContent = document.getElementById('sidebar-content');

if (toggleBtn && sidebarContent) {
    toggleBtn.addEventListener('click', () => {
        const collapsed = sidebarContent.classList.contains('collapsed');
        sidebarContent.classList.toggle('collapsed');
        toggleBtn.classList.toggle('collapsed');
        toggleBtn.classList.toggle('expanded');
        toggleBtn.innerHTML = collapsed ? '&#9660;' : '&#9650;';
    });
}

// ===== 좋아요 토글 =====
document.addEventListener('click', (e) => {
    const likeBtn = e.target.closest('.glt2-like-btn');
    if (!likeBtn) return;

    const userId = likeBtn.dataset.id;

    fetch(URL_LIKE_TOGGLE, {
        method: "POST",
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `llm_id=${userId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'like') {
            likeBtn.innerHTML = '<span class="heart-filled"></span>';
        } else if (data.status === 'unlike') {
            likeBtn.innerHTML = '<span class="heart-empty"></span>';
        } else {
            alert(data.message);
        }
    })
    .catch(err => console.error("좋아요 토글 오류:", err));
});

// ===== 팔로우 토글 =====
document.addEventListener('click', (e) => {
    const followBtn = e.target.closest('.glt2-follow-btn');
    if (!followBtn) return;

    const userId = followBtn.dataset.id;
    if (!userId) return;

    fetch(URL_TOGGLE_FOLLOW, {
        method: "POST",
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `user_id=${encodeURIComponent(userId)}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'follow') {
            followBtn.textContent = "Following";
            followBtn.classList.add('following');
        } else if (data.status === 'unfollow') {
            followBtn.textContent = "Follow";
            followBtn.classList.remove('following');
        } else {
            alert(data.message);
        }
    })
    .catch(err => console.error("팔로우 토글 오류:", err));
});

// ===== 목소리 저장 =====
function saveVoice(celebrityId) {
    fetch(URL_SAVE_VOICE, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ "celebrity_id": celebrityId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "ok") {
            alert("보이스가 저장되었습니다!");
        } else if (data.status === "exists") {
            alert("이미 저장된 보이스입니다.");
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error("보이스 저장 오류:", error));
}
