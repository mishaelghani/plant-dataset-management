# -*- coding: utf-8 -*-
"""VGG16

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pWtn-9Uoc1zHriRmyuTXowM30rx2w4o5
"""

path = "/content/drive/MyDrive/2023.Cabai/Dataset.Resize.Pad.4"

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

model = tf.keras.applications.vgg16.VGG16(
    include_top=True, weights=None, classes=4, input_shape=(224, 224, 3)
)
model.compile(
    optimizer="adam",
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=["accuracy"],
)

callback = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=5, start_from_epoch=0
)

history = model.fit(train_ds, epochs=1, validation_data=val_ds, callbacks=[callback])

with open("vgg16.pkl", "wb") as f:
    pickle.dump(history, f)
