import os
from collections import deque
from tensorflow import keras
import cv2
import numpy as np

model = keras.models.load_model('../ML/Models/Hockey_nofight_fight_Accuracy_98.9.h5')
image_height, image_width = 64, 64

classes_list = ["Normal", "Abnormal"]


def predict_on_video(video_file_path , window_size):

    predicted_labels_probabilities_deque = deque(maxlen=window_size)
    video_reader = cv2.VideoCapture(video_file_path)

    while True:
        status, frame = video_reader.read()                                                           # Reading The Frame
        if not status:
            break

        resized_frame = cv2.resize(frame, (image_height, image_width))                                # Resize the Frame to fixed Dimensions

        # Normalize the resized frame by dividing it with 255 so that each pixel value then lies between 0 and 1
        normalized_frame = resized_frame / 255

        # Passing the Image Normalized Frame to the model and receiving Predicted Probabilities.
        predicted_labels_probabilities = model.predict(np.expand_dims(normalized_frame, axis=0))[0]
        decimal_pred = list(map(decimal_str, predicted_labels_probabilities))
        # print(decimal_pred)
        # Appending predicted label probabilities to the deque object
        predicted_labels_probabilities_deque.append(predicted_labels_probabilities)

        # Assuring that the Deque is completely filled before starting the averaging process
        if len(predicted_labels_probabilities_deque) == window_size:
            # Converting Predicted Labels Probabilities Deque into Numpy array
            predicted_labels_probabilities_np = np.array(predicted_labels_probabilities_deque)

            # Calculating Average of Predicted Labels Probabilities Column Wise
            predicted_labels_probabilities_averaged = predicted_labels_probabilities_np.mean(axis=0)

            # Converting the predicted probabilities into labels by returning the index of the maximum value.
            predicted_label = np.argmax(predicted_labels_probabilities_averaged)

            # Accessing The Class Name using predicted label.
            predicted_class_name = classes_list[predicted_label]

            # Overlaying Class Name Text Ontop of the Frame
            cv2.putText(frame, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print(predicted_class_name)
        cv2.imshow('Predicted Frames', frame)

        key_pressed = cv2.waitKey(1)

        if key_pressed == ord('q'):
            break

    cv2.destroyAllWindows()

    # Closing the VideoCapture and VideoWriter objects and releasing all resources held by them.
    video_reader.release()





def decimal_str(x: float, decimals: int = 4) -> str:
    return format(x, f".{decimals}f").lstrip().rstrip('0')


def predict_on_live_video(frame , window_size):

    predicted_labels_probabilities_deque = deque(maxlen=window_size)

    resized_frame = cv2.resize(frame, (image_height, image_width))
    normalized_frame = resized_frame / 255

    predicted_labels_probabilities = model.predict(np.expand_dims(normalized_frame, axis=0))[0]
    decimal_pred = list(map(decimal_str, predicted_labels_probabilities))
    # print(decimal_pred)

    predicted_labels_probabilities_deque.append(predicted_labels_probabilities)

    if len(predicted_labels_probabilities_deque) == window_size:
        predicted_labels_probabilities_np = np.array(predicted_labels_probabilities_deque)
        predicted_labels_probabilities_averaged = predicted_labels_probabilities_np.mean(axis=0)
        predicted_label = np.argmax(predicted_labels_probabilities_averaged)
        predicted_class_name = classes_list[predicted_label]

        cv2.putText(frame, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        print(predicted_class_name)
    # cv2.imshow("", frame)
    # cv2.waitKey(10000)
    return frame


if __name__ == '__main__':
    window_size = 25
    video_path = r"C:\Users\JiN\Desktop\IRIS\Videos\V_15.mp4"
    predict_on_video(video_path, window_size)