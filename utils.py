import requests
import json
from config import *

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):

        try:
            base_key = exchange[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchange[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(
                f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        p = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={exchange[base]}&tsyms={exchange[sym]}')
        resp = json.loads(p.content)
        new_price = resp[exchange[sym]] * float(amount)

        return round(new_price, 2)
