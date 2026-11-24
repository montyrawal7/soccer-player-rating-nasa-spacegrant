"""
mlp_inference.py: runs the trained MLP using only NumPy.

The network is trained with PyTorch (train_mlp_pytorch.py) and its weights are
saved to models/mlp_model.npz. A network like this is just matrix
multiplications and ReLU, so the hosted app does not need PyTorch.
"""

import numpy as np


class NumpyMLP:
    def __init__(self, x_mean, x_scale, y_mean, y_std, weights, biases):
        self.x_mean, self.x_scale = x_mean, x_scale
        self.y_mean, self.y_std = y_mean, y_std
        self.weights, self.biases = weights, biases

    @classmethod
    def load(cls, path):
        d = np.load(path)
        n_layers = sum(1 for k in d.files if k.startswith("W"))
        return cls(
            d["x_mean"], d["x_scale"], float(d["y_mean"]), float(d["y_std"]),
            [d[f"W{i}"] for i in range(n_layers)],
            [d[f"b{i}"] for i in range(n_layers)],
        )

    def predict(self, X):
        h = (np.asarray(X, dtype=np.float64) - self.x_mean) / self.x_scale
        last = len(self.weights) - 1
        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            h = h @ W.T + b          # same as PyTorch's Linear layer
            if i < last:
                h = np.maximum(h, 0)  # ReLU
        return h[:, 0] * self.y_std + self.y_mean
