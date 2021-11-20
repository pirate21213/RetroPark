import time
import os
import shutil
import csv
import numpy as np
import tensorflow as tf
from persona_trainer import edgify_image_from_path
from image_cutter import get_spotID

tf.get_logger().setLevel('ERROR')

TARGET_SIZE = (64, 32)
print("Summoning Quorum...")

# Placed here to speed up detect_occupancy_keras_list, the other three functions would also benefit from this but as
# they aren't being used, I won't clutter the top with it
tom = tf.keras.models.load_model("./Personalities/Tom/", compile=True)
jerry = tf.keras.models.load_model("./Personalities/Jerry/", compile=True)
tweety = tf.keras.models.load_model("./Personalities/Tweety/", compile=True)


def detect_occupancy(image_path, debug=False):
    start_time = time.time()
    from persona_trainer import create_model
    class_names = ['nocc', 'occ']
    # print(tf.version.VERSION)

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
    tom_img = tf.keras.preprocessing.image.load_img(image_path, target_size=TARGET_SIZE)
    tom_img_array = tf.keras.preprocessing.image.img_to_array(tom_img)
    tom_img_array = tf.expand_dims(tom_img_array, 0)

    jerry_path = edgify_image_from_path(image_path, r'./tempedgy/', style="Canny")
    jerry_img = tf.keras.preprocessing.image.load_img(jerry_path, target_size=TARGET_SIZE)
    jerry_img_array = tf.keras.preprocessing.image.img_to_array(jerry_img)
    jerry_img_array = tf.expand_dims(jerry_img_array, 0)

    tweety_path = edgify_image_from_path(image_path, r'./tempedgy/', style="Sobel")
    tweety_img = tf.keras.preprocessing.image.load_img(tweety_path, target_size=TARGET_SIZE)
    tweety_img_array = tf.keras.preprocessing.image.img_to_array(tweety_img)
    tweety_img_array = tf.expand_dims(tweety_img_array, 0)

    # Clean up temp directories
    shutil.rmtree('./tempedgy/')

    # Run the predictions
    predictions = [tom_probability.predict(tom_img_array), jerry_probability.predict(jerry_img_array),
                   tweety_probability.predict(tweety_img_array)]
    score = [tf.nn.softmax(predictions[0][0]), tf.nn.softmax(predictions[1][0]), tf.nn.softmax(predictions[2][0])]
    if debug:
        print(
            "Tom thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
            "percent confidence.".format(
                class_names[np.argmax(score[0])], 100 * np.max(score[0]), class_names[np.argmin(score[0])],
                                                  100 * np.min(score[0])))

        print(
            "Jerry thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
            "percent confidence.".format(
                class_names[np.argmax(score[1])], 100 * np.max(score[1]), class_names[np.argmin(score[1])],
                                                  100 * np.min(score[1])))
        print(
            "Tweety thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
            "percent confidence.".format(
                class_names[np.argmax(score[2])], 100 * np.max(score[2]), class_names[np.argmin(score[2])],
                                                  100 * np.min(score[2])))

    tom_conf = 100 * np.max(score[0])
    jerry_conf = 100 * np.max(score[1])
    tweety_conf = 100 * np.max(score[2])

    # Address the quorum for the final result
    # score[x][0] is nocc | score[x][1] is occ
    quorum_scores = [score[0][0] + score[1][0] + score[2][0], score[0][1] + score[1][1] + score[2][1]]
    judgement = ''

    # negative tug shows occ, positive tug shows nocc
    tug = quorum_scores[0] - quorum_scores[1]

    if tug > 0:
        judgement = 'nocc'
        confidence = np.sum(quorum_scores[0]) / 3
    else:
        judgement = 'occ'
        confidence = np.sum(quorum_scores[1]) / 3
    think_time = time.time() - start_time
    if debug:
        print("The quorum thinks that the spot is {} with a combined confidence of {:.2f}%. The tug is {:.4f}".format(
            judgement, confidence * 100, tug))
        print('occupancy detection took %s seconds to run' % (time.time() - start_time))
    # Convert tug from a tensor to a float
    scalar_tug = tug.numpy()

    return judgement, confidence, scalar_tug, think_time, tom_conf, jerry_conf, tweety_conf


