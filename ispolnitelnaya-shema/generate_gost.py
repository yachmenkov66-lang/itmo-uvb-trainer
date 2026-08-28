# -*- coding: utf-8 -*-
"""Исполнительная схема в формате чертежа: А4 альбомный, рамка и основная надпись
по мотивам ГОСТ 21.101. Геометрия задана в миллиметрах листа (viewBox 297x210),
поэтому при печати без масштабирования сохраняются заявленные масштабы видов.

Цветовая договорённость исполнительной документации:
    красный  — проектное значение (ВОР №1 от 10.07.2025);
    чёрный   — фактически выполненное.
"""

import io

RED = "#C00000"
INK = "#000000"
FONT = "'Roboto Condensed','PT Sans Narrow',Arial,sans-serif"

W, H = 297.0, 210.0
FR_L, FR_T, FR_R, FR_B = 20.0, 5.0, 292.0, 205.0
ST_L, ST_T = 107.0, 150.0          # основная надпись 185 x 55


# ------------------------------------------------------------------ примитивы
def ln(x1, y1, x2, y2, w=0.18, c=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{c}" stroke-width="{w}"{d}/>')


def rect(x, y, w_, h_, fill="none", sw=0.18, c=INK, extra=""):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w_:.2f}" height="{h_:.2f}" '
            f'fill="{fill}" stroke="{c}" stroke-width="{sw}"{extra}/>')


def txt(x, y, s, size=2.5, anchor="middle", fill=INK, weight="400", deco=None):
    d = f' text-decoration="{deco}"' if deco else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{fill}" font-weight="{weight}" '
            f'font-style="italic"{d}>{s}</text>')


def tw(s, size):
    return len(s) * size * 0.47


def halo(x, y, w_, h_):
    return rect(x, y, w_, h_, fill="#FFFFFF", sw=0)


def tick(x, y, c=INK, w=0.3, s=1.5):
    """засечка 45° — ограничение размерной линии на строительном чертеже"""
    return ln(x - s / 2, y + s / 2, x + s / 2, y - s / 2, w, c)


def pair(x, y, black, red, anchor="middle", size=2.6):
    """проектное (красное, подчёркнутое) над фактическим (чёрным)"""
    o = []
    if red:
        o.append(txt(x, y - 2.7, red, size, anchor=anchor, fill=RED, deco="underline"))
    o.append(txt(x, y, black, size, anchor=anchor))
    return "".join(o)


def dim_h(x1, x2, y, black, red=None, ext_y=None):
    o = []
    if ext_y is not None:
        o.append(ln(x1, ext_y, x1, y + 1.6, 0.15))
        o.append(ln(x2, ext_y, x2, y + 1.6, 0.15))
    o.append(ln(x1 - 2.5, y, x2 + 2.5, y, 0.2))
    o += [tick(x1, y), tick(x2, y)]
    o.append(pair((x1 + x2) / 2, y - 0.9, black, red))
    return "".join(o)


def dim_v(y1, y2, x, black, red=None, ext_x=None):
    o = []
    if ext_x is not None:
        o.append(ln(ext_x, y1, x + 1.6, y1, 0.15))
        o.append(ln(ext_x, y2, x + 1.6, y2, 0.15))
    o.append(ln(x, y1 - 2.5, x, y2 + 2.5, 0.2))
    o += [tick(x, y1), tick(x, y2)]
    ym = (y1 + y2) / 2
    o.append(pair(x + 1.4, ym + (1.4 if red else 0.9), black, red, anchor="start"))
    return "".join(o)


def elev(x, y, black, red=None, shelf=13, side=-1):
    """отметка уровня: стрелка, полка, значения над полкой"""
    o = [f'<path d="M{x:.2f},{y:.2f} L{x + 2.2 * side:.2f},{y - 1.3:.2f} '
         f'L{x + 2.2 * side:.2f},{y + 1.3:.2f} Z" fill="{INK}"/>']
    xs = x + shelf * side
    x_text = min(x, xs) + 0.6
    wmax = max(tw(black, 2.6), tw(red, 2.6) if red else 0, shelf)
    o.append(halo(min(x, xs) - 0.6, y - (7.0 if red else 4.4), wmax + 1.8, (7.0 if red else 4.4)))
    o.append(ln(x + 2.2 * side, y, xs, y, 0.25))
    o.append(pair(x_text, y - 0.9, black, red, anchor="start"))
    return "".join(o)


