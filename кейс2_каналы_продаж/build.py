# -*- coding: utf-8 -*-
"""Генерация заполненной таблицы «Кейс 2. Анализ каналов продаж» (футболки с принтом)."""
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

CH = ["сайт", "директ", "LaModa", "Ozon ", "WB", "Блогер", "канал n"]

# --- исходные данные воронки за месяц ---
pokazy   = [28000, 130000, 62000, 145000, 168000, 85000, 96000]
perehody = [2100,  1100,   2480,  5800,   5880,   1700,  768]
kliki    = [210,   77,     223,   522,    470,    136,   31]
prodazhi = [40,    12,     28,    54,     45,     20,    3]
zatr     = [17000, 24000,  18000, 26000,  30000,  35000, 22000]

# --- юнит-экономика (из Кейса 1: футболка 780 + принт 46 + упаковка 25 = 851 ₽) ---
cena     = [3390, 3390, 3390, 3390, 3390, 3051, 3390]   # блогер — промокод -10%
sebes    = 851
komiss   = [368, 368, 1337, 878, 930, 361, 368]         # комиссия МП + логистика + эквайринг
marzha   = [c - sebes - k for c, k in zip(cena, komiss)]
pribyl   = [m * p for m, p in zip(marzha, prodazhi)]
vyruchka = [c * p for c, p in zip(cena, prodazhi)]

wb = Workbook()
ws = wb.active
ws.title = "Воронка"

thin = Side(style="thin", color="B7B7B7")
bd = Border(left=thin, right=thin, top=thin, bottom=thin)
hdr_fill = PatternFill("solid", fgColor="D9E2F3")
in_fill  = PatternFill("solid", fgColor="FFF2CC")   # вводимые данные
out_fill = PatternFill("solid", fgColor="E2EFDA")   # расчётные

ws["A1"] = "АНАЛИЗ КАНАЛОВ ПРОДАЖ"
ws["A1"].font = Font(bold=True, size=14)
ws["B3"] = "Каналы продаж"
ws.merge_cells("B3:H3")
ws["B3"].alignment = Alignment(horizontal="center")
ws["B3"].font = Font(bold=True)

ws["A4"] = "Данные"
for i, name in enumerate(CH):
    ws.cell(row=4, column=2 + i, value=name)
ws["I4"] = "ИТОГО"
for c in range(1, 10):
    cell = ws.cell(row=4, column=c)
    cell.font = Font(bold=True)
    cell.fill = hdr_fill
    cell.alignment = Alignment(horizontal="center")

rows_in = [
    ("кол-во показов", pokazy, "#,##0"),
    ("кол-во переходов", perehody, "#,##0"),
    ("кол-во кликов (добавлений в корзину)", kliki, "#,##0"),
    ("кол-во продаж", prodazhi, "#,##0"),
    ("прибыль с продаж", pribyl, '#,##0\\ "р."'),
    ("затрачено", zatr, '#,##0\\ "р."'),
]
for r, (label, vals, fmt) in enumerate(rows_in, start=5):
    ws.cell(row=r, column=1, value=label).font = Font(bold=True)
    for i, v in enumerate(vals):
        c = ws.cell(row=r, column=2 + i, value=v)
        c.number_format = fmt
        c.fill = in_fill
    t = ws.cell(row=r, column=9, value=f"=SUM(B{r}:H{r})")
    t.number_format = fmt
    t.font = Font(bold=True)

rows_calc = [
    ("цена перехода",   "={c}10/{c}6", '#,##0.00\\ "р."'),
    ("цена клиента",    "={c}10/{c}8", '#,##0\\ "р."'),
    ("Деньги в кассе",  "={c}9-{c}10", '#,##0\\ "р."'),
    ("ROAS на 1 рубль", "={c}9/{c}10", "0.00"),
    ("показы - переходы",  "={c}6/{c}5", "0.00%"),
    ("переходы - клики",   "={c}7/{c}6", "0.00%"),
    ("клики - продажи",    "={c}8/{c}7", "0.00%"),
    ("переходы - продажи", "={c}8/{c}6", "0.00%"),
]
for r, (label, tpl, fmt) in enumerate(rows_calc, start=11):
    ws.cell(row=r, column=1, value=label).font = Font(bold=True)
    for col in range(2, 10):
        L = get_column_letter(col)
        c = ws.cell(row=r, column=col, value=tpl.format(c=L))
        c.number_format = fmt
        c.fill = out_fill
        if col == 9:
            c.font = Font(bold=True)

