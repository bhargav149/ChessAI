import cv2
import numpy as np
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import copy
import Until

#Using Clustering to filter out the noise intersection, because there will only have 81 intersection
#Thus I use 81 Clusters
def K_Means(corners):
    data_points_list = corners

    # Convert list of tuples to a NumPy array
    data_points = np.array(data_points_list)

    # fitting to 81 clustering 
    kmeans = KMeans(n_clusters = 81)
    kmeans.fit(data_points)

    # 81 centroids
    centroids = kmeans.cluster_centers_

    return centroids

    #debug purpose
    

    # Optional: Plotting the results
    plt.figure(figsize=(10, 6))
    plt.scatter(data_points[:, 0], data_points[:, 1], alpha=0.1, color='blue', label='Data Points')
    plt.scatter(centroids[:, 0], centroids[:, 1], color='red', marker='x', label='Centroids')
    plt.title('K-means Clustering')
    plt.legend()
    plt.show()




def find_corners_hough_transform(img_path):
    if not os.path.exists(img_path):
        print(f"The file {img_path} does not exist.")
        return None, None

    img = cv2.imread(img_path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 250, 1270, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 180)
    corners = []

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 10000 * (-b))
            y1 = int(y0 + 10000 * (a))
            x2 = int(x0 - 10000 * (-b))
            y2 = int(y0 - 10000 * (a))
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
        
        cv2.imshow('Corners with noise', img)
        cv2.waitKey(0)

        

    else:
        print("No lines were found")

    
    #cv2.destroyAllWindows()
    filtered_corners = [(x, y) for x, y in corners if x >= 0 and y >= 0]
    clustered = K_Means(filtered_corners)
    
    corners_tuple = [(int(x), int(y)) for x, y in clustered]

    for ac in corners_tuple:
        x, y = ac
        cv2.circle(img, (int(x), int(y)), 10, (255, 255, 255), -1)
    cv2.imshow('True Corners on Chessboard', img)
    cv2.waitKey(0)
    return img, corners_tuple  # Make sure to return corners



# sort corners in 2DArray.
def sort_corners(corner_list):

    sorted_y = sorted(corner_list, key=lambda p: p[1])
    sliced = corner_list[0]
    sorted_y = sorted(corner_list, key=lambda p: p[1])
    grid = [[None for _ in range(9)] for _ in range(9)]


    i = 0

    while len(sorted_y) > 0:
    
        first_nine = copy.deepcopy(sorted_y[0:9])
        sorted_x = sorted(first_nine, key=lambda p: p[0], reverse=False)
        sorted_x_copy = copy.deepcopy(sorted_x)
        grid[i] = sorted_x_copy
        sorted_y[0:9] = []

        i+=1
    return grid

def findGrid(points, x, y ):
    
    rows=8
    cols=8
    Smallest = float('inf')
    Coor = None
    # Points are assumed to be sorted row-wise
    for i in range(rows):
        for j in range(cols):
            top_left = points[i][j]
            top_right = points[i][j+1]
            bottom_left = points[i+1][j]
            bottom_right = points[i+1][j+1]
            
            difference = Until.areaDiff(top_left[0], top_left[1], top_right[0], top_right[1], bottom_left[0], bottom_left[1], bottom_right[0], bottom_right[1], x, y)
            if difference < Smallest:
                
                Smallest = difference
                Coor = (j,i)

    return Coor
    