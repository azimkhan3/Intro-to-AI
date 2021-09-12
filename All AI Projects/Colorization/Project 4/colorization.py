import numpy as np
import matplotlib.pyplot as plt
from PIL import Image



class Colorization(object):
    def __init__(self, file):
        self.file = file
        pass

    def unpickle(self):
        import pickle
        with open(self.file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict

    def rgb2gray(self):
        self.rgb = self.unpickle()[b'data']
        self.size = int(len(self.rgb[0]) / 3)
        self.gray = 0.21 * self.rgb[:, 0:self.size] + 0.72 * self.rgb[:, self.size:self.size * 2] + 0.07 * self.rgb[:,
                                                                                                           self.size * 2:]
        self.gray = self.gray.astype(int)
        image = np.reshape(self.gray[0], [32, 32])
        origin_red = np.reshape(self.rgb[0][0:self.size], [32, 32])
        origin_green = np.reshape(self.rgb[0][self.size:self.size * 2], [32, 32])
        origin_blue = np.reshape(self.rgb[0][self.size * 2:], [32, 32])
        # num = 9000
        # aa = self.rgb[0]
        # r = Image.fromarray(np.reshape(aa[0:1024], [32, 32])).convert('L')
        # g = Image.fromarray(np.reshape(aa[1024:2048], [32, 32])).convert('L')
        # b = Image.fromarray(np.reshape(aa[2048:3072], [32, 32])).convert('L')
        # ic = Image.merge("RGB", (r, g, b))
        # plt.imshow(ic)
        # plt.show()
        # print(image)
        # print(origin_red)
        # plt.imshow(image, cmap=plt.cm.gray)
        # plt.show()
        return {'gray': image, 'red': origin_red, 'green': origin_green, 'blue': origin_blue}


# cn = Colorization('cifar-10-batches-py/data_batch_1')
# cn.rgb2gray()
