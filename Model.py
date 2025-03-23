import tensorflow as tf
from tensorflow import keras
import os
import numpy as np
import time

class NumberModel:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Hides info, warnings, and errors

        print("Made Model Object")

        self.batch_size = 32 
        self.epochs = 20

        self.model_img_dim = None
        self.model = None

    def load_model(self,filepath):
        print("loaded model")


    def save_model(self):
        print("saved model")

    def train_model(self, image_dim, window_instance):
        window_instance = window_instance
        # Checks if dataset/img_dim is found
        if not os.path.isdir("dataset/" + str(image_dim) + "px/"):
            print("ERROR: Can't find dataset/" + str(image_dim) + "px/")
            window_instance.show_error("ERROR: Can't find dataset/" + str(image_dim) + "px/")
            return

        # Checks if all numbers 0-9 sub-directories are found.
        for t in range (10):
            if not os.path.isdir("dataset/" + str(image_dim) + "px/" + str(t) + "/"):
                print("ERROR: Cant find dataset/" + str(image_dim) + "px/" + str(t) + "/")
                window_instance.show_error("ERROR: Can't find dataset/" + str(image_dim) + "px/" + str(t) + "/")
                return
    
        print("All required directories found!")

        dataset_path = "dataset/" + str(image_dim) + "px"

        # Make dataset
        dataset = tf.keras.utils.image_dataset_from_directory(
            dataset_path,
            image_size=(image_dim, image_dim),
            batch_size = self.batch_size,
            color_mode = "grayscale",
            label_mode = "int"
        ).map(lambda x, y: (x / 255.0, y)) # Normalize from 0-255 to 0-1
        
        # Build model
        model = keras.Sequential()
        model.add(keras.layers.Flatten(input_shape=(image_dim, image_dim))) # input layer
        model.add(keras.layers.Dense(128, activation='relu'))
        model.add(keras.layers.Dense(64, activation='relu'))
        model.add(keras.layers.Dense(10, activation='softmax')) #output layer

        # Compile model
        model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        # Train model
        model.fit(dataset, epochs = self.epochs)

        # Save model
        print("Model saved!")
        model.save('model.keras')
        self.model = model
        self.model_img_dim = image_dim

    def predict_num(self, numArray):
        if numArray.shape != (self.model_img_dim, self.model_img_dim):
            print("ERROR: Model dimension =/= image dimension")
            return
        
        prediction = self.model.predict(np.expand_dims(numArray, axis=0))
        return(np.argmax(prediction))
        