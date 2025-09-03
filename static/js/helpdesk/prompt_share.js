// 기존 FAQ 스크립트
document.querySelectorAll('.faq-question').forEach((btn) => {
    btn.addEventListener('click', () => {
        const item = btn.parentElement;
        item.classList.toggle('active');
    });
});

// 프롬프트 관련 스크립트
function toggleLike(promptId) {
    console.log('Like toggled for prompt:', promptId);
}

function toggleBookmark(promptId) {
    console.log('Bookmark toggled for prompt:', promptId);
}

function sharePrompt(promptId) {
    if (navigator.share) {
        navigator.share({
            title: '{% trans "프롬프트 공유" %}',
            text: '{% trans "이 프롬프트를 확인해보세요!" %}',
            url: window.location.href
        });
    } else {
        navigator.clipboard.writeText(window.location.href);
        alert('{% trans "링크가 클립보드에 복사되었습니다!" %}');
    }
}

// 검색 기능
document.querySelector('.search-input').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
});

// 필터 기능
document.querySelectorAll('.filter-select').forEach(select => {
    select.addEventListener('change', function() {});
});