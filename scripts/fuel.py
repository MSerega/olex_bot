import enum
import re

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
import time
from settings.config import FUEL_ANP_SHELL
from db import db_connect as db

from dataclasses import dataclass


class StationType(enum.Flag):
    BENZINE = {
        "A95 Energy": "A-95 Energy",
        "A95": "A-95",
        "A92 Energy": "A-92 Energy",
        "A92": "A-92"
    }
    GAS = {"ГАЗ": "Газ"}
    DIESEL = {"ДП Energy": "ДП"}
    BENZINE_AND_DIESEL = BENZINE | DIESEL
    ALL = BENZINE | GAS | DIESEL


STATION_INFO = {
    'ANP13': {'coord': (242, 66),
              'type': StationType.BENZINE_AND_DIESEL,
              'link': 'https://goo.gl/maps/HbSKHm9PJMfUpWeJ8'},
    'ANP12': {'coord': (371, 163),
              'type': StationType.BENZINE_AND_DIESEL,
              'link': 'https://goo.gl/maps/fyg9YvkQ9NdPWF5R6'},
    'ANP32': {'coord': (367, 187), 'type': StationType.GAS,
              'link': 'https://goo.gl/maps/zYrEcrjJhjDW2mps5'},
    'ANP11': {'coord': (585, 440),
              'type': StationType.BENZINE_AND_DIESEL,
              'link': 'https://goo.gl/maps/ZDqwnLN2s9vj2oZx5'},
    # 'SHELL': {'coord': (428, 565),
    #           'type': StationType.ALL,
    #           'link': 'https://goo.gl/maps/iC8S4Li1emtS35es7'},
}


@dataclass
class StationData:
    address: str
    fuel_types: list[str]


def parse_address(content: str) -> str:
    if m := re.search(r'^Адреса:\s(.*?)$', content, re.DOTALL | re.MULTILINE):
        return m.group(1)
    else:
        raise RuntimeError(f'Can not parse address: {content}')


def parse_fuel_types(content: str) -> list[str]:
    # Пальне в наявності / Наявність пального
    if m := re.search(r'^(?:Пальне в наявності|Наявність пального):\s*(.*?)$',
                      content,
                      re.DOTALL | re.MULTILINE | re.IGNORECASE):
        value = m.group(1)
        return value.split(', ') if 'немає' not in value.lower() else []
    else:
        raise RuntimeError(f'Can not find fuel line: {content}')


def make_text(name: str, link: str, type_: StationType, data: StationData) -> str:
    fuel_types_str = []
    for original, result in type_.value.items():
        icon = "✅" if original in data.fuel_types else "❌"
        fuel_types_str.append(f'{icon} {result}')
    fuel_types_str = '\n       '.join(fuel_types_str)

    return (f"⛽ <b>Заправка {name}:</b>\n"
            f"📫 Адреса: <a href='{link}'>{data.address}</a>\n"
            f"🛢 Пальне в наявності:\n       {fuel_types_str}\n")


def get_station_data(driver, coord: tuple[int, int]) -> StationData:
    driver.get(FUEL_ANP_SHELL)
    time.sleep(4)
    ActionChains(driver).move_by_offset(*coord).click().perform()
    waiter = WebDriverWait(driver, 15)
    xpath = '//div[@class="mapboxgl-popup-content"]'
    popup_contents_el = waiter.until(ec.presence_of_element_located((By.XPATH, xpath)))
    address = parse_address(popup_contents_el.text)
    fuel_types = parse_fuel_types(popup_contents_el.text)
    return StationData(address, fuel_types)


# def fix_shell_address(address: str) -> str:
#     ignores = ('обл.', 'р-н')
#     parts = []
#     for part in address.split(','):
#         for ignore in ignores:
#             if ignore in part:
#                 break
#         else:
#             parts.append(part.strip())
#     return ', '.join(parts)


def make_message(driver):
    parts = []
    for station_name, info in STATION_INFO.items():
        link = STATION_INFO[station_name]['link']
        type_ = info['type']
        coord = info['coord']
        # print(f'{station_name=} {coord=} {type_} {link=}')

        data = get_station_data(driver, coord)
        # if station_name == 'SHELL':
        #     data.address = fix_shell_address(data.address)

        print(f'{data}')
        message_text = make_text(station_name, link, type_, data)
        # print(f'{message_text=}')
        parts.append(message_text)

        ActionChains(driver).reset_actions()
        driver.refresh()
    return '\n\n'.join(parts)


def get_fuel_from_db():
    data = db.get_fuel()

    text = ''
    for station in data:
        name = station['station']
        address = station['address']
        link = station['link']

        fuel_types_str = ''
        dict_fuel = {
            "А-95": "fuel_95",
            "А-92": "fuel_92",
            "ДП": "fuel_diezel",
            "Газ": "fuel_gaz"
        }
        if name == 'Shell':
            for i in ['А-95', 'А-92', 'ДП', 'Газ']:
                fuel_types_str += f'       {("❌", "✅")[station[dict_fuel[i]]]} {i}\n'

        elif name == 'Mac':
            for i in ['А-95', 'А-92', 'ДП']:
                fuel_types_str += f'       {("❌", "✅")[station[dict_fuel[i]]]} {i}\n'

        elif name == 'Belarus':
            for i in ['Газ']:
                fuel_types_str += f'       {("❌", "✅")[station[dict_fuel[i]]]} {i}\n'

        text += f"⛽ <b>Заправка {name}:</b>\n" \
                f"📫 Адреса: <a href='{link}'>{address}</a>\n" \
                f"🛢 Пальне в наявності:\n{fuel_types_str}\n\n"
    return text


def get_fuel():
    s = 3
    while s != 0:
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

            size = capabilities = {
                "resolution": "980x724"
            }

            with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  desired_capabilities=size,
                                  options=options) as driver:
                msg = make_message(driver)
                msg += '\n\n' + get_fuel_from_db()
                return msg
        except WebDriverException as e:
            s -= 1
    return f"Виникла помилка. Спробуйте виконати команду ще раз."
