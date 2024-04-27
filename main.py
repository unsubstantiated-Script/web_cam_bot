import cv2
import time
from email_server import send_email

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
count = 0
status_list = []

while True:
    count += 1
    status = 0
    check, frame = video.read()
    # Applying gray scale and Gaussian Blur to the images to make them easier to process.
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if count > 20:

        # Grabbing the first frame out of the While Loop here.
        if first_frame is None:
            first_frame = gray_frame_gau

        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

        # Organizing our pixels and setting thresholds for what we consider to be movement.
        thresh_frame = cv2.threshold(delta_frame, 20, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

        contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            # If we are within bounds, we're setting up the outline of the moving object here
            x, y, w, h = cv2.boundingRect(contour)
            # Adding in the x,y,w,h in tuple
            rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if rectangle.any():
                status = 1

        status_list.append(status)
        # Grabbing the last two items in the list
        status_list = status_list[-2:]

        # Seeing the change as the object leaves the screen 1 -> 0
        if status_list[0] == 1 and status_list[1] == 0:
            send_email()

        cv2.imshow('My Video', frame)
    else:
        pass

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
