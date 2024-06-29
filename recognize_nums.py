import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from PIL import Image
import numpy as np

model = tf.keras.models.load_model('mnist_model.keras')

img = Image.open('Frame 1.jpg').convert('L')
img = img.resize((28, 28))
img_array = np.array(img).reshape((1, 28, 28, 1)) / 255.0

# Делаем предсказание
predictions = model.predict(img_array)
digit = np.argmax(predictions)
print(digit)
