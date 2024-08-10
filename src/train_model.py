from ultralytics import YOLO
from source_gen import generate

#Populates the dataset
generate(1000,.9)


#NB: the dataset directory can lead to issues. 
def train_squares():
    try:
        #Use a pretrained model
        model = YOLO("yolov8n.pt")
        results = model.train(data="datasets/square_dataset/data.yaml", epochs=10)
        model.export()
    except (FileNotFoundError, RuntimeError) as e:
        raise Exception("Check settings.yaml.")




