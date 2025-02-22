import cv2
import os
import re

def get_image():
    cam = cv2.VideoCapture(0)
    img_name = ""

    while True:
        ret, frame = cam.read()
        if not ret:
            print('failed to grab frame')
            break

        cv2.imshow("Take image of reciept", frame)
        k  = cv2.waitKey(1)

        # stop app when esc key pressed
        if k%256 == 27:
            break
        # take screenshot when space key pressed
        elif k%256 == 32:
            path = f"{os.getcwd()}/bills_image"
            if not os.path.isdir(path):
                os.mkdir(path)
                num = 1
            else:
                file_nums = [int(f[8:-4]) for f in os.listdir(path) if re.match(r'bill_[0-9]+.(?:JPG|jpg)', f)]
                if len(file_nums) > 0:
                    num = max(file_nums) + 1
                else:
                    num = 1
            img_name = f"{path}/receipt_{num}.png"
            cv2.imwrite(img_name, frame)
            break

    cam.release()
    cv2.destroyAllWindows()
    return img_name


if __name__ == "__main__":
    get_image()