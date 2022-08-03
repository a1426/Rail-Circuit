from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.tools.visualization import circuit_drawer
from random import randint, choice
import matplotlib.pyplot as plt
import gate_finder
from collections import defaultdict
def random_component(obj):
    return choice([obj.x, obj.y, obj.z,obj.h, obj.i, obj.s, obj.sdg, obj.t, obj.tdg])
class Simple_Square_Gates:
    def __init__(self,size):
        self.circuit=QuantumCircuit(size)
        self.history= defaultdict(int)
        self.gates={}
        for x in range(randint(5,10)):
            method=random_component(self.circuit)
            pos=randint(0,size-1)
            self.history[pos]+=1
            method(pos)
            self.gates[f'{pos}-{self.history[pos]}']=method.__name__
        print(self.gates)

    def export(self):
        self.circuit.draw(output="mpl")
        plt.savefig("src2/generated_circuits/test.png")
c1=Simple_Square_Gates(2)
c1.export()
gate_finder.clear()

gate_finder.isolate_gates("src2/generated_circuits/test.png")
