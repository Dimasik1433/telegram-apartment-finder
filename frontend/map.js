// Файл для работы с Яндекс.Картами

// Получение координат по адресу (геокодирование)
async function geocodeAddress(address) {
    return new Promise((resolve, reject) => {
        if (typeof ymaps === 'undefined') {
            reject('Yandex Maps API не загружен');
            return;
        }
        
        ymaps.geocode(address, {
            results: 1
        }).then(function (res) {
            const firstGeoObject = res.geoObjects.get(0);
            if (firstGeoObject) {
                const coords = firstGeoObject.geometry.getCoordinates();
                resolve(coords);
            } else {
                reject('Адрес не найден');
            }
        }).catch(reject);
    });
}

// Добавление метки на карту
function addComplexToMap(complex, map) {
    if (!map || !complex) return null;
    
    // Пробуем получить координаты из complex или геокодировать по адресу
    const coords = complex.coordinates || [59.9343, 30.3351]; // Заглушка
    
    const placemark = new ymaps.Placemark(coords, {
        balloonContentHeader: `<strong>${complex.title}</strong>`,
        balloonContentBody: `
            <p>${complex.district || ''}</p>
            <p>Статус: ${complex.status || ''}</p>
            ${complex.description ? `<p>${complex.description}</p>` : ''}
        `,
        balloonContentFooter: '<button onclick="showApartmentsForComplex()">Выбрать квартиру</button>',
        hintContent: complex.title
    }, {
        preset: 'islands#blueHomeIcon'
    });
    
    map.geoObjects.add(placemark);
    return placemark;
}

// Показать все комплексы на карте
function showAllComplexesOnMap(complexes) {
    if (!window.complexMap || !complexes) return;
    
    // Очищаем карту
    window.complexMap.geoObjects.removeAll();
    
    // Добавляем каждый комплекс
    const bounds = [];
    
    complexes.forEach(complex => {
        const placemark = addComplexToMap(complex, window.complexMap);
        if (placemark) {
            bounds.push(placemark.geometry.getCoordinates());
        }
    });
    
    // Если есть метки, центрируем карту чтобы показать все
    if (bounds.length > 0) {
        window.complexMap.setBounds(ymaps.util.bounds.fromPoints(bounds), {
            checkZoomRange: true
        });
    }
}

// Инициализация расширенной карты с поиском
function initAdvancedMap() {
    if (typeof ymaps === 'undefined') return;
    
    ymaps.ready(function() {
        const map = new ymaps.Map('advanced-map', {
            center: [59.9343, 30.3351],
            zoom: 11,
            controls: ['searchControl', 'typeSelector', 'zoomControl', 'fullscreenControl']
        });
        
        // Добавляем панель маршрутизации
        map.controls.add('routeButtonControl', {
            float: 'right'
        });
        
        return map;
    });
}

// Экспорт функций
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        geocodeAddress,
        addComplexToMap,
        showAllComplexesOnMap,
        initAdvancedMap
    };
}