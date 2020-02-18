from tensorflow.keras.models import model_from_json
import numpy as np
# import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import glob, os, random


json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights('model.h5')

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
model.summary()

test_datagen = ImageDataGenerator(rescale=1. / 255)

batch_size = 16

labels = {0: 'glass', 1: 'metal', 2: 'paper', 3: 'plastic', 4: 'trash'}

validation_generator = test_datagen.flow_from_directory(
    'static/images/downloaded_images', target_size=(224, 224))
test_x, test_y = validation_generator.__getitem__(0)
preds = model.predict(test_x)
print('pred:%s' % (labels[np.argmax(preds[0])]))
f = open("prediction.txt", "w")
f.write(str(labels[np.argmax(preds[0])]))
f.close()
