// Основной JavaScript файл

document.addEventListener('DOMContentLoaded', function() {
    // Загрузка застройщиков
    loadDevelopers();
    
    // Загрузка популярных комплексов
    loadPopularComplexes();
    
    // Инициализация карты
    initMap();
    
    // Настройка поиска
    setupSearch();
});

// Загрузка застройщиков из API
async function loadDevelopers() {
    try {
        const response = await fetch('/api/developers');
        const developers = await response.json();
        
        const container = document.getElementById('developers-container');
        container.innerHTML = '';
        
        if (developers.error) {
            container.innerHTML = `
                <div class="col-12 text-center">
                    <div class="alert alert-danger">
                        Ошибка загрузки: ${developers.error}
                    </div>
                </div>
            `;
            return;
        }
        
        developers.forEach(developer => {
            const col = document.createElement('div');
            col.className = 'col-md-4 mb-4';
            
            col.innerHTML = `
                <div class="card developer-card">
                    ${developer.logo ? 
                        `<img src="${developer.logo}" class="card-img-top" alt="${developer.name}">` : 
                        `<div class="card-img-top bg-secondary d-flex align-items-center justify-content-center" style="height: 200px;">
                            <i class="fas fa-building fa-4x text-white"></i>
                        </div>`
                    }
                    <div class="card-body text-center">
                        <h3 class="card-title">${developer.name}</h3>
                        <p class="text-muted">
                            <i class="fas fa-home"></i> 
                            ${developer.complexes_count} жилых комплексов
                        </p>
                        <button class="btn btn-primary view-developer-btn" data-developer='${JSON.stringify(developer)}'>
                            <i class="fas fa-eye"></i> Смотреть комплексы
                        </button>
                    </div>
                </div>
            `;
            
            container.appendChild(col);
        });
        
        // Навешиваем обработчики на кнопки
        document.querySelectorAll('.view-developer-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const developer = JSON.parse(this.getAttribute('data-developer'));
                openDeveloperModal(developer);
            });
        });
        
    } catch (error) {
        console.error('Ошибка загрузки застройщиков:', error);
        document.getElementById('developers-container').innerHTML = `
            <div class="col-12 text-center">
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle"></i>
                    Не удалось загрузить застройщиков. Проверьте подключение к интернету.
                </div>
            </div>
        `;
    }
}

// Загрузка популярных комплексов
async function loadPopularComplexes() {
    try {
        const response = await fetch('/api/complexes');
        const complexes = await response.json();
        
        const container = document.getElementById('complexes-container');
        container.innerHTML = '';
        
        if (complexes.error) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-warning">Нет данных о комплексах</div>
                </div>
            `;
            return;
        }
        
        // Отображаем первые 3 комплекса
        complexes.slice(0, 3).forEach(complex => {
            const col = document.createElement('div');
            col.className = 'col-md-4';
            
            const statusClass = complex.status === 'Новостройка' ? 'bg-success' : 'bg-warning';
            
            col.innerHTML = `
                <div class="card complex-card">
                    ${complex.image ? 
                        `<img src="${complex.image}" class="card-img-top" alt="${complex.title}">` : 
                        `<div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
                            <i class="fas fa-building fa-4x text-secondary"></i>
                        </div>`
                    }
                    <div class="card-body">
                        <h5 class="card-title">${complex.title || 'Без названия'}</h5>
                        <p class="card-text">
                            <i class="fas fa-map-marker-alt"></i> 
                            ${complex.district || 'Район не указан'}
                        </p>
                        <span class="badge ${statusClass}">${complex.status || 'Статус не указан'}</span>
                        <div class="mt-3">
                            <button class="btn btn-outline-primary btn-sm view-complex-btn" data-complex='${JSON.stringify(complex)}'>
                                <i class="fas fa-info-circle"></i> Подробнее
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            container.appendChild(col);
        });
        
        // Навешиваем обработчики на кнопки комплексов
        document.querySelectorAll('.view-complex-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const complex = JSON.parse(this.getAttribute('data-complex'));
                openComplexModal(complex);
            });
        });
        
    } catch (error) {
        console.error('Ошибка загрузки комплексов:', error);
    }
}

