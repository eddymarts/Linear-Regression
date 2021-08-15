from dataset import DataSet
from linear_regression import LinearRegression
from sklearn import datasets
from sklearn.metrics import *
from multiprocessing import cpu_count
import torch
from torch.utils.data import *
import matplotlib.pyplot as plt
import numpy as np

X, y = datasets.load_boston(return_X_y=True)

boston_data = DataSet(X, y, normalize=True, split=True)
train_load = DataLoader(boston_data.splits[0], batch_size=16,
            shuffle=True, num_workers=round(cpu_count()/2))

X_val = boston_data.splits[1].dataset.X
y_val = boston_data.splits[1].dataset.y

linear_regressor = LinearRegression(boston_data.n_features, boston_data.n_labels)
loss = linear_regressor.fit(train_load, X_val, y_val, return_loss=True)

y_hat_val = linear_regressor(X_val)
print(torch.cat((y_val, y_hat_val), dim=1))
print("R^2 score:", r2_score(y_hat_val.detach().numpy(), y))
plt.plot(loss['training'], label="Training set loss")
plt.plot(loss['validation'], label="Validation set loss")
plt.xlabel(f"Epochs\nl={loss['validation'][-1]}")
plt.ylabel("MSE")
plt.show()
# plt.savefig(fname="linear_regression.jpg")


