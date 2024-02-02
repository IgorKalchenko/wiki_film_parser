# Wikipedia film parser

Парсер для сбора информации о фильмах из Википедии

Извлекает:
- Название
- Жанр
- Режиссёра
- Страну
- Год

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:IgorKalchenko/wiki_film_parser.git
```

```
cd wiki_film_parser
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейдите в директорию с файлом scrapy.cfg:

```
cd film_parser/
```

Запустите парсер:

```
scrapy crawl film -O moviedata.csv
```