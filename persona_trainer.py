import glob
import shutil
import matplotlib.pyplot as plt
import numpy as np
import os
import pathlib
import cv2

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

# from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
print("Tensorflow version:", tf.__version__)

data_dir = pathlib.Path("./Bulk Dataset/")
image_count = len(list(data_dir.glob('*/*.jpg')))
print("Num Images: %s" % image_count)

batch_size = 32
img_height = 64
img_width = 32


def train_model(persona, epochs=10):
    if persona == "Tom":
        print("Retraining Tom")
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)

        class_names = train_ds.class_names
        print("Loaded Training Classes: %s" % class_names)

        AUTOTUNE = tf.data.AUTOTUNE

        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        model = create_model()

        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )
        print("Saving Tom weights...")
        model.save_weights("./Personalities/Tom/Tom")
        print("Tom weights saved.")
        print("Saving Tom model...")
        tf.keras.models.save_model(model, "./Personalities/Tom/")
        print("Tom model saved.")

    elif persona == "Jerry":
        print("Retraining Jerry")
        # make the temporary folder that clones the dataset and performs edge detection on them
        os.makedirs("./temp/occ")
        os.makedirs("./temp/nocc")
        for image in glob.glob("Bulk Dataset/occ/*.jpg"):
            n = cv2.imread(image)
            n = edgify_image(n)
            cv2.imwrite(os.path.join("./temp/occ", os.path.basename(image)), n)
            print(os.path.join("./temp/occ", os.path.basename(image)))
        for image in glob.glob("Bulk Dataset/nocc/*.jpg"):
            n = cv2.imread(image)
            n = edgify_image(n)
            cv2.imwrite(os.path.join("./temp/nocc", os.path.basename(image)), n)
            print(os.path.join("./temp/nocc", os.path.basename(image)))

        # Override Jerry's datapath to be the canny edge detected images
        edgydir = pathlib.Path("./temp/")

        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            edgydir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            edgydir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)

        class_names = train_ds.class_names
        print("Loaded Training Classes: %s" % class_names)

        AUTOTUNE = tf.data.AUTOTUNE

        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        model = create_model()

        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )
        model.save_weights("./Personalities/Jerry/Jerry")
        print("Saving Jerry model...")
        tf.keras.models.save_model(model, "./Personalities/Jerry/")
        print("Jerry model saved.")

    elif persona == "Tweety":
        print("Retraining Tweety")
        # make the temporary folder that clones the dataset and performs edge detection on them
        os.makedirs("./temp/occ")
        os.makedirs("./temp/nocc")
        for image in glob.glob("Bulk Dataset/occ/*.jpg"):
            n = cv2.imread(image)
            n = edgify_image(n, "Sobel")
            cv2.imwrite(os.path.join("./temp/occ", os.path.basename(image)), n)
            print(os.path.join("./temp/occ", os.path.basename(image)))
        for image in glob.glob("Bulk Dataset/nocc/*.jpg"):
            n = cv2.imread(image)
            n = edgify_image(n, "Sobel")
            cv2.imwrite(os.path.join("./temp/nocc", os.path.basename(image)), n)

        # Override Tweety's datapath to be the canny edge detected images
        edgydir = pathlib.Path("./temp/")

        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            edgydir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            edgydir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)

        class_names = train_ds.class_names
        print("Loaded Training Classes: %s" % class_names)

        AUTOTUNE = tf.data.AUTOTUNE

        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        model = create_model()

        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )
        model.save_weights("./Personalities/Tweety/Tweety")
        print("Saving Tweety model...")
        tf.keras.models.save_model(model, "./Personalities/Tweety/")
        print("Tweety model saved.")
        shutil.rmtree('./temp')

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

    if os.path.exists('./temp'):
        shutil.rmtree('./temp')

    print("Result should be occ")
    test_persona("./Processed Images/19_17_38_56.jpg", persona, class_names)
    print("Result should be nocc")
    test_persona("./Processed Images/20_17_38_56.jpg", persona, class_names)
    print("Result should be nocc")
    test_persona("./Processed Images/25_17_38_56.jpg", persona, class_names)


def edgify_image(image, style="Canny"):
    # Blur the image for better edge detection
    image = cv2.GaussianBlur(image, (3, 3), 0)
    if style == "Canny":
        image = cv2.Canny(image=image, threshold1=20, threshold2=80)  # Canny Edge Detection
    elif style == "Sobel":
        image = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)  # Combined X and Y Sobel Edge Detection
    return image


def edgify_image_from_path(image_path, output_path, style="Canny"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # Blur the image for better edge detection
    image = cv2.imread(image_path)
    image = edgify_image(image, style)
    cv2.imwrite(os.path.join(output_path, '{}.jpg'.format(style)), image)
    return os.path.join(output_path, '{}.jpg'.format(style))


def test_persona(image_path, persona, class_names):
    if persona == "Jerry":
        n = cv2.imread(image_path)
        n = edgify_image(n)
        # Check if temp exists, if not make it - Useful if we ever call this function from outside of this script
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
        cv2.imwrite("./temp/testcase.jpg", n)
        image_path = "./temp/testcase.jpg"
    elif persona == "Tweety":
        n = cv2.imread(image_path)
        n = edgify_image(n, "Sobel")
        # Check if temp exists, if not make it - Useful if we ever call this function from outside of this script
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
        cv2.imwrite("./temp/testcase.jpg", n)
        image_path = "./temp/testcase.jpg"
    img = tf.keras.preprocessing.image.load_img(
        image_path, target_size=(img_height, img_width)
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    model = create_model()
    model.load_weights('./Personalities/{}/{}'.format(persona, persona))

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "{} thinks that this image most likely belongs to {} with a {:.2f} percent confidence."
            .format(persona, class_names[np.argmax(score)], 100 * np.max(score))
    )

    # Display the testing image
    disp = cv2.imread(image_path)
    cv2.imshow("This is what {} saw.".format(persona), disp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if os.path.exists('./temp'):
        shutil.rmtree('./temp')


def create_model():
    num_classes = 2

    model = Sequential([
        tf.keras.layers.experimental.preprocessing.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
        layers.Conv2D(8, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model

# Test Cases
# train_model("Tom")
# train_model("Jerry")
# train_model("Tweety")
