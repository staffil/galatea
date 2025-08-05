    document.querySelector('.generate_image').addEventListener('click', function () {
      const prompt = document.getElementById('imagePrompt').value.trim();

      if (!prompt) {
        alert('프롬프트를 입력해주세요.');
        return;
      }

      const loadingText = document.getElementById('loadingText');
      const generateBtn = document.querySelector('.generate_image');

      loadingText.classList.add('show');
      generateBtn.disabled = true;
      generateBtn.textContent = '생성 중...';

      fetch('/image/generate_image/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': '{{ csrf_token }}',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ prompt: prompt })
      })
        .then(response => response.json())
        .then(data => {
          if (data.image_url) {
            const originalUrl = data.image_url;
            const proxyUrl = `/image/proxy_image/?url=${encodeURIComponent(originalUrl)}`;

            const imageElement = document.getElementById('generatedImage');
            const downloadBtn = document.getElementById('downloadBtn');
            const placeholder = document.getElementById('imagePlaceholder');

            imageElement.src = proxyUrl;
            imageElement.style.display = 'block';
            placeholder.style.display = 'none';

            downloadBtn.href = proxyUrl;
            downloadBtn.style.display = 'inline-block';
          } else {
            alert('이미지 생성에 실패했습니다.');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('이미지 생성 중 오류가 발생했습니다.');
        })
        .finally(() => {
          loadingText.classList.remove('show');
          generateBtn.disabled = false;
          generateBtn.textContent = '생성하기';
        });
    });

    document.getElementById('downloadBtn').addEventListener('click', function (e) {
      e.preventDefault();
      const url = this.href;

      if (!url || url === '#') {
        alert('다운로드할 이미지가 없습니다.');
        return;
      }

      fetch(url)
        .then(response => response.blob())
        .then(blob => {
          const blobUrl = URL.createObjectURL(blob);
          const link = document.createElement('a');

          link.href = blobUrl;
          link.download = "generated_image.png";
          document.body.appendChild(link);
          link.click();
          link.remove();
          URL.revokeObjectURL(blobUrl);
        })
        .catch(() => alert("이미지 다운로드에 실패했습니다."));
    });

    // Ctrl + Enter 로 생성하기 단축키 추가
    document.getElementById('imagePrompt').addEventListener('keydown', function (e) {
      if (e.ctrlKey && e.key === 'Enter') {
        document.querySelector('.generate_image').click();
      }
    });