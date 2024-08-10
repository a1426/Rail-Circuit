from qiskit import QuantumCircuit
import random
from gate_finder import single_square_gates
from collections import defaultdict
import yaml
import matplotlib.pyplot as plt
from math import pi
with open("dataset/square_dataset/data.yaml") as file:
    try:
        names=yaml.safe_load(file)["names"]
    except yaml.YAMLError as e:
        print(e)

#Creates a quantum circuit consisting of 10 gates
class Simple_Square_Gates:
    def __init__(self):
        self.folder_sizes = defaultdict(int)
        self.circuit=QuantumCircuit(1)
        self.gates=[]
        for x in range(10):
            #A strange approach here here
            method=eval("self.circuit."+random.choice(list(names.values())))
            args=[]
            for x in range(method.__code__.co_argcount - (0 if method.__defaults__ is None else len(method.__defaults__))):
                a=random(-1,1000)
                if(a<0):
                    a=pi/random.randint(2,10)
                args.append(a)
            method(*args,0)
            self.gates.append(method.__name__)
    def export(self, path, validate=False):
        #Determines whether to export the figure to the training or validation directory.
        spl="train" if validate==False else "val"
        #Generates the image.
        self.circuit.draw(output="mpl")
        plt.savefig(f"dataset/square_dataset/images/{spl}/{path}.png")
        plt.close()
        #Generates the labels.
        with open(f"dataset/square_dataset/labels/{spl}/{path}.txt","w") as file:
            #code to write labels here
            widths,min_y,max_y,w,h=single_square_gates(f"dataset/square_dataset/images/{spl}/{path}.png")
            for x in range(10):
                file.write(f"{next(k for k, v in names.items() if v == self.gates[x])} {(widths[x][1]+widths[x][0])/(2*w)} {(min_y+max_y)/(2*h)} {(widths[x][1]-widths[x][0])/w} {(max_y-min_y)/h}\n")
            
def generate(num, split, start=0):
    for x in range(int(num*split)):
        Simple_Square_Gates().export(str(x+start))
    for x in range(int(num*(1-split))):
        Simple_Square_Gates().export(str(x+start), True)
