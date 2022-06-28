import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import image
import re

def find_gates(num_qubit,px):
    qubit_reg= {num_qubit: []}
    reg=re.compile("[0]{5,}")
    #This is a strange approach. Maybe improve this method?
    color_string=("".join(str(st) for st in px))
    for match in re.finditer(reg,color_string):
        qubit_reg[num_qubit].append(match.span())
    return qubit_reg

def find_lines(inp, debug = None):
    pix_matrix = cv2.imread(inp,cv2.IMREAD_GRAYSCALE)
    #The "q" representing each qubit causes an extra edge to appear. This is a lazy fix. Make this more dyamic
    pix_matrix=pix_matrix[:,100:]
    # These numbers are random, if the sensivity seems off, look here. Remove Magic Numbers.
    edges = cv2.Canny(pix_matrix, 80, 120)
    lines = cv2.HoughLines(edges, 1, np.pi / 2, 20, None)
    try:
        hor_lines,ver_lines=[],[]
        for line in lines:
            rho, theta = line[0]
            x, y = round(math.cos(theta)), round(math.sin(theta))
            x0 = x * round(rho)
            y0 = y * round(rho)
            if x:
                ver_lines.append(x0)
            elif y:
                hor_lines.append(y0)
            if debug:
                pt1 = (x0 - 100 * y,y0 + 100 * x)
                pt2 = (x0 + 100 * y,y0 - 100 * x)
                cv2.line(pix_matrix, pt1, pt2, (0, 0, 0), 1)
    except TypeError:
        raise TypeError("No lines were detected.")
    hor_lines.sort(),ver_lines.sort()
    if debug:
        cv2.imwrite(debug, pix_matrix)
    pure_lines = []
    other_lines=[]
    for i in range(len(hor_lines) - 1):
        # The 2 is the width of every line representing a qubit.
        if hor_lines[i + 1] - (v := hor_lines[i]) == 2:
            pure_lines.append((v+1,pix_matrix[v + 1,:]))
        elif hor_lines[i]-hor_lines[i-1]==2:
            pass
        else:
            other_lines.append(hor_lines[i])
    qubit_registry = {}
    for ind,col in pure_lines:
        qubit_registry.update(find_gates(ind,col))
find_lines("diagram2.png","lines3.png")
