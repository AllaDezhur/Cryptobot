import requests
import json
from Config import moneys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одну и ту же валюту {base}')

        try:
            quote_ticker = moneys[quote]
        except KeyError:
            raise ConvertionException(f'Данная валюта отсутствует {quote}')

        try:
            base_ticker = moneys[base]
        except KeyError:
            raise ConvertionException(f'Данная валюта отсутствует {base}')

        try:
            if float(amount) > 0:
             amount = float(amount)
            else:
                raise ConvertionException(f'Количество валюты не может быть отрицательным {amount}.\n Введите другое число.')
        except ValueError:
            raise ConvertionException(f'Количество введено некорректно {amount}.\n Используйте только цифры')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = amount * json.loads(r.content)[moneys[base]]

        return total_base


class DeclensionByCases():
    def __init__(self, word, num):
        self.word = word
        self.num = num

    def incline(self):
        if self.word != 'евро':
            if (2 <= self.num % 10 <= 4 and self.num % 100 not in [12, 13, 14]) or not self.num.is_integer():
                return 'рубля' if self.word == 'рубль' else self.word + 'a'
            if (self.num % 10 == 0 or 5 <= self.num % 10 <= 9 or 11 <= self.num % 100 <= 14) and self.num.is_integer():
                return 'рублей' if self.word == 'рубль' else self.word + 'ов'
        return self.word