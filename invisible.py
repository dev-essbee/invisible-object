import cv2
import numpy as np
import time

captured_video = cv2.VideoCapture(0)
currentFrame = 0


# Define the codec and create VideoWriter object
# uncomment to save output as video:

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc, 20, (640,480))


time.sleep(3)
background = 0
for i in range(25):
    returned_val, background = captured_video.read()

background = np.flip(background, axis=1)
while captured_video.isOpened():
    returned_val, image = captured_video.read()
    if not returned_val:
        break

    image = np.flip(image, axis=1)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # hsv for green colour
    lower_color = np.array([60, 60, 60])
    upper_color = np.array([75, 255, 255])

    mask_1 = cv2.inRange(hsv, lower_color, upper_color)
    # hsv for green colour
    lower_color = np.array([75, 60, 60])
    upper_color = np.array([90, 255, 255])

    mask_2 = cv2.inRange(hsv, lower_color, upper_color)

    mask_1 += mask_2

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask_1 = cv2.dilate(mask_1, np.ones((3, 3), np.uint8), iterations=1)
    mask_2 = cv2.bitwise_not(mask_1)

    result_1 = cv2.bitwise_and(background, background, mask=mask_1)
    result_2 = cv2.bitwise_and(image, image, mask=mask_2)

    output = cv2.addWeighted(result_1, 1, result_2, 1, 0)

    # Uncomment to save output as video:
    # out.write(output)

    cv2.imshow('Make Invisible', output)

    key = cv2.waitKey(10)
    if key == 27:
        break
cv2.destroyAllWindows()
captured_video.release()
