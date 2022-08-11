from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.tools.visualization import circuit_drawer
from random import randint, choice
import matplotlib.pyplot as plt
import gate_finder
from collections import defaultdict
from os import makedirs,getcwd
from json import dumps
def random_component(obj):
    return choice([obj.x, obj.y, obj.z,obj.h, obj.i, obj.s, obj.sdg, obj.t, obj.tdg])
class Simple_Square_Gates:
    def __init__(self,size):
        self.circuit=QuantumCircuit(size)
        self.history= defaultdict(int)
        self.gates={}
        for x in range(1,10):
            method=random_component(self.circuit)
            pos=randint(0,size-1)
            self.history[pos]+=1
            method(pos)
            self.gates[f'{pos}-{self.history[pos]}']=method.__name__
    def export(self):
        self.circuit.draw(output="mpl")
        print(getcwd())
        plt.savefig("generated_circuits/test.png")
    def generate_folder(self,path):
        try:
            makedirs(path)
        except FileExistsError:
            gate_finder.clear("img_save")
        gate_finder.isolate_gates("generated_circuits/test.png",path)
        with open(f"{path}/labels.json","w+") as file:
            data=dumps(self.gates)
            file.write(data)
def generate(size):
    c1=Simple_Square_Gates(size)
    c1.export()
    c1.generate_folder(f"img_save")
