import json
import requests
from config import abbreviations


class APIException(Exception):  # Класс ошибок для работы программы
    pass


class Convertor:
    @staticmethod
    def get_price(old: str, new: str, amount: str):  # Получаем аргументы: из какой валюты, в какую валюту, количество
        if old.upper() in abbreviations.values():  # Если пользователь ввел код валюты, то ключи уже не смотрим
            old_key = old.upper()
        else:
            try:  # Проверяем наличие первой введенной валюты среди ключей в словаре аббревиатур
                old_key = abbreviations[old.lower()]  # Сохраняем аббревиатуру валюты в old_key
            except KeyError:  # Вызываем ошибку, если валюты в словаре нет
                raise APIException(f'Валюта "{old}" не найдена!')

        if new.upper() in abbreviations.values():  # Если пользователь ввел код валюты, то ключи уже не смотрим
            new_key = new.upper()
        else:
            try:  # Проверяем наличие второй введенной валюты среди ключей в словаре аббревиатур
                new_key = abbreviations[new.lower()]  # Сохраняем аббревиатуру валюты в new_key
            except KeyError:  # Вызываем ошибку, если валюты в словаре нет
                raise APIException(f'Валюта "{new}" не найдена!')

        if old_key == new_key:  # Вызываем ошибку, если указаны одинаковые валюты
            raise APIException(f'Указаны одинаковые валюты "{old}"!')

        try:  # Проверяем, что количество валюты указано в корректной форме
            amount = float(amount.replace(',', '.'))  # Заменяем разделитель в числе с запятой на точку
        except ValueError:  # Вызываем ошибку, если amount не число
            raise APIException(f'Указаны неверные данные "{amount}" для количества валюты!')

        # Делаем запрос по API с указанием из какой валюты в какую переводим
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={old_key}&tsyms={new_key}")
        rate = json.loads(r.content)[new_key]  # По ключу второй валюты получаем курс первой валюты для второй
        new_price = round(rate * amount, 3)  # Умножаем курс на количество и округляем до трех знаков после запятой
        # Получаем результат. Я использовал аббревиатуры валют, чтобы не было проблем с окончаниями слов
        message = f"Цена {amount} {old_key} составляет {new_price} {new_key}"
        return message
