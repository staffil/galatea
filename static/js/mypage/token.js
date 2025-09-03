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