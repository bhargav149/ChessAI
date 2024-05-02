import copy
import cv2
import numpy as np
import os
from ultralytics import YOLO
from PIL import Image
import torch
import ChessBoard as cb
import ChessCls
import GridLocator as GL
from ChessCls import ChessCls
from functools import lru_cache
import chess
import chess.polyglot

def main():

    classfier = ChessCls()
    Locations_2d = classfier.testLocation('/Users/zhiyangcheng/Downloads/Chess Pieces.v23-raw.yolov8/test/images/8ff752f9ed443e6e49d495abfceb2032_jpg.rf.c3e91277eea99c26328e39a6f0285189.jpg')

    board = cb.chessBoardToPyBoard(Locations_2d)
    isWhite = input("(yes or no) if your are white")
    board.turn = isWhite.lower() == "yes"
    val, move = cb.aphaBeta(board)

    print(board)
    print('A B C D E F G H')
    print("Chess Board score: " + str(val))
    print("Chess Board move: " + str(move))
    
    

if __name__ == '__main__':
    main()
