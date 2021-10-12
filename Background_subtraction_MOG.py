import cv2

cap = cv2.VideoCapture('video_files/GH010347.MP4')
#cap = cv2.VideoCapture('E:/Pictures & Videos/Videos/GoPro/GH010347.MP4')
#cap = cv2.VideoCapture('video_files/PXL_20210522_093608367.mp4')
#cap = cv2.VideoCapture("video_files/highway.mp4")

cap.set(cv2.CAP_PROP_BUFFERSIZE, 50)
#cap2.set(cv2.CAP_PROP_BUFFERSIZE, 40)

BS_MOG2 = cv2.createBackgroundSubtractorMOG2()

#tracker = cv2.TrackerMOSSE_create()
while cap.isOpened():
    #timer = cv2.getTickCount()
    success, img = cap.read()
    #success2, img2 = cap2.read()

    #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    #cv2.putText(img, str(int(cap.get(cv2.CAP_PROP_FPS))), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    #cv2.putText(img2, str(int(cap2.get(cv2.CAP_PROP_FPS))), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.namedWindow("Pier cam", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions

    imS = cv2.resize(img, (960, 540))  # Resize image
    #imS2 = cv2.resize(img2, (960, 540))  # Resize image

    cv2.rectangle(imS, (10, 2), (100,20), (255,255,255), -1)
    cv2.putText(imS, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))

    cv2.imshow("Pier cam2", imS)



    fgMog = BS_MOG2.apply(img)

    fgMogRs = cv2.resize(fgMog, (960, 540))  # Resize image

    cv2.rectangle(fgMogRs, (10, 2), (140, 20), (255, 255, 255), -1)
    cv2.putText(fgMogRs, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    cv2.putText(fgMogRs, str(int(cap.get(cv2.CAP_PROP_FPS))), (75, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv2.imshow("Foreground MOG", fgMogRs)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