def leader(pts, text, size=2.4, side=1, stack=None):
    """выноска: ломаная + горизонтальная полка + надпись над полкой.
    side = +1 полка вправо, -1 полка влево. stack = (black, red) вместо текста."""
    o = ['<polyline points="' + " ".join(f"{a:.2f},{b:.2f}" for a, b in pts) +
         f'" fill="none" stroke="{INK}" stroke-width="0.18"/>']
    ex, ey = pts[-1]
    body = text if stack is None else stack[0]
    sh = tw(body, size) + 1.5
    xs = ex + sh * side
    o.append(ln(ex, ey, xs, ey, 0.2))
    x_text = min(ex, xs) + 0.7
    if stack is None:
        o.append(txt(x_text, ey - 1.1, text, size, anchor="start"))
    else:
        o.append(pair(x_text, ey - 1.1, stack[0], stack[1], anchor="start", size=size))
    return "".join(o)


# ------------------------------------------------------------------ лист
def frame():
    return rect(0, 0, W, H, fill="#FFFFFF", sw=0) + \
           rect(FR_L, FR_T, FR_R - FR_L, FR_B - FR_T, sw=0.7)


def view_title(x, name, scale, half=14):
    return (txt(x, 18, name, 5.0, weight="700") +
            txt(x, 24.4, scale, 4.0) +
            ln(x - half, 26.2, x + half, 26.2, 0.4))


def stamp(sheet_no, sheets, drawing_name):
    x0, y0 = ST_L, ST_T
    o = [rect(x0, y0, 185, 55, sw=0.7)]

    cols = [9, 11, 9, 11, 15, 10]
    xs, cx = [x0], x0
    for c in cols:
        cx += c
        xs.append(cx)
    xl = xs[-1]
    o.append(ln(xl, y0, xl, y0 + 55, 0.7))

    for i in range(1, 4):
        o.append(ln(x0, y0 + 5 * i, xl, y0 + 5 * i, 0.18))
    o.append(ln(x0, y0 + 15, xl, y0 + 15, 0.18))
    o.append(ln(x0, y0 + 20, xl, y0 + 20, 0.35))
    o.append(ln(x0, y0 + 25, xl, y0 + 25, 0.35))
    for x in xs[1:-1]:
        o.append(ln(x, y0, x, y0 + 25, 0.18))
    for i, hname in enumerate(["Изм.", "Кол.уч", "Лист", "№док.", "Подпись", "Дата"]):
        o.append(txt((xs[i] + xs[i + 1]) / 2, y0 + 23.4, hname, 2.3))

    for i, r in enumerate(["Геодезист", "Прораб", "Гл. инженер"]):
        yy = y0 + 25 + 10.0 * i
        if i:
            o.append(ln(x0, yy, xl, yy, 0.18))
        o.append(txt(x0 + 1.2, yy + 6.4, r, 2.5, anchor="start"))
    for i in (2, 4, 5):
        o.append(ln(xs[i], y0 + 25, xs[i], y0 + 55, 0.18))

    o.append(ln(xl, y0 + 25, x0 + 185, y0 + 25, 0.7))
    o.append(txt((xl + x0 + 185) / 2, y0 + 11.0, "Исполнительная схема №1", 5.0))
    o.append(txt((xl + x0 + 185) / 2, y0 + 20.0,
                 "г. Санкт-Петербург, Полюстровский пр., д. 12", 3.4))

    xm = x0 + 143
    o.append(ln(xm, y0 + 25, xm, y0 + 55, 0.7))
    o.append(ln(xl, y0 + 40, xm, y0 + 40, 0.35))
    o.append(txt((xl + xm) / 2, y0 + 32.5, "Текущий ремонт шлагбаума", 3.4))
    o.append(txt((xl + xm) / 2, y0 + 37.2, "ГБУЗ ЛОКБ", 3.4))
    for i, s in enumerate(drawing_name):
        o.append(txt((xl + xm) / 2, y0 + 46.0 + i * 4.4, s, 3.0))

    o.append(ln(xm, y0 + 33, x0 + 185, y0 + 33, 0.35))
    o.append(ln(xm, y0 + 41, x0 + 185, y0 + 41, 0.35))
    for i in (1, 2):
        o.append(ln(xm + 14 * i, y0 + 25, xm + 14 * i, y0 + 41, 0.18))
    for i, (hname, v) in enumerate([("Стадия", "ИД"), ("Лист", str(sheet_no)),
                                    ("Листов", str(sheets))]):
        o.append(txt(xm + 7 + 14 * i, y0 + 30.5, hname, 2.6))
        o.append(txt(xm + 7 + 14 * i, y0 + 38.5, v, 3.2, weight="700"))
    o.append(txt(xm + 21, y0 + 47.5, "Подрядная организация:", 2.4))
    o.append(ln(xm + 3, y0 + 52.5, x0 + 182, y0 + 52.5, 0.18))
    return "".join(o)


