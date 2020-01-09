from typing import Callable, Optional, Dict

import jax.numpy as tensor
from jax import random

from dnet import activations


class Layer:
    pass


class FC(Layer):
    _prev_units: Optional[int] = None

    def __init__(self, units: int, activation: str = "linear", input_dim: Optional[int] = None) -> None:
        self.units: int = units
        self.act_name: str = activation
        self.activation: Callable[[tensor.array], tensor.array] = getattr(activations, activation)
        if FC._prev_units is None:
            FC._prev_units = input_dim
        self.key = random.PRNGKey(0)
        self.init_weights()

    def init_weights(self) -> None:
        self.key, subkey = random.split(self.key)
        self.weights: tensor.array = random.normal(key=subkey, shape=(self.units, FC._prev_units)) * 0.01
        self.bias: tensor.array = tensor.zeros(shape=(self.units, 1))
        FC._prev_units = self.units

    def forward(self, params: Dict[str, tensor.array], inputs: tensor.array) -> tensor.array:
        z: tensor.array = tensor.dot(params.get("w"), inputs) + params.get("b")
        return self.activation(z)

    def update_weights(self, grad: Dict[str, tensor.array], lr: float) -> None:
        self.weights -= lr * grad.get("w")
        self.bias -= lr * grad.get("b")

    def __str__(self):
        return f"""
        FC layer info :-
        {"-" * 10}
        # units => {self.units},
        Activation fn => {self.act_name},
        Weights dims => {self.weights.shape},
        Bias dims => {self.bias.shape}
        {"-" * 10}"""
