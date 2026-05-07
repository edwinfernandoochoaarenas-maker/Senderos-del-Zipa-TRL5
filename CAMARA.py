import cv2
cap = cv2.VideoCapture(0) # Prueba con 0, 1 o 2
while True:
    ret, frame = cap.read()
    if not ret:
        print("No encuentro la cámara...")
        break
    cv2.imshow("Prueba de Camara", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