def detect_occupancy_list(image_list, out_file, debug=False):
    from persona_trainer import create_model
    class_names = ['nocc', 'occ']
    # print(tf.version.VERSION)

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

    f = open(out_file, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['spotID', 'judgement', 'confidence', 'tug', 'dtime', 'tom_conf', 'jerry_conf', 'tweety_conf'])
    for image_path in image_list:
        start_time = time.time()
        # isolate the image into its own dataset
        tom_img = tf.keras.preprocessing.image.load_img(image_path, target_size=TARGET_SIZE)
        tom_img_array = tf.keras.preprocessing.image.img_to_array(tom_img)
        tom_img_array = tf.expand_dims(tom_img_array, 0)

        jerry_path = edgify_image_from_path(image_path, r'./tempedgy/', style="Canny")
        jerry_img = tf.keras.preprocessing.image.load_img(jerry_path, target_size=TARGET_SIZE)
        jerry_img_array = tf.keras.preprocessing.image.img_to_array(jerry_img)
        jerry_img_array = tf.expand_dims(jerry_img_array, 0)

        tweety_path = edgify_image_from_path(image_path, r'./tempedgy/', style="Sobel")
        tweety_img = tf.keras.preprocessing.image.load_img(tweety_path, target_size=TARGET_SIZE)
        tweety_img_array = tf.keras.preprocessing.image.img_to_array(tweety_img)
        tweety_img_array = tf.expand_dims(tweety_img_array, 0)

        # Clean up temp directories
        shutil.rmtree('./tempedgy/')

        # Run the predictions
        predictions = [tom_probability.predict(tom_img_array), jerry_probability.predict(jerry_img_array),
                       tweety_probability.predict(tweety_img_array)]
        score = [tf.nn.softmax(predictions[0][0]), tf.nn.softmax(predictions[1][0]), tf.nn.softmax(predictions[2][0])]
        if debug:
            print(
                "Tom thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
                "percent confidence.".format(
                    class_names[np.argmax(score[0])], 100 * np.max(score[0]), class_names[np.argmin(score[0])],
                                                      100 * np.min(score[0])))

            print(
                "Jerry thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
                "percent confidence.".format(
                    class_names[np.argmax(score[1])], 100 * np.max(score[1]), class_names[np.argmin(score[1])],
                                                      100 * np.min(score[1])))
            print(
                "Tweety thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
                "percent confidence.".format(
                    class_names[np.argmax(score[2])], 100 * np.max(score[2]), class_names[np.argmin(score[2])],
                                                      100 * np.min(score[2])))

        tom_conf = 100 * np.max(score[0])
        jerry_conf = 100 * np.max(score[1])
        tweety_conf = 100 * np.max(score[2])

        # Address the quorum for the final result
        # score[x][0] is nocc | score[x][1] is occ
        quorum_scores = [score[0][0] + score[1][0] + score[2][0], score[0][1] + score[1][1] + score[2][1]]
        judgement = ''

        # negative tug shows occ, positive tug shows nocc
        tug = quorum_scores[0] - quorum_scores[1]

        if tug > 0:
            judgement = 'nocc'
            confidence = np.sum(quorum_scores[0]) / 3
        else:
            judgement = 'occ'
            confidence = np.sum(quorum_scores[1]) / 3
        dtime = time.time() - start_time
        if debug:
            print(
                "The quorum thinks that the spot is {} with a combined confidence of {:.2f}%. The tug is {:.4f}".format(
                    judgement, confidence * 100, tug))
            print('occupancy detection took %s seconds to run' % (time.time() - start_time))
        # Convert tug from a tensor to a float
        scalar_tug = tug.numpy()
        print("=>{} is {} with {:2f} confidence, the tug is {:4f}. dtime={:4f}".format(image_path, judgement, confidence, tug, dtime))
        writer.writerow([get_spotID(image_path), judgement, confidence, scalar_tug, dtime, tom_conf, jerry_conf, tweety_conf])
    f.close()


