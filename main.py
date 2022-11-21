import json

import cv2
import time

from serverRequests import get_token_info, login

camera_id = 0
delay = 1
window_name = 'OpenCV QR Code'

qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(camera_id)

font = cv2.FONT_HERSHEY_DUPLEX

authToken = login()['result']

while True:
    success, frame = cap.read()

    if not success:
        continue

    success_qr, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(frame)

    if success_qr:
        for qr_data, qr_points in zip(decoded_info, points):
            if qr_data:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)

            frame = cv2.polylines(frame, [qr_points.astype(int)], True, color, 8)

        response = get_token_info(authToken, qr_data)
        positionY = 50
        cv2.waitKey(2000)
        for text in response:
            print(text +"\n")
            positionY = positionY + 20
            frame = cv2.putText(frame, text, (50, positionY), font, 5, 0, 2)
            frame = cv2.putText(frame, text, (50, positionY), font, 4, 255, 2)



    cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cv2.destroyWindow(window_name)
