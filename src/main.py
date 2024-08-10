import yaml
from ultralytics import YOLO
from PIL import Image
from qiskit import QuantumCircuit

#Names, to map the ids of the boxes onto the names.
with open("datasets/square_dataset/data.yaml") as file:
        try:
            names=yaml.safe_load(file)["names"]
        except yaml.YAMLError as e:
            print(e)

class single_gate():
    def __init__(self, box):
        self.act=""
        self.x1,self.y1,self.x2,self.y2=box.xyxy[0]
        self.conf=box.conf[0]
        self.cls=box.cls[0]
        self.name=names[int(self.cls)]
        #Single gates, with no perameters.
        if(self.cls<=10):
            self.act=f"{self.name()}"
        
def find_qubits(im):
    #Find qubits
    #TODO:Fix.
    previously_colored=False
    for y in range(im.size[1]):
        colored_column=False
        counter=0
        for x in range(im.size[0]):
            r,g,b=im.getpixel((x,y))
            if(r==g==b<10):
                counter+=1
            else:
                counter=0
            if(counter>=15):
                colored_column=True
                break
        if(colored_column and not previously_colored):
            qubits_y.append([y])
        if(previously_colored and not colored_column):
            qubits_y[-1]=(qubits_y[-1][0]+y)//2
        previously_colored=colored_column
    return qubits_y

def find_y(gate):
    for y in range(len(qubits_y)):
        if gate.y1<qubits_y[y]<gate.y2:
            qubits[y].append(gate)
            return y


def main(img):

    im=Image.open(img).convert("RGB")
    global qubits_y
    qubits_y=[]
    find_qubits(im)

    qc=QuantumCircuit(len(qubits_y))
    global qubits
    qubits={x:[] for x in range(len(qubits_y))}
    ss_model = YOLO("models/squares/best.pt")
    shapes=ss_model(img)[0]
    single_gates=[]
    shapes.save(filename="result.jpg") #save to disk
    #Test for overlapping boxes
    for box in shapes.boxes:
        g1=single_gate(box)
        y=find_y(g1)
        for box2 in qubits[y]:
            g2=single_gate(box2)
            if box is not box2 and (g1.x1 <= g2.x2 and g1.x2 >= g2.x1 and g1.y1 <= g2.y2 and g1.y2 >= g2.y3):
                if(g1.conf<g2.conf):
                    qubits[y].remove(g1)
                    qubits[y].add(g2)

    single_gates.sort(key=lambda box:box.xyxy[0][0])
    
    for k,v in qubits.items():
        for box in v:
            exec(f"qc.{names[int(box.cls[0])]}({k})")
    return qc
