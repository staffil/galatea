


    function createIndicators() {
        const indicatorsContainer = document.getElementById('indicators');
        indicatorsContainer.innerHTML = '';
        
        for (let i = 0; i < totalImages; i++) {
            const indicator = document.createElement('div');
            indicator.className = 'indicator';
            indicator.onclick = () => goToSlide(i);
            indicatorsContainer.appendChild(indicator);
        }
    }

    function updateSlider() {
        if (!newsTab) return;
        const translateX = -(currentSlideIndex * 100);
        newsTab.style.transform = `translateX(${translateX}%)`;
        updateIndicators();
    }

    function updateIndicators() {
        const indicators = document.querySelectorAll('.indicator');
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentSlideIndex);
        });
    }

    function updateButtons() {
        const prevBtn = document.querySelector('.slider-btn.prev');
        const nextBtn = document.querySelector('.slider-btn.next');
        
        if (prevBtn) prevBtn.disabled = currentSlideIndex <= 0;
        if (nextBtn) nextBtn.disabled = currentSlideIndex >= totalImages - 1;
    }

    function slideNews(direction) {
        const newIndex = currentSlideIndex + direction;
        
        if (newIndex < 0 || newIndex >= totalImages) {
            return;
        }
        
        currentSlideIndex = newIndex;
        updateSlider();
        updateButtons();
    }

    function goToSlide(index) {
        if (index < 0 || index >= totalImages) return;
        
        currentSlideIndex = index;
        updateSlider();
        updateButtons();
    }

    // 음성 플레이어
    let currentAudio = null;
    let currentCharacter = null;

    function toggleAudio(character) {
        const wrapper = character.closest('.voice-wrapper');
        const audio = wrapper.querySelector('.voice-audio');
        const playOverlay = character.querySelector('.play-overlay');
        const progressBar = wrapper.querySelector('.voice-progress-bar');
        const timeDisplay = wrapper.querySelector('.voice-time');

        if (currentAudio && currentAudio !== audio) {
            currentAudio.pause();
            currentCharacter.classList.remove('playing');
            currentCharacter.querySelector('.play-overlay').innerHTML = '<div class="play-icon"></div>';
        }

        if (audio.paused) {
            audio.play();
            character.classList.add('playing');
            playOverlay.innerHTML = '<div class="pause-icon"></div>';
            currentAudio = audio;
            currentCharacter = character;
            setupAudioEvents(audio, character, progressBar, timeDisplay);
        } else {
            audio.pause();
            character.classList.remove('playing');
            playOverlay.innerHTML = '<div class="play-icon"></div>';
            currentAudio = null;
            currentCharacter = null;
        }
    }

    function setupAudioEvents(audio, character, progressBar, timeDisplay) {
        const playOverlay = character.querySelector('.play-overlay');
        
        audio.removeEventListener('timeupdate', audio._timeUpdateHandler);
        audio.removeEventListener('ended', audio._endedHandler);

        audio._timeUpdateHandler = function() {
            if (audio.duration) {
                const progress = (audio.currentTime / audio.duration) * 100;
                progressBar.style.width = progress + '%';
                
                const currentMin = Math.floor(audio.currentTime / 60);
                const currentSec = Math.floor(audio.currentTime % 60);
                const durationMin = Math.floor(audio.duration / 60);
                const durationSec = Math.floor(audio.duration % 60);
                
                timeDisplay.textContent = 
                    `${currentMin.toString().padStart(2, '0')}:${currentSec.toString().padStart(2, '0')} / ` +
                    `${durationMin.toString().padStart(2, '0')}:${durationSec.toString().padStart(2, '0')}`;
            }
        };

        audio._endedHandler = function() {
            character.classList.remove('playing');
            playOverlay.innerHTML = '<div class="play-icon"></div>';
            progressBar.style.width = '0%';
            timeDisplay.textContent = '00:00 / 00:00';
            currentAudio = null;
            currentCharacter = null;
        };

        audio.addEventListener('timeupdate', audio._timeUpdateHandler);
        audio.addEventListener('ended', audio._endedHandler);
    }

    function seekAudio(event, progressContainer) {
        event.stopPropagation();
        const wrapper = progressContainer.closest('.voice-wrapper');
        const audio = wrapper.querySelector('.voice-audio');
        
        if (audio.duration) {
            const rect = progressContainer.getBoundingClientRect();
            const clickX = event.clientX - rect.left;
            const progress = clickX / rect.width;
            audio.currentTime = progress * audio.duration;
        }
    }

    function copyVoiceId(button) {
        const wrapper = button.closest('.voice-wrapper');
        const hiddenInput = wrapper.querySelector('input[type="hidden"]');
        
        if (hiddenInput && hiddenInput.value) {
            navigator.clipboard.writeText(hiddenInput.value).then(() => {
                const originalText = button.textContent;
                button.textContent = '✓';
                button.classList.add('copied');
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                const textArea = document.createElement('textarea');
                textArea.value = hiddenInput.value;
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    button.textContent = '✓';
                    button.classList.add('copied');
                    setTimeout(() => {
                        button.textContent = '복사';
                        button.classList.remove('copied');
                    }, 2000);
                } catch (err) {
                    alert('복사에 실패했습니다.');
                }
                document.body.removeChild(textArea);
            });
        }
    }

    // LLM 모달
    function openModal(llm_id) {
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

        const LANGUAGE_CODE = "{{ LANGUAGE_CODE }}";
        fetch(`/${LANGUAGE_CODE}/intro/${llm_id}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('llm-container').innerHTML = html;
        });
    }

    function closeModal() {
        const modal = document.getElementById('llm-modal');
        if (modal) modal.remove();
    }


    // 초기화
    document.addEventListener('DOMContentLoaded', () => {
        initNewsSlider();
    });

    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // 쿠키 이름 확인
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



  // LLM 모달
    function openModal(llm_id) {
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


        const LANGUAGE_CODE = "{{ LANGUAGE_CODE }}";
        fetch(`/${LANGUAGE_CODE}/intro/${llm_id}`)
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
  

        // 사이드바 토글
    const toggleBtn = document.getElementById('sidebar-toggle');
    const sidebarContent = document.getElementById('sidebar-content');

    toggleBtn.addEventListener('click', () => {
        const collapsed = sidebarContent.classList.contains('collapsed');
        sidebarContent.classList.toggle('collapsed');
        toggleBtn.classList.toggle('collapsed');
        toggleBtn.classList.toggle('expanded');
        toggleBtn.innerHTML = collapsed ? '&#9660;' : '&#9650;'; // ▼ / ▲
    });

// //팔로우 토글
// document.addEventListener('click', (e) => {
//     const followBtn = e.target.closest('.glt2-follow-btn');
//     if (!followBtn) return;

//     const userId = followBtn.dataset.id;
//     if (!userId) return;

//     fetch("{% url 'home:toggle_follow' %}", {
//         method: "POST",
//         headers: {
//             "X-CSRFToken": "{{ csrf_token }}",
//             "Content-Type": "application/x-www-form-urlencoded"
//         },
//         body: `user_id=${encodeURIComponent(userId)}`
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === 'follow') {
//             followBtn.textContent = 'Following';
//             followBtn.classList.add('following');
//         } else if (data.status === 'unfollow') {
//             followBtn.textContent = 'Follow';
//             followBtn.classList.remove('following');
//         } else {
//             alert(data.message);
//         }
//     })
//     .catch(err => console.error('팔로우 토글 오류:', err));
// });
  

  // 가로 스크롤 개선 스크립트
document.addEventListener('DOMContentLoaded', function() {
    
    // 모든 가로 스크롤 컨테이너
    const horizontalContainers = document.querySelectorAll(
        '.cv-scroll, .genre-tags-container, .character-cards-container, .llm-cards-container'
    );
    
    horizontalContainers.forEach(container => {
        // 마우스 휠로 가로 스크롤
        container.addEventListener('wheel', function(e) {
            if (e.deltaY !== 0) {
                e.preventDefault();
                container.scrollLeft += e.deltaY;
            }
        });
        
        // 드래그 스크롤 (데스크톱)
        let isDown = false;
        let startX;
        let scrollLeft;
        
        container.addEventListener('mousedown', function(e) {
            isDown = true;
            container.style.cursor = 'grabbing';
            startX = e.pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
        });
        
        container.addEventListener('mouseleave', function() {
            isDown = false;
            container.style.cursor = 'grab';
        });
        
        container.addEventListener('mouseup', function() {
            isDown = false;
            container.style.cursor = 'grab';
        });
        
        container.addEventListener('mousemove', function(e) {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - container.offsetLeft;
            const walk = (x - startX) * 2;
            container.scrollLeft = scrollLeft - walk;
        });
        
        // 기본 커서 스타일
        container.style.cursor = 'grab';
    });
    
    // 스크롤 인디케이터 생성 (옵션)
    function createScrollIndicator(container) {
        const indicator = document.createElement('div');
        indicator.className = 'scroll-indicator';
        indicator.style.cssText = `
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%);
            height: 2px;
            background: rgba(139,92,246,0.3);
            border-radius: 1px;
            width: 60px;
        `;
        
        const thumb = document.createElement('div');
        thumb.style.cssText = `
            height: 100%;
            background: linear-gradient(90deg, #8b5cf6, #06b6d4);
            border-radius: 1px;
            transition: width 0.2s ease;
            width: 30%;
        `;
        
        indicator.appendChild(thumb);
        
        // 상대적 위치를 위해 부모에 relative 추가
        const parent = container.parentElement;
        if (parent && getComputedStyle(parent).position === 'static') {
            parent.style.position = 'relative';
        }
        parent.appendChild(indicator);
        
        // 스크롤 이벤트로 인디케이터 업데이트
        container.addEventListener('scroll', function() {
            const scrollPercent = (container.scrollLeft / (container.scrollWidth - container.clientWidth)) * 100;
            thumb.style.width = Math.max(10, Math.min(90, scrollPercent)) + '%';
        });
    }
    
    // 키보드 네비게이션
    document.addEventListener('keydown', function(e) {
        const focusedContainer = document.querySelector('.cv-scroll:hover, .genre-tags-container:hover, .character-cards-container:hover, .llm-cards-container:hover');
        
        if (focusedContainer) {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                focusedContainer.scrollLeft -= 200;
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                focusedContainer.scrollLeft += 200;
            }
        }
    });
    
    // 터치 디바이스에서 스크롤 개선
    if ('ontouchstart' in window) {
        horizontalContainers.forEach(container => {
            container.style.scrollBehavior = 'smooth';
            container.style.WebkitOverflowScrolling = 'touch';
        });
    }
    
    // 접근성: 포커스 시 자동 스크롤
    horizontalContainers.forEach(container => {
        const items = container.children;
        Array.from(items).forEach(item => {
            item.addEventListener('focus', function() {
                const containerRect = container.getBoundingClientRect();
                const itemRect = item.getBoundingClientRect();
                
                if (itemRect.left < containerRect.left) {
                    container.scrollLeft -= (containerRect.left - itemRect.left + 20);
                } else if (itemRect.right > containerRect.right) {
                    container.scrollLeft += (itemRect.right - containerRect.right + 20);
                }
            });
        });
    });
});

// 스크롤 성능 최적화
const optimizeScroll = () => {
    const containers = document.querySelectorAll('.cv-scroll, .genre-tags-container, .character-cards-container, .llm-cards-container');
    
    containers.forEach(container => {
        container.style.scrollBehavior = 'smooth';
        
        // Intersection Observer로 뷰포트 밖 요소 최적화
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.transform = 'none';
                } else {
                    entry.target.style.transform = 'translateZ(0)'; // 하드웨어 가속
                }
            });
        }, {
            root: container,
            rootMargin: '50px'
        });
        
        Array.from(container.children).forEach(child => {
            observer.observe(child);
        });
    });
};

// 페이지 로드 후 최적화 실행
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', optimizeScroll);
} else {
    optimizeScroll();
}

let currentSlide = 0;
const slides = document.querySelectorAll('.news-slide');
const indicators = document.querySelectorAll('.indicator');
const slider = document.getElementById('newsSlider');

function slideNews(direction) {
    if (slides.length <= 1) return;
    
    currentSlide += direction;
    
    if (currentSlide >= slides.length) {
        currentSlide = 0;
    } else if (currentSlide < 0) {
        currentSlide = slides.length - 1;
    }
    
    updateSlider();
}

function goToSlide(index) {
    if (slides.length <= 1) return;
    
    currentSlide = index;
    updateSlider();
}

function updateSlider() {
    if (!slider) return;
    
    slider.style.transform = `translateX(-${currentSlide * 100}%)`;
    
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentSlide);
    });
}

// 자동 슬라이드 (5초마다)
if (slides.length > 1) {
    setInterval(() => {
        slideNews(1);
    }, 5000);
}

// 키보드 네비게이션
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        slideNews(-1);
    } else if (e.key === 'ArrowRight') {
        slideNews(1);
    }
});

// 터치 스와이프 지원 (모바일)
let startX = 0;
let endX = 0;

slider?.addEventListener('touchstart', (e) => {
    startX = e.changedTouches[0].screenX;
});

slider?.addEventListener('touchend', (e) => {
    endX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const threshold = 50; // 최소 스와이프 거리
    const diff = startX - endX;
    
    if (Math.abs(diff) > threshold) {
        if (diff > 0) {
            slideNews(1); // 왼쪽으로 스와이프 = 다음 슬라이드
        } else {
            slideNews(-1); // 오른쪽으로 스와이프 = 이전 슬라이드
        }
    }
}


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
    .catch(err => console.error('좋아요 토글 오류:', err))
})

    // 카드 클릭 시 모달 열기
    document.querySelectorAll('.glt2-card').forEach(card => {
        card.addEventListener('click', (e) => {
            // 버튼 클릭이면 모달 열지 않음
            if (e.target.closest('.glt2-follow-btn') || e.target.closest('.glt2-like-btn') || e.target.closest('.glt2-chat-btn')) return;

            // 카드 내용 모달로 복사
            modalContent.innerHTML = card.innerHTML;
            modalOverlay.style.display = 'flex';
        });
    });

document.addEventListener("click", function(e) {
    if (e.target.classList.contains("share-btn")) {
        const link = e.target.getAttribute("data-link");
        navigator.clipboard.writeText(link).then(() => {
            alert("링크가 복사되었습니다!");
        });
    }
});

// 목소리 저장하기
function saveVoice(celebrityId){
    fetch("{% url 'home:save_voice' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken') // CSRF 처리
        },
        body: JSON.stringify({ "celebrity_id": celebrityId })
    })
    .then(res => res.json())
    .then(data=>{
        if (data.status === "ok") {
            alert("보이스가 저장되었습니다!");
        }else if (data.status === "exists") alert("이미 저장된 보이스입니다.");
        else alert(data.error);
        })
        
    .catch(error => console.error("Error:", error));
}


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
                followBtn.textContent = 'Following';
                followBtn.classList.add('following');
            } else if (data.status === 'unfollow') {
                followBtn.textContent = 'Follow';
                followBtn.classList.remove('following');
            } else {
                alert(data.message);
            }
        })
        .catch(err => console.error('팔로우 토글 오류:', err));
    });




