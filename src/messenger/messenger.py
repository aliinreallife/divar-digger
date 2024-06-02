from os import getenv
from typing import Any, Dict, List

import requests

from constants import TELEGRAM_TOKEN

IDs = []

map = {
    "title": "عنوان",
    "price": "قیمت",
    "metrage": "متراژ",
    "year_of_construction": "سال ساخت",
    "number_of_rooms": "تعداد اتاق",
    "has_elevator": "آسانسور",
    "has_parking": "پارکینگ",
    "has_storage_room": "انباری",
    "agency": "آژانس",
    "agent": "مشاور",
    "has_image": "عکس",
    "description": "توضیحات",
    "_id": "لینک",
}


def send_to_telegram(data: Dict[str, Any], IDs: List[int] = IDs):
    text = data_to_text(data)
    for id in IDs:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": id, "text": text, "disable_notification": "true"},
        )


def data_to_text(data: Dict[str, Any]) -> str:
    text = ""
    for key, value in data.items():
        value = (
            "دارد" if value is True else "----" if value is False else value
        )  # True or False to دارد و ندارد
        if key == "price":
            value = f"{value:,}"
        elif key == "_id":
            value = BASE_URL + value
        elif key == "description":
            value = f"\n--------------------\n{value}"

        persian_key = map[key]
        text += f"{persian_key}: {value}\n"
    return text
