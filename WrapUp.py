import copy
import cv2
import numpy as np
import os
from ultralytics import YOLO
from PIL import Image
import torch
from ChessBoard import ChessBoard
import ChessCls
import GridLocator as GL
from ChessCls import ChessCls

def main():

    
    
     
    
    
  
    classfier = ChessCls()
    Locations_2d = classfier.testLocation('/Users/zhiyangcheng/Downloads/Chess Pieces.v23-raw.yolov8/test/images/8ff752f9ed443e6e49d495abfceb2032_jpg.rf.c3e91277eea99c26328e39a6f0285189.jpg')
    board = ChessBoard(board_state=Locations_2d )

    print(board)
    
    

   

   
    #print(detections_int)
    

    # Create the new tensor in the format [x_center, y_center, w, h]
   
    #print("Chess coordinates:", chess_coordinates)



if __name__ == '__main__':
    main()
