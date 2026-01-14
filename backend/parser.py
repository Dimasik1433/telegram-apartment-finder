import xml.etree.ElementTree as ET
import requests
import sqlite3
from datetime import datetime

class FidParser:
    def __init__(self, fid_url):
        self.fid_url = fid_url
    
    def parse_feed(self):
        """Парсит фид и возвращает список квартир"""
        try:
            response = requests.get(self.fid_url)
            response.raise_for_status()
            
            # Парсинг XML (пример для формата Яндекс.Недвижимость)
            root = ET.fromstring(response.content)
            apartments = []
            
            for offer in root.findall('.//offer'):
                apartment = {
                    'id': offer.get('internal-id'),
                    'type': offer.find('type').text if offer.find('type') is not None else '',
                    'category': offer.find('category').text if offer.find('category') is not None else '',
                    'price': float(offer.find('price').text) if offer.find('price') is not None else 0,
                    'rooms': int(offer.find('rooms').text) if offer.find('rooms') is not None else 0,
                    'area': float(offer.find('area').text) if offer.find('area') is not None else 0,
                    'district': offer.find('district').text if offer.find('district') is not None else '',
                    'address': offer.find('address').text if offer.find('address') is not None else '',
                    'description': offer.find('description').text if offer.find('description') is not None else '',
                    'images': [img.text for img in offer.findall('image') if img.text],
                    'url': offer.find('url').text if offer.find('url') is not None else '',
                    'updated': datetime.now().isoformat()
                }
                apartments.append(apartment)
            
            return apartments
            
        except Exception as e:
            print(f"Ошибка парсинга фида: {e}")
            return []

# Пример использования
if __name__ == "__main__":
    parser = FidParser("https://ваш-сайт.ru/fid.xml")
    apartments = parser.parse_feed()
    print(f"Найдено {len(apartments)} квартир")
