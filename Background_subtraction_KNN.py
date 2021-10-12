import cv2

cap = cv2.VideoCapture('video_files/GH010347.MP4')
#cap = cv2.VideoCapture('E:/Pictures & Videos/Videos/GoPro/GH010347.MP4')
#cap = cv2.VideoCapture('video_files/PXL_20210522_093608367.mp4')
cap.set(cv2.CAP_PROP_BUFFERSIZE, 40)
#cap2.set(cv2.CAP_PROP_BUFFERSIZE, 40)

success, img = cap.read()

myvideo=cv2.VideoWriter("video_files/forgroundKNN.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, (int(img.shape[1]),int(img.shape[0])))

BS_KNN = cv2.createBackgroundSubtractorKNN()

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

    cv2.imshow("Pier cam", imS)
    #cv2.imshow("Pier cam 2", imS2)



    fgKnn = BS_KNN.apply(img)

    fg = cv2.copyTo(img, fgKnn)
    myvideo.write(fg)

    fgKnnRs = cv2.resize(fgKnn, (960, 540))  # Resize image

    cv2.rectangle(fgKnnRs, (10, 2), (140, 20), (255, 255, 255), -1)
    cv2.putText(fgKnnRs, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    cv2.putText(fgKnnRs, str(int(cap.get(cv2.CAP_PROP_FPS))), (75, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))


    cv2.imshow("Foreground KNN", fgKnnRs)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
