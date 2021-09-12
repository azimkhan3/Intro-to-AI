import random
import numpy as np
#The Neural Network will be comprised of these steps:
#
#
# Taking the input values
# Making Predictions
# Comparing Predictions to Desired values
# Altering layers to make better predictions
#
#WE will start off by adding activation functions. We tried several other functions but sigmoid and tanh were the best options

def sigmoid(input):
    return (1 / (1 + np.exp(-input)))

def slope_sigmoid(input):
    return (np.exp ** (-input)) / ((1 + (np.exp ** (-input))) ** 2)

def tanh(input):
    return np.tanh(input)

def slope_tanh(input):  # derivative of tanh. this represents the slope

    return 1.0 - np.tanh(input) ** 2

    # the sigmoid function limits the output to a range between 0 and 1.

class NeuNet:
    def __init__(self, layers, af='sigmoid'): #we can also try the tanh one

        #AF = Activation_Function()
        if af == 'tanh':
            self.activation = tanh

            self.activation_der = slope_tanh

        elif af == 'sigmoid':
            self.activation = sigmoid

            self.activation_der = slope_sigmoid

        #Weights are learnable parameters inside the network. A teachable neural network will randomize the weight values
        # before learning initially begins


        self.weights = [] #initializing a list to store all the weights

        # initializing random weights and iterating through all the layers

        for i in range(1, len(layers)):
            # SETTING WEIGHT depending on direction
            if i == len(layers) - 1:

                self.weights.append((np.random.random((layers[i - 1] + 1, layers[i])) - 1))
            # SETTING WEIGHT depending on direction
            else:
                self.weights.append((np.random.random((layers[i - 1] + 1, layers[i] + 1)) - 1))

    #input is what we are putting in initially, output is what we want, epoch is the number of cycles
    def model_fit(self, training_input, output, rate=0.2, EPOCH=10000):

        #we will be taking in our data generated from MegaMind
        training_input = np.atleast_2d(training_input)

        #initializing so that everying in list is 1
        train = np.ones([training_input.shape[0], training_input.shape[1] + 1])

        #BIAS: sets the result when all the other independent variables are equal to zero,
        # We will be setting it equal to the input values so the ones go away
        train[:, 0:-1] = training_input

        training_input = train

        output = np.array(output)

        for i in range(EPOCH):
            random_values = np.random.randint(training_input.shape[0])
            current = [training_input[random_values]]
            # propagates forward
            for j in range(len(self.weights)):

                current.append(self.activation(np.dot(current[j], self.weights[j])))

            error = output[random_values] - current[-1] #calcuate the error between current and random value
            delta = [error * self.activation_der(current[-1])] #using the derivatives  to set up the back propogation based on error
            #Propagates backwards
            for j in range(len(current) - 2, 0, -1):

                delta.append(delta[-1].dot(self.weights[1].T) * self.activation_der(current[1]))

            delta.reverse()

            for k in range(len(self.weights)):

                layer = np.atleast_2d(current[k])
                delta = np.atleast_2d(delta[k])
                self.weights[k] += rate * layer.T.dot(delta)

    #takes in input data and uses the chosen activation function and weights to output a
    # prediction based on what the neural network has already processed.

    def predict_outcome(self, training_input):

        training_input = np.array(training_input)

        training = np.ones(training_input.shape[0] + 1)

        training[0:-1] = training_input

        prediction = training

        for i in range(0, len(self.weights)):
            # takes a dot product. This tells us how similar in terms of direction and magnitude the 2 vectors are
            prediction = self.activation(np.dot(prediction, self.weights[i]))

        return prediction