#import yaml
#from ultralytics import YOLO
from PIL import Image


qubits=[]
def find_qubits(img):
    im=Image.open(img).convert("RGB")
    width, height = im.size
    previously_colored=False
    for y in range(height):
        colored_column=False
        counter=0
        for x in range(width):
            r,g,b=im.getpixel((x,y))
            if(r==g==b>200):
                counter+=1
            if(counter>=20):
                colored_column=True
                break
        print(colored_column+","+ previously_colored)
        if(colored_column and not previously_colored):
                print(1)
                qubits.append([x])
        if(previously_colored and not colored_column):
            print(2)
            qubits[-1].append(x)
        previously_colored=colored_column
    for qubit in qubits:
        break
        if (type(qubit)==list):
            qubits.append((qubit[0]+qubit[1])/2)



find_qubits("/Users/robert/Projects/RailConverter/Rail-Circuit/src/test.png")
print(qubits)


#Names, to map the ids of the boxes onto the 
with open("/Users/robert/Projects/datasets/testDataset/data.yaml") as file:
    try:
        #names=yaml.safe_load(file)["names"]
        pass
    except yaml.YAMLError as e:
        #print(e)


#ss_model = YOLO("models/squares/best.pt")

#def labels(path):
    #TODO:
    #shapes=ss_model(path)[0]
    #for box in shapes.boxes.cls:
    #    print(names[int(box)])
    
    #shapes.save(filename="result.jpg")  # save to disk



#labels("/Users/robert/Projects/datasets/testDataset/images/train/1.png")