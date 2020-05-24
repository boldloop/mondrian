#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# mondrian.py


from random import random


def check_terminus(const, v, opp_lines, limit):
    if v in [0, limit]:
        return True
    else:
        opp_with_v = [opp for opp in opp_lines if opp[0] == v]
        for opp in opp_with_v:
            c0, cf = opp[1]
            if c0 < const < cf:
                return True
    return False


def check_termini(line, opp_lines, limit):
    const, (v0, vf) = line
    response = [check_terminus(const, v, opp_lines, limit) for v in [v0, vf]]
    return tuple(response)


def check_line(line, opp_lines, limit):
    return all(check_termini(line, opp_lines, limit))


def invalid(x_lines, y_lines, width, height):
    for x_line in x_lines:
        if not check_line(x_line, y_lines, width):
            return True
    for y_line in y_lines:
        if not check_line(y_line, x_lines, height):
            return True
    return False


def border_chance():
    i = 0
    while True:
        i += 1
        yield 2 ** (-i)


def build_terminus(const, v, direction, opps, limit, opp_limit,
                   border_chance):
    if check_terminus(const, v, opps, limit):
        return v, []
    else:
        if random() < (1 - 2*border_chance):
            # continuing the current line, maybe doing something else
            step = random() * direction * 20

            # in this list comp, need to check both ways if step is negative
            opps_with_v = [opp for opp in opps if
                           (v <= opp[0] <= v+step or v >= opp[0] >= v+step)]
            intersect_vs = []
            for opp in opps_with_v:
                c0, cf = opp[1]
                if c0 <= const <= cf:
                    intersect_vs.append(opp[0])

            if len(intersect_vs) > 0:
                # return the v that our line would hit first
                pass_through = direction if random() < .5 else 0
                if direction == 1:
                    return min(intersect_vs) + pass_through, []
                else:
                    return max(intersect_vs) + pass_through, []

            elif v + step <= 0:
                return 0, []
            elif limit <= v + step:
                return limit, []

            else:
                v += step
                new_opp_v = v
                new_opp_c0 = const - 1 if random() < border_chance else const
                new_opp_cf = const + 1 if random() < border_chance else const
                if new_opp_c0 != new_opp_cf:
                    return v, [(new_opp_v, (new_opp_c0, new_opp_cf))]
                else:
                    return v, []
        else:
            return v, [(v, (const - 1, const + 1))]


def build_line(line, opps, limit, opp_limit, border_chance):
    new_line_vs, new_opps = tuple(), list()
    for i, v in enumerate(line[1]):
        direction = {0: -1, 1: 1}[i]  # which way to extend line
        nv, new_term_opps = build_terminus(line[0], v, direction, opps, limit,
                                           opp_limit, border_chance)
        new_line_vs += (nv,)
        new_opps.extend(new_term_opps)
    return (line[0], new_line_vs), new_opps


def gen_lines(width, height, starting_x, starting_y):
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
        border_chance = .05 if len(x_lines + y_lines) <= 12 else 0
    return x_lines, y_lines


if __name__ == '__main__':
    print(gen_lines(100, 100, [(40, (20, 80))], []))


# done.
