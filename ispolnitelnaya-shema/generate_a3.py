# -*- coding: utf-8 -*-
"""Исполнительная схема №1 — лист А3 альбомный по образцу КОМПАС-чертежа заказчика.

Композиция повторяет исходный лист: продольный разрез дорожной одежды по трассе,
разрез А—А, основная надпись по ГОСТ 2.104 форма 1, графы подшивки слева.
Геометрия задана в миллиметрах листа (viewBox 420x297) — масштабы видов
сохраняются при печати без подгонки.
"""

import io

INK = "#000000"
RED = "#C00000"
FONT = "'Roboto Condensed','PT Sans Narrow',Arial,sans-serif"

W, H = 420.0, 297.0
FR = (20.0, 5.0, 415.0, 292.0)                     # рамка: лево, верх, право, низ
ST_W, ST_H = 185.0, 55.0
ST_X, ST_Y = FR[2] - ST_W, FR[3] - ST_H            # основная надпись


# ---------------------------------------------------------------- примитивы
def ln(x1, y1, x2, y2, w=0.2, c=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{c}" stroke-width="{w}"{d}/>')


def rect(x, y, w_, h_, fill="none", sw=0.2, c=INK):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w_:.2f}" height="{h_:.2f}" '
            f'fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')


def txt(x, y, s, size=3.0, anchor="middle", fill=INK, weight="400", rot=None):
    tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{fill}" font-weight="{weight}" '
            f'font-style="italic"{tr}>{s}</text>')


def tw(s, size):
    return len(s) * size * 0.47


def arrow(x, y, ux, uy, L=2.8, half=0.85, c=INK):
    """закрашенная стрелка: остриё в (x, y), направлена по (ux, uy)"""
    bx, by = x - ux * L, y - uy * L
    px, py = -uy * half, ux * half
    return (f'<path d="M{x:.2f},{y:.2f} L{bx + px:.2f},{by + py:.2f} '
            f'L{bx - px:.2f},{by - py:.2f} Z" fill="{c}"/>')


def dim_h(x1, x2, y, text, ext_y=None, size=3.0, over=1.2):
    o = []
    if ext_y is not None:
        o.append(ln(x1, ext_y, x1, y + 1.5 * (1 if ext_y > y else -1), 0.15))
        o.append(ln(x2, ext_y, x2, y + 1.5 * (1 if ext_y > y else -1), 0.15))
    o.append(ln(x1, y, x2, y, 0.2))
    o += [arrow(x1, y, -1, 0), arrow(x2, y, 1, 0)]
    o.append(txt((x1 + x2) / 2, y - over, text, size))
    return "".join(o)


def dim_v(y1, y2, x, text, ext_x=None, size=3.0, side=1, alen=2.8):
    o = []
    if ext_x is not None:
        o.append(ln(ext_x, y1, x + 1.5 * (1 if ext_x < x else -1), y1, 0.15))
        o.append(ln(ext_x, y2, x + 1.5 * (1 if ext_x < x else -1), y2, 0.15))
    o.append(ln(x, y1, x, y2, 0.2))
    o += [arrow(x, y1, 0, -1, L=alen, half=alen * 0.3),
          arrow(x, y2, 0, 1, L=alen, half=alen * 0.3)]
    an = "start" if side > 0 else "end"
    o.append(txt(x + 1.4 * side, (y1 + y2) / 2 + 1.1, text, size, anchor=an))
    return "".join(o)


def leader(pts, text, size=3.0, side=1):
    """выноска: ломаная + полка + надпись над полкой"""
    o = ['<polyline points="' + " ".join(f"{a:.2f},{b:.2f}" for a, b in pts) +
         f'" fill="none" stroke="{INK}" stroke-width="0.2"/>']
    ex, ey = pts[-1]
    sh = tw(text, size) + 2.0
    xs = ex + sh * side
    o.append(ln(ex, ey, xs, ey, 0.2))
    o.append(txt(min(ex, xs) + 1.0, ey - 1.3, text, size, anchor="start"))
    return "".join(o)


