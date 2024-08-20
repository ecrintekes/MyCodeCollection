import cv2
import numpy as np
import datetime
import winsound
import matplotlib.pyplot as plt


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


video_source = 0
cap = cv2.VideoCapture(video_source)


fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)


motion_count = 0
motion_duration = []
start_time = datetime.datetime.now()


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('motion_output.avi', fourcc, 20.0, (640, 480))


ROI_x, ROI_y, ROI_w, ROI_h = 100, 100, 400, 400

while True:
    ret, frame = cap.read()
    if not ret:
        break


    fgmask = fgbg.apply(frame)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, 'Face Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)


    cv2.rectangle(frame, (ROI_x, ROI_y), (ROI_x + ROI_w, ROI_y + ROI_h), (255, 0, 0), 2)


    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            if ROI_x < x < ROI_x + ROI_w and ROI_y < y < ROI_y + ROI_h:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True

    if motion_detected:
        motion_count += 1
        motion_duration.append((datetime.datetime.now() - start_time).total_seconds())
        winsound.Beep(1000, 200)  # Alarm sesi


        out.write(frame)


    cv2.putText(frame, f"Motion Count: {motion_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if motion_duration:
        average_duration = sum(motion_duration) / len(motion_duration)
        cv2.putText(frame, f"Avg Motion Duration: {average_duration:.2f} sec", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv2.imshow('Frame', frame)
    cv2.imshow('FG Mask', fgmask)


    if cv2.waitKey(30) & 0xFF == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()


plt.plot(motion_duration)
plt.title('Hareket Süreleri')
plt.xlabel('Olay Numarası')
plt.ylabel('Süre (saniye)')
plt.show()