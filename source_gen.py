from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.tools.visualization import circuit_drawer
from random import randint, choice
import matplotlib.pyplot as plt
def random_component(obj):
    return choice([obj.x, obj.y, obj.z])
class Pauli_XYZ:
    def __init__(self,size):
        self.circuit=QuantumCircuit(size)
        self.history=""
        for x in range(randint(1,10)):
            #Seems to be strangely biased against Y. ?? Need to review.
            method=random_component(self.circuit)
            pos=randint(0,size-1)
            method(pos)
            #Note: This is a lazy implementation for xyz gates, but works. FIX LATER.
            self.history+=(str(method)[29]+f"{pos}")
    def export(self):
        self.circuit.draw(output="mpl")
        plt.savefig("generated_circuits/test.pdf")
    def give_result(self):
        #Should return the correct classification. DO LATER
        pass
c1=Pauli_XYZ(2)
print(c1.history)
c1.export()


