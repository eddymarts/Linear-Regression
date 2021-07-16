import numpy as np
from mini_batch import MiniBatch

class LinearRegression:
    """
    Class representing Linear Regression predicting model
    implemented from scratch.
    Only accepts numerical features.
    
    Methods created to match the ones used by Sci-kit Learn models.
    """
    def __init__(self, n_features) -> None:
        self.w = np.random.randn(n_features)
        self.b = np.random.randn()

    def _get_MSE(self, y_hat, y):
        """
        Gets Mean Squared Error between predictions (y_hat) and actual value (y).
        """
        return np.mean((y_hat - y)**2)
    
    def _get_validation_loss(self, X_val, y_val):
        y_hat_val = self.predict(X_val)
        validation_loss = self._get_MSE(y_hat_val, y_val)
        return np.mean(validation_loss)
    
    def _get_gradients(self, X, y, y_hat):
        """
        Gets the gradients for the Linear Regression parameters
        when optimising them for the given data.

        INPUTS: X -> Matrix of numerical datapoints.
                y -> Target for each row of X.
                y_hat -> Current linear prediction of each target.
        """
        error = y_hat - y
        grad_w = 2 * np.mean(np.matmul(error, X), axis=0)
        grad_b = 2 * np.mean(error)
        return grad_w, grad_b
    
    def _update_parameters(self, lr, X_batch, y_batch, y_hat):
        """
        Updates the parameters of the model by substracting the
        product of the learning rate and the gradient of the loss
        with respect to each parameter.
        """
        grad_w, grad_b = self._get_gradients(X_batch, y_batch, y_hat)
        self.w -= lr * grad_w
        self.b -= lr * grad_b


    def predict(self, X):
        """
        Predicts the value of an output for each row of X
        using the fitted Linear Regression model.
        """
        return np.matmul(X, self.w) + self.b

    def fit(self, X, y, X_val, y_val, lr = 0.001, epochs=1000,
            acceptable_error=0.001, return_loss=False):
        """
        Optimises the Linear Regression parameters for the given data.

        INPUTS: X -> Matrix of numerical datapoints.
                y -> Target for each row of X.
                lr -> Learning Rate of Mini-batch Gradient Descent.
                        default = 0.001.
                epochs -> Number of iterationns of Mini-Batch Gradient Descent.
                        default = 100
        """
        mean_loss = []
        mean_validation_loss = []
        for epoch in range(epochs):
            minibatches = MiniBatch(X, y)
            loss_per_epoch = []
            validation_loss_per_epoch = []
            for X_batch, y_batch in minibatches:
                y_hat = self.predict(X_batch)
                loss = self._get_MSE(y_hat, y_batch)
                self._update_parameters(lr, X_batch, y_batch, y_hat)
                loss_per_epoch.append(loss)
                validation_loss_per_epoch.append(self._get_validation_loss(X_val, y_val))
            mean_loss.append(np.mean(loss_per_epoch))
            mean_validation_loss.append(np.mean(validation_loss_per_epoch))

            if epoch > 2 and abs(mean_validation_loss[-2]- mean_validation_loss[-1]) < acceptable_error:
                print(f"Validation loss for epoch {epoch} is {mean_validation_loss[-1]}")
                break

        if return_loss:
            return {'training_set': mean_loss,
                    'validation_set': mean_validation_loss}