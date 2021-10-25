import os

import numpy as np
import tensorflow as tf


def detect_occupancy(image_path):
    from persona_trainer import create_model
    class_names = ['nocc', 'occ']
    print(tf.version.VERSION)

    # Load Personas
    tom = create_model()
    tom.load_weights('./Personalities/Tom/Tom')
    jerry = create_model()
    jerry.load_weights('./Personalities/Jerry/Jerry')
    tweety = create_model()
    tweety.load_weights('./Personalities/Tweety/Tweety')

    # Set up probability
    tom_probability = tf.keras.Sequential([tom, tf.keras.layers.Softmax()])
    jerry_probability = tf.keras.Sequential([jerry, tf.keras.layers.Softmax()])
    tweety_probability = tf.keras.Sequential([tweety, tf.keras.layers.Softmax()])

    # isolate the image into its own dataset
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(640, 320))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    # Run the predictions
    predictions = [tom_probability.predict(img_array), jerry_probability.predict(img_array),
                   tweety_probability.predict(img_array)]
    score = [tf.nn.softmax(predictions[0][0]), tf.nn.softmax(predictions[1][0]), tf.nn.softmax(predictions[2][0])]

    print(
        "Tom thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} percent confidence.".format(
            class_names[np.argmax(score[0])], 100 * np.max(score[0]), class_names[np.argmin(score[0])],
            100 * np.min(score[0])))
    print(
        "Jerry thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} percent confidence.".format(
            class_names[np.argmax(score[1])], 100 * np.max(score[1]), class_names[np.argmin(score[1])],
            100 * np.min(score[1])))
    print(
        "Tweety thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} percent confidence.".format(
            class_names[np.argmax(score[2])], 100 * np.max(score[2]), class_names[np.argmin(score[2])],
            100 * np.min(score[2])))

    # Address the quorum for the final result
    # score[0] is nocc | score[1] is occ
    quorum_scores = [score[0][0] + score[1][0] + score[2][0], score[0][1] + score[1][1] + score[2][1]]
    judgement = ''
    confidence = np.abs(quorum_scores[0] - quorum_scores[1])

    if quorum_scores[0] > quorum_scores[1]:
        judgement = 'nocc'
    else:
        judgement = 'occ'

    print("The quorum thinks that the spot is {} with a combined confidence of {:.2f}%.".format(judgement, confidence))
