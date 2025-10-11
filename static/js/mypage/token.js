        // 토큰 사용률 애니메이션
        document.addEventListener('DOMContentLoaded', function() {
            const progressBar = document.querySelector('.token-progress-bar');
            if (progressBar) {
                const targetWidth = progressBar.style.width;
                progressBar.style.width = '0%';
                
                setTimeout(() => {
                    progressBar.style.width = targetWidth;
                }, 500);
            }

            // 토큰 카드 애니메이션
            const tokenCards = document.querySelectorAll('.token-card');
            tokenCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 200 * (index + 1));
            });
        });

        // 반응형 대응
        function handleResize() {
            const isMobile = window.innerWidth <= 768;
            const tokenCards = document.querySelectorAll('.token-card');
            
            tokenCards.forEach(card => {
                const icon = card.querySelector('.token-icon');
                const info = card.querySelector('.token-info');
                
                if (isMobile) {
                    card.style.display = 'flex';
                    card.style.textAlign = 'left';
                } else {
                    card.style.display = 'block';
                    card.style.textAlign = 'center';
                }
            });
        }

        window.addEventListener('resize', handleResize);
        window.addEventListener('orientationchange', handleResize);
        handleResize(); // 초기 실행



// static/js/mypage/token.js
let selectedPaymentId = null;

function requestRefund(paymentId, tokenAmount) {
    selectedPaymentId = paymentId;
    document.getElementById('refundTokenAmount').textContent = tokenAmount + 'T';
    
    if (confirm(`환불 요청 시 ${tokenAmount} 토큰이 차감됩니다. 계속하시겠습니까?`)) {
        document.getElementById('refundModal').style.display = 'flex';
    }
}

function closeRefundModal() {
    document.getElementById('refundModal').style.display = 'none';
    document.getElementById('refundReason').value = '';
    selectedPaymentId = null;
}

async function confirmRefund() {
    const reason = document.getElementById('refundReason').value.trim();
    
    if (!reason) {
        alert('환불 사유를 입력해주세요.');
        return;
    }
    
    try {
        const response = await fetch(`/mypage/refund/${selectedPaymentId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ reason: reason })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`환불이 완료되었습니다.\n환불 금액: ${result.refunded_amount}원\n차감 토큰: ${result.refunded_token}T`);
            location.reload();
        } else {
            alert('환불 실패: ' + result.error);
        }
    } catch (error) {
        alert('환불 처리 중 오류가 발생했습니다.');
        console.error(error);
    }
    
    closeRefundModal();
}

function showRefundReason(reason) {
    document.getElementById('reasonText').textContent = reason;
    document.getElementById('reasonModal').style.display = 'flex';
}

function closeReasonModal() {
    document.getElementById('reasonModal').style.display = 'none';
}

function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}