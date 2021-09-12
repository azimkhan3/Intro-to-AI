import tensorflow as tf
from keras.preprocessing.image import img_to_array, load_img
from skimage.transform import resize
from skimage.io import imsave, imshow
import numpy as np
from skimage import io, color
import matplotlib.pyplot as plt

from skimage.color import rgb2lab, lab2rgb

model = tf.keras.models.load_model('other_files/image_colorization.model',custom_objects=None, compile=True)

img1_color=[]
img = io.imread('sunrise.jpg')
img2 = color.rgb2gray(img)
test_image=img_to_array(load_img('sunrise.jpg'))
test_image = resize(test_image ,(256,256))
img1_color.append(test_image)

img1_color = np.array(img1_color, dtype=float)
img1_color = rgb2lab(1.0/255*img1_color)[:,:,:,0]
img1_color = img1_color.reshape(img1_color.shape+(1,))

output1 = model.predict(img1_color)
output1 = output1*128

result = np.zeros((256, 256, 3))
result[:,:,0] = img1_color[0][:,:,0]
result[:,:,1:] = output1[0]
#imshow(lab2rgb(result))
#imsave("result.png", lab2rgb(result))

plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
plt.title('Original')
plt.imshow(img)
plt.subplot(2, 2, 4)
plt.title('GrayScale')
plt.imshow(img2, cmap="gray")
plt.subplot(2, 2, 3)
plt.title('Result')
plt.imshow(lab2rgb(result))
plt.show()