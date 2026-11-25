# Лабораторная работа 3. Каталог объектов

Предметная модель: библиотечные книги
## Структура проекта

```
.
├── src/
│   ├── main.py                  # Точка входа
│   ├── catalog.py               # Операции с каталогом
│   ├── constans.py              # Константные данные
│   ├── models.py                # Модель книги
│   ├── repository.py            # Загрузка и сохранение каталога
│   ├── errors.py                # Исключения
│   ├── mocks/                   # Примеры входных JSON-файлов
│   │   ├── v1.json
│   │   └── v2.json
│   └── results/                 # Результаты сохранения
├── scripts/
│   └── v1/
│       └── catalog_demo.py      # Демонстрационный запуск
└── tests/
    ├── test_catalog.py         
    ├── test_json.py             
    └── test_models.py           
```


## Установка и локальный запуск

Для запуска нужен Python 3.12 и новее и uv
```bash
uv sync
make run
```

Тесты
```bash
make test 
```

## Использование модели


```python
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from src.catalog import Catalog
from src.models import BookModel

book = BookModel(
    id="5",
    title="The Time Machine",
    category="Science Fiction",
    timestamp=datetime(2026, 1, 5, 10, tzinfo=UTC),
    author="H. G. Wells",
    price=Decimal("9.75"),
) # Создание экземпляра модели

catalog = Catalog() # Инициализация каталога
catalog.add(book) # Добавления объекта в каталог

print(catalog.get("5").title) # получить объект из каталога
print(catalog.find_by_name("the time machine").author) # поиск объекта в каталоге

catalog.save(Path("example.json")) # Сохранить каталог в JSON формате

restored = Catalog()
restored.load(Path("results/example.json")) # загрузить каталог из JSON
assert restored.get("5") == book

restored.remove("5") # удалить объект из каталога
assert len(restored) == 0
```

## Формат JSON хранилища
```json
{
    "format_version": 1,
    "data": {
        "unique_id": {
            "id": "str",
            "title": "str",
            "category": "str",
            "author": "str",
            "timestamp": "date in timezone",
            "price": "Decimal format"
        },
    }
}
```


