from skimage import color, measure, exposure
from matplotlib import pyplot
from imageio import imread
from numpy import percentile, zeros


def search_edges(image):
    beginning, end = percentile(image, (10, 40))
    image = exposure.rescale_intensity(image, in_range=(beginning, end))
    image = color.rgb2hsv(image)
    colors = zeros([len(image), len(image[0])])

    for i in range(len(image)):
        for j in range(len(image[i])):
            colors[i][j] = 1 - image[i][j][2]
            image[i][j] = [0, 0, 0]

    contours = measure.find_contours(colors, 0.3)

    return image, contours


def draw_plots(images):
    figure = pyplot.figure(facecolor="black")
    i = 0

    for image in images:
        pyplot.subplot(231+i)
        frame = pyplot.gca()
        frame.axes.get_xaxis().set_visible(False)
        frame.axes.get_yaxis().set_visible(False)
        image, contours = search_edges(image)
        for n, contours in enumerate(contours):
            pyplot.plot(contours[:, 1], contours[:, 0], linewidth=0.8, color="w")
        pyplot.imshow(image)
        i += 1

    pyplot.tight_layout()
    pyplot.show()
    figure.savefig("planes.pdf", facecolor="black")
    pyplot.close()


if __name__ == '__main__':
    directory_name = "./planes/"

    files = [
        directory_name + "samolot15.jpg",
        directory_name + "samolot16.jpg",
        directory_name + "samolot17.jpg",
        directory_name + "samolot18.jpg",
        directory_name + "samolot19.jpg",
        directory_name + "samolot20.jpg"
    ]
    images = []

    for file in files:
        images.append(imread(file))

    draw_plots(images)
