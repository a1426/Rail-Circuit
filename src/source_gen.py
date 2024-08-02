from qiskit import QuantumCircuit
from random import choice
import matplotlib.pyplot as plt
from gate_finder import single_square_gates
from collections import defaultdict
def random_component(obj):
    return choice([obj.x, obj.y, obj.z,obj.h, obj.id, obj.s, obj.sdg, obj.t, obj.tdg])
component_list=["x","y","z","h","id","s","sdg","t","tdg"]

#Creates a quantum circuit consisting of 10 gates
class Simple_Square_Gates:
    def __init__(self):
        self.folder_sizes = defaultdict(int)
        self.circuit=QuantumCircuit(1)
        self.gates=[]
        for x in range(10):
            method=random_component(self.circuit)
            method(0)
            self.gates.append(method.__name__)
    def export(self, path, validate=False):
        #Determines whether to export the figure to the training or validation directory.
        spl="train" if validate==False else "val"
        #Generates the image.
        self.circuit.draw(output="mpl")
        plt.savefig(f"/Users/robert/Projects/datasets/testDataset/images/{spl}/{path}.png")
        plt.close()
        #Generates the labels.
        with open(f"/Users/robert/Projects/datasets/testDataset/labels/{spl}/{path}.txt","w") as file:
            #code to write labels here
            widths,min_y,max_y,w,h=single_square_gates(f"/Users/robert/Projects/datasets/testDataset/images/{spl}/{path}.png")
            for x in range(10):
                file.write(f"{component_list.index(self.gates[x])} {(widths[x][1]+widths[x][0])/(2*w)} {(min_y+max_y)/(2*h)} {(widths[x][1]-widths[x][0])/w} {(max_y-min_y)/h}\n")
            

def generate(num, split):
    for x in range(int(num*split)):
        Simple_Square_Gates().export(str(x))
    for x in range(int(num*(1-split))):
        Simple_Square_Gates().export(str(x), True)

