import cv2 as cv 
import mediapipe as mp
import screen_brightness_control as sbc
import numpy as np

camera = cv.VideoCapture(0)
if not camera.isOpened():
    print("Error: Unable to access the camera.")
    exit()

camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils

print("Press 'g' to toggle grayscale mode.")    
print("Press 's' to save the current frame.")  
print("Press 'e' to get only the edges of your frame.")
print("Press 'q' to quit the program.")
is_grayscale = False
is_edges = False
save_count = 0
x1 = y1 = x2 = y2 = distance = 0
Update_Interval = 0.15

while True:
    ret, frame = camera.read()
    frame = cv.flip(frame, 1)
    display_frame = frame.copy()

    frame_height, frame_width = display_frame.shape[:2]

    if is_grayscale:
        display_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    elif is_edges:
        display_frame = cv.Canny(frame, 100, 100)

    RGB_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(RGB_frame)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(display_frame, handLms, mpHands.HAND_CONNECTIONS)
            landmarks = handLms.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv.circle(img = display_frame, center =(x,y), radius=4, color=(255,0,0), thickness=-1)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv.circle(img = display_frame, center =(x,y), radius=4, color=(255,0,0), thickness=-1)
                    x2 = x
                    y2 = y
                cv.line(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                distance = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                cv.putText(display_frame, f'Distance: {distance}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                brightness = int(np.interp(distance, [20, 200], [0, 100]))
                brightness = max(0, min(100, distance))

                sbc.set_brightness(brightness)

    cv.imshow('WEBCAM', display_frame)
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        print("Exiting Frame Capture.")
        break

    elif key == ord('g'):
        is_grayscale = not is_grayscale
        mode1 = "ON" if is_grayscale else "OFF"
        print(f"Grayscale mode: {mode1}")  

    elif key == ord('e'):
        is_edges = not is_edges
        mode2 = "ON" if is_edges else "OFF"
        print(f"Edge Mode: {mode2}")

    elif key == ord('s'):
        filename = f"frame_{save_count}.png"
        cv.imwrite(filename, frame)
        print(f"Saved current frame as {filename}")
        save_count += 1

camera.release()
cv.destroyAllWindows()
