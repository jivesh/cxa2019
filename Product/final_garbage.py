from keras.models import model_from_json
import numpy as np
# import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img
from keras.layers import Conv2D, Flatten, MaxPooling2D, Dense
from keras.models import Sequential

import glob, os, random
import tensorflow as tf

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = tf.keras.models.model_from_json(loaded_model_json)
model.load_weights('model.h5')

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
model.summary()




test_datagen = ImageDataGenerator(
    rescale=1./255
)

batch_size = 16


labels = {0: 'cardboard', 1: 'glass', 2: 'metal', 3: 'paper', 4: 'plastic', 5: 'trash'}


validation_generator = test_datagen.flow_from_directory('static/images/downloaded_images', target_size=(224, 224))
test_x, test_y= validation_generator.__getitem__(0)
preds = model.predict(test_x)
print('pred:%s' % (labels[np.argmax(preds[0])]))
f = open("prediction.txt","w")
f.write(str(labels[np.argmax(preds[0])]))
f.close()
