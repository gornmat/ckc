import matplotlib.pyplot as plt
from numpy import min
from numpy import max
from math import floor


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


def load_points(file_name):
    with open(file_name) as file:
        file_values = file.read().splitlines()

    file_values = [i.split(' ') for i in file_values]
    height = int(file_values[0][0])
    width = int(file_values[0][1])
    distance = int(file_values[0][2])
    del file_values[0]

    for i in range(len(file_values)):
        del file_values[i][-1]
        file_values[i] = [float(point) for point in file_values[i]]

    return file_values, width, height, distance


def to_hsv_matrix(height, width):
    hsv_matrix = []

    for i in range(height):
        hsv_matrix.append([])

        for j in range(width):
            hsv_matrix[i].append([0, 1, 1])

    return hsv_matrix


def prepare_map(maps, height, width):
    minimum = min(maps)
    maximum = max(maps) - minimum
    hsv_map = to_hsv_matrix(height, width)

    for i in range(height):
        for j in range(width):
            hsv_map[i][j][0] = (1 - ((maps[i][j] - minimum) / maximum)) * 120
            hsv_map[i][j] = hsv2rgb(hsv_map[i][j][0], hsv_map[i][j][1], hsv_map[i][j][2])

    return hsv_map


if __name__ == '__main__':
    map_values, map_height, map_width, distance = load_points("big.dem")
    final_map = prepare_map(map_values, map_height, map_width)
    fig = plt.figure()
    plt.imshow(final_map)
    plt.show()
    fig.savefig("maps.pdf")
    plt.close()
