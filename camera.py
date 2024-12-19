import cv2 as cv 

camera = cv.VideoCapture(0) 
if not camera.isOpened():
    print("Error: Unable to access the camera.")
    exit()
print("Press 'g' to toggle grayscale mode.")    
print("Press 's' to save the current frame.")  
print("Press 'o' to get only the edges of your frame.")
print("Press 'q' to quit the program.")
is_grayscale = False
is_edges = False
frame_count = 0

while True:
    ret, frame = camera.read()
    if not ret:
        print("Error: Unable to capture a frame.")
        break

    display_frame = frame
    if is_grayscale:
        display_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    elif is_edges:
        display_frame = cv.Canny(frame, 100, 200)  
    cv.imshow('WEBCAM', display_frame)
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        print("Exiting Frame ;)")
        break

    elif key == ord('g'):
        is_grayscale = not is_grayscale
        mode1 = "ON" if is_grayscale else "OFF"
        print(f"Grayscale mode : {mode1}")  

    elif key == ord('e'):
        is_edges = not is_edges
        mode2 = "ON" if is_edges else "OFF"
        print(f"Edge Mode : {mode2}")

    elif key == ord('s'):
        filename = f"frame_{frame_count}.png"
        cv.imwrite(filename, frame)
        print(f"Saved current frame as {filename}")
        frame_count += 1

camera.release()
cv.destroyAllWindows()
