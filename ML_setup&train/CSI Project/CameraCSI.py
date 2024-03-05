import cv2
import numpy as np
from datetime import datetime

cap = cv2.VideoCapture(0)  # Use 0 for the default camera

def detect_color_object(frame, color_lower, color_upper, color_name, label, rows, cols):
    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the frame to detect the specified color
    color_mask = cv2.inRange(hsv_frame, color_lower, color_upper)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour is found
    for contour in contours:
        # Get the largest contour (assumed to be the object)
        if cv2.contourArea(contour) > 500:
            # Get the bounding box around the object
            x, y, w, h = cv2.boundingRect(contour)

            # Draw a rectangle around the detected object with the specified color
            cv2.rectangle(frame, (x, y), (x+w, y+h), color_name, 2)

            # Calculate the center of the bounding box
            center_x = x + w // 2
            center_y = y + h // 2

            # Calculate the grid cell coordinates
            grid_row = center_y // (frame.shape[0] // rows)
            grid_col = center_x // (frame.shape[1] // cols)

            # Draw a rectangle around the grid cell where the object is located
            cell_width = frame.shape[1] // cols
            cell_height = frame.shape[0] // rows
            cv2.rectangle(frame, (int(grid_col * cell_width), int(grid_row * cell_height)),
                          (int((grid_col + 1) * cell_width), int((grid_row + 1) * cell_height)),
                          (0, 255, 0), 2)

            # Output tracking information with timestamp and color label to the console
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} - Object in grid: ({int(grid_row)}, {int(grid_col)}) - {label} Object")

            # Return after detecting one object to prioritize one color over the other
            return frame

    return frame

def draw_grid(frame, rows, cols):
    height, width, _ = frame.shape
    cell_width = width // cols
    cell_height = height // rows

    # Draw vertical lines
    for i in range(1, cols):
        cv2.line(frame, (i * cell_width, 0), (i * cell_width, height), (255, 255, 255), 1)

    # Draw horizontal lines
    for j in range(1, rows):
        cv2.line(frame, (0, j * cell_height), (width, j * cell_height), (255, 255, 255), 1)

    return frame

def main():
    # Open the webcam
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera

    # Define the lower and upper bounds for the red color
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Define the lower and upper bounds for the blue color
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([140, 255, 255])

    rows = 4
    cols = 5

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Draw a 4x5 grid on top of the frame
        frame_with_grid = draw_grid(frame.copy(), rows, cols)

        # Detect red objects and draw red rectangles around them
        result_frame = detect_color_object(frame_with_grid, lower_red1, upper_red1, (0, 0, 255), "Red", rows, cols)
        if result_frame is not frame_with_grid:
            # Continue to the next frame if a red object is detected
            continue

        result_frame = detect_color_object(result_frame, lower_red2, upper_red2, (0, 0, 255), "Red", rows, cols)

        # Detect blue objects and draw blue rectangles around them
        result_frame = detect_color_object(result_frame, lower_blue, upper_blue, (255, 0, 0), "Blue", rows, cols)

        # Display the result frame with either a red or a blue object
        cv2.imshow('Color Object Detection with 4x5 Grid', result_frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
