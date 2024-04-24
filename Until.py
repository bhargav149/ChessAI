

def get_bottom_center_abs(x_center, y_center, width, height):
    # Convert normalized coordinates to absolute coordinates
    x_center_abs = x_center
    y_center_abs = y_center
    width_abs = width
    height_abs = height

    # Calculate the middle of the bottom line
    x_bottom_center = x_center_abs
    y_bottom = y_center_abs + (height_abs / 2)

    return (x_bottom_center, y_bottom)

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