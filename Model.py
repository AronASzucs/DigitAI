import tensorflow as tf
import pathlib

dataset_path = "dataset/16px/"
data_dir = pathlib.Path(dataset_path)

# Image properties
batch_size = 100
img_height = 16
img_width = 16

# Load dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    image_size=(img_height, img_width),
    batch_size=batch_size,  
    color_mode="grayscale",  # Use 'rgb' if images are colored
    label_mode="int"
)

# Normalize images (0-255 → 0-1)
normalization_layer = tf.keras.layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))

# Build CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(img_height, img_width, 1)),  # 1 for grayscale
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')  # 10 output classes (0-9)
])

# Compile model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train model
epochs = 100
model.fit(train_ds, epochs=epochs)

# Save trained model
model.save("digit_classifier.h5")

print("Model training complete and saved as 'digit_classifier.h5' 🎉")