def detect_occupancy_keras_list(image_list, out_file, debug=False):
    start_time = time.time()
    class_names = ['nocc', 'occ']

    f = open(out_file, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['spotID', 'judgement', 'confidence', 'tug', 'dtime', 'tom_conf', 'jerry_conf', 'tweety_conf'])
    for image_path in image_list:
        start_time = time.time()
        # isolate the image into its own dataset
        tom_img = tf.keras.preprocessing.image.load_img(image_path, target_size=TARGET_SIZE)
        tom_img_array = tf.keras.preprocessing.image.img_to_array(tom_img)
        tom_img_array = tf.expand_dims(tom_img_array, 0)

        jerry_path = edgify_image_from_path(image_path, r'./tempedgy/', style="Canny")
        jerry_img = tf.keras.preprocessing.image.load_img(jerry_path, target_size=TARGET_SIZE)
        jerry_img_array = tf.keras.preprocessing.image.img_to_array(jerry_img)
        jerry_img_array = tf.expand_dims(jerry_img_array, 0)

        tweety_path = edgify_image_from_path(image_path, r'./tempedgy/', style="Sobel")
        tweety_img = tf.keras.preprocessing.image.load_img(tweety_path, target_size=TARGET_SIZE)
        tweety_img_array = tf.keras.preprocessing.image.img_to_array(tweety_img)
        tweety_img_array = tf.expand_dims(tweety_img_array, 0)

        # Clean up temp directories
        shutil.rmtree('./tempedgy/')

        # Run the predictions
        predictions = [tom.predict(tom_img_array), jerry.predict(jerry_img_array),
                       tweety.predict(tweety_img_array)]
        score = [tf.nn.softmax(predictions[0][0]), tf.nn.softmax(predictions[1][0]), tf.nn.softmax(predictions[2][0])]
        if debug:
            print(
                "Tom thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
                "percent confidence.".format(
                    class_names[np.argmax(score[0])], 100 * np.max(score[0]), class_names[np.argmin(score[0])],
                                                      100 * np.min(score[0])))

            print(
                "Jerry thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
                "percent confidence.".format(
                    class_names[np.argmax(score[1])], 100 * np.max(score[1]), class_names[np.argmin(score[1])],
                                                      100 * np.min(score[1])))
            print(
                "Tweety thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
                "percent confidence.".format(
                    class_names[np.argmax(score[2])], 100 * np.max(score[2]), class_names[np.argmin(score[2])],
                                                      100 * np.min(score[2])))

        tom_conf = 100 * np.max(score[0])
        jerry_conf = 100 * np.max(score[1])
        tweety_conf = 100 * np.max(score[2])

        # Address the quorum for the final result
        # score[x][0] is nocc | score[x][1] is occ
        quorum_scores = [score[0][0] + score[1][0] + score[2][0], score[0][1] + score[1][1] + score[2][1]]
        judgement = ''

        # negative tug shows occ, positive tug shows nocc
        tug = quorum_scores[0] - quorum_scores[1]

        if tug > 0:
            judgement = 'nocc'
            confidence = np.sum(quorum_scores[0]) / 3
        else:
            judgement = 'occ'
            confidence = np.sum(quorum_scores[1]) / 3
        dtime = time.time() - start_time
        if debug:
            print("The quorum thinks that the spot is {} with a combined confidence of {:.2f}%. The tug is {:.4f}".format(
                judgement, confidence * 100, tug))
            print('occupancy detection took %s seconds to run' % (time.time() - start_time))
        # Convert tug from a tensor to a float
        scalar_tug = tug.numpy()
        print(
            "=>{} is {} with {:2f} confidence, the tug is {:4f}. dtime={:4f}".format(image_path, judgement, confidence,
                                                                                     tug, dtime))
        writer.writerow(
            [get_spotID(image_path), judgement, confidence, scalar_tug, dtime, tom_conf, jerry_conf, tweety_conf])
    f.close()


