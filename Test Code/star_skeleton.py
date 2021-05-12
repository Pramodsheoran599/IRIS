# Importing Libraries
import math

import numpy as np
import cv2 as cv
import imutils
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter


# Global Variables
N = 0                                                                   # For Number of Contour Points
x_co_ordinates = []                                                     # For X-Coordinates of Contour Points
y_co_ordinates = []                                                     # For Y-Coordinates of Contour Points
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 9))             # Ellipsoid Kernel


def plot_graph(x, y, title, x_label, y_label):
    """Plot a Graph for the Given X and Y values"""

    plt.plot(x, y)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.show(block=True)
    plt.interactive(False)


class StarSkeleton:
    def __init__(self, path):
        original_img = cv.imread(path)

        gray = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (3, 3), 0)

        edged = self.auto_canny(gray)

        dilated = cv.dilate(edged, kernel)
        contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        contour_points = max(contours, key=cv.contourArea)

        cv.drawContours(original_img, contour_points, -1, (0, 255, 0), 4)

        centroid = self.calc_centroid(contour_points)
        cv.circle(original_img, centroid, 6, (0, 0, 255), thickness=cv.FILLED)

        extreme_points = self.calc_extreme_points(centroid)
        for point in extreme_points:
            cv.circle(original_img, tuple(contour_points[point][0]), 6, (0, 0, 255), thickness=cv.FILLED)
            cv.line(original_img, centroid, tuple(contour_points[point][0]), (255, 255, 0), 2)

        cv.imshow("Orignal Image", original_img)
        cv.imshow("Edge Image", edged)

        cv.waitKey(0)

    @staticmethod
    def auto_canny(image, sigma=0.33):
        """Canny Edge Detection with Automatic Thresholding By Computing Median of the Image"""

        v = np.median(image)                                                # Compute the median of the single channel pixel intensities
        lower = int(max(0, (1.0 - sigma) * v))                              # Lower threshold
        upper = int(min(255, (1.0 + sigma) * v))                            # Upper threshold
        edged = cv.Canny(image, lower, upper)                               # Canny Edge Detection

        return edged                                                        # return the edged image

    @staticmethod
    def calc_centroid(contour_points):
        """Calculate Centroid of a Given Contour Points List"""

        global N, x_co_ordinates, y_co_ordinates                                # Accessing Global Variables

        N = len(contour_points)                                                 # Number of Contour Points
        x_co_ordinates = [contour_points[x][0][0] for x in range(N)]            # Extracting X-Coordinates of Contour Points
        y_co_ordinates = [contour_points[y][0][1] for y in range(N)]            # Extracting Y-Coordinates of Contour Points

        ##########################################
        ## Formula for Coordinates of centroid:
        ##      Xc = (Σ Xi) / N
        ##      Yc = (Σ Yi) / N
        ##########################################

        Xc = int((1 / N) * sum(x_co_ordinates))                                 # X-Coordinate of Centroid
        Yc = int((1 / N) * sum(y_co_ordinates))                                 # Y-Coordinate of Centroid

        return Xc, Yc                                                           # Return Centroid

    @staticmethod
    def calc_extreme_points(centroid):
        """Calculate the Coordinates of features like Head, Hands, Legs based on their Distance form Centroid"""

        global N, x_co_ordinates, y_co_ordinates                                # Accessing Global Variables

        Xc = centroid[0]                                                        # X-Coordinate of Centroid
        Yc = centroid[1]                                                        # Y-Coordinate of Centroid

        di = []                                                                 # List of Distances of all points from centroid

        ###################################################
        ## Formula for Distance of a Point from centroid:
        ##      d = √((Xi - Xc)² + (Yi - Yc)²)
        ###################################################
        for i in range(N):
            d = int(math.sqrt(((x_co_ordinates[i] - Xc) ** 2) + (y_co_ordinates[i] - Yc) ** 2))
            di.append(d)

        x = np.array(range(N))                                                  # Converting into Numpy Array
        di = np.array(di)

        x = savgol_filter(x, 111, 3)                                            # Smoothing the Curve
        y = savgol_filter(di, 111, 3)                                           # Smoothing the Curve

        #########################################################################################
        ## Formula for Peaks: A graph has a peak if dy/dx changes from +ve to -ve and Vice-Versa
        #########################################################################################

        peaks = (np.diff(y) / np.diff(x))
        local_maxima = {}                                                  # Local Maxima { point : distance }

        for index, peak in enumerate(peaks[:N - 2]):
            if peak > 0 >= peaks[index + 1]:
                local_maxima[index] = di[index]
            elif peak < 0 <= peaks[index + 1]:
                local_maxima[index] = di[index]

        features = []                                                      # Coordinated of the Desired Features
        for _ in range(5):                                                 # Selecting the 5 Points based on their Distance
            distance = max(local_maxima, key=lambda k: local_maxima[k])
            features.append(distance)
            local_maxima.pop(distance)

        plot_graph(x, y,'Extreme Points', 'Border Points i', 'di')         # Plotting the Graph of Points wrt their Distances

        return features                                                    # Returning Feature List


path = r"Images\women.jpg"
skeleton = StarSkeleton(path)
