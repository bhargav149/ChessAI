import cv2
import numpy as np
import os




def find_corners_hough_transform(img_path):
    if not os.path.exists(img_path):
        print(f"The file {img_path} does not exist.")
        return None, None

    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 180)
    corners = []

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        for i, line1 in enumerate(lines):
            for line2 in lines[i + 1:]:
                rho1, theta1 = line1[0]
                rho2, theta2 = line2[0]

                if abs(theta1 - theta2) > 0.1:
                    A = np.array([[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]])
                    B = np.array([[rho1], [rho2]])
                    intersection = np.linalg.solve(A, B)
                    x, y = intersection.ravel()
                    corners.append((int(x), int(y)))
                    cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)

        if corners:
            for corner in corners:
                x, y = corner
                cv2.circle(img, (int(x), int(y)), 10, (255, 0, 0), -1)  # Draw corners in blue

    else:
        print("No lines were found")

    #cv2.imshow('Corners on Chessboard', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return img, corners  # Make sure to return corners

corners_image, detected_corners = find_corners_hough_transform(r'C:\Users\bharg\Desktop\college\spring24\ai\mini project\updated_board.jpg')
#print("Detected corners:", detected_corners)



# Assuming detected_corners is a list of tuples (x, y), sorted from top-left to bottom-right
def sort_corners(corners):
    # Assuming the top left corner is the first one and bottom right is the last one
    # Sort corners to get them in order: top-left, top-right, bottom-left, bottom-right
    corners = sorted(corners, key=lambda x: x[0])  # Sort by x coordinate
    top_corners = sorted(corners[:2], key=lambda x: x[1])  # Smallest y is top-left
    bottom_corners = sorted(corners[2:], key=lambda x: x[1], reverse=True)  # Largest y is bottom-right
    ordered_corners = [top_corners[0], top_corners[1], bottom_corners[0], bottom_corners[1]]
    return ordered_corners

# Function to convert pixel to chess coordinates
def pixel_to_chess(pixel, corners):
    # Get the top-left, top-right, bottom-left, and bottom-right corners
    (tl, tr, bl, br) = sort_corners(corners)

    # Prepare the points for perspective transformation
    src_pts = np.array([tl, tr, bl, br], dtype='float32')
    dst_pts = np.array([[0, 0], [7, 0], [0, 7], [7, 7]], dtype='float32')

    # Get the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # Apply the perspective transformation to the pixel coordinates
    pixel_array = np.array([pixel], dtype='float32')
    pixel_array = np.array([pixel_array])
    chess_coord = cv2.perspectiveTransform(pixel_array, matrix)
    
    chess_coord = cv2.perspectiveTransform(pixel_array, matrix)

    # Rounding the coordinates to the nearest whole number
    chess_coord_rounded = np.round(chess_coord[0][0]).astype(int)

    # Ensuring the coordinates are within the bounds of the chessboard
    chess_coord_clamped = np.clip(chess_coord_rounded, 0, 7)
    return chess_coord_clamped