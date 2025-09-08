#!/usr/bin/env python3
"""
Скрипт для тестирования подключения к Redis
Запуск: python3 scripts/test_redis.py
"""

import redis
import json
from datetime import datetime

def test_redis_connection():
    """Тестирует подключение к Redis и базовые операции"""
    
    try:
        # Подключение к Redis
        r = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        
        # Проверка подключения
        if r.ping():
            print("✅ Redis подключение успешно!")
        
        # Тест базовых операций
        test_key = "test:connection"
        test_value = {
            "timestamp": datetime.now().isoformat(),
            "message": "Hello from Python!",
            "test": True
        }
        
        # Сохранение данных
        r.setex(test_key, 60, json.dumps(test_value))
        print(f"✅ Данные сохранены с ключом: {test_key}")
        
        # Получение данных
        stored_value = r.get(test_key)
        if stored_value:
            parsed_value = json.loads(stored_value)
            print(f"✅ Данные получены: {parsed_value}")
        
        # Проверка TTL
        ttl = r.ttl(test_key)
        print(f"✅ TTL ключа: {ttl} секунд")
        
        # Информация о Redis
        info = r.info()
        print(f"✅ Версия Redis: {info.get('redis_version')}")
        print(f"✅ Используемая память: {info.get('used_memory_human')}")
        print(f"✅ Количество подключений: {info.get('connected_clients')}")
        
        # Очистка тестовых данных
        r.delete(test_key)
        print("✅ Тестовые данные очищены")
        
        return True
        
    except redis.ConnectionError as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при тестировании Redis: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Тестирование подключения к Redis...")
    success = test_redis_connection()
    
    if success:
        print("\n🎉 Все тесты Redis прошли успешно!")
    else:
        print("\n💥 Обнаружены проблемы с Redis")
        exit(1)