def detect_occupancy_keras(image_path, debug=False):
    class_names = ['nocc', 'occ']

    tom = tf.keras.models.load_model("./Personalities/Tom/", compile=True)
    jerry = tf.keras.models.load_model("./Personalities/Jerry/", compile=True)
    tweety = tf.keras.models.load_model("./Personalities/Tweety/", compile=True)

    # isolate the image into its own dataset
    tom_img = tf.keras.preprocessing.image.load_img(image_path, target_size=TARGET_SIZE)
    tom_img_array = tf.keras.preprocessing.image.img_to_array(tom_img)
    tom_img_array = tf.expand_dims(tom_img_array, 0)

    jerry_path = edgify_image_from_path(image_path, r'./tempedgy/', style="Canny")
    jerry_img = tf.keras.preprocessing.image.load_img(jerry_path, target_size=TARGET_SIZE)
    jerry_img_array = tf.keras.preprocessing.image.img_to_array(jerry_img)
    jerry_img_array = tf.expand_dims(jerry_img_array, 0)

    tweety_path = edgify_image_from_path(image_path, r'./tempedgy/', style="Sobel")
    tweety_img = tf.keras.preprocessing.image.load_img(tweety_path, target_size=TARGET_SIZE)
    tweety_img_array = tf.keras.preprocessing.image.img_to_array(tweety_img)
    tweety_img_array = tf.expand_dims(tweety_img_array, 0)

    # Clean up temp directories
    shutil.rmtree('./tempedgy/')

    # Run the predictions
    predictions = [tom.predict(tom_img_array), jerry.predict(jerry_img_array),
                   tweety.predict(tweety_img_array)]
    score = [tf.nn.softmax(predictions[0][0]), tf.nn.softmax(predictions[1][0]), tf.nn.softmax(predictions[2][0])]
    if debug:
        print(
            "Tom thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
            "percent confidence.".format(
                class_names[np.argmax(score[0])], 100 * np.max(score[0]), class_names[np.argmin(score[0])],
                                                  100 * np.min(score[0])))

        print(
            "Jerry thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
            "percent confidence.".format(
                class_names[np.argmax(score[1])], 100 * np.max(score[1]), class_names[np.argmin(score[1])],
                                                  100 * np.min(score[1])))
        print(
            "Tweety thinks that this image most likely belongs to {} with a {:.2f} percent confidence. {} had {:.2f} "
            "percent confidence.".format(
                class_names[np.argmax(score[2])], 100 * np.max(score[2]), class_names[np.argmin(score[2])],
                                                  100 * np.min(score[2])))

    tom_conf = 100 * np.max(score[0])
    jerry_conf = 100 * np.max(score[1])
    tweety_conf = 100 * np.max(score[2])

    # Address the quorum for the final result
    # score[x][0] is nocc | score[x][1] is occ
    quorum_scores = [score[0][0] + score[1][0] + score[2][0], score[0][1] + score[1][1] + score[2][1]]
    judgement = ''

    # negative tug shows occ, positive tug shows nocc
    tug = quorum_scores[0] - quorum_scores[1]

    if tug > 0:
        judgement = 'nocc'
        confidence = np.sum(quorum_scores[0]) / 3
    else:
        judgement = 'occ'
        confidence = np.sum(quorum_scores[1]) / 3
    think_time = time.time() - start_time
    if debug:
        print("The quorum thinks that the spot is {} with a combined confidence of {:.2f}%. The tug is {:.4f}".format(
            judgement, confidence * 100, tug))
        print('occupancy detection took %s seconds to run' % (time.time() - start_time))
    # Convert tug from a tensor to a float
    scalar_tug = tug.numpy()

    return judgement, confidence, scalar_tug, think_time, tom_conf, jerry_conf, tweety_conf
