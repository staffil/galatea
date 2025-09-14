       
       


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

  // LLM 모달
    function openModal(LLM_id) {
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


        fetch(`/${LANGUAGE_CODE}/intro/${LLM_id}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('llm-container').innerHTML = html;
        });
    }

    function closeModal() {
        const modal = document.getElementById('llm-modal');
        if (modal) modal.remove();
    document.body.style.overflow = "auto";
    document.documentElement.style.overflow = "auto";

    }

    // 초기화
    document.addEventListener('DOMContentLoaded', () => {
        initNewsSlider();
    });



    