// app.js - Основной файл Mini App
console.log("🏠 Mini App для поиска квартир загружен");

// Глобальные переменные
let tg = null;
let currentUser = null;
let selectedRooms = [];
let currentFilters = {};

// Основная инициализация
document.addEventListener('DOMContentLoaded', function() {
    console.log("🚀 DOM загружен");
    
    // Инициализация Telegram
    initTelegram();
    
    // Инициализация приложения
    initApp();
    
    // Установка даты
    document.getElementById('currentDate').textContent = new Date().toLocaleDateString('ru-RU');
});

// Инициализация Telegram Web App
function initTelegram() {
    if (window.Telegram && Telegram.WebApp) {
        tg = Telegram.WebApp;
        
        // Настройка Telegram
        tg.expand();
        tg.enableClosingConfirmation();
        tg.BackButton.show();
        
        // Обработка кнопки Назад
        tg.BackButton.onClick(() => {
            if (document.getElementById('imageModal').style.display === 'block') {
                closeModal();
            } else {
                tg.BackButton.hide();
            }
        });
        
        // Получаем данные пользователя
        currentUser = tg.initDataUnsafe.user;
        if (currentUser) {
            showUserInfo(currentUser);
        }
        
        // Применяем тему
        applyTelegramTheme();
        
        // Готово
        tg.ready();
        console.log("✅ Telegram Web App инициализирован");
        
    } else {
        console.log("🌐 Режим браузера (тестирование)");
        // Тестовые данные для разработки
        currentUser = {
            id: 123456,
            first_name: "Тестовый",
            last_name: "Пользователь"
        };
        showUserInfo(currentUser);
    }
}

// Показать информацию о пользователе
function showUserInfo(user) {
    const userInfoElement = document.getElementById('userInfo');
    if (userInfoElement && user) {
        const name = user.first_name || user.username || 'Гость';
        userInfoElement.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                <i class="fas fa-user-circle"></i>
                <span>${name}</span>
            </div>
        `;
    }
}

// Применить тему Telegram
function applyTelegramTheme() {
    if (!tg) return;
    
    const theme = tg.themeParams;
    document.body.style.backgroundColor = theme.bg_color || '#ffffff';
    document.body.style.color = theme.text_color || '#000000';
    
    console.log("🎨 Применена тема Telegram");
}

// Инициализация приложения
function initApp() {
    console.log("🏠 Инициализация приложения");
    
    // Инициализация фильтров
    initFilters();
    
    // Обработчики событий
    document.getElementById('searchBtn').addEventListener('click', searchApartments);
    document.getElementById('resetBtn').addEventListener('click', resetFilters);
    
    // Инициализация слайдера цены
    const priceSlider = document.getElementById('priceRange');
    const minPriceInput = document.getElementById('minPrice');
    const maxPriceInput = document.getElementById('maxPrice');
    
    priceSlider.addEventListener('input', function() {
        maxPriceInput.value = this.value;
        updatePriceLabel(this.value);
    });
    
    minPriceInput.addEventListener('change', function() {
        priceSlider.min = this.value || 0;
    });
    
    maxPriceInput.addEventListener('change', function() {
        priceSlider.value = this.value || priceSlider.max;
        updatePriceLabel(this.value);
    });
    
    // Модальное окно
    document.querySelector('.close').addEventListener('click', closeModal);
    document.getElementById('imageModal').addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });
}

// Инициализация фильтров
function initFilters() {
    console.log("⚙️ Инициализация фильтров");
    
    // Выбор комнат
    const roomButtons = document.querySelectorAll('.room-btn');
    roomButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const rooms = this.getAttribute('data-rooms');
            
            // Удаляем активный класс у всех кнопок
            roomButtons.forEach(b => b.classList.remove('active'));
            
            // Добавляем активный класс текущей кнопке
            this.classList.add('active');
            
            // Сохраняем выбранные комнаты
            if (rooms === 'all') {
                selectedRooms = [];
            } else {
                selectedRooms = [rooms];
            }
            
            console.log("Выбраны комнаты:", selectedRooms);
        });
    });
}

// Обновление метки цены
function updatePriceLabel(value) {
    const formattedValue = new Intl.NumberFormat('ru-RU').format(value);
    document.querySelector('.range-labels span:last-child').textContent = formattedValue + ' руб.';
}

// Поиск квартир
async function searchApartments() {
    console.log("🔍 Начинаем поиск квартир");
    
    // Собираем фильтры
    const filters = {
        min_price: document.getElementById('minPrice').value || null,
        max_price: document.getElementById('maxPrice').value || null,
        rooms: selectedRooms.length > 0 ? selectedRooms.join(',') : null,
        district: document.getElementById('district').value || null
    };
    
    // Сохраняем текущие фильтры
    currentFilters = filters;
    
    // Показываем загрузку
    showLoading(true);
    
    // Очищаем предыдущие результаты
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = '';
    
    try {
        // Здесь будет реальный запрос к вашему API
        // Временная заглушка с тестовыми данными
        const apartments = await fetchMockApartments(filters);
        
        // Показываем результаты
        displayApartments(apartments);
        
        // Обновляем счетчик
        document.getElementById('resultsCount').textContent = apartments.length;
        
    } catch (error) {
        console.error("Ошибка поиска:", error);
        showError("Ошибка при загрузке данных");
    } finally {
        showLoading(false);
    }
}

// Отображение квартир
function displayApartments(apartments) {
    const resultsContainer = document.getElementById('resultsContainer');
    
    if (apartments.length === 0) {
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-home fa-3x"></i>
                <h3>Квартиры не найдены</h3>
                <p>Попробуйте изменить параметры поиска</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    apartments.forEach(apartment => {
        // Форматируем цену
        const formattedPrice = new Intl.NumberFormat('ru-RU', {
            style: 'currency',
            currency: 'RUB',
            minimumFractionDigits: 0
        }).format(apartment.price);
        
        // Генерируем HTML для изображений
        let imagesHTML = '';
        if (apartment.images && apartment.images.length > 0) {
            apartment.images.forEach((img, index) => {
                if (index === 0) {
                    imagesHTML += `<img src="${img}" alt="Квартира ${apartment.id}" onclick="openImageModal('${img}')">`;
                }
            });
            
            if (apartment.images.length > 1) {
                imagesHTML += `<div class="image-counter">+${apartment.images.length - 1}</div>`;
            }
        } else {
            imagesHTML = '<div class="no-image">Нет фото</div>';
        }
        
        html += `
        <div class="apartment-card">
            <div class="apartment-images">
                ${imagesHTML}
            </div>
            <div class="apartment-info">
                <div class="apartment-header">
                    <div class="apartment-title">${apartment.rooms}-комнатная квартира</div>
                   
