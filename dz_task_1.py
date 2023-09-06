import csv
from random import randint
import json


#Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла
def equation_decorator(filename):
    def decorator(func):
        def wrapper():
            results = []
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    a, b, c = map(int, row)
                    result = func(a, b, c)
                    results.append({'equation': f'{a}x^2 + {b}x + {c} = 0',
                                    'result': result})
            return results
        return wrapper
    return decorator



#Декоратор, сохраняющий переданные параметры и результаты работы функции в json файл
def to_json_decorator(filename: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, 'w') as f:
                json.dump(result, f, indent=4)
            return result
        return wrapper
    return decorator


#Генерация csv файла с тремя случайными числами в каждой строке. 100-1000 строк
def generate_csv_file(filename: str):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(randint(100, 1001)):
            writer.writerow([randint(1, 100) for _ in range(3)])


#Функция нахождения корней квадртного уравнения
@to_json_decorator('equation_sol.json')
@equation_decorator('roots.csv')
def find_roots_equation(a: int, b: int, c: int,) -> tuple[str, str] | str:
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        x1 = (-b+discriminant**(0.5)) / (2*a)
        x2 = (-b-discriminant**(0.5)) / (2*a)
        return str(x1), str(x2)
    else:
        return "Complex roots"


if __name__ == '__main__':
    generate_csv_file('roots.csv')
    find_roots_equation()
