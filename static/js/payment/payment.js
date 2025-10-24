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

// KG 이니시스 V2 결제 함수 수정
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
            redirectUrl: `https://galatea.website/payment/complete/?merchant_uid=${merchant_uid}&rank_id=${rank_id}`
        };

        console.log("=== KG Inicis V2 Payment Data ===", paymentData);

        const response = await PortOne.requestPayment(paymentData);

        // 👇 Response 상세 확인
        console.log("=== KG Inicis V2 Response ===", response);
        console.log("Response code:", response.code);
        console.log("Response message:", response.message);
        console.log("Response paymentId:", response.paymentId);
        console.log("Response 전체:", JSON.stringify(response, null, 2));

        // code가 null이 아니면 결제 실패
        if (response.code != null) {
            alert(`결제 실패: ${response.message}`);
            return;
        }

        // 결제 성공 - 서버에서 검증
        console.log("서버 검증 시작...");
        const verificationResult = await fetch('/payment/verify_payment_v2/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                payment_id: response.paymentId,
                merchant_uid: merchant_uid,
                rank_id: rank_id
            })
        });

        console.log("서버 응답 상태:", verificationResult.status);
        const result = await verificationResult.json();
        console.log("서버 응답 내용:", result);
        
        if (result.status === 'success') {
            alert('결제가 성공적으로 완료되었습니다!');
            window.location.href = "/payment/complete/";
        } else {
    console.error("결제 실패 상세:", result);
    alert("결제 처리 실패: " + (result.message || JSON.stringify(result)));
        }

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
        if (typeof PortOne !== 'undefined') {
        } else {
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
            }
        };

        console.log("=== PayPal V2 Payment Data ===", paymentData);

        const response = await PortOne.requestPayment(paymentData);

        if (response.code != null) {
            alert(`결제 실패: ${response.message}`);
            return;
        }

        console.log("=== PayPal V2 Response ===", response);

        // 결제 성공 - 서버에서 검증
        const verificationResult = await fetch('/payment/verify_payment_v2/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                payment_id: response.paymentId,
                merchant_uid: merchant_uid,
                rank_id: rank_id
            })
        });

        const result = await verificationResult.json();
        
        if (result.status === 'success') {
            alert('결제가 성공적으로 완료되었습니다!');
            window.location.href = "/payment/complete/";
        } else {
            alert("결제 처리 실패: " + result.message);
        }

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
            fetch(`/payment/verify_payment/?imp_uid=${rsp.imp_uid}&merchant_uid=${merchant_uid}&rank_id=${rank_id}`)
            .then(res => res.json())
            .then(result => {
                if (result.status) {
                    alert(`결제 성공! 상태: ${result.status}`);
                    window.location.href = "/payment/complete/";
                } else {
                    alert("결제 처리 실패: " + JSON.stringify(result));
                }
            }).catch(err => {
                alert("결제 처리 중 오류가 발생했습니다.");
                console.error(err);
            });
        } else {
            alert("결제 실패: " + rsp.error_msg);
        }
    });
}

// 전역 함수 수정
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