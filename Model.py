import tensorflow as tf
from tensorflow import keras

class NumberModel:
    def __init__(self):
        print("Made Model Object")

    def load_model(self,filepath):
        print("loaded model")

    def save_model(self):
        print("saved model")

    def train_model(self, image_dim):
        print("training model")
        model = tf.keras.Sequential()

    def predict_num(self, numArray):
        return 0    
    