DEFS = f'''<defs>
  <pattern id="asf" width="3.0" height="3.0" patternUnits="userSpaceOnUse">
    <rect width="3.0" height="3.0" fill="#ffffff"/>
    <path d="M0,3 L3,0 M-0.75,0.75 L0.75,-0.75 M2.25,3.75 L3.75,2.25" stroke="{INK}" stroke-width="0.16"/>
    <path d="M0,0 L3,3 M-0.75,2.25 L0.75,3.75 M2.25,-0.75 L3.75,0.75" stroke="{INK}" stroke-width="0.16"/>
  </pattern>
  <pattern id="shb" width="3.2" height="3.2" patternUnits="userSpaceOnUse">
    <rect width="3.2" height="3.2" fill="#ffffff"/>
    <path d="M0,3.2 L3.2,0 M-0.8,0.8 L0.8,-0.8 M2.4,4.0 L4.0,2.4" stroke="{INK}" stroke-width="0.16"/>
    <path d="M1.1 1.9 L1.9 1.2 L2.1 2.1 Z" fill="none" stroke="{INK}" stroke-width="0.14"/>
  </pattern>
  <pattern id="pes" width="2.6" height="2.6" patternUnits="userSpaceOnUse">
    <rect width="2.6" height="2.6" fill="#ffffff"/>
    <circle cx="0.6" cy="0.7" r="0.17" fill="{INK}"/>
    <circle cx="1.9" cy="1.9" r="0.17" fill="{INK}"/>
    <circle cx="2.0" cy="0.4" r="0.13" fill="{INK}"/>
    <path d="M0.3 2.2 L0.8 1.7 L1.0 2.3 Z" fill="none" stroke="{INK}" stroke-width="0.13"/>
  </pattern>
  <pattern id="gr" width="2.2" height="2.2" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
    <rect width="2.2" height="2.2" fill="#ffffff"/>
    <line x1="0" y1="0" x2="0" y2="2.2" stroke="#000000" stroke-width="0.15"/>
  </pattern>
  <pattern id="bet" width="4.0" height="4.0" patternUnits="userSpaceOnUse">
    <rect width="4.0" height="4.0" fill="#ffffff"/>
    <path d="M0,4 L4,0 M-1,1 L1,-1 M3,5 L5,3" stroke="{INK}" stroke-width="0.15"/>
    <circle cx="2.6" cy="1.2" r="0.3" fill="none" stroke="{INK}" stroke-width="0.15"/>
    <path d="M0.7 3.1 L1.5 2.5 L1.8 3.4 Z" fill="none" stroke="{INK}" stroke-width="0.15"/>
  </pattern>
</defs>'''


# ---------------------------------------------------------------- рамка и графы
def frame():
    o = [rect(0, 0, W, H, fill="#FFFFFF", sw=0),
         rect(FR[0], FR[1], FR[2] - FR[0], FR[3] - FR[1], sw=0.8)]
    # графы 19–23 ГОСТ 2.104 в поле подшивки
    x0, x1 = 8.0, 20.0
    cells = [("Инв. № подл.", 25), ("Подп. и дата", 35), ("Взам. инв. №", 25),
             ("Инв. № дубл.", 25), ("Подп. и дата", 35)]
    y = FR[3]
    o.append(ln(x0, FR[3], x0, FR[3] - sum(c[1] for c in cells), 0.5))
    for name, h in cells:
        o.append(ln(x0, y, x1, y, 0.5))
        o.append(txt((x0 + x1) / 2 + 1.0, y - h / 2, name, 2.6, rot=-90))
        y -= h
    o.append(ln(x0, y, x1, y, 0.5))
    return "".join(o)


