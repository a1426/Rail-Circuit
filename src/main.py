import yaml
from ultralytics import YOLO
from PIL import Image
from qiskit import QuantumCircuit

def main(img):
    #Names, to map the ids of the boxes onto the names.
    with open("/Users/robert/Projects/datasets/testDataset/data.yaml") as file:
        try:
            names=yaml.safe_load(file)["names"]
        except yaml.YAMLError as e:
            print(e)
    #Find qubits
    #TODO:Fix.
    qubits_y=[]
    im=Image.open(img).convert("RGB")
    width, height = im.size
    previously_colored=False
    for y in range(height):
        colored_column=False
        counter=0
        for x in range(width):
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


    qc=QuantumCircuit(len(qubits_y))
    qubits={x:[] for x in range(len(qubits_y))}

    ss_model = YOLO("models/squares/best.pt")

    boxes=[]

    shapes=ss_model(img)[0]
    shapes.save(filename="result.jpg") #save to disk
    #Test for overlapping boxes
    for box in shapes.boxes:
        for box2 in boxes:
            c1=box.xyxyn[0]
            c2=box2.xyxyn[0]
            if (c1[0] <= c2[2] and c1[2] >= c2[0] and c1[1] <= c2[3] and c1[3] >= c2[1]):
                if(box2.conf[0]<box.conf[0]):
                    boxes.remove(box2)
                    boxes.append(box)
                break
        else:
            boxes.append(box)
        if(len(boxes)==0):
            boxes.append(box)
    
    boxes.sort(key=lambda box:box.xyxyn[0][0])
    print(qubits_y)
    for box in boxes:
        for y in range(len(qubits_y)):
            if box.xyxy[0][1]<qubits_y[y]<box.xyxy[0][3]:
                qubits[y].append(box)
    
    for k,v in qubits.items():
        for box in v:
            exec(f"qc.{names[int(box.cls[0])]}({k})")
    return qc
