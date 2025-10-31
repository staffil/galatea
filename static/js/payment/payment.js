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

// KG 이니시스 V2 결제 함수
async function requestInicisV2(btn) {
    const merchant_uid = "order_" + new Date().getTime();
    const amountKRW = parseInt(btn.getAttribute("data-price"), 10);
    const rank_id = btn.getAttribute("data-rank-id");
    const channelKey = btn.getAttribute("data-channel");

    btn.classList.add('loading');

    try {
        if (typeof PortOne === 'undefined') {
            throw new Error("PortOne V2 SDK not loaded");
        }

        const paymentData = {
            storeId: "store-05d93aaf-0f35-4c20-b72e-e56011f78d9e",
            paymentId: merchant_uid,
            orderName: "GALATEA 등급 결제",
            totalAmount: amountKRW,
            currency: "KRW",
            channelKey: channelKey,
            payMethod: "CARD",
            customer: {
                customerId: btn.getAttribute("data-user-id") || "guest",
                fullName: btn.getAttribute("data-buyer-name") || "",
                phoneNumber: btn.getAttribute("data-buyer-tel") || "",
                email: btn.getAttribute("data-buyer-email") || ""
            },
            // 결제 완료 후 이동할 페이지
            redirectUrl: `https://galatea.website/payment/complete/?merchant_uid=${merchant_uid}&rank_id=${rank_id}`
        };

        console.log("=== KG Inicis V2 Payment Data ===", paymentData);

        const response = await PortOne.requestPayment(paymentData);

        console.log("=== KG Inicis V2 Response ===", response);
        console.log("Response paymentId:", response.paymentId);
        console.log("Response 전체:", JSON.stringify(response, null, 2));

        if (response.code != null) {
            alert(`결제 실패: ${response.message}`);
            return;
        }

        // ✅ 서버 검증 fetch 제거
        alert("결제 요청이 완료되었습니다. 결제 페이지로 이동합니다.");
        
    } catch (error) {
        console.error('KG Inicis V2 Payment error:', error);
        alert("결제 처리 중 오류가 발생했습니다: " + error.message);
    } finally {
        btn.classList.remove('loading');
    }
}

// PayPal V2 결제 함수
async function requestPayPalV2(btn) {
    const merchant_uid = "order_" + new Date().getTime();
    const dallerAmount = parseFloat(btn.getAttribute("data-daller-price"));
    const rank_id = btn.getAttribute("data-rank-id");
    const channelKey = btn.getAttribute("data-channel");

    btn.classList.add('loading');

    try {
        if (typeof PortOne === 'undefined') {
            throw new Error("PortOne V2 SDK not loaded");
        }

        const paymentData = {
            storeId: "store-05d93aaf-0f35-4c20-b72e-e56011f78d9e",
            paymentId: merchant_uid,
            orderName: "GALATEA 등급 결제",
            totalAmount: Math.round(dallerAmount * 100),
            currency: "USD",
            channelKey: channelKey,
            payMethod: "PAYPAL",
            customer: {
                customerId: btn.getAttribute("data-user-id") || "guest",
                email: btn.getAttribute("data-buyer-email") || ""
            },
            redirectUrl: `https://galatea.website/payment/complete/?merchant_uid=${merchant_uid}&rank_id=${rank_id}`
        };

        console.log("=== PayPal V2 Payment Data ===", paymentData);

        const response = await PortOne.requestPayment(paymentData);

        if (response.code != null) {
            alert(`결제 실패: ${response.message}`);
            return;
        }

        console.log("=== PayPal V2 Response ===", response);
        alert("결제 요청이 완료되었습니다. 결제 페이지로 이동합니다.");

    } catch (error) {
        console.error('PayPal V2 Payment error:', error);
        alert("결제 처리 중 오류가 발생했습니다: " + error.message);
    } finally {
        btn.classList.remove('loading');
    }
}

// 기존 V1 결제 함수
function requestPayV1(pgName, btn) {
    const merchant_uid = "order_" + new Date().getTime();
    const amountKRW = parseInt(btn.getAttribute("data-price"), 10);
    const rank_id = btn.getAttribute("data-rank-id");
    const isMobile = window.innerWidth <= 480;

    // PG사별 코드 매핑
    let pgCode;
    const pgLower = pgName.toLowerCase();
    if (pgLower === "kakaopay" || pgLower === "kakao") {
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
        m_redirect_url: "https://galatea.website/payment/complete/",
        name: "GALATEA 등급 결제",
    };

    if (isMobile) {
        data.m_redirect_url = `https://galatea.website/payment/complete/?merchant_uid=${merchant_uid}&rank_id=${rank_id}`;
    }

    console.log("=== V1 request_pay data ===", data);

    btn.classList.add('loading');

    IMP.init("imp28654630");

    IMP.request_pay(data, function(rsp) {
        btn.classList.remove('loading');
        if (rsp.success) {
            alert("결제 성공! 결제 완료 페이지로 이동합니다.");
            window.location.href = `/payment/complete/?merchant_uid=${merchant_uid}&rank_id=${rank_id}`;
        } else {
            alert("결제 실패: " + rsp.error_msg);
        }
    });
}

// 전역 함수
window.requestPay = function(pgName, btn) {
    console.log("requestPay 호출됨:", pgName);
    const pgLower = pgName.toLowerCase();

    if (pgLower === "paypal") {
        console.log("PayPal V2 결제 시작");
        requestPayPalV2(btn);
    } else if (pgLower === "kg" || pgLower === "kg이니시스" || pgLower === "inicis") {
        console.log("KG 이니시스 V2 결제 시작");
        requestInicisV2(btn);
    } else {
        console.log("V1 결제 시작:", pgName);
        requestPayV1(pgName, btn);
    }
};
const response = await PortOne.requestPayment(paymentData);

console.log("=== KG Inicis V2 Response ===", response);

if (response.code != null) {
    alert(`결제 실패: ${response.message}`);
    return;
}

// ✅ 서버 검증 호출
await fetch("/payment/verify_payment_v2/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken()
    },
    body: JSON.stringify({
        payment_id: response.paymentId,
        merchant_uid: merchant_uid,
        rank_id: rank_id
    })
});

alert("결제 요청이 완료되었습니다. 결제 페이지로 이동합니다.");
