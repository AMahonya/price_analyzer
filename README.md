# Анализатор прайс-листов:

Скрипт для анализа прайс-листов различных поставщиков и выгрузки их в HTML и JSON

## Требования:

- Python 3.6+
- os
- csv
- json

## Как использовать:
1. Скачать данный репозиторий: `git clone https://github.com/AMahonya/price_analyzer`
2. Поместите в папку `pryses` ваши `csv-файлы`  или замените на свою папку, 
а также можно и просто закинуть прайс листы в проект но нужно 
будет изменить  `pm.load_prices('pryses')` на `pm.load_prices("Название вашей папки или оставь пустым)`, 
а если ваши csv файлы имею другое название в отличии от представленных в пример то замените эту строку 
`if "price" in filename.lower():` на `if "Ваше слово из название csv-файлов" in filename.lower():` 
3. Запустите скрипт с помощью команды: `python project.py`
4. После того как в консоли появиться текст: `("Введите текст для поиска (или 'exit' для выхода),`
делаем запросы которые нужно найти в прайс листах

## Json:
Json файл сохраняется в`data/` (папка `data` создаётся автоматически).

## Визуализация:
Визуализация происходит в консоли в виде таблицы:
<table>
                        <tr>
                            <th>№</th>
                            <th>Наименование</th>
                            <th>Цена</th>
                            <th>Вес</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>
</table>

HTML файл сохраняются в `templates/` (папка `templates` создаётся автоматически).


## Автор проекта 
Андрей Маханец