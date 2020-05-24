#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# draw.py


from mondrian import gen_lines


def tup_pairs_from_lines(x_lines, y_lines, mult=1):
    x_pairs = [((v[0]*mult, c*mult), (v[1]*mult, c*mult)) for c, v in x_lines]
    y_pairs = [((c*mult, v[0]*mult), (c*mult, v[1]*mult)) for c, v in y_lines]
    return x_pairs + y_pairs


def draw_lines(x_lines, y_lines, width, height, out_fn):
    mult = 5
    tup_pairs = tup_pairs_from_lines(x_lines, y_lines, mult)
    import drawBot
    drawBot.newDrawing()
    drawBot.newPage(width*mult, height*mult)
    drawBot.fill(1, 1, 1)
    drawBot.rect(0, 0, width*mult, height*mult)
    drawBot.stroke(0)
    for pair in tup_pairs:
        drawBot.line(*pair)
    drawBot.saveImage(out_fn)
    drawBot.endDrawing()


if __name__ == '__main__':
    lines = gen_lines(100, 100, [(40, (20, 80))], [])
    print(lines)
    draw_lines(*lines, 100, 100, 'test.png')
