function copyToClipboard() {
    navigator.clipboard.writeText(window.location.href).then(function() {
        alert("{% trans '링크가 클립보드에 복사되었습니다.' %}");
    });
}

function printPage() {
    window.print();
}