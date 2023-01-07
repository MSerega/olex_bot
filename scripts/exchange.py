import requests
import json
from settings import config


def get_exchange():
    response = requests.get(config.PRIVAT_ECHANGE).text
    data = json.loads(response)
    s = ''
    for r in data:
        if r["ccy"] == 'BTC':
            s += (
                f'{r["ccy"]} / {r["base_ccy"]}:\n'
                f'🔺 Купівля: {round(float(r["buy"]), 2)} $\n'
                f'🔻 Продаж: {round(float(r["sale"]), 2)} $\n\n'
            )
        else:
            s += (
                f'{r["ccy"]} / {r["base_ccy"]}:\n'
                f'🔺 Купівля: {round(float(r["buy"]), 2)} грн.\n'
                f'🔻 Продаж: {round(float(r["sale"]), 2)} грн.\n\n'
            )
    return s
