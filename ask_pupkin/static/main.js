// Анимация голосования
document.addEventListener('DOMContentLoaded', function() {
    // Голосование за вопросы
    const voteButtons = document.querySelectorAll('.vote-btn');
    
    voteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const voteBtn = this;
            const isUpvote = voteBtn.classList.contains('upvote');
            const voteCount = voteBtn.closest('.question-voting, .answer-voting').querySelector('.vote-count');
            let currentCount = parseInt(voteCount.textContent);
            
            // Анимация
            voteBtn.style.transform = 'scale(0.9)';
            setTimeout(() => {
                voteBtn.style.transform = 'scale(1)';
            }, 150);
            
            // Обновление счетчика с анимацией
            if (isUpvote) {
                currentCount++;
                voteCount.style.color = '#28a745';
            } else {
                currentCount--;
                voteCount.style.color = '#dc3545';
            }
            
            voteCount.textContent = currentCount;
            
            // Возврат цвета через секунду
            setTimeout(() => {
                voteCount.style.color = '#333';
            }, 1000);
        });
    });
    
    // Анимация добавления в избранное
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            this.style.color = this.classList.contains('active') ? '#ffc107' : '#ccc';
            
            // Анимация звезды
            this.style.transform = 'scale(1.3)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 300);
        });
    });
    
    // Плавная прокрутка к якорям
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Динамическая загрузка контента для пагинации
    const pageLinks = document.querySelectorAll('.page-number, .page-nav');
    pageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!this.getAttribute('href').includes('#')) {
                e.preventDefault();
                const url = this.getAttribute('href');
                
                // Показать спиннер загрузки
                const spinner = document.createElement('div');
                spinner.className = 'loading-spinner';
                spinner.style.display = 'block';
                
                const contentArea = document.querySelector('.questions-list') || 
                                  document.querySelector('.answers-list') || 
                                  document.querySelector('.left-column');
                if (contentArea) {
                    contentArea.parentNode.insertBefore(spinner, contentArea.nextSibling);
                }
                
                // Загрузка контента
                fetch(url)
                    .then(response => response.text())
                    .then(html => {
                        // Обновление контента
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        const newContent = doc.querySelector('.questions-list, .answers-list, .left-column');
                        
                        if (newContent && contentArea) {
                            contentArea.innerHTML = newContent.innerHTML;
                        }
                        
                        // Обновление URL
                        window.history.pushState({}, '', url);
                    })
                    .finally(() => {
                        spinner.remove();
                    });
            }
        });
    });
    
    // Анимация появления элементов при скролле
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Наблюдение за вопросами и ответами
    document.querySelectorAll('.question-item, .answer-item, .sidebar-widget').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(element);
    });
    
    // Поиск с автодополнением
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(() => {
                const query = this.value.trim();
                if (query.length > 2) {
                    // Здесь можно добавить AJAX запрос для поиска
                    console.log('Searching for:', query);
                }
            }, 500);
        });
    }
});