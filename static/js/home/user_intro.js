        // 모달 기능
        function openModal(llmId) {
            const modal = document.getElementById('modalOverlay');
            const modalContent = document.getElementById('modalContent');
            
            modalContent.innerHTML = `
                <h2 style="color: white; margin-bottom: 20px;">AI 상세 정보</h2>
                <p style="color: #b8c5d1; line-height: 1.6;">
                    선택하신 AI의 상세 정보입니다. 
                </p>
                <div style="margin-top: 30px; text-align: center;">
                    <button style="
                        padding: 12px 30px;
                        background: linear-gradient(135deg, #4facfe, #00f2fe);
                        border: none;
                        border-radius: 25px;
                        color: white;
                        font-weight: 600;
                        cursor: pointer;
                    " onclick="closeModal()">
                        대화 시작하기
                    </button>
                </div>
            `;
            
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            const modal = document.getElementById('modalOverlay');
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }

        // 모달 이벤트
        document.getElementById('modalOverlay').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        document.getElementById('modalClose').addEventListener('click', closeModal);

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeModal();
        });

        // 가로 스크롤 개선
        document.querySelectorAll('.ai-scroll, .prompt-scroll').forEach(container => {
            let isDown = false;
            let startX;
            let scrollLeft;

            container.addEventListener('mousedown', (e) => {
                isDown = true;
                startX = e.pageX - container.offsetLeft;
                scrollLeft = container.scrollLeft;
            });

            container.addEventListener('mouseleave', () => {
                isDown = false;
            });

            container.addEventListener('mouseup', () => {
                isDown = false;
            });

            container.addEventListener('mousemove', (e) => {
                if (!isDown) return;
                e.preventDefault();
                const x = e.pageX - container.offsetLeft;
                const walk = (x - startX) * 2;
                container.scrollLeft = scrollLeft - walk;
            });

            // 마우스 휠로 가로 스크롤
            container.addEventListener('wheel', (e) => {
                if (e.deltaY !== 0) {
                    e.preventDefault();
                    container.scrollLeft += e.deltaY;
                }
            });
        });

