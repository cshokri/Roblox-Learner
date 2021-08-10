from Controller import Controller
from fastai.vision.all import *
from PIL import ImageGrab
import cv2
import keyboard
import timeit

# The model needs the label function


def label_func(image):
    name = image.parent.name
    return name[:name.index("_")]


path = "C:\\Users\\cshok\\OneDrive\\Desktop\\Projects\\RobloxLearner"
games = ["speed_race_data", "speed_run_data"]
model_path = os.path.join(path, games[1], "export.pkl")

player = Controller()
agent = load_learner(model_path, cpu=False)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
agent.to(device)
print(device)

# auto_canny method from https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/


def auto_canny(image, sigma=0.05):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


"""
    Time per frame(resnet34)
     - auto_canny and blur       : 0.13510064517750459
     - auto_canny                : 0.1166222815243703
     - blur                      : 0.13222424189249674
     - none                      : 0.11297382911046346
"""


def process_image(image):
    original_image = image
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #processed_img = cv2.medianBlur(processed_img, 9)
    processed_img = auto_canny(processed_img)
    #processed_img = cv2.Canny(processed_img, threshold1=250, threshold2=350)
    #processed_img = cv2.Canny(processed_img, threshold1=33, threshold2=42)
    processed_img = cv2.resize(processed_img, (224, 224))
    return processed_img


def play_game():
    window_x = 20
    window_y = 20
    window_width = 800
    window_height = 640
    window_y_offset = 80  # 30 for removing window header

    player.display_game(window_x, window_y, window_width, window_height)
    keyboard.press("w")
    total = 0
    total_time = 0
    while True:
        start = time.time()
        screen = np.array(ImageGrab.grab(
            bbox=(window_x, window_y + window_y_offset, window_width, window_height - window_y_offset)))
        new_screen = process_image(screen)
        result = ""
        result = agent.predict(new_screen)
        #action = result[0]
        predictions = result[2]
        predicted_actions = [predictions[0].item(), predictions[1].item(
        ), predictions[2].item(), predictions[3].item()]
        # print(predicted_actions)
        player.move_player(predicted_actions)
        # print(action)
        total_time += time.time() - start
        total += 1
        if cv2.waitKey(1) & keyboard.is_pressed("g"):  # Stop playing
            print(total_time/total)
            break


def main():
    player.start_program_func(play_game, "q")
    keyboard.wait("x")


if __name__ == "__main__":
    main()