def stamp():
    x0, y0 = ST_X, ST_Y
    o = [rect(x0, y0, ST_W, ST_H, sw=0.8)]

    # ---- таблица изменений, 65 мм
    cols = [7, 9, 9, 15, 13, 12]
    xs, cx = [x0], x0
    for c in cols:
        cx += c
        xs.append(cx)
    xl = xs[-1]
    o.append(ln(xl, y0, xl, y0 + ST_H, 0.8))
    for i in range(1, 11):
        o.append(ln(x0, y0 + 5 * i, xl, y0 + 5 * i, 0.2 if i not in (5, 6) else 0.4))
    for x in xs[1:-1]:
        o.append(ln(x, y0, x, y0 + ST_H, 0.2))
    for i, hname in enumerate(["Изм.", "Колич.", "Лист", "№докум.", "Подп.", "Дата"]):
        o.append(txt((xs[i] + xs[i + 1]) / 2, y0 + 29.0, hname, 2.5))

    # ---- наименование документа
    o.append(ln(xl, y0 + 16, x0 + ST_W, y0 + 16, 0.8))
    o.append(txt((xl + x0 + ST_W) / 2, y0 + 11.0, "Исполнительная схема №1", 6.2))

    # ---- наименование объекта и правые графы
    xr = x0 + 135                                    # 365
    o.append(ln(xr, y0 + 16, xr, y0 + ST_H, 0.8))
    o.append(txt((xl + xr) / 2, y0 + 30.0, "Текущий ремонт шлагбаума", 4.2))
    o.append(txt((xl + xr) / 2, y0 + 36.5, "ГБУЗ ЛОКБ", 4.6))

    cw = (x0 + ST_W - xr) / 3.0
    for yy, wd in ((21, 0.3), (34, 0.4), (40, 0.3)):
        o.append(ln(xr, y0 + yy, x0 + ST_W, y0 + yy, wd))
    for i in (1, 2):
        o.append(ln(xr + cw * i, y0 + 16, xr + cw * i, y0 + ST_H, 0.2))
    for i, (hname, v) in enumerate([("Стадия", "ИД"), ("Масса", "—"), ("Масштаб", "1:50")]):
        o.append(txt(xr + cw * (i + 0.5), y0 + 20.0, hname, 2.4))
        o.append(txt(xr + cw * (i + 0.5), y0 + 28.5, v, 3.6))
    o.append(txt(xr + cw * 2.5, y0 + 32.6, "(А—А 1:10)", 2.3))
    for i, (hname, v) in enumerate([("Лист", "1"), ("Листов", "1"), ("Формат", "А3")]):
        o.append(txt(xr + cw * (i + 0.5), y0 + 38.8, hname, 2.4))
        o.append(txt(xr + cw * (i + 0.5), y0 + 49.0, v, 3.6))
    return "".join(o)


# ---------------------------------------------------------------- главный вид
VX1, VX2 = 55.0, 295.0            # 12 000 мм, М гор. 1:50
Y0 = 90.0                         # верх асфальта
Y_A, Y_S, Y_B = 97.5, 110.0, 120.0    # низ асфальта / щебня / песка, М верт. 1:20
Y_PIPE = 115.0                    # ось стального футляра — 0,50 м от уровня асфальта

# фундамент шлагбаума (М гор. 1:50, верт. 1:20)
PIT_L, PIT_R, PIT_B = 41.5, 68.5, 120.0        # общая глубина 0,60 м — как у траншеи
BET_B = 105.0                                  # бетон В25 П3, 0,30 м
PEN_B = 107.0                                  # утеплитель пеноплэкс, 0,04 м
SHB_B = 114.5                                  # щебень, 0,15 м; ниже песок 0,11 м