# --- справочный блок ---
ws["A20"] = "СПРАВОЧНО — как получена «прибыль с продаж» (маржинальная прибыль)"
ws["A20"].font = Font(bold=True, size=12)
ref = [
    ("Цена продажи, ₽", cena, '#,##0\\ "р."'),
    ("Себестоимость юнита, ₽ (футболка 780 + принт 46 + упаковка 25)", [sebes] * 7, '#,##0\\ "р."'),
    ("Комиссия канала + логистика + эквайринг на 1 заказ, ₽", komiss, '#,##0\\ "р."'),
    ("Маржа с 1 заказа, ₽", marzha, '#,##0\\ "р."'),
    ("Выручка, ₽", vyruchka, '#,##0\\ "р."'),
]
for r, (label, vals, fmt) in enumerate(ref, start=21):
    ws.cell(row=r, column=1, value=label)
    for i, v in enumerate(vals):
        c = ws.cell(row=r, column=2 + i, value=v)
        c.number_format = fmt
    if label == "Выручка, ₽":
        t = ws.cell(row=r, column=9, value=f"=SUM(B{r}:H{r})")
        t.number_format = fmt
        t.font = Font(bold=True)
ws.cell(row=26, column=1, value="ДРР (доля рекламных расходов в выручке), %")
for col in range(2, 10):
    L = get_column_letter(col)
    c = ws.cell(row=26, column=col, value=f"={L}10/{L}25")
    c.number_format = "0.0%"

ws.column_dimensions["A"].width = 58
for col in range(2, 10):
    ws.column_dimensions[get_column_letter(col)].width = 14
for r in range(4, 19):
    for col in range(1, 10):
        ws.cell(row=r, column=col).border = bd

wb.save("Кейс2_Анализ_каналов_продаж_заполнено.xlsx")

# --- CSV с формулами для загрузки в Google Таблицы ---
rows = [[""] * 9 for _ in range(26)]
rows[0][0] = "АНАЛИЗ КАНАЛОВ ПРОДАЖ"
rows[2][1] = "Каналы продаж"
rows[3] = ["Данные"] + CH + ["ИТОГО"]
for idx, (label, vals, _) in enumerate(rows_in):
    rows[4 + idx] = [label] + [str(v) for v in vals] + [f"=SUM(B{5+idx}:H{5+idx})"]
for idx, (label, tpl, _) in enumerate(rows_calc):
    r = 11 + idx
    rows[10 + idx] = [label] + [tpl.format(c=get_column_letter(col)) for col in range(2, 10)]
rows[19][0] = "СПРАВОЧНО — как получена «прибыль с продаж» (маржинальная прибыль)"
for idx, (label, vals, _) in enumerate(ref):
    r = 21 + idx
    rows[20 + idx] = [label] + [str(v) for v in vals] + ([f"=SUM(B{r}:H{r})"] if idx == 4 else [""])
rows[25] = ["ДРР (доля рекламных расходов в выручке), %"] + [
    f"={get_column_letter(col)}10/{get_column_letter(col)}25" for col in range(2, 10)]

with open("Кейс2_Анализ_каналов_продаж_заполнено.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerows(rows)

# --- контроль ---
print("продажи:", sum(prodazhi), "| выручка:", sum(vyruchka), "| прибыль:", sum(pribyl),
      "| затрачено:", sum(zatr), "| касса:", sum(pribyl) - sum(zatr),
      "| ROAS:", round(sum(pribyl) / sum(zatr), 2))
for i, n in enumerate(CH):
    print(f"{n:8s} марж/шт {marzha[i]:5d} | приб {pribyl[i]:7d} | касса {pribyl[i]-zatr[i]:8d} | "
          f"ROAS {pribyl[i]/zatr[i]:.2f} | CAC {zatr[i]/prodazhi[i]:7.0f} | "
          f"цена перех {zatr[i]/perehody[i]:6.2f} | ДРР {zatr[i]/vyruchka[i]:.1%} | "
          f"CR перех→прод {prodazhi[i]/perehody[i]:.2%}")