// Открытие модального окна застройщика
function openDeveloperModal(developer) {
    document.getElementById('modalTitle').textContent = developer.name;
    
    // Загружаем комплексы этого застройщика
    fetch('/api/complexes')
        .then(response => response.json())
        .then(complexes => {
            if (complexes.error) throw new Error(complexes.error);
            
            const developerComplexes = complexes.filter(c => 
                c.developer === developer.name || (!c.developer && developer.name === 'Аквилон')
            );
            
            let html = `
                <div class="row">
                    <div class="col-md-4">
                        ${developer.logo ? 
                            `<img src="${developer.logo}" class="img-fluid rounded" alt="${developer.name}">` : 
                            `<div class="bg-light p-5 text-center rounded">
                                <i class="fas fa-building fa-5x text-secondary"></i>
                            </div>`
                        }
                    </div>
                    <div class="col-md-8">
                        <h4>${developer.name}</h4>
                        <p><i class="fas fa-home"></i> Комплексов: ${developerComplexes.length}</p>
                        <hr>
                        <h5>Жилые комплексы:</h5>
            `;
            
            if (developerComplexes.length > 0) {
                developerComplexes.forEach(complex => {
                    html += `
                        <div class="complex-item mb-3 p-3 border rounded">
                            <h6>${complex.title}</h6>
                            <p class="mb-1"><small>${complex.district}</small></p>
                            <span class="badge ${complex.status === 'Новостройка' ? 'bg-success' : 'bg-secondary'}">
                                ${complex.status}
                            </span>
                            <button class="btn btn-sm btn-outline-primary float-end view-apartments-btn" 
                                    data-complex='${JSON.stringify(complex)}'>
                                Выбрать квартиру
                            </button>
                        </div>
                    `;
                });
            } else {
                html += '<p class="text-muted">Нет доступных комплексов</p>';
            }
            
            html += `</div></div>`;
            document.getElementById('modalBody').innerHTML = html;
            
            // Навешиваем обработчики на кнопки выбора квартир
            document.querySelectorAll('.view-apartments-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const complex = JSON.parse(this.getAttribute('data-complex'));
                    // Здесь можно открыть страницу с выбором квартир
                    alert(`Открываем выбор квартир для комплекса: ${complex.title}`);
                    // В будущем здесь будет переход на страницу complex.html
                });
            });
        })
        .catch(error => {
            document.getElementById('modalBody').innerHTML = `
                <div class="alert alert-danger">
                    Ошибка загрузки данных: ${error.message}
                </div>
            `;
        });
    
    // Показываем модальное окно
    const modal = new bootstrap.Modal(document.getElementById('developerModal'));
    modal.show();
}

