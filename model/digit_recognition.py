from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Input, Conv2D, MaxPool2D, Dropout
from tensorflow.keras.callbacks import EarlyStopping

(X_train, y_train), (X_test, y_test) = mnist.load_data()

early_stopping_callback = EarlyStopping(monitor='val_loss', patience=15, min_delta=0.04)

model = Sequential(
    [
        # Input(shape=[28, 28, 1]),
        Conv2D(
            filters=32,
            kernel_size=(3, 3),
            strides=(1, 1),
            padding='same',
            activation='relu',
            input_shape=(28, 28, 1)
        ),
        MaxPool2D(
            pool_size=(2, 2),
            strides=None,  # (2,2)
            padding='same'
        ),
        Dropout(rate=0.2, seed=7),
        Conv2D(
            filters=16,
            kernel_size=(3, 3),
            strides=(1, 1),
            padding='same',
            activation='relu'
        ),
        MaxPool2D(
            pool_size=(2, 2),
            strides=None,  # (2,2)
            padding='same'
        ),
        Dropout(rate=0.15, seed=7),
        Flatten(),
        Dense(256, activation="relu"),
        Dense(64, activation="relu"),
        Dense(10, activation="softmax"),
    ]
)

model.compile(
    loss="sparse_categorical_crossentropy", metrics=["accuracy"], optimizer="adam"
)

history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    batch_size=512,
    epochs=50,
    shuffle=True,
    callbacks=[early_stopping_callback]
).history

model.save("digit_recognition_model")
