 function copyToClipboard(text){
        navigator.clipboard.writeText(text).then(() => {
            alert("id 가 복사되었습니다.")
        }).catch(err => {
            alert('복사에 실패했습니다.')
        })
    }