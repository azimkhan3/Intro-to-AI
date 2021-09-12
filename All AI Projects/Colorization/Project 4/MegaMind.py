import numpy as np
from skimage import io, color
import matplotlib.pyplot as plt
from k_means_adi import Colors
from neural_network import NeuNet
from Patrick import color_distance, five_color


#We will display the original image
plt.figure(figsize=(10,10))
img = io.imread('doggo.jpeg')


#plt.subplot(2,2,1)
#plt.title('Original Pic')
#plt.imshow(img)
colors = Colors('doggo.jpeg')


# recoloring based on five representative colors and these were determined by kmeans
def recolorization(image):
    rec_pic = image

    for i in range(rec_pic.shape[0]):
        for j in range(rec_pic.shape[1]):
            min_x = float('inf')
            min_y = []
            RGB = [rec_pic[i, j, 0], rec_pic[i, j, 1], rec_pic[i, j, 2]]
            for k in colors:
                np_c = np.array(k)
                length = color_distance(np_c, RGB)
                if length < min_x:
                    min_x = length
                    min_y = k

            rec_pic[i, j, 0] = min_y[0]
            rec_pic[i, j, 1] = min_y[1]
            rec_pic[i, j, 2] = min_y[2]

    return rec_pic

img_new = recolorization(img) #This is the recolored image with the 5 represntative colors



#determining similarity between 3x3 pixel patches in the test data and training data
# to determine what color should be assigned to the pixel.
def patching(image, x, y):

    patch = []
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            patch.append(image[i, j])
    return patch


#makes processing simple, corrosponf an index to a color. If red is most dominant, it will be classified as 1
def one_hot_code(input):
    oh = [0, 0, 0, 0, 0]
    index = colors.index(input.tolist())
    oh[index] = 1
    return oh

# and change back to a initial color
def reverse_hot(input):
    one = input.tolist().index(max(input))
    return colors[one]

# calculate difference between expected and result
def change(initial, beg):
    incorrect = 0

    for i in range(initial.shape[0]):
        for j in range(initial.shape[1]):
            if not np.array_equal(initial[i, j], beg[i, j]):
                incorrect += 1

    sum = initial.shape[0] * initial.shape[1]
    return incorrect / sum

# input layer: 9
# output layer: 5 (one hot code)

layers = [9, 9, 5]

#we adjusted these parameters to prevent overfitting
learn_rate = 0.1
EPOCH = 20000
#training the black and white image
bw_training = color.rgb2gray(img_new[:, 0:int(img_new.shape[1] / 2), :])

#training the recolored image
recolor_training = img_new[:, 0:int(img_new.shape[1] / 2), :]

#Predicitng
bw_prediction= color.rgb2gray(img_new[:, int(img_new.shape[1] / 2):img_new.shape[1], :])

recolor_prediction = img_new[:, int(img_new.shape[1] / 2):img_new.shape[1], :]

# calling the NEURAL NETWORK
input_data = []
NN = NeuNet(layers, 'tanh')
compiled_data = []

# training the data
for i in range(1, bw_training.shape[0] - 1):
    for j in range(1, bw_training.shape[1] - 1):
        input_data.append(patching(bw_training, i, j))
        compiled_data.append(one_hot_code(recolor_training[i, j]))



NN.model_fit(input_data, compiled_data, learn_rate, EPOCH)

# Predicts image
print("predict: ", NN.predict_outcome(patching(bw_prediction, 100, 100)))

resolution = np.zeros([bw_prediction.shape[0], bw_prediction.shape[1], 3], dtype = np.uint8)

for i in range(1, bw_prediction.shape[0] - 1):
    for j in range(1, bw_prediction.shape[1] - 1):
        resolution[i, j, 0] = reverse_hot(NN.predict_outcome(patching(bw_prediction, i, j)))[0]
        resolution[i, j, 1] = reverse_hot(NN.predict_outcome(patching(bw_prediction, i, j)))[1]
        resolution[i, j, 2] = reverse_hot(NN.predict_outcome(patching(bw_prediction, i, j)))[2]

resolution.astype(np.int)

# display width and height of figure in inches: set to be 10x10 but you can change it
plt.figure(figsize=(10,10))

plt.subplot(2,1,1)
plt.title('Recolored Pic')
plt.imshow(img_new)

plt.subplot(2,2,3)
plt.title('Right Side: Grayscale')

plt.imshow(bw_prediction, cmap="gray")

plt.subplot(2,2,4)
plt.title('Right Side: Predicted')
plt.imshow(resolution)

print("Difference: {}".format(change(recolor_prediction, resolution)))
plt.show()