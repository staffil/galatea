        // 입력 필드에 포커스 효과 추가
        const input = document.querySelector('input[type="text"]');
        
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });

        // 폼 제출 시 간단한 애니메이션
        document.querySelector('form').addEventListener('submit', function(e) {
            const btn = document.querySelector('.submit-btn');
            btn.style.transform = 'scale(0.95)';
            btn.innerHTML = '처리 중...';
        });



        