import numpy as np

class NeuralNetwork():
    
    def __init__(self):
        #make the weights for 3x3 matrix
        self.weights = 2 * np.random.random((3, 3)) - 1

    def sigmoid(self, x):
        #activation function using sigmoid function
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        #derivative of sigmoid function
        return x * (1 - x)

    def train(self, training_inputs, training_outputs, epochs = 10000):
        
        #train the model using back propagation 
        for epochs in range(epochs):
            
            #use the predict_outcome function to set the weights
            current_output = self.predicting_outcome(training_inputs)

            #find the error using back propagation
            error = training_outputs - current_output
            
            #make the adjustment for the weights
            adjustments = np.dot(training_inputs.T, error * self.sigmoid_derivative(output))

            self.weights += adjustments

    def predicting_outcome(self, training_inputs):  
        #converting the training input to floats
        inputs = training_inputs.astype(float)
        #using the activation function and weights to make adjustment
        output = self.sigmoid(np.dot(inputs, self.weights))
        return output