def main_view():
    o = [txt(175, 24, "Продольный разрез по трассе", 5.2, weight="700"),
         txt(175, 31, "М гор. 1:50, верт. 1:20", 3.6),
         ln(146, 33.2, 204, 33.2, 0.4)]

    o.append(f'<rect x="{VX1}" y="{Y0}" width="{VX2 - VX1}" height="{Y_A - Y0}" fill="url(#asf)"/>')
    o.append(f'<rect x="{VX1}" y="{Y_A}" width="{VX2 - VX1}" height="{Y_S - Y_A}" fill="url(#shb)"/>')
    o.append(f'<rect x="{VX1}" y="{Y_S}" width="{VX2 - VX1}" height="{Y_B - Y_S}" fill="url(#pes)"/>')
    o.append(rect(VX1, Y0, VX2 - VX1, Y_B - Y0, sw=0.5))
    o.append(ln(VX1, Y_A, VX2, Y_A, 0.3))
    o.append(ln(VX1, Y_S, VX2, Y_S, 0.3))

    # стальной футляр 76x3,5 по трассе
    o.append(ln(PIT_R + 1, Y_PIPE - 1.9, VX2 - 2, Y_PIPE - 1.9, 0.4))
    o.append(ln(PIT_R + 1, Y_PIPE + 1.9, VX2 - 2, Y_PIPE + 1.9, 0.4))
    o.append(ln(PIT_R + 1, Y_PIPE, VX2 - 2, Y_PIPE, 0.18, dash="7 1.6 1 1.6"))

    # фундамент шлагбаума: котлован, обратная засыпка, щебень, пеноплекс, бетон
    w = PIT_R - PIT_L
    o.append(rect(PIT_L, Y0, w, PIT_B - Y0, fill="#ffffff", sw=0))
    o.append(f'<rect x="{PIT_L}" y="{Y0}" width="{w}" height="{BET_B - Y0:.2f}" fill="url(#bet)"/>')
    o.append(rect(PIT_L, BET_B, w, PEN_B - BET_B, fill="#d0d0d0", sw=0))
    o.append(f'<rect x="{PIT_L}" y="{PEN_B}" width="{w}" height="{SHB_B - PEN_B:.2f}" fill="url(#shb)"/>')
    o.append(f'<rect x="{PIT_L}" y="{SHB_B}" width="{w}" height="{PIT_B - SHB_B:.2f}" fill="url(#pes)"/>')
    for yy in (BET_B, PEN_B, SHB_B):
        o.append(ln(PIT_L, yy, PIT_R, yy, 0.3))
    o.append(rect(PIT_L, Y0, w, PIT_B - Y0, sw=0.6))

    # шлагбаум: стойка и стрела
    o.append(rect(53.6, 68, 2.8, Y0 - 68, fill="#ffffff", sw=0.5))
    o.append(ln(56.4, 71.5, 165, 71.5, 0.5))
    o.append(ln(56.4, 74.0, 165, 74.0, 0.5))
    o.append(ln(165, 71.5, 165, 74.0, 0.5))
    o.append(txt(55, 64, "Шлагбаум", 3.0))

    # фундамент Ф2 и стойка фотоэлемента
    fx = VX2
    o.append(f'<path d="M{fx - 6},{Y0} L{fx - 4},{Y0 - 6} L{fx + 4},{Y0 - 6} L{fx + 6},{Y0} Z" '
             f'fill="url(#bet)" stroke="{INK}" stroke-width="0.5"/>')
    o.append(rect(fx - 0.9, Y0 - 22, 1.8, 16, fill="#ffffff", sw=0.5))
    o.append(leader([(fx + 4, Y0 - 5), (317, 68)], "Фундамент Ф2, стойка фотоэлемента", 3.0))

    o.append(dim_h(VX1, VX2, 52, "12 м", ext_y=Y0 - 2, size=4.0, over=1.6))

    o.append(rect(219.0, 98.0, 12.0, 5.0, fill="#FFFFFF", sw=0))
    o.append(dim_v(Y0, Y_PIPE, 232, "0,50м", ext_x=None, size=3.0, side=-1))
    o.append(leader([(250, Y_PIPE + 1.9), (285, 60)],
                    "Стальной футляр 76×3,5 с трубами ПНД d32, 2 шт.", 3.0))

    o.append(dim_v(Y0, BET_B, 38, "0,30м", ext_x=PIT_L, size=2.8, side=-1, alen=1.8))
    o.append(dim_v(BET_B, PEN_B, 38, "0,04м", ext_x=PIT_L, size=2.8, side=-1, alen=0.7))
    o.append(dim_v(PEN_B, SHB_B, 38, "0,15м", ext_x=PIT_L, size=2.8, side=-1, alen=1.6))
    o.append(dim_v(SHB_B, PIT_B, 38, "0,11*м", ext_x=PIT_L, size=2.8, side=-1, alen=1.4))
    o.append(dim_v(Y0, PIT_B, 30, "0,60м", ext_x=PIT_L, size=2.5, side=-1, alen=2.2))
    o.append(leader([(52, 98), (80, 145)],
                    "Фундамент шлагбаума, бетон В25 П3, V = 0,329 м³, глубина 0,30 м", 2.9))
    o.append(leader([(64, 117), (80, 152)],
                    "Утеплитель пеноплэкс 40 мм, щебень 0,15 м, песок — до общей глубины 0,60 м", 2.9))

    for y in (Y0, Y_A, Y_S, Y_B):
        o.append(ln(VX2 + 8, y, 405, y, 0.15))
    for (ya, yb, sname) in ((Y0, Y_A, "0,15 м — Асфальт"),
                            (Y_A, Y_S, "0,25 м — Щебень"),
                            (Y_S, Y_B, "0,20 м — Песок")):
        o.append(ln(340, ya, 340, yb, 0.2))
        o += [arrow(340, ya, 0, -1), arrow(340, yb, 0, 1)]
        o.append(txt(344, (ya + yb) / 2 + 1.1, sname, 3.0, anchor="start"))

    xc = 180.0
    for yy, uy in ((82.0, -1), (128.0, 1)):
        dy = -6 if uy < 0 else 6
        o.append(ln(xc, yy, xc, yy + dy, 0.8))
        o.append(ln(xc, yy + dy, xc + 5, yy + dy, 0.8))
        o.append(arrow(xc + 5, yy + dy, 1, 0, L=3.0, half=1.0))
        o.append(txt(xc - 2.6, yy + (-6.5 if uy < 0 else 8.5), "А", 5.0, anchor="end"))
    return "".join(o)


