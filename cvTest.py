import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import image

def find_lines(inp,out):
    # These numbers are random, if the sensivity seems off, look here.
    pix_matrix = cv2.imread(inp,cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(pix_matrix, 80, 120)
    lines = cv2.HoughLines(edges, 1, np.pi / 2, 20, None, 0, 0)
    try:
        for line in lines:
            rho, theta = line[0]
            x, y = math.cos(theta), math.sin(theta)
            x0 = x * rho
            y0 = y * rho
            pt1 = (int(x0-y), int(y0+x))
            pt2 = (int(x0+y), int(y0 - x))
            print(pt1,pt2)
            cv2.line(pix_matrix, pt1, pt2, (255, 0, 255), 1)
    except TypeError:
        raise TypeError("No lines were detected.")
    cv2.imwrite(out, pix_matrix)

find_lines("diagram2.png","lines2.png")