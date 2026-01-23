        // 검색 기능
        const searchInput = document.getElementById('searchInput');
        const genresGrid = document.getElementById('genresGrid');
        const genreCount = document.getElementById('genreCount');
        let allGenres = Array.from(document.querySelectorAll('.genre-card'));

        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            let visibleCount = 0;

            allGenres.forEach(card => {
                const genreName = card.dataset.genre;
                const isVisible = genreName.includes(searchTerm);
                card.style.display = isVisible ? 'flex' : 'none';
                if (isVisible) visibleCount++;
            });

            genreCount.textContent = visibleCount;
            
            // 검색 결과가 없을 때
            const existingEmptyState = document.querySelector('.search-empty-state');
            if (visibleCount === 0 && searchTerm.trim() !== '') {
                if (!existingEmptyState) {
                    const emptyState = document.createElement('div');
                    emptyState.className = 'empty-state search-empty-state';
                    emptyState.innerHTML = `
                        <div class="empty-icon">🔍</div>
                        <div class="empty-message">검색 결과가 없습니다</div>
                        <div class="empty-submessage">"${searchTerm}"와 일치하는 장르가 없습니다</div>
                    `;
                    genresGrid.appendChild(emptyState);
                }
            } else if (existingEmptyState) {
                existingEmptyState.remove();
            }
        });

        // 정렬 기능
        const sortButtons = document.querySelectorAll('.sort-button');
        
        sortButtons.forEach(button => {
            button.addEventListener('click', function() {
                sortButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const sortType = this.dataset.sort;
                sortGenres(sortType);
            });
        });

        function sortGenres(sortType) {
            const cards = Array.from(document.querySelectorAll('.genre-card'));
            
            cards.sort((a, b) => {
                switch(sortType) {
                    case 'name':
                        return a.dataset.genre.localeCompare(b.dataset.genre);
                    case 'popular':
                        // 캐릭터 수 기준 정렬 (많은 순)
                        const aCount = parseInt(a.querySelector('.genre-stats').textContent) || 0;
                        const bCount = parseInt(b.querySelector('.genre-stats').textContent) || 0;
                        return bCount - aCount;
                    case 'newest':
                        // 최신순 (실제 구현시 날짜 데이터 필요)
                        return Math.random() - 0.5; // 임시로 랜덤 정렬
                    default:
                        return 0;
                }
            });

            // 재배치
            const parent = cards[0].parentNode;
            cards.forEach(card => parent.appendChild(card));
        }

        // 장르 페이지로 이동
        function goToGenre(genreId) {
            window.location.href = `/genre/${genreId}/`;
        }

        // 페이지네이션
        function goToPage(pageNum) {
            const url = new URL(window.location);
            url.searchParams.set('page', pageNum);
            window.location.href = url.toString();
        }

        // 카드 호버 효과 강화
        document.querySelectorAll('.genre-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.zIndex = '10';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.zIndex = '1';
            });
        });

        // 로딩 애니메이션 (이미지 로드 완료 후 제거)
        document.addEventListener('DOMContentLoaded', function() {
            const images = document.querySelectorAll('.genre-card-image img');
            let loadedImages = 0;

            images.forEach(img => {
                if (img.complete) {
                    loadedImages++;
                } else {
                    img.addEventListener('load', function() {
                        loadedImages++;
                        if (loadedImages === images.length) {
                            document.body.classList.add('loaded');
                        }
                    });
                }
            });

            if (loadedImages === images.length) {
                document.body.classList.add('loaded');
            }
        });

        // 키보드 네비게이션 지원
        document.addEventListener('keydown', function(e) {
            if (e.key === '/') {
                e.preventDefault();
                searchInput.focus();
            }
        });