def section_aa():
    cx, sy = 120.0, 182.0                    # ось траншеи, верх асфальта, М 1:10
    tl, tr = cx - 12.5, cx + 12.5            # 0,25 м
    ya, ys, yb = sy + 15, sy + 40, sy + 60   # 0,15 / 0,25 / 0,20
    yp = sy + 50                             # ось футляра, 0,50 м

    o = [txt(cx, 158, "А—А", 6.0, weight="700"),
         txt(cx, 165, "М 1:10", 3.6),
         ln(cx - 14, 167.0, cx + 14, 167.0, 0.4)]

    for x1, x2 in ((70.0, tl), (tr, 170.0)):
        o.append(f'<rect x="{x1}" y="{sy}" width="{x2 - x1:.2f}" height="15" fill="url(#asf)"/>')
        o.append(rect(x1, sy, x2 - x1, 15, sw=0.5))

    o.append(f'<rect x="{tl}" y="{sy}" width="25" height="15" fill="url(#asf)"/>')
    o.append(f'<rect x="{tl}" y="{ya}" width="25" height="25" fill="url(#shb)"/>')
    o.append(f'<rect x="{tl}" y="{ys}" width="25" height="20" fill="url(#pes)"/>')
    o.append(rect(tl, sy, 25, 60, sw=0.6))
    o.append(ln(tl, ya, tr, ya, 0.3))
    o.append(ln(tl, ys, tr, ys, 0.3))

    # стальной футляр d72 с двумя трубами ПНД d32
    o.append(f'<circle cx="{cx}" cy="{yp}" r="3.8" fill="#ffffff" stroke="{INK}" stroke-width="0.4"/>')
    o.append(f'<circle cx="{cx}" cy="{yp}" r="3.45" fill="none" stroke="{INK}" stroke-width="0.2"/>')
    for dx in (-1.6, 1.6):
        o.append(f'<circle cx="{cx + dx}" cy="{yp}" r="1.6" fill="none" stroke="{INK}" stroke-width="0.25"/>')

    # обозначение узла
    o.append(f'<circle cx="{cx}" cy="{yp}" r="6.2" fill="none" stroke="{INK}" '
             f'stroke-width="0.2" stroke-dasharray="2.5 1.2"/>')
    o.append(ln(cx + 4.4, yp - 4.4, 141, 214, 0.2))
    o.append(ln(141, 214, 146, 214, 0.2))
    o.append(txt(143.5, 212.6, "1", 3.6, anchor="middle"))

    o.append(dim_h(tl, tr, sy - 6, "0,25м", ext_y=sy - 1, size=3.4, over=1.4))
    o.append(dim_v(sy, yp, 151, "0,50м", ext_x=tr, size=3.2))
    o.append(dim_v(sy, yb, 167, "0,60м", ext_x=tr, size=3.4))
    o.append(txt(70, sy - 3, "Существующее а/б покрытие", 2.8, anchor="start"))
    return "".join(o)


