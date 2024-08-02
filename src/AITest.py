from ultralytics import YOLO
from source_gen import generate
#Populates the dataset
#generate(1000,.9)
#Using a pretrained model
model = YOLO("yolov8n.pt")
#NB: the dataset directory can lead to issues
results = model.train(data="/Users/robert/Projects/datasets/testDataset/data.yaml", epochs=3)

model.export()

def labels(path):
    results=model(path)
    for result in results:
        print("a")
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        result.save(filename="result.jpg")  # save to disk
labels("/Users/robert/Projects/datasets/testDataset/images/train/1.png")
