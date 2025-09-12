const currentLlmId = LLM_ID;
        let pageNumber = 1;

        function sendNovel() {
            const userText = document.getElementById("text-input").value.trim();
            if(!userText) return;

            const novelContainer = document.getElementById("novel-container");
            const pageNumberElement = document.getElementById("page-number");
            
            // 첫 번째 메시지일 경우 기본 텍스트 제거
            const firstP = novelContainer.querySelector('p:not(.user-message):not(.ai-message)');
            if (firstP && firstP.textContent.includes('AI가 소설체로 답변할 예정입니다')) {
                firstP.remove();
            }
            
            // 사용자 메시지 추가
            const userMessage = document.createElement('p');
            userMessage.className = 'user-message';
            userMessage.innerHTML = `<strong>독자의 요청:</strong> ${userText}`;
            novelContainer.insertBefore(userMessage, pageNumberElement);

            const formData = new FormData();
            formData.append("text", userText);
formData.append("llm_id", LLM_ID);

fetch(NOVEL_PROCESS_URL, {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if(data.novel_text){
                    // AI 메시지 추가 (소설 내용)
                    const aiMessage = document.createElement('p');
                    aiMessage.className = 'ai-message';
                    aiMessage.innerHTML = `<strong>AI:</strong> ${data.novel_text}`;
                    novelContainer.insertBefore(aiMessage, pageNumberElement);
                    
                    // 페이지 번호 업데이트
                    pageNumber++;
                    pageNumberElement.textContent = pageNumber;
                    
                    // 스크롤을 맨 아래로
                    novelContainer.scrollTop = novelContainer.scrollHeight;
                }
                if(data.tts_audio_url){
                    const audioElem = document.getElementById("tts-audio");
                    audioElem.src = data.tts_audio_url;
                    document.getElementById("audio-container").style.display = "block";
                    audioElem.play();
                }
            })
            .catch(err => alert("오류 발생: " + err.message));

            document.getElementById("text-input").value = "";
        }

        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const hamburger = document.querySelector('.hamburger');
            
            sidebar.classList.toggle('active');
            hamburger.classList.toggle('active');
        }

        // 링크 복사하기
        document.addEventListener("click", function(e) {
            if (e.target.classList.contains("share-btn")) {
                const link = e.target.getAttribute("data-link");
                navigator.clipboard.writeText(link).then(() => {
                    alert("링크가 복사되었습니다!");
                });
            }
        });