def detail_node():
    """Узел 1 — стальной футляр d72 с трубами ПНД d32, М 1:2"""
    cx, cy = 45.0, 215.0
    o = [txt(cx, 186, "Узел 1", 5.2, weight="700"),
         txt(cx, 192, "М 1:2", 3.4),
         ln(cx - 12, 193.6, cx + 12, 193.6, 0.4)]
    o.append(f'<circle cx="{cx}" cy="{cy}" r="19" fill="#ffffff" stroke="{INK}" stroke-width="0.6"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="17.25" fill="none" stroke="{INK}" stroke-width="0.35"/>')
    for dx in (-8.0, 8.0):
        o.append(f'<circle cx="{cx + dx}" cy="{cy}" r="8" fill="none" stroke="{INK}" stroke-width="0.4"/>')
        o.append(f'<circle cx="{cx + dx}" cy="{cy}" r="6.6" fill="none" stroke="{INK}" stroke-width="0.2"/>')
    o.append(ln(cx - 23, cy, cx + 23, cy, 0.15, dash="6 1.5 1 1.5"))
    o.append(ln(cx, cy - 23, cx, cy + 23, 0.15, dash="6 1.5 1 1.5"))
    o.append(leader([(cx + 13.4, cy + 13.4), (66, 240)], "Труба стальная 76×3,5 — футляр", 2.8))
    o.append(leader([(cx + 8, cy + 6.6), (60, 249)], "Труба гофрированная ПНД d32, 2 шт.", 2.8))
    return "".join(o)


# ---------------------------------------------------------------- ведомость
def table():
    TX, TY = 192.0, 150.0
    cols = [(8, "№"), (68, "Наименование"), (12, "Ед."), (24, "По ВОР"),
            (22, "Факт"), (26, "Отклонение"), (58, "Расчёт факта")]
    rows = [
        ("1", "Разработка траншеи (0,25×0,60 против 0,60×1,00)", "м³", "7,20", "1,80", "−5,40", "0,25×0,60×12,00"),
        ("1.1", "Грунт для утилизации, ρ = 1,4 т/м³", "м³/т", "7,20/10,08", "1,80/2,52", "−5,40/−7,56", "1,80×1,4"),
        ("2", "Песок: подсыпка и засыпка с трамбовкой", "м³", "2,16", "0,60", "−1,56", "0,25×0,20×12,00"),
        ("3", "Щебень: засыпка с трамбовкой", "м³", "4,54", "0,75", "−3,79", "0,25×0,25×12,00"),
        ("4", "Восстановление покрытия холодным асфальтом", "м²", "7,20", "3,00", "−4,20", "0,25×12,00"),
        ("4.1", "То же, объём асфальтобетонной смеси", "м³", "—", "0,45", "—", "3,00×0,15"),
        ("5", "Труба гофрированная ПНД d32, 2 шт. (в футляре)", "м", "12,00", "12,00", "0,00", "по поз. 16 ВОР"),
        ("6", "Труба стальная 76×3,5 — футляр", "м", "15,00", "12,00", "−3,00", "по длине траншеи"),
        ("7", "Выемка грунта под фундамент шлагбаума", "м³", "1,00", "1,00", "0,00", "по поз. 10 ВОР"),
        ("8", "Щебёночная подготовка под фундамент, слой 150 мм", "м³", "0,15", "0,15", "0,00", "по поз. 11 ВОР"),
        ("9", "Засыпка вокруг фундамента", "м³", "0,60", "0,60", "0,00", "по поз. 12 ВОР"),
        ("10", "Бетонирование фундамента, бетон В25 П3", "м³", "0,329", "0,329", "0,00", "по поз. 13 ВОР"),
        ("11", "Утеплитель Пеноплэкс 40×585×1185 под фундамент", "шт", "1,00", "1,00", "0,00", "по поз. 15 ВОР"),
    ]
    rh, hh = 5.3, 6.2
    tot = sum(c[0] for c in cols)
    o = [txt(TX, TY - 2.6, "Ведомость фактически выполненных объёмов", 3.8,
             anchor="start", weight="700")]
    o.append(rect(TX, TY, tot, hh + rh * len(rows), sw=0.5))
    o.append(ln(TX, TY + hh, TX + tot, TY + hh, 0.5))
    cx = TX
    for wd, hname in cols:
        if cx > TX:
            o.append(ln(cx, TY, cx, TY + hh + rh * len(rows), 0.2))
        o.append(txt(cx + wd / 2, TY + 4.4, hname, 2.4, weight="700"))
        cx += wd
    for i, r in enumerate(rows):
        yy = TY + hh + rh * i
        if i:
            o.append(ln(TX, yy, TX + tot, yy, 0.2))
        cx = TX
        for j, wd in enumerate([c[0] for c in cols]):
            if j == 1:
                o.append(txt(cx + 1.4, yy + 3.7, r[j], 2.4, anchor="start"))
            else:
                o.append(txt(cx + wd / 2, yy + 3.7, r[j], 2.4, fill=RED if j == 3 else INK))
            cx += wd
    o.append(txt(TX, TY + hh + rh * len(rows) + 4.4,
                 "Графа «По ВОР» — проектные значения по Ведомости объёмов работ №1 от 10.07.2025, показаны красным.",
                 2.6, anchor="start"))
    return "".join(o)


