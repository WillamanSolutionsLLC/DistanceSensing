import cv2

video_stream = 0
threshold = 80

def convert_frame_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def calculate_variance_of_laplacian(grayscale_frame):
    return cv2.Laplacian(grayscale_frame, cv2.CV_64F).var()


def is_tire_in_focus():
    cap = cv2.VideoCapture(video_stream)
    while True:
        ret, original_frame = cap.read()

        if not ret:
            break

        grayscale_frame = convert_frame_to_grayscale(original_frame)
        variance = calculate_variance_of_laplacian(grayscale_frame)

        if variance > threshold:
            text_color = (0, 255, 0)
            display_text = 'Tire in focus'
        else:
            display_text = 'Tire is out of focus'
            text_color = (0, 0, 255)

        cv2.putText(original_frame, display_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

        # Display the frame
        cv2.imshow("LiveStream Video", original_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


is_tire_in_focus()

