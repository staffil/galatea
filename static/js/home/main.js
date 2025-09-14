window.openUserModal = function(USER_ID) {
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

    fetch(`/${LANGUAGE_CODE}/user_intro/${USER_ID}`)
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