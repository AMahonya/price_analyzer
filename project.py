import os
import csv
import json


class PriceMachine:
    def __init__(self):
        self.data = []
        self.result = []
        self.name_length = 0

    def load_prices(self, file_path='.'):
        """
        Сканирует указанный каталог. Ищет файлы со словом price в названии.
        В файле ищет столбцы с названием товара, ценой и весом.
        Допустимые названия для столбца с товаром:
            товар
            название
            наименование
            продукт

        Допустимые названия для столбца с ценой:
            розница
            цена

        Допустимые названия для столбца с весом (в кг.):
            вес
            масса
            фасовка
        """
        for filename in os.listdir(file_path):
            if "price" in filename.lower():
                full_path = os.path.join(file_path, filename)
                if os.path.isfile(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as csvfile:

                            reader = csv.reader(csvfile)
                            headers = next(reader)

                            product_col, price_col, weight_col = self._search_product_price_weight(headers)

                            if product_col is not None and price_col is not None and weight_col is not None:
                                for row in reader:
                                    try:
                                        product = row[product_col].strip()
                                        price = float(row[price_col].strip())
                                        weight = float(row[weight_col].strip())

                                        self.data.append({
                                            'название': product,
                                            'цена': price,
                                            'вес': weight,
                                            'файл': filename,
                                            'цена за кг': price / weight if weight > 0 else 0,
                                        })
                                    except (ValueError, IndexError):
                                        print(f"Ошибка при переборе строк в {filename}, строка {row}. Пропуск строки.")
                            else:
                                print(f"Не указаны необходимые столбцы в {filename}. Файл пропущен.")

                    except Exception as e:
                        print(f"Ошибка при чтении файла {filename}: {e}")

        return self.data


    def _search_product_price_weight(self, headers):
        """
        Возвращает номера столбцов с товаром, ценой и весом.
        """
        product_col, price_col, weight_col = None, None, None
        for i, header in enumerate(headers):
            header = header.strip().lower()
            if header in ["название", "продукт", "товар", "наименование"]:
                product_col = i
            elif header in ["цена", "розница"]:
                price_col = i
            elif header in ["фасовка", "масса", "вес"]:
                weight_col = i
        return product_col, price_col, weight_col

    def export_to_html(self, results, search_text, fname='templates/output.html'):
        """
        Выгружает запрашиваемые данных в HTML в виде таблицы,
         при каждом запросе добавляется наименование запроса
         и создаётся соответствующая таблица согласно запроса
        """
        result = ""
        if not os.path.exists(fname):
            result = '''
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                <meta charset="UTF-8">
                    <title>Анализатор прайс-листов.</title>
             <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
        </head>
        '''
        else:
            with open(fname, 'r', encoding='utf-8') as f:

                result = f.read().replace('</body></html>', '')  # удаляем body и html для новых данных


        result += f'''
                    <h2>Текст который использовался в поиске: {search_text}</h2>
                    <table>
                        <tr>
                            <th>Номер</th>
                            <th>Название</th>
                            <th>Цена</th>
                            <th>Фасовка</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>
                '''
        for i, item in enumerate(results):
            result += f'''
                        <tr>
                            <td>{i + 1}</td>
                            <td>{item['название']}</td>
                            <td>{item['цена']}</td>
                            <td>{item['вес']}</td>
                            <td>{item['файл']}</td>
                            <td>{item['цена за кг']:.2f}</td>
                        </tr>
                        '''
        result += '''
                    </table>
                '''
        result += '''
        </body></html>
                '''
        if not os.path.exists('templates'):
            os.makedirs('templates')

        try:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(result)
            return f"Данные успешно созданы в HTML: {fname}"
        except Exception as e:
            return f"Ошибка при создании данных в HTML: {e}"

    def find_text(self, text):
        """
        получает текст и возвращает список позиций, содержащий этот текст в названии продукта
        """
        results = [item for item in self.data if text.lower() in item['название'].lower()]
        results.sort(key=lambda x: x['цена за кг'])
        return results

    def display_results(self, results):
        """
        выводит результаты поиска в консоль
        """
        if not results:
            print("Товар не найден.")
            return

        print("{:<4} {:<30} {:<8} {:<8} {:<15} {:<10}".format("№", "Наименование", "Цена", "Вес", "Файл",
                                                              "Цена за кг."))
        for i, item in enumerate(results):
            print("{:<4} {:<30} {:<8} {:<8} {:<15} {:<10.2f}".format(i + 1, item['название'], item['цена'],
                                                                     item['вес'], item['файл'], item['цена за кг']))

    def export_to_json(self, results, fname='data/output.json'):
        """
        Экспортирует запросы в JSON формат для работы с ними в дальнейшем
        """
        try:
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            return f"Data exported to {fname}"
        except Exception as e:
            return f"Error exporting to JSON: {e}"


def project():
    """
    Функционал проекта
    """
    output_file = 'templates/output.html'
    # Создание директории
    os.makedirs('data', exist_ok=True)  # создаёт директорию для json файла

    pm = PriceMachine()

    pm.load_prices('pryses')  # папка в которой происходит поиск прайсов

    while True:
        text = input("Введите текст для поиска (или 'exit' для выхода): ")
        if text.lower() == "exit":
            print("Работа закончена.")
            break

        results = pm.find_text(text)
        pm.display_results(results)
        print(pm.export_to_html(results, text))
        print(pm.export_to_json(results))
    os.system(f"start {os.path.abspath(output_file)}")  # запускает HTML файл после завершения скрипта


if __name__ == "__main__":
    project()
