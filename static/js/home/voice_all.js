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
window.saveVoice = function(celebrityId){
    fetch(SAVE_VOICE_URL, {
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
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}
