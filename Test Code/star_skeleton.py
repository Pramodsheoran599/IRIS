import cv2 as cv
import numpy as np
from scipy.signal import argrelextrema
import math
from matplotlib import pyplot as plt


def calc_centroid(contour_points):
    N = len(contour_points)
    # print(contour_points)
    x_co_ordinates = [contour_points[x][0][0] for x in range(N)]
    y_co_ordinates = [contour_points[y][0][1] for y in range(N)]

    print(x_co_ordinates)
    print(y_co_ordinates)

    Xc = int((1 / N) * sum(x_co_ordinates))
    Yc = int((1 / N) * sum(y_co_ordinates))

    return Xc, Yc


def calc_extreme_points(centroid, countour_points):
    N = len(contour_points)

    Xc = centroid[0]
    Yc = centroid[1]

    x_co_ordinates = [contour_points[x][0][0] for x in range(N)]
    y_co_ordinates = [contour_points[y][0][1] for y in range(N)]

    di = []

    for i in range(N):
        d = int(math.sqrt(((x_co_ordinates[i] - Xc) ** 2) + (y_co_ordinates[i] - Yc) ** 2))
        di.append(d)

    x = np.array(range(N))
    di = np.array(di)

    sortId = np.argsort(x)
    x = x[sortId]
    y = di[sortId]

    # this way the x-axis corresponds to the index of x
    plot_graph(x, y)
    maxm = argrelextrema(y, np.less)
    # print(maxm)


def plot_graph(x, y):
    plt.plot(x, y)

    plt.xlabel('Border Points i')
    plt.ylabel('di')

    plt.title("Extreme Points")

    plt.show(block=True)
    plt.interactive(False)


if __name__ == "__main__":
    original_img = cv.imread(r'Images\Human.jpg')

    gray = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 3)

    edged = cv.Canny(gray, 30, 200)

    contours, _ = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contour_points = max(contours, key=cv.contourArea)

    cv.drawContours(original_img, contours, -1, (0, 255, 0), 2)

    centroid = calc_centroid(contour_points)
    POINT = tuple(contour_points[288][0])

    calc_extreme_points(centroid, contour_points)
    cv.circle(original_img, centroid, 8, (0, 0, 255), thickness=cv.FILLED)
    cv.circle(original_img, POINT, 8, (0, 0, 255), thickness=cv.FILLED)
    cv.line(original_img, centroid, POINT, (255, 0, 0), 3)

    cv.imshow("Orignal Image", original_img)
    cv.imshow("Edge Image", edged)

    cv.waitKey(0)