def notes(lines, x=22.5, y=151.0, size=2.2, lead=3.1):
    o = [txt(x, y, "Примечания:", size + 0.3, anchor="start", weight="700")]
    for i, s in enumerate(lines):
        o.append(txt(x, y + lead * (i + 1), s, size, anchor="start"))
    return "".join(o)


DEFS = f'''<defs>
  <pattern id="pg" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="2.6" stroke="{INK}" stroke-width="0.14"/>
  </pattern>
  <pattern id="pa" width="1.4" height="1.4" patternUnits="userSpaceOnUse">
    <rect width="1.4" height="1.4" fill="#3f3f3f"/>
    <circle cx="0.35" cy="0.45" r="0.22" fill="#ffffff" opacity="0.5"/>
    <circle cx="1.0" cy="1.05" r="0.18" fill="#ffffff" opacity="0.4"/>
  </pattern>
  <pattern id="pn" width="1.4" height="1.4" patternUnits="userSpaceOnUse">
    <rect width="1.4" height="1.4" fill="#8e8e8e"/>
    <circle cx="0.35" cy="0.45" r="0.24" fill="#ffffff" opacity="0.85"/>
    <circle cx="1.0" cy="1.05" r="0.2" fill="#2a2a2a" opacity="0.8"/>
  </pattern>
  <pattern id="pk" width="2.6" height="2.6" patternUnits="userSpaceOnUse">
    <rect width="2.6" height="2.6" fill="#ffffff"/>
    <path d="M0.3 1.0 L1.0 0.4 L1.3 1.2 Z" fill="none" stroke="{INK}" stroke-width="0.15"/>
    <path d="M1.6 2.1 L2.3 1.6 L2.45 2.35 Z" fill="none" stroke="{INK}" stroke-width="0.15"/>
    <path d="M1.85 0.4 L2.4 0.85 L1.75 1.0 Z" fill="none" stroke="{INK}" stroke-width="0.15"/>
  </pattern>
  <pattern id="ps" width="1.8" height="1.8" patternUnits="userSpaceOnUse">
    <rect width="1.8" height="1.8" fill="#ffffff"/>
    <circle cx="0.45" cy="0.55" r="0.17" fill="{INK}"/>
    <circle cx="1.3" cy="1.3" r="0.17" fill="{INK}"/>
    <circle cx="1.35" cy="0.3" r="0.12" fill="{INK}"/>
  </pattern>
</defs>'''


# ------------------------------------------------------------------ лист 1
SX = 120.0                              # ось траншеи
TL, TR = SX - 12.5, SX + 12.5           # 250 мм в М 1:10
Y_0, Y_G, Y_S, Y_B = 62.0, 77.0, 102.0, 122.0
GL, GR, GB = 44.0, 196.0, 134.0


