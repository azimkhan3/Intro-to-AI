import numpy as np


# ACTIVATION FUNCTIONS, first step for neural networks. Without these we would only have regression

#def logistic(input):
 #   return 1 / (1 + np.exp(-input))

#def slope_logistic(input):  # derivative of the logistic
#    return logistic(input) * (1 - logistic(input))

def sigmoid(input):
    return (1 / (1 + np.exp(-input)))

def slope_sigmoid(input):
    return (np.exp**(-input))/((1+(np.exp**(-input)))**2)

def tanh(input):
    return np.tanh(input)

def slope_tanh(input):  # derivative of tanh. this represents the slope
    return 1.0 - np.tanh(input) ** 2


# NEURAL NETWORK

class NeuNet:
    def __init__(self, layers, af='sigmoid'): #we can also try the sigmoid one
        # layers = number of units per layer
        # a = activation function

        if af == 'tanh':
            self.activation = tanh
            self.activation_der = slope_tanh

        elif af == 'sigmoid':
            self.activation = sigmoid
            self.activation_der = slope_sigmoid
    #Weights are learnable parameters inside the network. A teachable neural network will randomize the weight values
        # before learning initially begins

        self.weights = []
        # initializing random weights
        for i in range(1, len(layers)):
            if i == len(layers) - 1:
                self.weights.append((2 * np.random.random((layers[i - 1] + 1, layers[i])) - 1) * 0.25)
            else:
                self.weights.append((2 * np.random.random((layers[i - 1] + 1, layers[i] + 1)) - 1) * 0.25)
    # fit function accepts input data, training data, a learning rate,
    # and the number of epochs to run, and then performs a forward pass,
    # backpropagation, and updates weights for each epoch.

    def model_fit(self, input_values, label, learning_rate=0.2, EPOCH=10000):

        input_values = np.atleast_2d(input_values)
        t = np.ones([input_values.shape[0], input_values.shape[1] + 1])
        t[:, 0:-1] = input_values  # add bias
        input_values = t
        label = np.array(label)

        for i in range(EPOCH):
            ran = np.random.randint(input_values.shape[0])
            curr = [input_values[ran]]

            for j in range(len(self.weights)):
                # forward
                curr.append(self.activation(np.dot(curr[j], self.weights[j])))

            err = label[ran] - curr[-1]
            delt = [err * self.activation_der(curr[-1])]

            for j in range(len(curr) - 2, 0, -1):
                # back
                delt.append(delt[-1].dot(self.weights[1].T) * self.activation_der(curr[1]))

            delt.reverse()

            for k in range(len(self.weights)):
                # update
                l = np.atleast_2d(curr[k])  # layer
                d = np.atleast_2d(delt[k])  # delta
                self.weights[k] += learning_rate * l.T.dot(d)

    #takes in input data and uses the chosen activation function and weights to output a
    # prediction based on what the neural network has already processed.

    def predict_outcome(self, input_data):
        input_data = np.array(input_data)
        t = np.ones(input_data.shape[0] + 1)
        t[0:-1] = input_data
        prediction = t
        for i in range(0, len(self.weights)):
            prediction = self.activation(np.dot(prediction, self.weights[i]))
        return prediction