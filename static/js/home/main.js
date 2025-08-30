


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






