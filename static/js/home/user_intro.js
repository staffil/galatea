       
       






    // 유저 모달 열기
    function openUserModal(user_id) {
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

        // 안전하게 URL 생성 (STATIC과 LANGUAGE_CODE 영향을 받지 않음)
        fetch(`/user_intro/${user_id}/`)
            .then(res => {
                if (!res.ok) throw new Error('{% trans "사용자 정보를 불러올 수 없습니다" %}');
                return res.text();
            })
            .then(html => {
                document.getElementById('llm-container').innerHTML = html;
            })
            .catch(err => {
                console.error(err);
                alert('{% trans "사용자 정보를 불러오는 데 실패했습니다." %}');
                closeModal();
            });
    }

    function closeModal() {
        const modal = document.getElementById('llm-modal');
        if (modal) modal.remove();
        document.body.style.overflow = "auto";
        document.documentElement.style.overflow = "auto";
    }

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



    
    // 팔로우 토글
    document.addEventListener('click', (e) => {
        const followBtn = e.target.closest('.glt2-follow-btn');
        if (!followBtn) return;

        const userId = followBtn.dataset.id;
        if (!userId) return;

        fetch("{% url 'home:toggle_follow' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `user_id=${encodeURIComponent(userId)}`
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'follow') {
                followBtn.textContent = '{% trans "Following" %}';
                followBtn.classList.add('following');
            } else if (data.status === 'unfollow') {
                followBtn.textContent = '{% trans "Follow" %}';
                followBtn.classList.remove('following');
            } else {
                alert(data.message);
            }
        })
        .catch(err => console.error('{% trans "팔로우 토글 오류:" %}', err));
    });
// like btn
document.addEventListener('click', (e)=>{
    const likeBtn = e.target.closest('.glt2-like-btn');
    if (!likeBtn) return;

    const userId = likeBtn.dataset.id;

    fetch("{% url 'home:like_toggle' %}", {
        method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `llm_id=${userId}`
    })
    .then(response => response.json())
    .then(data=>{
        if (data.status === 'like'){
            likeBtn.innerHTML  = '<span class="heart-filled"></span>';
        } else if(data.status === 'unlike'){
            likeBtn.innerHTML  = '<span class="heart-empty"></span>';
        } else{
            alert(data.message)
        }
 

            


    })
    .catch(err => console.error('{% trans "좋아요 토글 오류:" %}', err))
})