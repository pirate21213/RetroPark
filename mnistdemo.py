import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print("Tensorflow version:", tf.__version__)

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 784).astype("float32") / 255.0   # Keep dimension, image w*h / normalize
x_test = x_test.reshape(-1, 784).astype("float32") / 255.0   # Keep dimension, image w*h / normalize

model = keras.Sequential(
    [
        layers.Dense(512, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(10),
    ]
)

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.Adam(lr=0.001),
    metrics=["accuracy"],
)

model.fit(x_train, y_train, batch_size=32, epochs=5)
model.evaluate(x_test, y_test, batch_size=32)
