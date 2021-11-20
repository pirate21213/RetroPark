import tensorflow as tf

print("Optimizing Tom...")

# load the model
model = tf.keras.models.load_model('./Personalities/Tom/')

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open('model.tflite', 'wb') as f:
  f.write(tflite_model)


print("Tom Optimized.")
