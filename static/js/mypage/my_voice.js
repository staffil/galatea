  function copyToClipboard(text){
        navigator.clipboard.writeText(text).then(() => {
            alert("id 가 복사되었습니다.")
        }).catch(err => {
            alert('복사에 실패했습니다.')
        })
    }
      // 클립보드에 복사하는 함수
        function copyToClipboard(text) {
            if (navigator.clipboard && window.isSecureContext) {
                // 모던 브라우저에서 Clipboard API 사용
                navigator.clipboard.writeText(text).then(() => {
                    showCopyFeedback();
                }).catch(err => {
                    fallbackCopyTextToClipboard(text);
                });
            } else {
                // 폴백 방법
                fallbackCopyTextToClipboard(text);
            }
        }

        // 폴백 복사 방법
        function fallbackCopyTextToClipboard(text) {
            const textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.top = "0";
            textArea.style.left = "0";
            textArea.style.position = "fixed";
            textArea.style.opacity = "0";
            
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                showCopyFeedback();
            } catch (err) {
                console.error('복사 실패:', err);
                alert('{% trans "복사에 실패했습니다. 수동으로 복사해주세요." %}');
            }
            
            document.body.removeChild(textArea);
        }

        // 복사 완료 피드백 표시
        function showCopyFeedback() {
            // 기존 알림 제거
            const existingAlert = document.querySelector('.copy-alert');
            if (existingAlert) {
                existingAlert.remove();
            }

            // 새 알림 생성
            const alert = document.createElement('div');
            alert.className = 'copy-alert';
            alert.innerHTML = '✅ {% trans "복사되었습니다!" %}';
            alert.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                padding: 15px 25px;
                border-radius: 12px;
                font-weight: 600;
                z-index: 10000;
                box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
                animation: copyFadeIn 0.3s ease;
            `;

            document.body.appendChild(alert);

            // 2초 후 제거
            setTimeout(() => {
                alert.style.animation = 'copyFadeOut 0.3s ease';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 300);
            }, 2000);
        }

        // CSS 애니메이션 추가
        const style = document.createElement('style');
        style.textContent = `
            @keyframes copyFadeIn {
                from { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
                to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            }
            @keyframes copyFadeOut {
                from { opacity: 1; transform: translate(-50%, -50%) scale(1); }
                to { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
            }
        `;
        document.head.appendChild(style);

        // 사이드바 토글 함수들 (기존 sidebar.js와 연동)
        function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            const menuToggle = document.querySelector('.menu-toggle');
            
            if (sidebar && overlay && menuToggle) {
                sidebar.classList.toggle('active');
                overlay.style.display = sidebar.classList.contains('active') ? 'block' : 'none';
                menuToggle.classList.toggle('active');
            }
        }

        function closeSidebar() {
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            const menuToggle = document.querySelector('.menu-toggle');
            
            if (sidebar && overlay && menuToggle) {
                sidebar.classList.remove('active');
                overlay.style.display = 'none';
                menuToggle.classList.remove('active');
            }
        }

        // 화면 크기 변경 시 사이드바 상태 리셋
        window.addEventListener('resize', () => {
            if (window.innerWidth > 1024) {
                closeSidebar();
            }
        });