def sheet1():
    o = [DEFS, frame(), view_title(SX, "1—1", "М 1:10")]

    o.append(f'<rect x="{GL}" y="{Y_0}" width="{TL - GL:.2f}" height="15" fill="url(#pa)"/>')
    o.append(f'<rect x="{TR}" y="{Y_0}" width="{GR - TR:.2f}" height="15" fill="url(#pa)"/>')
    o.append(f'<rect x="{GL}" y="{Y_G}" width="{TL - GL:.2f}" height="{GB - Y_G:.2f}" fill="url(#pg)"/>')
    o.append(f'<rect x="{TR}" y="{Y_G}" width="{GR - TR:.2f}" height="{GB - Y_G:.2f}" fill="url(#pg)"/>')

    o.append(f'<rect x="{TL}" y="{Y_0}" width="25" height="15" fill="url(#pn)"/>')
    o.append(f'<rect x="{TL}" y="{Y_G}" width="25" height="25" fill="url(#pk)"/>')
    o.append(f'<rect x="{TL}" y="{Y_S}" width="25" height="20" fill="url(#ps)"/>')

    o.append(ln(GL, Y_0, GR, Y_0, 0.5))
    o.append(f'<path d="M{TL},{Y_0} L{TL},{Y_B} L{TR},{Y_B} L{TR},{Y_0}" fill="none" '
             f'stroke="{INK}" stroke-width="0.6"/>')
    for yy in (Y_G, Y_S):
        o.append(ln(TL, yy, TR, yy, 0.3))
    o.append(ln(GL, Y_G, TL, Y_G, 0.35))
    o.append(ln(TR, Y_G, GR, Y_G, 0.35))

    pts, x, k = [], GL, 0
    while x < GR:
        pts.append((x, GB + (1.3 if k % 2 else -1.3)))
        x += 7.6
        k += 1
    pts.append((GR, GB))
    o.append('<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) +
             f'" fill="none" stroke="{INK}" stroke-width="0.3"/>')

    for px in (SX - 5.0, SX + 5.0):     # трубы ПНД d32, 2 шт.
        o.append(f'<circle cx="{px}" cy="112" r="1.6" fill="#ffffff" stroke="{INK}" stroke-width="0.3"/>')
        o.append(f'<circle cx="{px}" cy="112" r="1.05" fill="none" stroke="{INK}" stroke-width="0.15"/>')

    o.append(dim_h(TL, TR, 52, "0,25", "0,60", ext_y=Y_0 - 1))
    o.append(dim_v(Y_0, Y_G, 206, "0,15", None, ext_x=TR))
    o.append(dim_v(Y_G, Y_S, 206, "0,25", "0,63", ext_x=TR))
    o.append(dim_v(Y_S, Y_B, 206, "0,20", "0,30", ext_x=TR))
    o.append(dim_v(Y_0, Y_B, 228, "0,60", "1,00", ext_x=TR))
    o.append(txt(232, 128, "H траншеи", 2.3, anchor="start"))

    o.append(elev(TL, Y_0, "0,000"))
    o.append(elev(TL, Y_G, "−0,150"))
    o.append(elev(TL, Y_S, "−0,400"))
    o.append(elev(TL, Y_B, "−0,600", "−1,000"))

    o.append(leader([(112, 69), (82, 31)], "Холодный асфальт, 0,15", side=-1))
    o.append(leader([(112, 89), (82, 38)], "Щебень фр. 5(3)–20, М600", side=-1))
    o.append(leader([(112, 112), (82, 45)], "Песок природный мелкий", side=-1))
    o.append(leader([(150, 69), (238, 31)], "Существующее а/б покрытие", side=1))
    o.append(leader([(176, 110), (238, 45)], "Существующий грунт основания", side=1))
    o.append(leader([(SX + 5, 113.6), (150, 143)], "Труба гофрированная ПНД d32, 2 шт.", side=1))

    o.append(notes([
        "1. Все размеры на схеме указаны в метрах, отметки условные.",
        "2. Красным показаны проектные значения по ВОР №1 от 10.07.2025,",
        "    чёрным — фактически выполненные.",
        "3. За отметку 0,000 принят верх существующего а/б покрытия проезда.",
        "4. Фактические слои 0,20+0,25+0,15 = 0,60 м равны глубине траншеи.",
        "    Проектные слои по ВОР 0,10+0,20+0,63 = 0,93 м проектной глубине",
        "    1,00 м не соответствуют.",
        "5. Обратная засыпка послойная с уплотнением, стенки траншеи",
        "    вертикальные, без крепления.",
        "6. Основание: ВОР №1 от 10.07.2025, ЛСР 02-01-01.",
        "7. Работы выполнены по СП 45.13330.2017 и СП 78.13330.2012.",
    ]))
    o.append(stamp(1, 2, ["Исполнительная схема траншеи", "под кабельную линию. Разрез 1—1"]))
    return "".join(o)


