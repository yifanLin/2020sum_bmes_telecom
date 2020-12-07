import cv2, numpy

cap = cv2.VideoCapture(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]

#while(True):
ret, frame = cap.read()
result, encimg = cv2.imencode('.jpg', frame, encode_param)
decimg = cv2.imdecode(encimg, 1)
print(len(decimg[0]))
cv2.imshow('frame', decimg)
#if cv2.waitKey(1) & 0xFF == ord('q'):
#    break

cap.release()
cv2.destroyAllWindows()