// Открытие модального окна комплекса
function openComplexModal(complex) {
    document.getElementById('modalTitle').textContent = complex.title;
    
    let html = `
        <div class="row">
            <div class="col-md-6">
                ${complex.image ? 
                    `<img src="${complex.image}" class="img-fluid rounded" alt="${complex.title}">` : 
                    `<div class="bg-light p-5 text-center rounded">
                        <i class="fas fa-building fa-5x text-secondary"></i>
                    </div>`
                }
            </div>
            <div class="col-md-6">
                <h4>${complex.title}</h4>
                <p><i class="fas fa-map-marker-alt"></i> ${complex.district || 'Район не указан'}</p>
                <p><i class="fas fa-info-circle"></i> ${complex.status || 'Статус не указан'}</p>
                
                <hr>
                
                <h5>Выбор квартиры:</h5>
                <div class="mb-3">
                    <label class="form-label">Количество комнат:</label>
                    <select class="form-select" id="roomsSelect">
                        <option value="1">1-комнатные</option>
                        <option value="2">2-комнатные</option>
                        <option value="3">3-комнатные</option>
                        <option value="4">4+ комнаты</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Площадь (м²):</label>
                    <div class="input-group">
                        <input type="number" class="form-control" placeholder="от" id="areaFrom">
                        <span class="input-group-text">-</span>
                        <input type="number" class="form-control" placeholder="до" id="areaTo">
                    </div>
                </div>
                
                <button class="btn btn-primary w-100" id="findApartmentsBtn">
                    <i class="fas fa-search"></i> Найти квартиры
                </button>
                
                <div class="mt-3">
                    <button class="btn btn-outline-success w-100" id="showOnMapBtn">
                        <i class="fas fa-map-marked-alt"></i> Показать на карте
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('modalBody').innerHTML = html;
    
    // Обработчики кнопок в модальном окне
    document.getElementById('findApartmentsBtn').addEventListener('click', function() {
        const rooms = document.getElementById('roomsSelect').value;
        const areaFrom = document.getElementById('areaFrom').value;
        const areaTo = document.getElementById('areaTo').value;
        
        alert(`Поиск квартир в комплексе "${complex.title}":\nКомнат: ${rooms}\nПлощадь: ${areaFrom || 'любая'} - ${areaTo || 'любая'} м²`);
        
        // Здесь будет загрузка реальных данных о квартирах
        showApartmentsList(complex, {rooms, areaFrom, areaTo});
    });
    
    document.getElementById('showOnMapBtn').addEventListener('click', function() {
        // Показываем комплекс на карте
        if (window.ymaps && window.complexMap) {
            // Центрируем карту на комплексе (заглушка - центр СПб)
            window.complexMap.setCenter([59.9343, 30.3351], 14);
            
            // Закрываем модальное окно
            bootstrap.Modal.getInstance(document.getElementById('developerModal')).hide();
            
            // Прокручиваем к карте
            document.getElementById('map').scrollIntoView({behavior: 'smooth'});
        }
    });
    
    const modal = new bootstrap.Modal(document.getElementById('developerModal'));
    modal.show();
}

// Показать список квартир (заглушка)
function showApartmentsList(complex, filters) {
    // Здесь будет загрузка реальных данных о квартирах
    // Пока что показываем заглушку
    const html = `
        <div class="mt-4">
            <h6>Доступные квартиры (фильтры: ${filters.rooms} комнат):</h6>
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                В настоящий момент данные о квартирах загружаются...
                <br><br>
                <button class="btn btn-sm btn-outline-primary" onclick="loadDemoApartments('${complex.title}')">
                    <i class="fas fa-bolt"></i> Загрузить демо-данные
                </button>
            </div>
        </div>
    `;
    
    document.getElementById('modalBody').innerHTML += html;
}

// Демо-функция загрузки квартир
window.loadDemoApartments = function(complexName) {
    const demoApartments = [
        {id: 1, rooms: 1, area: 35, price: 4500000, floor: 5},
        {id: 2, rooms: 1, area: 42, price: 5200000, floor: 8},
        {id: 3, rooms: 2, area: 65, price: 7800000, floor: 3},
        {id: 4, rooms: 2, area: 72, price: 8500000, floor: 12},
        {id: 5, rooms: 3, area: 95, price: 11500000, floor: 7}
    ];
    
    let html = '<div class="mt-3"><h6>Демо-квартиры:</h6><div class="list-group">';
    
    demoApartments.forEach(apt => {
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${apt.rooms}-комнатная, ${apt.area} м²</h6>
                    <strong>${apt.price.toLocaleString('ru-RU')} ₽</strong>
                </div>
                <p class="mb-1">Этаж: ${apt.floor} | Комплекс: ${complexName}</p>
                <button class="btn btn-sm btn-success mt-2">
                    <i class="fas fa-phone"></i> Забронировать просмотр
                </button>
            </div>
        `;
    });
    
    html += '</div></div>';
    
    // Находим последний alert и заменяем его
    const modalBody = document.getElementById('modalBody');
    const alertElement = modalBody.querySelector('.alert');
    if (alertElement) {
        alertElement.outerHTML = html;
    }
}

// Настройка поиска
function setupSearch() {
    const searchInput = document.querySelector('.search-box input');
    const searchBtn = document.querySelector('.search-box button');
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') performSearch();
    });
    
    function performSearch() {
        const query = searchInput.value.trim();
        if (query) {
            alert(`Поиск: "${query}"\n\nВ будущем здесь будет реальный поиск по базам данных.`);
            // Здесь будет реализация поиска
        }
    }
}

// Инициализация карты (базовая версия)
function initMap() {
    if (typeof ymaps === 'undefined') {
        console.warn('Yandex Maps API не загружен');
        return;
    }
    
    ymaps.ready(function() {
        const mapElement = document.getElementById('map');
        if (!mapElement) return;
        
        window.complexMap = new ymaps.Map('map', {
            center: [59.9343, 30.3351], // Центр СПб
            zoom: 11,
            controls: ['zoomControl', 'fullscreenControl']
        });
        
        // Добавляем метки для жилых комплексов (демо)
        const demoComplexes = [
            {coords: [59.9343, 30.3351], title: 'Аквилон All in 3.0', hint: '106 квартир'},
            {coords: [59.8516, 30.2671], title: 'Аквилон Янино', hint: '303 квартиры'},
            {coords: [59.9571, 30.4099], title: 'Другой комплекс', hint: 'Строится'}
        ];
        
        demoComplexes.forEach(complex => {
            const placemark = new ymaps.Placemark(complex.coords, {
                hintContent: complex.hint,
                balloonContent: `<strong>${complex.title}</strong><br>${complex.hint}`
            });
            
            window.complexMap.geoObjects.add(placemark);
        });
        
        console.log('Карта Яндекс инициализирована');
    });
}