
from keras.models import model_from_json
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img
from keras.layers import Conv2D, Flatten, MaxPooling2D, Dense
from keras.models import Sequential

import glob, os, random


# In[2]:


base_path = 'Garbage classification'

img_list = glob.glob(os.path.join(base_path, '*/*.jpg'))

print(img_list[0])


# In[3]:


for i, img_path in enumerate(random.sample(img_list, 6)):
    img = load_img(img_path)
    img = img_to_array(img, dtype=np.uint8)

    plt.subplot(2, 3, i+1)
    plt.imshow(img.squeeze())


# In[4]:
batch_size = 16

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.1,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    vertical_flip=True,
    validation_split=0.1
)

test_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.1
)

train_generator = train_datagen.flow_from_directory(
    base_path,
    target_size=(300, 300),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training',
    seed=0
)

validation_generator = test_datagen.flow_from_directory(
    base_path,
    target_size=(300, 300),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation',
    seed=0
)

labels = (train_generator.class_indices)
labels = dict((v,k) for k,v in labels.items())

print(labels)


# In[5]:

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights('model.h5')

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
model.summary()


# # Take a Shot

# In[6]:


model.fit_generator(train_generator, steps_per_epoch = train_generator.n // batch_size, epochs=1, validation_data=validation_generator, validation_steps = validation_generator.n // batch_size)


# # Another Shot

# In[7]:

# In[11]:


test_x, test_y = validation_generator.__getitem__(1)

preds = model.predict(test_x)

'''
model_json = model.to_json()
with open('model.json', 'w') as json_file:
	json_file.write(model_json)
model.save_weights('model.h5')
'''
