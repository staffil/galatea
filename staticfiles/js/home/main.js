    :root {
            --pink-bg-light: rgba(255, 182, 193, 0.2);
            --purple-bg-light: rgba(221, 160, 221, 0.2);
            --blue-bg-light: rgba(173, 216, 230, 0.2);
            --text-color: #333;
            --main-pink: #F359DE;
        }

        body {
            font-family: 'Noto Sans KR', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            min-height: 100vh;
            padding-top: 80px;
            position: relative;
            overflow-x: hidden;
        }

        .circle-bg {
            position: absolute;
            border-radius: 50%;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            z-index: -1;
        }

        .circle-1 {
            width: 3000px;
            height: 3000px;
            background: rgba(243, 89, 222, 0.12);
        }

        .circle-2 {
            width: 2400px;
            height: 2400px;
            background: rgba(243, 89, 222, 0.28);
        }

        .circle-3 {
            width: 1800px;
            height: 1800px;
            background: rgba(243, 89, 222, 0.51);
        }

        .circle-4 {
            width: 1200px;
            height: 1200px;
            background: rgba(243, 89, 222, 0.28);
        }

        .circle-5 {
            width: 800px;
            height: 800px;
            background: #F359DE;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .circle-5 img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 50%;
        }

        .main-content {
            width: 100%;
            max-width: 1200px;
            padding: 20px;
            text-align: center;
            position: relative;
            z-index: 1;
            margin: 90px auto 50px auto;
        }

        .section-title {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #333;
            text-align: left;
            margin-bottom: 40px;
            padding-left: 20px;
        }

        .character-cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 35px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .character-card {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
            border-radius: 25px;
            padding: 0;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                0 1px 8px rgba(0, 0, 0, 0.06);
            text-align: center;
            width: 100%;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }

        .character-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transition: left 0.6s;
        }

        .character-card:hover::before {
            left: 100%;
        }

        .character-card:hover {
            transform: translateY(-12px) scale(1.02);
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.15),
                0 5px 15px rgba(243, 89, 222, 0.2);
            cursor: pointer;
        }

        .card-header {
            background: linear-gradient(135deg, #F359DE, #E91E63);
            color: white;
            padding: 25px 20px;
            margin: 0;
            position: relative;
            overflow: hidden;
        }

        .card-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
            transform: rotate(45deg);
            transition: all 0.3s ease;
        }

        .character-card:hover .card-header::before {
            transform: rotate(45deg) scale(1.2);
        }

        .celebrity-name {
            font-size: 1.6rem;
            font-weight: 900;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            position: relative;
            z-index: 1;
        }

        .card-content {
            padding: 30px 25px;
            display: flex;
            flex-direction: column;
            align-items: center;
            flex-grow: 1;
            position: relative;
        }

        .character-image {
            position: relative;
            margin-bottom: 25px;
        }

        .character-image img {
            width: 100%;
            height: 400px;
            object-fit: cover;
            border: 4px solid #fff;
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.15),
                0 0 0 2px rgba(243, 89, 222, 0.3);
            transition: all 0.4s ease;
        }

        .character-card:hover .character-image img {
            transform: scale(1.1);
            box-shadow: 
                0 12px 35px rgba(0, 0, 0, 0.2),
                0 0 0 4px rgba(243, 89, 222, 0.5);
        }

        .character-image::after {
            content: '';
            position: absolute;
            top: -8px;
            left: -8px;
            right: -8px;
            bottom: -8px;
            border-radius: 50%;
            background: conic-gradient(#F359DE, #E91E63, #9C27B0, #673AB7, #F359DE);
            z-index: -1;
            opacity: 0;
            transition: opacity 0.4s ease;
        }

        .character-card:hover .character-image::after {
            opacity: 0.7;
            animation: rotate 3s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .character-description {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 1rem;
            line-height: 1.7;
            color: #555;
            text-align: left;
            background: rgba(248, 249, 250, 0.8);
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #F359DE;
            position: relative;
            flex-grow: 1;
            display: flex;
            align-items: center;
        }

        .character-description::before {
            content: '"';
            font-size: 3rem;
            color: #F359DE;
            position: absolute;
            top: -10px;
            left: 10px;
            font-family: Georgia, serif;
            opacity: 0.3;
        }

        .chat-button {
            margin-top: 25px;
            padding: 12px 30px;
            background: linear-gradient(135deg, #F359DE, #E91E63);
            color: white;
            border: none;
            border-radius: 25px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(243, 89, 222, 0.3);
            position: relative;
            overflow: hidden;
        }

        .chat-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.6s;
        }

        .chat-button:hover::before {
            left: 100%;
        }

        .chat-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(243, 89, 222, 0.4);
        }

        .status-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #4CAF50;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
            100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
        }

        /* 카드별 색상 테마 */
        .character-card.pink .card-header {
            background: linear-gradient(135deg, #FF6B9D, #F359DE);
        }

        .character-card.purple .card-header {
            background: linear-gradient(135deg, #9C27B0, #673AB7);
        }

        .character-card.blue .card-header {
            background: linear-gradient(135deg, #2196F3, #3F51B5);
        }

        .character-card.pink .character-description {
            border-left-color: #FF6B9D;
        }

        .character-card.purple .character-description {
            border-left-color: #9C27B0;
        }

        .character-card.blue .character-description {
            border-left-color: #2196F3;
        }

        /* 반응형 디자인 */
        @media (max-width: 768px) {
            .section-title {
                font-size: 1.8rem;
                text-align: center;
                padding-left: 0;
            }

            .character-cards-container {
                grid-template-columns: 1fr;
                gap: 25px;
                padding: 10px;
            }

            .character-card {
                min-height: 380px;
            }

            .celebrity-name {
                font-size: 1.4rem;
            }

            .character-description {
                font-size: 0.9rem;
                padding: 15px;
            }
        }