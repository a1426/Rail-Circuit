import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import image
import re
from itertools import chain
def find_gates(location,px):
    qubit_reg= {location: []}
    reg=re.compile("[0]{5,}")
    #This is a strange approach. Maybe improve this method?
    color_string=("".join(str(st) for st in px))
    for match in re.finditer(reg,color_string):
        qubit_reg[location].append(match.span())
    return qubit_reg
def cut_off(img):
    prev = -1
    current_run=[]
    whites=[]
    for index,column in enumerate(img.T):
    #Fix this
        if np.all(column==255):
            if index==prev+1:
                current_run.append(index)
                print(current_run,end="-\n")
        else:
            if current_run:
                whites.append(current_run)
            print("reached")
            current_run = []
        prev=index
    print(whites)

def find_lines(inp, debug = ""):
    pix_matrix = cv2.imread(inp,cv2.IMREAD_GRAYSCALE)
    #The "q" representing each qubit causes an extra edge to appear. This is a lazy fix. Make this more dynamic
    cut_off(pix_matrix)
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
    #Array of tuples that stores
    corresponding_lines=[]
    other_lines=[]
    for i in range(len(hor_lines) - 1):
        # The 2 is the width of every line representing a qubit.
        if hor_lines[i + 1] - (v := hor_lines[i]) == 2:
            pure_lines.append(v+1)
            corresponding_lines.append((v+1,pix_matrix[v + 1,:]))
        elif hor_lines[i]-hor_lines[i-1]==2:
            pass
        else:
            other_lines.append(hor_lines[i])
    #print(corresponding_lines)
    qubit_registry = {}
    for y_pos,col in corresponding_lines:
        qubit_registry.update(find_gates(y_pos,col))
    print(qubit_registry)
    print(other_lines)
    print(pure_lines)
    for key in qubit_registry.values():
        print([0]+list(chain(*key)))
find_lines("diagram2.png","lines3.png")



