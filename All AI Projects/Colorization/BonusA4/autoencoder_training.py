from keras.layers import Conv2D, UpSampling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb
from skimage.transform import resize
from skimage.io import imsave
from skimage import io
import numpy as np
import tensorflow as tf

path = 'Pictures/'         #input the folder of the pictures

#Rescale all of the images in the folder by diving it by 255
#Each pixel values in each channel of RGB is being divided 

generate_data = ImageDataGenerator(rescale=1. / 255)

# Normalized pixel value into 0 to 1 in order to use relu activation function

#Resize images, if needed
image_training = generate_data.flow_from_directory(path, target_size=(256, 256), batch_size=340, class_mode=None)
#convert RGB to LAB
X =[] #L channel

Y =[] #A and B channel

for img in image_training[0]:

  try:
      lab = rgb2lab(img) #convert RGB to LAB 
      X.append(lab[:,:,0]) 
      Y.append(lab[:,:,1:] / 128) #A and B values range from -127 to 128, 
      #so we divide the values by 128 to restrict values to between -1 and 1.
  except:
     print('error')
X = np.array(X)
Y = np.array(Y)
X = X.reshape(X.shape+(1,)) #dimensions to be the same for X and Y
print(X.shape)
print(Y.shape)
#Encoder

model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', padding='same', strides=2, input_shape=(256, 256, 1)))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3,3), activation='relu', padding='same', strides=2))
model.add(Conv2D(256, (3,3), activation='relu', padding='same'))
model.add(Conv2D(256, (3,3), activation='relu', padding='same', strides=2))
model.add(Conv2D(512, (3,3), activation='relu', padding='same'))
model.add(Conv2D(512, (3,3), activation='relu', padding='same'))
model.add(Conv2D(256, (3,3), activation='relu', padding='same'))
#Decoder
#Decoder
#Most of our model uses the relu activation function since we restrict the value from 0 to 1 
#however since for the last prediction layer we restricted between -1 to 1 we need to use tanh activation function
model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
model.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))
model.add(UpSampling2D((2, 2)))
model.compile(optimizer='adam', loss='mse' , metrics=['accuracy'])
model.summary()


model.fit(X,Y,validation_split=0.1, epochs=100, batch_size=16)

model.save('other_files/image_colorization.model')