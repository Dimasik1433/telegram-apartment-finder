import json
import requests
import logging
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class ApartmentFeed:
    def __init__(self, feed_url: str = None):
        # Ваш фид с GitHub
        self.feed_url = feed_url or "https://raw.githubusercontent.com/dsmaznova-source/my-telegram-app2/refs/heads/main/complexes.json"
        self.last_update = None
        self.cached_data = []
        self.complexes_data = {}  # Данные о ЖК
    
    def fetch_all_data(self) -> Dict:
        """Загрузить все данные из фида"""
        try:
            logger.info(f"Загрузка данных из {self.feed_url}")
            response = requests.get(self.feed_url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            self.last_update = datetime.now()
            
            # Парсим данные
            self.complexes_data = data
            
            # Преобразуем в список квартир
            apartments = self._parse_complexes(data)
            self.cached_data = apartments
            
            logger.info(f"Загружено {len(apartments)} квартир из {len(data.get('complexes', []))} ЖК")
            return {
                'complexes': data.get('complexes', []),
                'apartments': apartments,
                'total_apartments': len(apartments),
                'total_complexes': len(data.get('complexes', []))
            }
            
        except Exception as e:
            logger.error(f"Ошибка загрузки фида: {e}")
            return {
                'complexes': [],
                'apartments': self.cached_data,
                'total_apartments': len(self.cached_data),
                'total_complexes': 0
            }
    
    def _parse_complexes(self, data: Dict) -> List[Dict]:
        """Парсинг данных о ЖК в список квартир"""
        apartments = []
        
        # Основная структура вашего фида
        complexes = data.get('complexes', [])
        
        for complex_data in complexes:
            complex_id = complex_data.get('id')
            complex_name = complex_data.get('name', 'ЖК')
            
            # Парсим квартиры в этом ЖК
            complex_apartments = complex_data.get('apartments', [])
            
            for apt in complex_apartments:
                # Базовые данные
                apartment = {
                    'id': f"{complex_id}_{apt.get('id', '')}",
                    'complex_id': complex_id,
                    'complex_name': complex_name,
                    'title': apt.get('title', f'Квартира в {complex_name}'),
                    'price': self._parse_price(apt.get('price', '0 ₽')),
                    'price_display': apt.get('price', '0 ₽'),
                    'rooms': self._parse_rooms(apt.get('title', '')),
                    'area': apt.get('area', '0 м²'),
                    'area_value': self._parse_area(apt.get('area', '0 м²')),
                    'floor': apt.get('floor', ''),
                    'floor_display': apt.get('floor_display', ''),
                    'building': apt.get('building', ''),
                    'section': apt.get('section', ''),
                    'deadline': apt.get('deadline', ''),
                    'status': apt.get('status', 'available'),
                    'image': apt.get('image', ''),
                    'images': apt.get('images', []),
                    'features': apt.get('features', []),
                    'plan_url': apt.get('plan_url', ''),
                    'booking_url': apt.get('booking_url', ''),
                    'description': apt.get('description', ''),
                    
                    # Данные ЖК
                    'complex_address': complex_data.get('address', ''),
                    'complex_class': complex_data.get('class', ''),
                    'complex_decor': complex_data.get('decor', ''),
                    'complex_developer': complex_data.get('developer', ''),
                    'complex_metro': complex_data.get('metro', []),
                    'complex_delivery_date': complex_data.get('delivery_date', ''),
                    'complex_images': complex_data.get('images', []),
                    'complex_features': complex_data.get('features', [])
                }
                
                # Если нет изображения квартиры, используем первое изображение ЖК
                if not apartment['image'] and complex_data.get('images'):
                    apartment['image'] = complex_data['images'][0] if isinstance(complex_data['images'], list) else complex_data['images']
                
                apartments.append(apartment)
        
        return apartments
    
    def _parse_price(self, price_str: str) -> float:
        """Извлечь числовое значение цены из строки"""
        try:
            # Убираем пробелы, валюту, символы
            cleaned = ''.join(c for c in price_str if c.isdigit() or c == '.')
            return float(cleaned) if cleaned else 0.0
        except:
            return 0.0
    
    def _parse_rooms(self, title: str) -> int:
        """Определить количество комнат из названия"""
        title_lower = title.lower()
        
        if 'студия' in title_lower or 'апартаменты' in title_lower:
            return 0
        elif '1-комн' in title_lower or '1-комнат' in title_lower:
            return 1
        elif '2-комн' in title_lower or '2-комнат' in title_lower:
            return 2
        elif '3-комн' in title_lower or '3-комнат' in title_lower:
            return 3
        elif '4-комн' in title_lower or '4-комнат' in title_lower:
            return 4
        else:
            # Попробуем извлечь цифру из текста
            import re
            match = re.search(r'(\d+)\s*[-]?\s*комн', title_lower)
            if match:
                return int(match.group(1))
            return 1  # По умолчанию
    
    def _parse_area(self, area_str: str) -> float:
        """Извлечь числовое значение площади"""
        try:
            # Ищем число в строке "85.5 м²"
            import re
            match = re.search(r'(\d+\.?\d*)', area_str)
            return float(match.group(1)) if match else 0.0
        except:
            return 0.0
    
    def get_apartments(self, filters: Dict = None) -> List[Dict]:
        """Получить квартиры с опциональными фильтрами"""
        # Если нет кэша, загружаем
        if not self.cached_data:
            self.fetch_all_data()
        
        apartments = self.cached_data
        
        # Применяем фильтры
        if filters:
            apartments = self._apply_filters(apartments, filters)
        
        return apartments
    
    def _apply_filters(self, apartments: List[Dict], filters: Dict) -> List[Dict]:
        """Применить фильтры к списку квартир"""
        filtered = apartments
        
        # Фильтр по цене
        if 'min_price' in filters:
            filtered = [a for a in filtered if a.get('price', 0) >= filters['min_price']]
        if 'max_price' in filters:
            filtered = [a for a in filtered if a.get('price', 0) <= filters['max_price']]
        
        # Фильтр по комнатам
        if 'rooms' in filters:
            filtered = [a for a in filtered if a.get('rooms', 1) == filters['rooms']]
        if 'min_rooms' in filters:
            filtered = [a for a in filtered if a.get('rooms', 0) >= filters['min_rooms']]
        if 'max_rooms' in filters:
            filtered = [a for a in filtered if a.get('rooms', 10) <= filters['max_rooms']]
        
        # Фильтр по площади
        if 'min_area' in filters:
            filtered = [a for a in filtered if a.get('area_value', 0) >= filters['min_area']]
        if 'max_area' in filters:
            filtered = [a for a in filtered if a.get('area_value', 1000) <= filters['max_area']]
        
        # Фильтр по статусу
        if 'status' in filters:
            filtered = [a for a in filtered if a.get('status') == filters['status']]
        
        # Фильтр по ЖК
        if 'complex_id' in filters:
            filtered = [a for a in filtered if a.get('complex_id') == filters['complex_id']]
        
        # Сортировка
        sort_by = filters.get('sort_by', 'price')
        sort_order = filters.get('sort_order', 'asc')
        
        if sort_by == 'price':
            filtered.sort(key=lambda x: x.get('price', 0), reverse=(sort_order == 'desc'))
        elif sort_by == 'area':
            filtered.sort(key=lambda x: x.get('area_value', 0), reverse=(sort_order == 'desc'))
        elif sort_by == 'rooms':
            filtered.sort(key=lambda x: x.get('rooms', 0), reverse=(sort_order == 'desc'))
        
        return filtered
    
    def get_complexes(self) -> List[Dict]:
        """Получить список жилых комплексов"""
        if not self.complexes_data:
            self.fetch_all_data()
        
        return self.complexes_data.get('complexes', [])
    
    def get_stats(self) -> Dict:
        """Статистика по квартирам"""
        apartments = self.get_apartments()
        
        if not apartments:
            return {
                'total': 0,
                'average_price': 0,
                'min_price': 0,
                'max_price': 0,
                'by_rooms': {},
                'by_complex': {}
            }
        
        prices = [a.get('price', 0) for a in apartments]
        rooms_count = {}
        
        for apt in apartments:
            rooms = apt.get('rooms', 1)
            rooms_count[rooms] = rooms_count.get(rooms, 0) + 1
        
        complexes_count = {}
        for apt in apartments:
            complex_name = apt.get('complex_name', 'Неизвестно')
            complexes_count[complex_name] = complexes_count.get(complex_name, 0) + 1
        
        return {
            'total': len(apartments),
            'average_price': sum(prices) / len(prices) if prices else 0,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'by_rooms': rooms_count,
            'by_complex': complexes_count
        }
    
    def search_apartments(self, query: str) -> List[Dict]:
        """Поиск квартир по тексту"""
        apartments = self.get_apartments()
        query_lower = query.lower()
        
        results = []
        for apt in apartments:
            # Поиск по названию, ЖК, адресу
            search_fields = [
                apt.get('title', ''),
                apt.get('complex_name', ''),
                apt.get('complex_address', ''),
                ' '.join(apt.get('features', [])),
                apt.get('description', '')
            ]
            
            text_to_search = ' '.join(str(f) for f in search_fields).lower()
            
            if query_lower in text_to_search:
                results.append(apt)
        
        return results

if __name__ == "__main__":
    # Тестирование
    feed = ApartmentFeed()
    data = feed.fetch_all_data()
    
    print(f"Загружено ЖК: {data['total_complexes']}")
    print(f"Загружено квартир: {data['total_apartments']}")
    
    if data['apartments']:
        print("\nПервые 3 квартиры:")
        for i, apt in enumerate(data['apartments'][:3], 1):
            print(f"{i}. {apt['title']} - {apt['price_display']} - {apt['area']}")
    
    stats = feed.get_stats()
    print(f"\nСтатистика:")
    print(f"Всего: {stats['total']} квартир")
    print(f"Средняя цена: {stats['average_price']:,.0f} ₽")
