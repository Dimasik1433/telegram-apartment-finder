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
                    <div class="apartment-price">${formattedPrice}</div>
                </div>
                
                <div class="apartment-details">
                    <span><i class="fas fa-ruler-combined"></i> ${apartment.area} м²</span>
                    <span><i class="fas fa-layer-group"></i> ${apartment.floor || '?'}/${apartment.total_floors || '?'}</span>
                    <span><i class="fas fa-map-marker-alt"></i> ${apartment.district}</span>
                </div>
                
                <div class="apartment-address">
                    <i class="fas fa-location-dot"></i> ${apartment.address || 'Адрес не указан'}
                </div>
                
                <div class="apartment-actions">
                    <button class="action-btn btn-primary" onclick="showDetails(${apartment.id})">
                        <i class="fas fa-info-circle"></i> Подробнее
                    </button>
                    <button class="action-btn btn-secondary" onclick="saveFavorite(${apartment.id})">
                        <i class="far fa-heart"></i> В избранное
                    </button>
                </div>
            </div>
        </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// Тестовые данные (заглушка)
async function fetchMockApartments(filters) {
    console.log("Используем тестовые данные с фильтрами:", filters);
    
    // Имитация задержки сети
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Тестовые данные
    return [
        {
            id: 1,
            rooms: 1,
            area: 35.5,
            price: 4500000,
            district: "Центральный",
            address: "ул. Ленина, 15",
            floor: 3,
            total_floors: 9,
            images: [
                "https://via.placeholder.com/600x400/3498db/ffffff?text=Квартира+1",
                "https://via.placeholder.com/600x400/2ecc71/ffffff?text=Планировка"
            ]
        },
        {
            id: 2,
            rooms: 2,
            area: 52.0,
            price: 6800000,
            district: "Северный",
            address: "пр. Победы, 42",
            floor: 7,
            total_floors: 12,
            images: [
                "https://via.placeholder.com/600x400/e74c3c/ffffff?text=Квартира+2"
            ]
        },
        {
            id: 3,
            rooms: 3,
            area: 75.5,
            price: 9500000,
            district: "Южный",
            address: "ул. Садовая, 8",
            floor: 1,
            total_floors: 5,
            images: [
                "https://via.placeholder.com/600x400/9b59b6/ffffff?text=Квартира+3",
                "https://via.placeholder.com/600x400/34495e/ffffff?text=Вид+из+окна"
            ]
        }
    ].filter(apt => {
        // Применяем фильтры
        if (filters.min_price && apt.price < filters.min_price) return false;
        if (filters.max_price && apt.price > filters.max_price) return false;
        if (filters.rooms && !filters.rooms.split(',').includes(apt.rooms.toString())) return false;
        if (filters.district && !apt.district.includes(filters.district)) return false;
        return true;
    });
}

// Сброс фильтров
function resetFilters() {
    console.log("🔄 Сброс фильтров");
    
    document.getElementById('minPrice').value = '';
    document.getElementById('maxPrice').value = '';
    document.getElementById('priceRange').value = 20000000;
    document.getElementById('district').value = '';
    
    // Сброс выбора комнат
    const roomButtons = document.querySelectorAll('.room-btn');
    roomButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-rooms') === 'all') {
            btn.classList.add('active');
        }
    });
    
    selectedRooms = [];
    updatePriceLabel(20000000);
    
    // Очищаем результаты
    document.getElementById('resultsContainer').innerHTML = `
        <div class="empty-state">
            <i class="fas fa-search fa-3x"></i>
            <h3>Установите фильтры и нажмите "Найти квартиры"</h3>
            <p>Мы покажем вам лучшие варианты из наших проектов</p>
        </div>
    `;
    
    document.getElementById('resultsCount').textContent = '0';
}

// Показать/скрыть загрузку
function showLoading(show) {
    const loadingElement = document.getElementById('loading');
    const resultsContainer = document.getElementById('resultsContainer');
    
    if (show) {
        loadingElement.style.display = 'block';
        resultsContainer.style.opacity = '0.5';
    } else {
        loadingElement.style.display = 'none';
        resultsContainer.style.opacity = '1';
    }
}

// Показать ошибку
function showError(message) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-exclamation-triangle fa-3x"></i>
            <h3>${message}</h3>
            <p>Попробуйте еще раз позже</p>
        </div>
    `;
}

// Открыть модальное окно с изображением
window.openImageModal = function(imageUrl) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    
    modalImage.src = imageUrl;
    modal.style.display = 'block';
    
    if (tg) {
        tg.BackButton.show();
    }
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById('imageModal').style.display = 'none';
    if (tg) {
        tg.BackButton.hide();
    }
}

// Показать детали квартиры
window.showDetails = function(apartmentId) {
    alert(`Детали квартиры #${apartmentId}\n\nЭта функция будет реализована в следующей версии.`);
    
    // В реальном приложении здесь будет переход на страницу деталей
    // или отправка данных в бота для связи с менеджером
}

// Сохранить в избранное
window.saveFavorite = function(apartmentId) {
    alert(`Квартира #${apartmentId} добавлена в избранное!`);
    
    // Здесь можно добавить сохранение в localStorage или отправку на сервер
    let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    if (!favorites.includes(apartmentId)) {
        favorites.push(apartmentId);
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }
    
    console.log("Избранное:", favorites);
}

// Функция для отладки
window.debugApp = function() {
    console.log("=== ОТЛАДКА ===");
    console.log("Текущие фильтры:", currentFilters);
    console.log("Выбранные комнаты:", selectedRooms);
    console.log("Текущий пользователь:", currentUser);
    console.log("Telegram доступен:", !!tg);
    console.log("=================");
}
