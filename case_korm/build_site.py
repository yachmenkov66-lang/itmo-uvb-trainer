# -*- coding: utf-8 -*-
"""Собирает готовую страницу: подставляет изображения как data URI.

Внешние картинки в опубликованном артефакте заблокированы политикой
безопасности, поэтому пять концептов упаковки вшиваются прямо в файл.

Запуск:  python3 case_korm/build_site.py
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "site.src.html")
DST = os.path.join(HERE, "index.html")
DST_LOCAL = os.path.join(HERE, "Корм для людей — сайт.html")

# Артефакт сам оборачивает страницу в doctype/head/body, а для локального
# файла это нужно дописать: без явной кодировки браузер может испортить
# кириллицу, без viewport — сломать вёрстку на телефоне.
SHELL = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Корм для людей — удобная еда для плотного расписания. Пять форматов одной идеи. Проект на стадии концепции.">
{head}
</head>
<body>
{body}
</body>
</html>
"""

IMAGES = {
    "{{IMG_GRANULES}}": "product-granules.webp",
    "{{IMG_POWDER}}": "product-powder.webp",
    "{{IMG_NOODLES}}": "product-noodles.webp",
    "{{IMG_SNACKS}}": "product-snacks.webp",
    "{{IMG_CUBES}}": "product-cubes.webp",
}


def data_uri(name):
    with open(os.path.join(HERE, "assets", name), "rb") as f:
        return "data:image/webp;base64," + base64.b64encode(f.read()).decode()


def main():
    with open(SRC, encoding="utf-8") as f:
        html = f.read()
    for token, name in IMAGES.items():
        if token not in html:
            raise SystemExit(f"в шаблоне нет метки {token}")
        html = html.replace(token, data_uri(name))
    with open(DST, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"saved: {DST}  ({os.path.getsize(DST) / 1024 / 1024:.2f} МБ)")

    # самостоятельная версия для локального компьютера и любого хостинга
    split = html.index("</style>") + len("</style>")
    with open(DST_LOCAL, "w", encoding="utf-8") as f:
        f.write(SHELL.format(head=html[:split].strip(), body=html[split:].strip()))
    print(f"saved: {DST_LOCAL}  ({os.path.getsize(DST_LOCAL) / 1024 / 1024:.2f} МБ)")


if __name__ == "__main__":
    main()
