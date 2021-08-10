from Controller import Controller
import numpy as np
from PIL import ImageGrab
import cv2
import sys
import os
import keyboard
sys.path.append(".")

# auto_canny method from https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/

player = Controller()
path = "C:\\Users\\cshok\\OneDrive\\Desktop\\Projects\\RobloxLearner"
games = ["speed_race_data", "speed_run_data"]
data_path = os.path.join(path, games[1])
os.chdir(data_path)
session_images = []


def auto_canny(image, sigma=0.05):  # 0.93 with blur works well
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


def process_image(image):
    original_image = image
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #processed_img = cv2.medianBlur(processed_img, 9)
    processed_img = auto_canny(processed_img)
    #processed_img = cv2.Canny(processed_img, threshold1=250, threshold2=350)
    #processed_img = cv2.Canny(processed_img, threshold1=33, threshold2=42)
    processed_img = cv2.resize(processed_img, (224, 224))
    return processed_img


def save_key_images(new_screen, player_movements):
    for key in player_movements:
        folder_name = key + "_key"
        folder_location = os.path.join(data_path, folder_name)
        image_name = key + str(len(os.listdir(folder_location))) + ".png"
        cv2.imwrite(os.path.join(folder_location, image_name), new_screen)

        # record all images saved during this recording session
        session_images.append([folder_location, image_name])


def screen_record():
    window_x = 20
    window_y = 20
    window_width = 800
    window_height = 640
    window_y_offset = 80  # 30 for removing window header

    player.display_game(window_x, window_y, window_width, window_height)
    print("recording")
    # Take screenshots, apply image modifiers, and save them to the correct folders
    while True:
        screen = np.array(ImageGrab.grab(
            bbox=(window_x, window_y + window_y_offset, window_width, window_height - window_y_offset)))
        player_movements = player.movement_state()
        # print(player.movement_state())

        new_screen = process_image(screen)
        save_key_images(new_screen, player_movements)

        #cv2.imshow('window', new_screen)
        global session_images
        if cv2.waitKey(10) & keyboard.is_pressed("g"):  # Stop recording
            print("stopped recording")
            cv2.destroyAllWindows()
            session_images = []
            break
        # Remove all images from this recording session and stop recording
        elif keyboard.is_pressed("r"):
            print("deleting recording...")
            for image_data in session_images:
                folder_location = image_data[0]
                image_name = image_data[1]
                try:
                    os.remove(os.path.join(folder_location, image_name))
                except Exception as e:
                    print(e)
                    break
            session_images = []
            break


def main():
    player.start_program_func(screen_record, "q")
    keyboard.wait("x")


if __name__ == "__main__":
    main()
