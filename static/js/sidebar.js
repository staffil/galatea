        // 기존 스크립트에 추가
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            const menuToggle = document.querySelector('.menu-toggle');
            
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
            menuToggle.classList.toggle('active');
            
            if (sidebar.classList.contains('active')) {
                overlay.style.display = 'block';
                document.body.style.overflow = 'hidden'; // 스크롤 방지
            } else {
                setTimeout(() => {
                    overlay.style.display = 'none';
                }, 300);
                document.body.style.overflow = 'auto';
            }
        }

        function closeSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            const menuToggle = document.querySelector('.menu-toggle');
            
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            menuToggle.classList.remove('active');
            
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 300);
            document.body.style.overflow = 'auto';
        }

