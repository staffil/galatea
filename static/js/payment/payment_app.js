const IMP = window.IMP;

// CSRF 토큰 가져오기
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// V1 결제 함수 (PortOne / 아임포트)
function requestPayV1(pgName, btn) {
    const merchant_uid = "order_" + new Date().getTime();
    const amountKRW = parseInt(btn.getAttribute("data-price"), 10);
    const rank_id = btn.getAttribute("data-rank-id");
    const isApp = typeof window.AndroidBridge !== "undefined"; // ✅ 앱 감지

    let pgCode;
    const pgLower = pgName.toLowerCase();

    if (pgLower === "kg" || pgLower === "kg이니시스") {
        pgCode = "inicis";
    } else if (pgLower === "kakaopay" || pgLower === "kakao") {
        pgCode = "kakaopay.CA36348663";
    } else {
        pgCode = pgLower;
    }

    let data = {
        pg: pgCode,
        pay_method: "card",
        merchant_uid: merchant_uid,
        amount: amountKRW,
        buyer_email: btn.getAttribute("data-buyer-email") || "",
        buyer_name: btn.getAttribute("data-buyer-name") || "",
        buyer_tel: btn.getAttribute("data-buyer-tel") || "",
        name: "GALATEA 등급 결제",

        // ✅ 앱에서는 앱 리다이렉트 스킴 사용
        m_redirect_url: isApp
            ? "myapp://payment-result"
            : `https://galatea.website/payment/complete_app/?merchant_uid=${merchant_uid}&rank_id=${rank_id}`,
    };

    console.log("=== V1 request_pay data ===", data);

    btn.classList.add("loading");
    IMP.init("imp28654630");

    IMP.request_pay(data, function (rsp) {
        btn.classList.remove("loading");
        if (rsp.success) {
            fetch(`/payment/verify_payment/?imp_uid=${rsp.imp_uid}&merchant_uid=${merchant_uid}&rank_id=${rank_id}`)
                .then(res => res.json())
                .then(result => {
                    if (result.status) {
                        alert(`결제 성공! 상태: ${result.status}`);
                        if (isApp) {
                            window.location.href = "https://galatea.website/app/mypage_app";
                        } else {
                            window.location.href = "/payment/complete_app/";
                        }
                    } else {
                        alert("결제 처리 실패: " + JSON.stringify(result));
                    }
                })
                .catch(err => {
                    alert("결제 처리 중 오류가 발생했습니다.");
                    console.error(err);
                });
        } else {
            alert("결제 실패: " + rsp.error_msg);
        }
    });
}

// 전역 함수
window.requestPay = function (pgName, btn) {
    console.log("requestPay 호출됨:", pgName);
    requestPayV1(pgName, btn);
};
