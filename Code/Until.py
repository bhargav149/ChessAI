
#calculating the bottom center coordination of box. Using abslout location 
def get_bottom_center_abs(x_center, y_center, width, height):
    
    x_center_abs = x_center
    y_center_abs = y_center
    width_abs = width
    height_abs = height

    # Calculate the middle of the bottom line
    x_bottom_center = x_center_abs
    y_bottom = y_center_abs + (height_abs / 2)

    return (x_bottom_center, y_bottom)
#calculating the bottom center coordination of box. Using normalized location
def get_bottom_center_nor(x_center, y_center, width, height, image_width, image_height):
    # Convert normalized coordinates to absolute coordinates
    x_center_abs = x_center * image_width
    y_center_abs = y_center * image_height
    width_abs = width * image_width
    height_abs = height * image_height

    # Calculate the middle of the bottom line
    x_bottom_center = x_center_abs
    y_bottom = y_center_abs + (height_abs / 2)

    return (x_bottom_center, y_bottom)

#calculating the triangle area
def area(x1, y1, x2, y2, x3, y3):
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)

#calculating the difference between the quadraliteral and four triangle
def areaDiff(x1, y1, x2, y2, x3, y3, x4, y4, x, y):
    # Calculate area of the full quadrangle
    whole_area = area(x1, y1, x2, y2, x3, y3) + area(x1, y1, x3, y3, x4, y4)
    
    # Calculate area of the triangles with the point included
    area1 = area(x1, y1, x2, y2, x, y)
    area2 = area(x2, y2, x3, y3, x, y)
    area3 = area(x3, y3, x4, y4, x, y)
    area4 = area(x4, y4, x1, y1, x, y)
    
    # return the area difference
    return abs((area1 + area2 + area3 + area4) - whole_area)