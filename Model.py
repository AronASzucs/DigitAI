import tensorflow as tf

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
        model.add(tf.keras.layers.Flatten(input_shape=(image_dim, image_dim)))
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(128, activation='relu'))




    def predict_num(self, numArray):
        return 0    
    