# ------------------------------------------------------------------ лист 2
def sheet2():
    o = [DEFS, frame(), view_title(156, "План траншеи", "М 1:100", half=17)]

    PL, PR, PY = 96.0, 216.0, 48.0       # 12 000 мм в М 1:100 = 120 мм
    o.append(f'<rect x="{PL - 26}" y="{PY - 10}" width="{PR - PL + 52}" height="22" '
             f'fill="url(#pa)" opacity="0.22"/>')
    o.append(f'<rect x="{PL}" y="{PY - 1.25}" width="{PR - PL}" height="2.5" fill="url(#pg)"/>')
    o.append(rect(PL, PY - 1.25, PR - PL, 2.5, sw=0.45))

    for cx in (PL, PR):
        o.append(rect(cx - 2.5, PY - 2.5, 5, 5, fill="#ffffff", sw=0.45))
        o.append(ln(cx - 2.5, PY - 2.5, cx + 2.5, PY + 2.5, 0.2))

    o.append(leader([(PL, PY - 3.0), (PL - 6, 33)], "Шлагбаум существующий,", side=-1))
    o.append(txt(PL - 6.7, 36.4, "фундамент 500×500×500 (поз. 1, 4, 21)", 2.3, anchor="end"))
    o.append(leader([(PR, PY - 3.0), (PR + 6, 33)], "Стойка фотоэлемента,", side=1))
    o.append(txt(PR + 6.7, 36.4, "фундамент Ф2 500×500×300 (поз. 14, 22)", 2.3, anchor="start"))

    xc = (PL + PR) / 2
    o.append(ln(xc, PY - 7, xc, PY + 7, 0.6))
    o.append(f'<path d="M{xc},{PY - 7} L{xc + 3.2},{PY - 6.1} L{xc},{PY - 5.2} Z" fill="{INK}"/>')
    o.append(f'<path d="M{xc},{PY + 7} L{xc + 3.2},{PY + 6.1} L{xc},{PY + 5.2} Z" fill="{INK}"/>')
    o.append(txt(xc - 2.4, PY - 7.4, "1", 3.2, anchor="end"))
    o.append(txt(xc - 2.4, PY + 11.2, "1", 3.2, anchor="end"))

    o.append(dim_h(PL, PR, 67, "12,00", "12,00", ext_y=PY + 2.5))

    # ширина траншеи текстом: план в М 1:100 не позволяет проставить её размером
    o.append(f'<text x="156" y="75" font-family="{FONT}" font-size="2.9" '
             f'text-anchor="middle" fill="{INK}" font-style="italic">'
             f'Ширина траншеи b (проект / факт): '
             f'<tspan fill="{RED}" text-decoration="underline">0,60</tspan> / '
             f'<tspan>0,25</tspan> м</text>')

    # ------------------------------------------------ ведомость объёмов
    TX, TY = 22.5, 86.0
    cols = [(10, "№"), (100, "Наименование"), (14, "Ед."), (28, "По ВОР"),
            (28, "Факт"), (28, "Отклонение"), (61, "Расчёт фактического объёма")]
    rows = [
        ("1", "Разработка траншеи (0,25×0,60 против 0,60×1,00)", "м³", "7,20", "1,80", "−5,40", "0,25×0,60×12,00"),
        ("1.1", "Грунт для утилизации, ρ = 1,4 т/м³", "м³/т", "7,20/10,08", "1,80/2,52", "−5,40/−7,56", "1,80×1,4"),
        ("2", "Песок: подсыпка и засыпка с трамбовкой", "м³", "2,16", "0,60", "−1,56", "0,25×0,20×12,00"),
        ("3", "Щебень: засыпка с трамбовкой", "м³", "4,54", "0,75", "−3,79", "0,25×0,25×12,00"),
        ("4", "Восстановление покрытия холодным асфальтом", "м²", "7,20", "3,00", "−4,20", "0,25×12,00"),
        ("4.1", "То же, объём асфальтобетонной смеси", "м³", "—", "0,45", "—", "3,00×0,15"),
        ("5", "Труба гофрированная ПНД d32 (основная и резервная)", "м", "12,00", "12,00", "0,00", "по поз. 16 ВОР"),
    ]
    rh, hh = 6.4, 7.4
    tot = sum(c[0] for c in cols)
    o.append(txt(TX, TY - 3.2, "Ведомость фактически выполненных объёмов", 3.4,
                 anchor="start", weight="700"))
    o.append(rect(TX, TY, tot, hh + rh * len(rows), sw=0.5))
    o.append(ln(TX, TY + hh, TX + tot, TY + hh, 0.5))
    cx = TX
    for wd, hname in cols:
        if cx > TX:
            o.append(ln(cx, TY, cx, TY + hh + rh * len(rows), 0.18))
        o.append(txt(cx + wd / 2, TY + 5.0, hname, 2.6, weight="700"))
        cx += wd
    for i, r in enumerate(rows):
        yy = TY + hh + rh * i
        if i:
            o.append(ln(TX, yy, TX + tot, yy, 0.18))
        cx = TX
        for j, wd in enumerate([c[0] for c in cols]):
            if j == 1:
                o.append(txt(cx + 1.5, yy + 4.3, r[j], 2.6, anchor="start"))
            else:
                o.append(txt(cx + wd / 2, yy + 4.3, r[j], 2.6,
                             fill=RED if j == 3 else INK))
            cx += wd
    o.append(txt(TX, TY + hh + rh * len(rows) + 5.2,
                 "Итого объём выемки траншеи 1,80 м³ при B = 0,25 м, H = 0,60 м, L = 12,00 м.",
                 2.9, anchor="start", weight="700"))

    o.append(notes([
        "1. Значения графы «По ВОР» — проектные, выделены красным цветом.",
        "2. Фактические объёмы приняты по обмерам траншеи, приведённым",
        "    на листе 1 (разрез 1—1).",
        "3. Объёмы земляных работ, песка, щебня и восстановления покрытия",
        "    подлежат корректировке в акте КС-2 и локальном сметном расчёте",
        "    02-01-01 по фактическим значениям настоящей схемы.",
    ]))
    o.append(stamp(2, 2, ["Исполнительная схема траншеи", "План трассы. Ведомость объёмов"]))
    return "".join(o)


