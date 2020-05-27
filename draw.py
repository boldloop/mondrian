#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# draw.py


from mondrian import gen_lines
from random import random, choice
import drawBot


def tup_pairs_from_lines(x_lines, y_lines, mult=1):
    x_pairs = [((v[0]*mult, c*mult), (v[1]*mult, c*mult)) for c, v in x_lines]
    y_pairs = [((c*mult, v[0]*mult), (c*mult, v[1]*mult)) for c, v in y_lines]
    return x_pairs + y_pairs


def draw_lines(x_lines, y_lines, mult):
    tup_pairs = tup_pairs_from_lines(x_lines, y_lines, mult)
    drawBot.stroke(0)
    drawBot.strokeWidth(3)
    for pair in tup_pairs:
        drawBot.line(*pair)


def draw_rect(x0, xf, y0, yf, mult):
    white_chance = .65
    if random() < white_chance:
        drawBot.fill(1)
        color = 'white'
    else:
        colors = ['red', 'yellow', 'blue']
        rgb_from_color = {'red': (1, 0, 0),
                          'yellow': (1, 1, 0),
                          'blue': (0, 0, 1)}
        color = choice(colors)
        drawBot.fill(*rgb_from_color[color])

    print(color, 'from', f'x: {x0} --> {xf}', f'y: {y0} --> {yf}')
    drawBot.rect(x0*mult, y0*mult, (xf - x0)*mult, (yf - y0)*mult)


def extend(c, v, lines, limit):
    lines_with_v = [line for line in lines if line[1][0] <= v <= line[1][1]]
    i = 0
    while True:
        if any([line[0] == c+i for line in lines_with_v]) or c+i == limit:
            cf = c+i
            break
        i += 1
    i = 0
    while True:
        if any([line[0] == c-i for line in lines_with_v]) or c-i == 0:
            c0 = c-i
            break
        i += 1
    return c0, cf


def draw_colors(x_lines, y_lines, width, height, mult):
    coord_pairs = [(x, y) for x in range(width) for y in range(height-1)]
    while len(coord_pairs) > 0:
        x, y = coord_pairs[0]
        print(x, y)
        y0, yf = extend(y, x, x_lines, height)
        x0, xf = extend(x, y, y_lines, height)
        print(x0, xf)
        print(y0, yf)
        draw_rect(x0, xf, y0, yf, mult)
        print()
        coord_pairs = [(x, y) for x, y in coord_pairs
                       if not (x0 <= x <= xf and y0 <= y <= yf)]


def draw(x_lines, y_lines, width, height, out_fn):
    mult = 10

    drawBot.newDrawing()
    drawBot.newPage(width*mult, height*mult)
    drawBot.fill(1, 1, 1)
    drawBot.rect(0, 0, width*mult, height*mult)

    draw_colors(x_lines, y_lines, width, height, mult)
    draw_lines(x_lines, y_lines, mult)

    drawBot.saveImage(out_fn)
    drawBot.endDrawing()


if __name__ == '__main__':
    w, h = 50, 60
    lines = gen_lines(w, h, [(40, (20, 30))], [])
    print(lines)
    draw(*lines, w, h, 'test.png')
