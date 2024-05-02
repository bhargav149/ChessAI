from ultralytics import YOLO

# Load a model
model = YOLO()



# Train the model with 2 GPUs
results = model.train(data='YOLO/data.yaml', epochs=50, imgsz=640, device='mps')
model.save('chessAi_10.pt')