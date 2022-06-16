import cv2
import time

cap = cv2.VideoCapture('video_files/GH010347.MP4')
cap2 = cv2.VideoCapture('video_files/PXL_20210522_093608367.mp4')
cap.set(cv2.CAP_PROP_BUFFERSIZE, 40)
cap2.set(cv2.CAP_PROP_BUFFERSIZE, 40)

col_images = []

success, img = cap.read()

while cap.isOpened():
    successNext, imgNext = cap.read()

    if successNext:
        fgMask = cv2.absdiff(img, imgNext)

        fgMaskRs = cv2.resize(fgMask, (960, 540))
        cv2.imshow('FG Mask', fgMaskRs)

        #BS_MOG2 = cv2.createBackgroundSubtractorMOG2()
        #BS_KNN = cv2.createBackgroundSubtractorKNN()

        #fgMog = BS_MOG2.apply(imgNext)
        #fgKnn = BS_KNN.apply(imgNext)

        #fgMogRs = cv2.resize(fgMog, (960, 540))  # Resize image
        #fgKnnRs = cv2.resize(fgKnn, (960, 540))  # Resize image

        #cv2.imshow("Foreground MOG", fgMogRs)
        #cv2.imshow("Foreground KNN", fgKnnRs)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

        img = imgNext

    if not successNext:
        break

cv2.destroyAllWindows()
cap.release()
