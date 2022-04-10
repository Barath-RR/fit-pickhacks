import argparse
import numpy as np
import os
import cv2
import time
from tensorflow.keras import layers, models, callbacks
from sklearn.utils import class_weight
from pathlib import Path
import time
# Add this in if you require sounds
from playsound import playsound

# Config settings
image_dimensions = (224, 224)
epochs = 10
model_name = 'test_model.h5'
keyboard_spacebar = 32
training_dir = 'train'
mp3file = 'sounds/what.mp3'

def doliveview(soundson):
    mymodel = models.load_model(model_name)
    flag = True
    # Video capture stuff
    videocapture = cv2.VideoCapture(0)
    if not videocapture.isOpened():
        raise IOError('Cannot open webcam')

    while True:
        _, frame = videocapture.read()
        cv2.imwrite('thisframe.png', frame)
        im_color = cv2.imread('thisframe.png')
        im = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)

        im = cv2.resize(im, image_dimensions)
        im = im / 255  # Normalize the image
        im = im.reshape(1, image_dimensions[0], image_dimensions[1], 1)

        predictions = mymodel.predict(im)
        class_pred = np.argmax(predictions)
        conf = predictions[0][class_pred]

        if (soundson and class_pred==1):
            # If slumped with sounds on
            playsound(mp3file)

        im_color = cv2.resize(im_color, (800, 480), interpolation = cv2.INTER_AREA)
        im_color = cv2.flip(im_color, flipCode=1) # flip horizontally

        if (class_pred==1):
            im_color = cv2.putText(im_color, 'Bad', (10, 70),  cv2.FONT_HERSHEY_SIMPLEX, 2,  (0, 0, 255), thickness = 3)
            if flag:
                tim = time.time()
                flag = False
            else:
                if (round(time.time()) - round(tim)) > 2:
                    playsound(mp3file)
                    tim = time.time()
                else:
                    pass
        else:
            im_color = cv2.putText(im_color, 'Good', (10, 70),  cv2.FONT_HERSHEY_SIMPLEX, 2,  (0, 255, 0), thickness = 2)

        msg = 'Confidence {}%'.format(round(int(conf*100)))
        im_color = cv2.putText(im_color, msg, (15, 110),  cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 0, 0), thickness = 2)

        cv2.imshow('', im_color)
        cv2.moveWindow('', 20, 20);
        key = cv2.waitKey(20)

        if key == keyboard_spacebar:
            break

    videocapture.release()
    cv2.destroyAllWindows()



def do_capture_action(action_n, action_label):
    img_count = 0
    output_folder = '{}/action_{:02}'.format(training_dir, action_n)
    print('Capturing samples for {} into folder {}'.format(action_n, output_folder))
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Video capture stuff
    videocapture = cv2.VideoCapture(0)
    if not videocapture.isOpened():
        raise IOError('Cannot open webcam')

    while True:
        _, frame = videocapture.read()
        filename = '{}/{:08}.png'.format(output_folder, img_count)
        cv2.imwrite(filename, frame)
        img_count += 1
        key = cv2.waitKey(1000)
        cv2.imshow('', frame)

        if key == keyboard_spacebar:
            break

    # Clean up
    videocapture.release()
    cv2.destroyAllWindows()


def do_training():
    train_images = []
    train_labels = []
    class_folders = os.listdir(training_dir)

    class_label_indexer = 0
    for c in class_folders:
        print('Training with class {}'.format(c))
        for f in os.listdir('{}/{}'.format(training_dir, c)):
            im = cv2.imread('{}/{}/{}'.format(training_dir, c, f), 0)
            im = cv2.resize(im, image_dimensions)
            train_images.append(im)
            train_labels.append(class_label_indexer)
        class_label_indexer = class_label_indexer + 1

    train_images = np.array(train_images)
    train_labels = np.array(train_labels)

    indices = np.arange(train_labels.shape[0])
    np.random.shuffle(indices)
    images = train_images[indices]
    labels = train_labels[indices]
    train_images = np.array(train_images)
    train_images = train_images / 255  # Normalize image
    n = len(train_images)
    train_images = train_images.reshape(n, image_dimensions[0], image_dimensions[1], 1)

    class_weights = class_weight.compute_sample_weight('balanced', train_labels)
    class_weights={i:j for i,j in enumerate(class_weights)}
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_dimensions[0], image_dimensions[1], 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(len(class_folders), activation='softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',  metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=epochs, class_weight = class_weights)
    model.save(model_name)

def main():
    parser = argparse.ArgumentParser(description='Posture monitor')
    parser.add_argument('--capture-good', help='capture example of good, healthy posture', action='store_true')
    parser.add_argument('--capture-slump', help='capture example of poor, slumped posture', action='store_true')
    parser.add_argument('--train', help='train model with captured images', action='store_true')
    parser.add_argument('--live', help='live view applying model to each frame', action='store_true')
    parser.add_argument('--sound', help='in conjunction with live view will make a sound', action='store_true')
    args = parser.parse_args()

    if args.train:
        do_training()
    elif args.live:
        doliveview(args.sound)
    elif args.capture_good:
        do_capture_action(1, 'Good')
    elif args.capture_slump:
        do_capture_action(2, 'Slumped')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
