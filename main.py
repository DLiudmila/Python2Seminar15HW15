# Напишите следующие функции:
# Нахождение корней квадратного уравнения
# Генерация csv файла с тремя случайными числами в каждой строке. 100-1000 строк.
# Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла.
# Декоратор, сохраняющий переданные параметры и результаты работы функции в json файл.
# Добавьте к ним логирование ошибок и полезной информации.
# Также реализуйте возможность запуска из командной строки с передачей параметров.

import csv
import json
import math
import random
import logging
import sys

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    file_handler = logging.FileHandler('app.log')
    logging.getLogger('').addHandler(file_handler)

def generate_csv(filename, rows):
    # Генерирует csv файл с тремя случайными числами в каждой строке для заданного количества строк
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['num1', 'num2', 'num3'])  # Записываем заголовок

        for _ in range(rows):
            row = [random.randint(1, 100) for _ in range(3)]
            writer.writerow(row)
        logging.info(f"Сгенерирован файл: {filename}")

def roots_from_csv_decorator(func):
    # Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла

    def wrapper(filename):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Пропускаем заголовок

            for row in reader:
                a, b, c = map(int, row)
                try:
                    roots = func(a, b, c)
                    logging.info(f"Корни для {a}, {b}, {c}: {roots}")
                except Exception as e:
                    logging.error(f"Ошибка при вычислении корней для {a}, {b}, {c}: {e}")

    return wrapper


def save_to_json_decorator(func):
    # Декоратор, сохраняющий параметры и результаты работы функции в JSON-файл для каждой тройки чисел из numbers.csv

    def wrapper(filename):
        results = []
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Пропускаем заголовок

            for row in reader:
                a, b, c = map(int, row)
                try:
                    result = func(a, b, c)
                    data = {
                        'parameters': {
                            'a': a,
                            'b': b,
                            'c': c
                        },
                        'result': result
                    }
                    results.append(data)
                    logging.info(f"Добавлен результат вычисления корней для {a}, {b}, {c}")
                except Exception as e:
                    logging.error(f"Ошибка при вычислении корней для {a}, {b}, {c}: {e}")

        with open('results.json', 'w') as jsonfile:
            json.dump(results, jsonfile, indent=4)
            logging.info("Результаты записаны в results.json")

    return wrapper


@roots_from_csv_decorator
def find_roots(a, b, c):
    # Функция для нахождения корней квадратного уравнения с заданными параметрами
    D = b**2 - 4*a*c
    if D < 0:
        raise ValueError("Корней нет")
    elif D == 0:
        x = (-b + math.sqrt(D)) / (2*a)
        return [x]
    else:
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        return [x1, x2]


def main():
    # Основная функция, запускающая программу из командной строки
    setup_logging()

    if len(sys.argv) != 3:
        print("Использование: python main.py <имя_файла> <количество_строк>")
        sys.exit(1)

    filename = sys.argv[1]
    rows = int(sys.argv[2])

    generate_csv(filename, rows)
    find_roots(filename)


if __name__ == '__main__':
    main()