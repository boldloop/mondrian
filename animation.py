#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2021, Gus Brocchini, GPL v2 or later
# ===========================================
# animation.py

import drawBot
from draw import draw_lines, draw_colors
from mondrian import invalid, build_line


def line_generator(width, height, starting_x, starting_y):
    x_lines = starting_x
    y_lines = starting_y
    border_chance = .2
    while invalid(x_lines, y_lines, width, height):
        new_x, new_y = [], []
        for x_line in x_lines:
            rev_x, y_to_add = build_line(x_line, y_lines, width, height,
                                         border_chance)
            new_x.append(rev_x)
            new_y.extend(y_to_add)
        for y_line in y_lines:
            rev_y, x_to_add = build_line(y_line, x_lines, height, width,
                                         border_chance)
            new_y.append(rev_y)
            new_x.extend(x_to_add)
        x_lines, y_lines = new_x, new_y
        yield x_lines, y_lines
        border_chance = .05 if len(x_lines + y_lines) <= 12 else 0
    return x_lines, y_lines


def page_with_lines(width, height, x_lines, y_lines, mult, dur, color=False):
    drawBot.newPage(width*mult, height*mult)
    drawBot.frameDuration(dur)
    drawBot.fill(1, 1, 1)
    drawBot.rect(0, 0, width*mult, height*mult)
    if color:
        draw_colors(x_lines, y_lines, width, height, mult)
    draw_lines(x_lines, y_lines, mult)


if __name__ == '__main__':
    w, h, x, y = 50, 70, [(30, (24, 30))], []
    mult = 10
    drawBot.newDrawing()
    page_with_lines(w, h, x, y, mult, 1/4)

    for x_lines, y_lines in line_generator(w, h, x, y):
        page_with_lines(w, h, x_lines, y_lines, mult, 1/4)

    page_with_lines(w, h, x_lines, y_lines, mult, 2, color=True)

    drawBot.saveImage('animation.gif')
    drawBot.endDrawing()

# done.
