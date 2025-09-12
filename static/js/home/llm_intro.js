document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.getElementById('glt2ModalOverlay');
    const modalContent = document.getElementById('glt2ModalContent');
    const modalClose = document.getElementById('glt2ModalClose');

    document.querySelectorAll('.glt2-card').forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.closest('.glt2-follow-btn') || e.target.closest('.glt2-like-btn') || e.target.closest('.glt2-chat-btn')) return;

            const contentClone = card.querySelector('.glt2-content').cloneNode(true);
            modalContent.innerHTML = '';
            modalContent.appendChild(contentClone);

            modalOverlay.style.display = 'flex';

            // 모달 내부 버튼 활성화
            modalContent.querySelectorAll('.glt2-like-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const heart = btn.querySelector('span');
                    heart.classList.toggle('heart-filled');
                    heart.classList.toggle('heart-empty');
                });
            });
            modalContent.querySelectorAll('.glt2-follow-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    btn.innerText = btn.innerText === '{% trans "Follow" %}' ? '{% trans "Following" %}' : '{% trans "Follow" %}';
                });
            });
        });
    });

    modalClose.addEventListener('click', () => {
        modalOverlay.style.display = 'none';
        modalContent.innerHTML = '';
    });

    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.style.display = 'none';
            modalContent.innerHTML = '';
        }
    });
});

