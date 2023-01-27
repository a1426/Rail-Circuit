from tensorflow.keras import utils, layers,Sequential, models, losses
from tensorflow.nn import softmax
import source_gen
from gate_finder import extra_margin
import cv2
import numpy as np

#Generate the data
#f_size=source_gen.generate(1)
#for x in range(100):
#    f_size=source_gen.generate(1,f_size)

t_dataset=utils.image_dataset_from_directory('gates',validation_split=0.2,subset='training',seed=1,color_mode="grayscale",image_size=(28,28))
v_dataset=utils.image_dataset_from_directory('gates', validation_split=0.2, subset='validation',seed=1,color_mode="grayscale",image_size=(28,28))


model = models.Sequential([
  layers.Flatten(input_shape=(28, 28)),
  layers.Dense(128, activation='relu'),
  layers.Dropout(0.2),
  layers.Dense(10)
])

model.compile(optimizer='adam',loss=losses.SparseCategoricalCrossentropy(from_logits=True))
model.fit(t_dataset, epochs=5)

probability_model = models.Sequential([model, layers.Softmax()])

img = cv2.imread("gates/h/2.png",cv2.IMREAD_GRAYSCALE)
img=cv2.resize(img,(28,28))
img=utils.img_to_array(img)
img=np.expand_dims(img,0)
predictions = probability_model.predict(img)
print(predictions)
print(np.argmax(predictions,axis=1))


score=softmax(prediction_arr)
print(score)
print(source_gen.component_list)
print(source_gen.component_list[np.argmax(score)])
print(100 * np.max(score))
print(100*score[3])

