import cv2
from main import output_code

cap = cv2.VideoCapture(0)
l = []
while True:
    try:
        output = output_code(cap)
        if output:
            l.append(output)
        else:
            print("No hand detected")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        print(l)
        break
cap.release()
cv2.destroyAllWindows()