# ------------------------------------------------------------------ страница
HTML = '''<title>Чертёж траншеи Полюстровский 12</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:ital,wght@0,400;0,700;1,400;1,700&display=swap">
<style>
:root{--desk:#E8E6E0;--edge:#B7B3A8;--label:#5A5A5A}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--desk:#13161A;--edge:#000;--label:#8B939A}}
:root[data-theme="dark"]{--desk:#13161A;--edge:#000;--label:#8B939A}
*{box-sizing:border-box}
body{margin:0;background:var(--desk);font-family:'Roboto Condensed',Arial,sans-serif}
.deck{display:flex;flex-direction:column;align-items:center;gap:10mm;padding:9mm 5mm}
figure{margin:0;display:flex;flex-direction:column;align-items:center;gap:2.5mm;width:100%}
figcaption{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--label)}
.sheet{background:#fff;box-shadow:0 2px 14px rgba(0,0,0,.26);border:1px solid var(--edge);width:297mm;max-width:100%}
.sheet svg{display:block;width:100%;height:auto}
@media print{
  @page{size:A4 landscape;margin:0}
  body{background:#fff}
  .deck{display:block;padding:0;gap:0}
  figcaption{display:none}
  figure{display:block}
  .sheet{width:297mm;height:210mm;border:none;box-shadow:none;break-after:page;page-break-after:always}
  .sheet:last-child{break-after:auto;page-break-after:auto}
}
</style>
<div class="deck">
@@FIGS@@
</div>'''

FIG = '''<figure>
  <figcaption>@@CAP@@</figcaption>
  <div class="sheet"><svg viewBox="0 0 297 210" role="img" aria-label="@@ALT@@">@@BODY@@</svg></div>
</figure>'''


def fig(cap, alt, body):
    return FIG.replace("@@CAP@@", cap).replace("@@ALT@@", alt).replace("@@BODY@@", body)


def main():
    figs = [fig("Лист 1 — Разрез 1—1", "Лист 1: разрез 1-1 траншеи", sheet1()),
            fig("Лист 2 — План трассы и ведомость объёмов",
                "Лист 2: план трассы и ведомость объёмов", sheet2())]
    io.open("shema-gost-a4.html", "w", encoding="utf-8").write(
        HTML.replace("@@FIGS@@", "\n".join(figs)))
    print("ok")


if __name__ == "__main__":
    main()
