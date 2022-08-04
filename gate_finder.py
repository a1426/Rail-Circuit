import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import image
import re
from itertools import chain
import os
extra_margin=10
def find_gates(location,px):
    locations=[]
    reg=re.compile("[0-]{5,}")
    #This is a strange approach. Maybe improve this method?
    color_string=("".join(str(st)[0] for st in px))
    for match in re.finditer(reg,color_string):
        locations.append(match.span())
    #The [0][0] is a precaition against false lines. All lines should start at the beggining, that is x=0
    #False lines do not start at x=0, so this prevents that.
    if locations and not locations[0][0]:
        return {location:locations}
    #A precaution against completely empty lines.
    else:
        return False
def high_low(value,selection_list, default_height):
    try:
        higher = min([element for element in selection_list if element-value > 0])
    except ValueError:
        higher=default_height
    try:
        lower = max(element for element in selection_list if element-value < 0)
    except ValueError:
        lower=0
    if lower-extra_margin>=0:
        lower-=extra_margin
    if higher+extra_margin<=default_height:
        higher+=extra_margin
    return lower,higher
def cut_off(img):
    current_run=[]
    n_white=[]
    prev=True
    for index,column in enumerate(img.T):
        if not (current:=np.all(column==255)):
            current_run.append(index)
        else:
            if not prev==current:
                n_white.append(current_run)
                current_run=[]
        prev=current
    #The last element is the circuit.
    main_circuit=n_white[-1]
    return main_circuit[0]+1,main_circuit[-1]+1
def clear(target):
    for f in os.listdir(target):
        os.remove(f"{target}/{f}")
def isolate_gates(inp, target, debug = ""):
    pix_matrix = cv2.imread(inp,cv2.IMREAD_GRAYSCALE) 
    begin, end=cut_off(pix_matrix)
    pix_matrix=pix_matrix[:,begin:end]
    height=pix_matrix.shape[0]
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
                img_clone= np.copy(pix_matrix)
                cv2.line(img_clone, pt1, pt2, (0, 0, 0), 1)
    except TypeError:
        raise TypeError("No lines were detected.")
    hor_lines.sort(),ver_lines.sort()
    if debug:
        cv2.imwrite(debug, img_clone)
    pure_lines = []
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
    qubit_registry = {}
    for y_pos,col in corresponding_lines:
        if qubit:=find_gates(y_pos,col):
            qubit_registry.update(qubit)
    qubit_num=0
    for key,value in qubit_registry.items():
        l,h = high_low(key,other_lines,height)
        flat_list = list(chain(*value))
        flat_list.pop()
        flat_list.remove(0)
        grouped_list = [flat_list[index:index + 2] for index in range(0,len(flat_list),2)]
        ct=0
        for left,right in grouped_list:
            ct += 1
            selection= pix_matrix[l:h,left:right]
            with open(name:=f"{target}/{qubit_num}-{ct}.png","w+"):
                cv2.imwrite(name,selection)
        qubit_num += 1
