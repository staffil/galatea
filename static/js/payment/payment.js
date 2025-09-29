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

    // PayPal V2 결제 함수
    async function requestPayPalV2(btn) {
        const merchant_uid = "order_" + new Date().getTime();
        const dallerAmount = parseFloat(btn.getAttribute("data-daller-price"));
        const rank_id = btn.getAttribute("data-rank-id");
        const channelKey = btn.getAttribute("data-channel");

        btn.classList.add('loading');

        try {
            // V2 SDK 초기화 시도
            if (typeof PortOne !== 'undefined') {
                console.log("PortOne V2 SDK loaded successfully");
            } else {
                throw new Error("PortOne V2 SDK not loaded");
            }

            // 다양한 storeId 형식 시도 (하나씩 테스트)
            let storeIdToTry;
            
            // 방법 1: 기존 형식 그대로
            storeIdToTry = "store-05d93aaf-0f35-4c2b-b72e-e56011f78d9e";
            
            // 방법 2: store- 접두사 제거 (주석 해제하여 테스트)
            // storeIdToTry = "05d93aaf-0f35-4c2b-b72e-e56011f78d9e";
            
            // 방법 3: V1 가맹점 코드 사용 (주석 해제하여 테스트) 
            // storeIdToTry = "imp28654630";

            const paymentData = {
                storeId: "store-05d93aaf-0f35-4c20-b72e-e56011f78d9e",
                paymentId: merchant_uid,
                orderName: "GALATEA 등급 결제",
                totalAmount: Math.round(dallerAmount * 100), // 센트 단위로 변환
                currency: "USD",
                channelKey: channelKey,
                payMethod: "PAYPAL",
                customer: {
                    customerId: "{{ request.user.id }}",
                    firstName: "{{ request.user.first_name|default:'User' }}",
                    lastName: "{{ request.user.last_name|default:'Name' }}",
                    phoneNumber: "{{ request.user.phonenumber|default:'010-0000-0000' }}",
                    email: "{{ request.user.email }}"
                }
            };

            console.log("시도하는 storeId:", paymentData.storeId);

            console.log("=== PayPal V2 Payment Data ===", paymentData);

            // PortOne V2 결제 요청
            const response = await PortOne.requestPayment(paymentData);

            if (response.code != null) {
                alert(`결제 실패: ${response.message}`);
                return;
            }

            console.log("=== PayPal V2 Response ===", response);

            // 결제 성공 - 서버에서 검증
            const verificationResult = await fetch(`{% url 'payment:verify_payment_v2' %}`, {
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

    // 기존 V1 결제 함수 (PayPal 제외)
    function requestPayV1(pgName, btn) {
        const merchant_uid = "order_" + new Date().getTime();
        const amountKRW = parseInt(btn.getAttribute("data-price"), 10);
        const rank_id = btn.getAttribute("data-rank-id");

        const isMobile = window.innerWidth <= 480;

        let data;

        if (pgName.toLowerCase() === "kg") {
            data = {
                pg: "html5_inicis",
                pay_method: "card",
                merchant_uid: merchant_uid,
                amount: amountKRW,
                buyer_email: "{{ request.user.email }}",
                buyer_name: "{{ request.user.get_full_name|default:request.user.username }}",
                buyer_tel: "{{ request.user.phonenumber }}",
                m_redirect_url: "https://galatea.website/payment/complete/",
                name: "GALATEA 등급 결제",
            };
        } else {
            data = {
                pg: pgName.toLowerCase(),
                pay_method: "card",
                merchant_uid: merchant_uid,
                amount: amountKRW,
                buyer_email: "{{ request.user.email }}",
                buyer_name: "{{ request.user.get_full_name|default:request.user.username }}",
                buyer_tel: "{{ request.user.phonenumber }}",
                m_redirect_url: "https://galatea.website/payment/complete/",
                name: "GALATEA 등급 결제",
            };
        }

        // 모바일이면 m_redirect_url에 rank_id 추가
        if (isMobile) {
            data.m_redirect_url = `https://galatea.website/payment/complete/?merchant_uid=${merchant_uid}&rank_id=${rank_id}`;
        }


        btn.classList.add('loading');

        IMP.init("imp28654630"); // V1 API 사용

        IMP.request_pay(data, function(rsp) {
            btn.classList.remove('loading');
            if (rsp.success) {
                fetch("{% url 'payment:verify_payment' %}?imp_uid=" + rsp.imp_uid + "&merchant_uid=" + merchant_uid + "&rank_id=" + rank_id)
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

    // 메인 결제 함수 - PayPal은 V2, 나머지는 V1
    window.requestPay = function(pgName, btn) {
        console.log("requestPay 호출됨:", pgName);
        if (pgName.toLowerCase() === "paypal") {
            // PayPal은 V2 API 사용
            console.log("PayPal V2 결제 시작");
            requestPayPalV2(btn);
        } else {
            // 다른 PG는 기존 V1 API 사용
            console.log("V1 결제 시작:", pgName);
            requestPayV1(pgName, btn);
        }
    };


    // ⭐ 중요: window 객체에 함수 등록 (전역으로 노출)
window.requestPay = function(pgName, btn) {
    console.log("requestPay 호출됨:", pgName);
    if (pgName.toLowerCase() === "paypal") {
        console.log("PayPal V2 결제 시작");
        requestPayPalV2(btn);
    } else {
        console.log("V1 결제 시작:", pgName);
        requestPayV1(pgName, btn);
    }
};