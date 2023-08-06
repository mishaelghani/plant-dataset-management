# -*- coding: utf-8 -*-
"""Alexnet

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DDw-aBrSpnfOMiF2yLUja40GjQCRJFgf
"""

path = "C:/Nabell/STTN/Tugas Akhir/Dataset.Resize.Pad.4"

import tensorflow as tf
import numpy as np
import pickle


SEED = 99

# Training, Validasi dan Testing => 70% : 10% : 20%

train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
    path,
    label_mode="categorical",
    image_size=(224, 224),
    subset="both",
    validation_split=0.3,
    seed=SEED,
)

val_batches = tf.data.experimental.cardinality(val_ds)

test_ds = val_ds.take((2 * val_batches) // 3)
val_ds = val_ds.take((2 * val_batches) // 3)

# train_y
train_y = []

for i, label in train_ds:
    for y in label:
        train_y.append(y.numpy())

np.unique(train_y, return_counts=True)

# val_y

val_y = []


for i, label in val_ds:
    for y in label:
        val_y.append(y.numpy())

np.unique(val_y, return_counts=True)

# test_y

test_y = []

for i, label in test_ds:
    for y in label:
        test_y.append(y.numpy())

np.unique(test_y, return_counts=True)

model = tf.keras.models.Sequential()

# Add the Resizing layer as a preprocessing step for input data
tf.keras.model.add(
    tf.keras.layers.experimental.preprocessing.Resizing(
        224, 224, interpolation="bilinear", input_shape=(224, 224, 3)
    )
)

model.add(tf.keras.layers.Conv2D(96, 11, strides=4, padding="same"))
model.add(tf.keras.layers.Lambda(tf.nn.local_response_normalization))
model.add(tf.keras.layers.Activation("relu"))
model.add(tf.keras.layers.MaxPooling2D(3, strides=2))

model.add(tf.keras.layers.Conv2D(256, 5, strides=4, padding="same"))
model.add(tf.keras.layers.Lambda(tf.nn.local_response_normalization))
model.add(tf.keras.layers.Activation("relu"))
model.add(tf.keras.layers.MaxPooling2D(3, strides=2))

model.add(tf.keras.layers.Conv2D(384, 3, strides=4, padding="same"))
model.add(tf.keras.layers.Activation("relu"))

model.add(tf.keras.layers.Conv2D(384, 3, strides=4, padding="same"))
model.add(tf.keras.layers.Activation("relu"))

model.add(tf.keras.layers.Conv2D(256, 3, strides=4, padding="same"))
model.add(tf.keras.layers.Activation("relu"))

model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(4096, activation="relu"))
model.add(tf.keras.layers.Dropout(0.5))

model.add(tf.keras.layers.Dense(4096, activation="relu"))
model.add(tf.keras.layers.Dropout(0.5))

# The last dense layer should have 4 neurons since you mentioned num_classes = 4
model.add(tf.keras.layers.Dense(4, activation="softmax"))

# Print the model summary
model.summary()

model.compile(
    optimizer="adam",
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=["accuracy"],
)

callback = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=5, start_from_epoch=0
)

history = model.fit(train_ds, epochs=1, validation_data=val_ds, callbacks=[callback])

with open("alexnet.pkl", "wb") as f:
    pickle.dump(history, f)
