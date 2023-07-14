import cv2

video_stream = 0
threshold = 80
circle_radius = 325


def convert_frame_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def calculate_variance_of_laplacian(grayscale_frame):
    return cv2.Laplacian(grayscale_frame, cv2.CV_64F).var()


def add_center_circle_to_window(grayscale_frame, original_frame, text_color):
    M = cv2.moments(grayscale_frame)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(original_frame, (cX, cY), circle_radius, text_color, 4)


def add_text_to_window(original_frame, display_text, text_color):
    cv2.putText(original_frame, display_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)


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

        add_text_to_window(original_frame, display_text, text_color)
        add_center_circle_to_window(grayscale_frame, original_frame, text_color)
        cv2.imshow("LiveStream Video", original_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


is_tire_in_focus()

