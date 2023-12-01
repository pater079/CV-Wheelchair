from datetime import datetime
import cv2
from handtrackingmodule import handTracker
import random
import json
from data_handling import handle_data
import base64
import gzip
import numpy as np


def main_loop_tests():
    """
    This function will run a loop that asks the user to change their hand position and will record the data of the user doing it
    ALSO this function gets your camera and runs some deep learning to figure out the 21 points of your hand
    the points go as follows.
    0: wrist
    1-4 Thumb (from base to tip so 1 is the base of the thumb and 4 is the tip of the thumb)
    5-8 index finger
    9-12 middle finger
    13-16 ring finger
    17-20 little finger (winter is coming)
    :param: NA
    :return:
    """
    cap = cv2.VideoCapture(0)
    tracker = handTracker()

    desired_fps = 30

    frame_accumulator = []  # To store frames for the last 3 seconds
    image_with_hand_accumulator = [] # the image quality is 480 x 640
    image_no_hand_accumulator = []
    start_time = datetime.now()  # Start time of the 5-second interval
    start_time_frames = datetime.now()
    text = ''
    rand_dict = {}
    font_color = (0,0,0)
    data_txt = handle_data('total_data/data.txt')
    labels_txt = handle_data('total_data/labels.txt')
    while True:

        success, image = cap.read()

        image_no_hand_accumulator.append(image)
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)

        blue_shift = 20  # You can adjust this value as needed

        # Split the image into its color channels (BGR order)
        b, g, r = cv2.split(image)

        b_shifted = np.clip(b + blue_shift, 0, 255)
        image = cv2.merge((b_shifted, g, r))

        if len(lmList) != 0:
            if lmList[20][1] < 30:
                print('Left')
            elif lmList[4][1] > 600:
                print('Right')

        # image_with_hand_accumulator.append(image)
        # image = add_text_to_image(image=image, text=text, font_color=font_color)
        cv2.imshow("Video", image)
        frame_accumulator.append(lmList)

        # Calculate the time taken for processing and display
        # frame_end_time = datetime.now()
        # elapsed_time = frame_end_time - frame_start_time
        # print(f"Frame processing time: {elapsed_time}")

        # Check if 5 seconds have elapsed
        current_time = datetime.now()
        if (current_time - start_time).total_seconds() >= 5:
            if not text == '':


                start_time = current_time
                start_time_frames = current_time
                store_data_data = [rand_dict['text'], frame_accumulator]
                data_txt.store_data(store_data_data)
                num_lines = data_txt.count_lines_in_file()
                image_data_with_dots = np.array(image_with_hand_accumulator)
                # np.save(f'total_data/data_with_dots_files/image_data{num_lines}.npy', image_data_with_dots)
                image_data_with_no_dots = np.array(image_no_hand_accumulator)
                # np.save(f'total_data/data_no_dots_files/image_data{num_lines}.npy', image_data_with_no_dots)
                labels_txt.store_data(data=[rand_dict['text2']])
                rand_dict = get_random()
                text = rand_dict['text']
                font_color = rand_dict['font_color']
                image_with_hand_accumulator = []
                image_no_hand_accumulator = []
            else:
                rand_dict = get_random()
                text = rand_dict['text']
                font_color = rand_dict['font_color']
                image_with_hand_accumulator = []
                image_no_hand_accumulator = []

        if (current_time - start_time_frames).total_seconds() >= 3:
            if not text == '':
                start_time_frames = current_time
                frame_accumulator = []
                image_with_hand_accumulator = []
                image_no_hand_accumulator = []
                text = rand_dict['text2']
                font_color = rand_dict['font_color2']

        key = cv2.waitKey(1000 // desired_fps)

        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def add_text_to_image(image, text,font_color, position=(100, 300), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, font_thickness=2):
    """
    Adds text to an image and returns the modified image.

    Args:
        image (numpy.ndarray): The input image.
        text (str): The text to be added.
        position (tuple): The (x, y) coordinates where the text will be placed.
        font (int): The font type (e.g., cv2.FONT_HERSHEY_SIMPLEX).
        font_scale (float): The font scale factor.
        font_color (tuple): The font color in BGR format.
        font_thickness (int): The thickness of the text.

    Returns:
        numpy.ndarray: The modified image with text.
    """

    output_image = image.copy()
    cv2.putText(output_image, text, position, font, font_scale, font_color, font_thickness)
    return output_image


def get_random():
    """
    randomly returns the text hand down, hand up, hand steady and the font color
    :return: text and font color
    """
    random_num = random.randint(0, 8)
    # 0 will be point hand down
    # 1 will be point hand up
    # 2 will be keep hand steady
    if random_num == 0:
        text = 'Start with HAND DOWN, '
        text2 = 'Than go to HAND MIDDLE'
        font_color = (255, 255, 0)
        font_color2 = (0, 255, 255)
    elif random_num == 1:
        text = 'Start with HAND DOWN, '
        text2 = 'Than go to HAND UP'
        font_color = (255, 255, 0)
        font_color2 = (255, 0, 255)
    elif random_num == 6:
        text = 'Start with HAND DOWN, '
        text2 = 'Than KEEP STILL'
        font_color = (255, 255, 0)
        font_color2 = (255, 255, 0)

    elif random_num == 2:
        text = 'Start with HAND MIDDLE, '
        text2 = 'Than go to HAND DOWN'
        font_color = (0, 255, 255)
        font_color2 = (255, 255, 0)
    elif random_num == 3:
        text = 'Start with HAND MIDDLE, '
        text2 = 'Than go to HAND UP'
        font_color = (0, 255, 255)
        font_color2 = (255, 0, 255)
    elif random_num == 4:
        text = 'Start with HAND MIDDLE, '
        text2 = 'Than KEEP STILL'
        font_color = (0, 255, 255)
        font_color2 = (0, 255, 255)

    elif random_num == 5:
        text = 'Start with HAND UP, '
        text2 = 'Than go to HAND DOWN'
        font_color = (255, 0, 255)
        font_color2 = (255, 255, 0)
    elif random_num == 7:
        text = 'Start with HAND UP, '
        text2 = 'Than KEEP STILL'
        font_color = (255, 0, 255)
        font_color2 = (255, 0, 255)
    elif random_num == 8:
        text = 'Start with HAND UP, '
        text2 = 'Than go to HAND MIDDLE'
        font_color = (255, 0, 255)
        font_color2 = (0, 255, 255)
    return {'text': text, 'font_color': font_color, "random_num": random_num, 'text2': text2, 'font_color2': font_color2}


def get_random_start():
    random_num = random.randint(0, 2)
    # 0 will be point hand down
    # 1 will be point hand up
    # 2 will be keep hand steady
    if random_num == 0:
        text = 'HAND DOWN'
        font_color = (255, 255, 0)
    elif random_num == 1:
        text = 'HAND UP'
        font_color = (255, 0, 255)
    else:
        text = 'KEEP HAND STEADY'
        font_color = (0, 255, 255)
    return text, font_color


def start_function():
    data_txt = handle_data('total_data/data.txt')
    labels_txt = handle_data('total_data/labels.txt')
    input_str = input('Hello, would you like to (gather) data or (view) data or (combine) data: ')
    if input_str.lower() == 'gather':
        print('Press q to exit out')
        num_lines = data_txt.count_lines_in_file()
        data_txt.delete_last_n_lines() # deletes last 3 lines of the txt file incase when shutting off you moved your hand weird
        labels_txt.delete_last_n_lines()
        data_txt.delete_video_data([num_lines, num_lines-1, num_lines-2])
        main_loop_tests()
    if input_str.lower() == 'view':
        for x in range(data_txt.count_lines_in_file()):
            data = data_txt.run_txt_to_data(x + 1)
            print(data)
    if input_str.lower() == 'combine':
        raise 'error'
        data_files = ['data.txt', 'data_1.txt', 'data_2.txt', 'data_3.txt', 'data_4.txt', 'data_5.txt', 'data_6.txt',  'data_7.txt']
        total_data = []
        for data_file in data_files:
            temp_data = []
            for x in range(count_lines_in_file(filename=data_file)):
                data = run_txt_to_data(x + 1)
                temp_data.append(data)
            total_data.append(temp_data)
            # for y in total_data:
            #     for z in y:
            #         print(z)

        # creates a new file called total_data with all the data
        # for data4 in total_data:
        #     for data3 in data4:
        #         store_data(data3, filename='total_data.txt')


import unittest
from PIL import Image

class TestImageFileType(unittest.TestCase):
    def test_is_png(self):
        # Provide the file path of the image you want to test
        image_file_path = 'your_image.png'  # Replace with the path to your image file

        try:
            # Try to open the file with Pillow (PIL)
            with Image.open(image_file_path) as img:
                # Check if the image format is 'PNG'
                self.assertEqual(img.format, 'PNG')
        except Exception as e:
            # Catch any exceptions (e.g., if the file is not a valid image)
            self.fail(f"Error while checking the image format: {str(e)}")

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    while True:
        start_function()
