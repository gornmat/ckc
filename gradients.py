from __future__ import division
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
from math import floor
from math import trunc
import numpy as np
matplotlib.use('Agg')


def plot_color_gradients(gradients, names):
    rc('legend', fontsize=10)

    column_width_pt = 400
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3] / 2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('gradients.pdf')


def create_point(point_list, single_point, rgb):
    point = trunc(single_point * (len(point_list) - 1))

    if point == len(point_list) - 1:
        point = len(point_list) - 2

    scale = single_point * (len(point_list) - 1) - point
    final_point = []

    for i in range(len(point_list[point])):
        left = point_list[point][i]
        right = point_list[point + 1][i]
        difference = right - left

        if rgb and difference != 0:
            point_value = (1 / difference) * scale
        elif not rgb:
            point_value = difference * scale
        else:
            point_value = 0

        final_point.append(left + point_value)

    return final_point


def hsv2rgb(h, s, v):
    if h >= 360:
        while h >= 360:
            h -= 360
    elif h < 0:
        while h < 0:
            h += 360

    c = v * s
    d = c * (1 - abs((h / 60) % 2 - 1))
    e = v - c

    switcher = {
        0: [c, d, 0],
        1: [d, c, 0],
        2: [0, c, d],
        3: [0, d, c],
        4: [d, 0, c],
        5: [c, 0, d]
    }
    rgb = switcher.get(floor(h / 60), [0, 0, 0])

    for i in range(len(rgb)):
        rgb[i] += e

    return rgb


def gradient_rgb_bw(v):
    return create_point([
        [0, 0, 0],
        [1, 1, 1]],
        v,
        True)


def gradient_rgb_gbr(v):
    return create_point([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]],
        v,
        True)


def gradient_rgb_gbr_full(v):
    return create_point([
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0]],
        v,
        True)


def gradient_rgb_wb_custom(v):
    return create_point([
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 0],
        [0, 1, 1],
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, 0]],
        v,
        True)


def gradient_hsv_bw(v):
    hsv = create_point([
        [0, 0, 0],
        [0, 0, 1]],
        v,
        False)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])


def gradient_hsv_gbr(v):
    hsv = create_point([
        [120, 1, 1],
        [180, 1, 1],
        [240, 1, 1],
        [300, 1, 1],
        [360, 1, 1]],
        v,
        False)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])


def gradient_hsv_unknown(v):
    hsv = create_point([
        [120, 0.5, 1],
        [60, 0.5, 1],
        [0, 0.5, 1]],
        v,
        False)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])


def gradient_hsv_custom(v):
    hsv = create_point([
        [20, 0.9, 0.96],
        [85, 0.6, 0.98],
        [150, 0.3, 0.64],
        [215, 0.6, 1],
        [280, 0.9, 1],
        [340, 0.6, 1]],
        v,
        False)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])


if __name__ == '__main__':
    def to_name(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [to_name(g) for g in gradients])
