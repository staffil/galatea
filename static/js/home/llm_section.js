


// llm_section.js (외부 JS)
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

// 모달 열기/닫기
window.openModal = function(llm_id) {
    const modalHTML = `
    <div id="llm-modal">
        <div class="modal-overlay" onclick="closeModal()"></div>
        <div class="modal-content">
            <button class="close-btn" onclick="closeModal()">X</button>
            <div id="llm-container" class="llm-container"></div>
        </div>
    </div>`;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
    document.body.style.overflow = "hidden";
    document.documentElement.style.overflow = "hidden";

    // URL 안전하게 구성
    const url = `/${LANGUAGE_CODE}/intro/${llm_id}/`;

    fetch(url)
        .then(res => res.text())
        .then(html => {
            document.getElementById('llm-container').innerHTML = html;
        })
        .catch(err => console.error("LLM fetch error:", err));
}

window.closeModal = function() {
    const modal = document.getElementById('llm-modal');
    if (modal) modal.remove();
    document.body.style.overflow = "auto";
    document.documentElement.style.overflow = "auto";
}

// 이벤트 위임: like / follow 버튼
document.addEventListener('click', (e) => {
    const likeBtn = e.target.closest('.glt2-like-btn');
    if (likeBtn) {
        const userId = likeBtn.dataset.id;
        fetch("/home/like_toggle/", {  // CSRF_TOKEN 변수 사용 가능
            method: "POST",
            headers: {
                "X-CSRFToken": CSRF_TOKEN,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `llm_id=${userId}`
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'like') likeBtn.innerHTML = '<span class="heart-filled"></span>';
            else if (data.status === 'unlike') likeBtn.innerHTML = '<span class="heart-empty"></span>';
            else alert(data.message);
        });
    }

    const followBtn = e.target.closest('.glt2-follow-btn');
    if (followBtn) {
        const userId = followBtn.dataset.id;
        fetch("/home/toggle_follow/", {
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
            } else alert(data.message);
        });
    }
});
    // 초기화
    document.addEventListener('DOMContentLoaded', () => {
        initNewsSlider();
    });