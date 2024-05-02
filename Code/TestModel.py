from ultralytics import YOLO
from PIL import Image

# Load a model
model = YOLO('/Users/zhiyangcheng/Documents/train11/weights/best.pt')  # pretrained YOLOv8n model

def resize_image(input_path, output_size):
    image = Image.open(input_path)
    # Use Image.Resampling.LANCZOS instead of Image.ANTIALIAS
    resized_image = image.resize(output_size, Image.Resampling.LANCZOS)
    return resized_image

#resized_img = resize_image('/Volumes/Zhiyang/Data/G000_IMG010.jpg', (640, 640))  # Resize to 640x640
#resized_img.save('/Volumes/Zhiyang/Data/resized_G000_IMG010.jpg')

# Run batched inference on a list of images
results = model('/Users/zhiyangcheng/Downloads/Chess Pieces.v23-raw.yolov8/test/images/8ff752f9ed443e6e49d495abfceb2032_jpg.rf.c3e91277eea99c26328e39a6f0285189.jpg', )  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    result.show()  # display to screen
    result.save(filename='result.jpg')  # save to disk