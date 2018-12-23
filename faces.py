import numpy as np
import cv2
import pickle

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

labels = {"person_name": 1}
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)
i = 0

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y-25:y+h+25, x-25:x+w+25]
        resized = cv2.resize(roi_color, (150, 150))

        id_, conf = recognizer.predict(roi_gray)
        if conf <= 85:
            print(id_, labels[id_], conf)

            # print(labels[id_])
            # print(conf)
        else:
            print("Unidentified person", conf)

        if cv2.waitKey(20) & 0xFF == ord('p'):
            i += 1
            img_name = str(labels[id_]) + str(i) + ".png"
            cv2.imwrite(img_name, roi_color)

        # img_item = "mae-image.png"
        # cv2.imwrite(img_item, roi_color)

        color = (255, 0, 0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)

        if conf <= 85:
            cv2.putText(frame, labels[id_] + " - " + str(conf), (x+5, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (239, 246, 255))
        else:
            cv2.putText(frame, "Unidentified person", (x+5, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (239, 246, 255))

        # cv2.putText(frame, labels[id_] + str(conf), (x+5, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (239, 246, 255))
        # cv2.imshow('frame2', roi_color)
        cv2.imshow('cropped', resized)


    cv2.imshow('frame', frame)
    

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()