NOTES = [
    "1. Размеры на схеме указаны в метрах. Толщины слоёв и глубины даны от верха асфальтобетонного покрытия проезда.",
    "2. Фактические параметры траншеи: ширина 0,25 м, глубина 0,60 м, длина 12,00 м; конструкция 0,20 песка + 0,25 щебня + 0,15 асфальта = 0,60 м.",
    "3. В траншее на всю длину 12,00 м уложена стальная труба-футляр 76×3,5, в которой проложены две гофрированные трубы ПНД d32 (см. узел 1).",
    "4. Ось футляра — на отметке 0,50 м от верха покрытия, в песчаном слое; при иных данных исполнительной съёмки значение уточнить.",
    "5. Фундамент шлагбаума выполнен на общую глубину 0,60 м — как у траншеи. Состав снизу вверх: песок 0,11* м, щебень 0,15 м,",
    "    утеплитель (пеноплэкс) 0,04 м, монолитный бетон В25 П3 0,30 м объёмом 0,329 м³ (поз. 10—13, 15 ВОР).",
    "6. * Толщина песчаного слоя принята как остаток до общей глубины: 0,60 − 0,30 − 0,04 − 0,15 = 0,11 м; при иных обмерах уточнить.",
    "7. По ВОР №1 от 10.07.2025 предусматривались траншея 0,60×1,00 м и 15,00 м трубы 76×3,5; фактические объёмы приведены в ведомости",
    "    и подлежат учёту в акте КС-2 и локальном сметном расчёте 02-01-01.",
    "8. Обратная засыпка выполнена послойно с уплотнением. Стенки траншеи вертикальные, без крепления.",
    "9. Основание: ВОР №1 от 10.07.2025, ЛСР 02-01-01. Работы выполнены по СП 45.13330.2017 и СП 78.13330.2012.",
]


def notes():
    o = [txt(22.5, 254.0, "Примечания:", 3.0, anchor="start", weight="700")]
    for i, s in enumerate(NOTES):
        o.append(txt(22.5, 258.2 + 3.3 * i, s, 2.5, anchor="start"))
    return "".join(o)


# ---------------------------------------------------------------- страница
HTML = '''<title>Исполнительная схема №1 — А3</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:ital,wght@0,400;0,700;1,400;1,700&display=swap">
<style>
:root{--desk:#E8E6E0;--edge:#B7B3A8;--label:#5A5A5A}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--desk:#13161A;--edge:#000;--label:#8B939A}}
:root[data-theme="dark"]{--desk:#13161A;--edge:#000;--label:#8B939A}
*{box-sizing:border-box}
body{margin:0;background:var(--desk);font-family:'Roboto Condensed',Arial,sans-serif}
.deck{display:flex;flex-direction:column;align-items:center;gap:4mm;padding:8mm 4mm}
figcaption{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--label)}
.sheet{background:#fff;box-shadow:0 2px 14px rgba(0,0,0,.26);border:1px solid var(--edge);width:420mm;max-width:100%}
.sheet svg{display:block;width:100%;height:auto}
@media print{
  @page{size:A3 landscape;margin:0}
  body{background:#fff}
  .deck{display:block;padding:0}
  figcaption{display:none}
  .sheet{width:420mm;height:297mm;border:none;box-shadow:none}
}
</style>
<div class="deck">
  <figcaption>Исполнительная схема №1 — лист А3</figcaption>
  <div class="sheet"><svg viewBox="0 0 420 297" role="img"
    aria-label="Исполнительная схема №1: продольный разрез по трассе, разрез А-А, ведомость объёмов">@@BODY@@</svg></div>
</div>'''


def main():
    body = "".join([DEFS, frame(), main_view(), section_aa(), detail_node(),
                    table(), notes(), stamp()])
    io.open("shema-a3-ispolnitelnaya.html", "w", encoding="utf-8").write(
        HTML.replace("@@BODY@@", body))
    print("ok")


if __name__ == "__main__":
    main()
