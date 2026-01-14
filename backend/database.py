import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_path="apartments.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица квартир
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS apartments (
                id TEXT PRIMARY KEY,
                type TEXT,
                category TEXT,
                price REAL,
                rooms INTEGER,
                area REAL,
                district TEXT,
                address TEXT,
                description TEXT,
                images TEXT,  -- JSON массив изображений
                url TEXT,
                updated TEXT,
                created TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица пользовательских фильтров
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_filters (
                user_id INTEGER,
                min_price REAL,
                max_price REAL,
                rooms TEXT,  -- JSON массив
                districts TEXT,  -- JSON массив
                updated TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_apartments(self, apartments):
        """Сохраняет или обновляет квартиры в БД"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for apt in apartments:
            cursor.execute('''
                INSERT OR REPLACE INTO apartments 
                (id, type, category, price, rooms, area, district, address, 
                 description, images, url, updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                apt['id'], apt['type'], apt['category'], apt['price'],
                apt['rooms'], apt['area'], apt['district'], apt['address'],
                apt['description'], json.dumps(apt['images']), 
                apt['url'], apt['updated']
            ))
        
        conn.commit()
        conn.close()
    
    def search_apartments(self, filters=None):
        """Поиск квартир по фильтрам"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM apartments WHERE 1=1"
        params = []
        
        if filters:
            if filters.get('min_price'):
                query += " AND price >= ?"
                params.append(filters['min_price'])
            if filters.get('max_price'):
                query += " AND price <= ?"
                params.append(filters['max_price'])
            if filters.get('rooms'):
                rooms_list = filters['rooms'].split(',')
                placeholders = ','.join(['?'] * len(rooms_list))
                query += f" AND rooms IN ({placeholders})"
                params.extend(rooms_list)
            if filters.get('district'):
                query += " AND district LIKE ?"
                params.append(f'%{filters["district"]}%')
        
        query += " ORDER BY price LIMIT 50"
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        # Преобразуем JSON поля
        for apt in results:
            if apt['images']:
                apt['images'] = json.loads(apt['images'])
        
        conn.close()
        return results
