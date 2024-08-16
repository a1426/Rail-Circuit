from yaml import safe_load, YAMLError
from ultralytics import YOLO
from PIL import Image
from qiskit import QuantumCircuit
from pytesseract import image_to_string
from numpy import ones, array, uint8
from cv2 import resize, erode
import re

class OCRException(Exception):
    pass

#Generates a dictionary that maps the classification values into gate names.
with open("datasets/square_dataset/data.yaml") as file:
        try:
            names=safe_load(file)["names"]
        except YAMLError as e:
            print(e)

class single_gate():
    def __init__(self, box):
        self.x1,self.y1,self.x2,self.y2=box.xyxy[0].numpy()
        self.conf=box.conf[0]
        self.cls=box.cls[0]
        self.name=names[int(self.cls)]
        self.method=eval(f"QuantumCircuit().{self.name}")
        self.args=[]
        #Single gates, with no perameters.
        if(self.cls<=10):
            pass
        else:
            #TODO: Refine the approach with Tesseract. This does not work with values that involve pi.
            greyscale=im.crop((self.x1,self.y1,self.x2,self.y2)).convert("L")
            #Some basic image manipulations to improve OCR accuracy.
            img=array(greyscale)
            img=resize(img,None,fx=10,fy=10)
            kernel = ones((2, 2), uint8) 
            img=erode(img, kernel, iterations=1)
            d=image_to_string(img,lang="eng+equ+grc",config=r'--oem 3 --psm 6')
            p=re.findall("[-]?\d+[.\d+]?",d.split("\n")[1])
            if len(p)!=self.method.__code__.co_argcount - (0 if self.method.__defaults__ is None else len(self.method.__defaults__))-2:
                raise OCRException()
            else:
                self.args=[int(x) for x in p] 
            
def find_qubits(im):
    #Finds the rails(horizontal black lines). A hacky approach, but effective.
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
    global im
    im=Image.open(img).convert("RGB")
    global qubits_y
    qubits_y=[]
    find_qubits(im)
    qc=QuantumCircuit(len(qubits_y))
    global qubits
    qubits={x:[] for x in range(len(qubits_y))}
    ss_model = YOLO("models/squares/best.pt")
    shapes=ss_model(img)[0]
    #Test for overlapping boxes
    for box in shapes.boxes:
        g1=single_gate(box)
        y=find_y(g1)
        for g2 in qubits[y]:
            if g1.x1!= g2.x1 and g1.y1!=g2.y1 and g1.x1 <= g2.x2 and g1.x2 >= g2.x1 and g1.y1 <= g2.y2 and g1.y2 >= g2.y3:
                if(g1.conf<g2.conf):
                    qubits[y].remove(g1)
                    qubits[y].add(g2)
    for x in qubits.values():
        x.sort(key=lambda x: x.x1)
    for k,v in qubits.items():
        for gate in v:
            exec(f"qc.{gate.name}{*gate.args, k}")
    return qc
