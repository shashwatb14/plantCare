import cv2
import numpy as np


def analyze_color_contrast(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    num_black_pixels = np.sum(thresholded == 0)
    num_white_pixels = np.sum(thresholded == 255)
    contrast_ratio = num_black_pixels / num_white_pixels
    return contrast_ratio


def main():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Error: Could not open camera.")
        return
    while True:
        ret, frame = capture.read()
        if not ret:
            print("Error: No frame captured.")
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        weaker = np.array([0, 0, 100])
        stronger = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, weaker, stronger)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = frame[y : y + h, x : x + w]
            contrast_ratio = analyze_color_contrast(roi)
            ripeness = "Ripe" if contrast_ratio > 1 else "Unripe"
            cv2.putText(
                result,
                f"Ripeness: {ripeness}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )
        cv2.putText(
            result,
            "Press 'Esc' to exit",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.imshow("Live Camera", result)
        key = cv2.waitKey(1)
        if key == 27:
            break
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
