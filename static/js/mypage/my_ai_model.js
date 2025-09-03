        // JS 기능 그대로 유지
        function initializeUIWithCurrentLlm() {
            const initialLlm = {
                id: "{{ llm.id|default:''|escapejs }}",
                prompt: "{{ llm.prompt|default:''|escapejs }}",
                voiceId: "{% if llm.voice %}{{ llm.voice.voice_id|default:''|escapejs }}{% else %}{% endif %}",
                language: "{{ llm.language|default:''|escapejs }}",
                stability: "{{ llm.stability|default:0.5|escapejs }}",
                speed: "{{ llm.speed|default:0.5|escapejs }}",
                style: "{{ llm.style|default:0.5|escapejs }}",
                temperature: "{{ llm.temperature|default:0.5|escapejs }}",
                model: "{{ llm.model|default:''|escapejs }}",
                llmImage: "{% if llm.llm_image %}{{ llm.llm_image.url }}{% else %}{% endif %}"
            };

            const llmImageElem = document.getElementById("llmImage");
            const noImageText = document.getElementById("noImageText");
            if (initialLlm.llmImage) {
                llmImageElem.src = initialLlm.llmImage;
                llmImageElem.style.display = "block";
                noImageText.style.display = "none";
            } else {
                llmImageElem.style.display = "none";
                noImageText.style.display = "block";
            }

            document.getElementById("promptInput").value = initialLlm.prompt;
            document.getElementById("promptDisplay").value = initialLlm.prompt;
            document.getElementById("voiceIdInput").value = initialLlm.voiceId;
            document.getElementById("voiceIdDisplay").value = initialLlm.voiceId;
            document.getElementById("languageInput").value = initialLlm.language;
            document.getElementById("languageDisplay").textContent = initialLlm.language;
            document.getElementById("stabilityInput").value = initialLlm.stability;
            document.getElementById("stabilitySlider").value = initialLlm.stability;
            document.getElementById("stabilityValue").textContent = initialLlm.stability;
            document.getElementById("speedInput").value = initialLlm.speed;
            document.getElementById("speedSlider").value = initialLlm.speed;
            document.getElementById("speedValue").textContent = initialLlm.speed;
            document.getElementById("styleInput").value = initialLlm.style;
            document.getElementById("styleSlider").value = initialLlm.style;
            document.getElementById("styleValue").textContent = initialLlm.style;
            document.getElementById("temperatureInput").value = initialLlm.temperature;
            document.getElementById("temperatureSlider").value = initialLlm.temperature;
            document.getElementById("temperatureValue").textContent = initialLlm.temperature;
            document.getElementById("modelInput").value = initialLlm.model;
            document.getElementById("modelDisplay").textContent = initialLlm.model;

            const llmSelect = document.getElementById("llmSelect");
            if (llmSelect && initialLlm.id) {
                for (let i = 0; i < llmSelect.options.length; i++) {
                    if (llmSelect.options[i].value === initialLlm.id) {
                        llmSelect.selectedIndex = i;
                        break;
                    }
                }
            }
        }

        function updatePromptAndVoice() {
            const llmSelect = document.getElementById("llmSelect");
            const selectedOption = llmSelect.options[llmSelect.selectedIndex];
            const selectedLlmId = selectedOption.value;
            const currentPath = window.location.pathname;
            const newUrl = currentPath.replace(/\/my_ai_models\/(\d+)\/?$/, `/my_ai_models/${selectedLlmId}/`);
            if (window.location.pathname !== newUrl) window.location.href = newUrl;
            document.getElementById("promptDisplay").value = selectedOption.dataset.prompt || "";

        }

        function setupSliderListeners() {
            document.getElementById("stabilitySlider").oninput = function () {
                document.getElementById("stabilityValue").textContent = this.value;
                document.getElementById("stabilityInput").value = this.value;
            };
            document.getElementById("speedSlider").oninput = function () {
                document.getElementById("speedValue").textContent = this.value;
                document.getElementById("speedInput").value = this.value;
            };
            document.getElementById("styleSlider").oninput = function () {
                document.getElementById("styleValue").textContent = this.value;
                document.getElementById("styleInput").value = this.value;
            };
            document.getElementById("temperatureSlider").oninput = function () {
                document.getElementById("temperatureValue").textContent = this.value;
                document.getElementById("temperatureInput").value = this.value;
            };
        }

        window.onload = function () {
            initializeUIWithCurrentLlm();
            setupSliderListeners();
        };