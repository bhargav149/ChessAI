
from ultralytics import YOLO
import GridLocator as GL
from PIL import Image, ImageDraw,ImageFont
import ChessBoard
import torch
import Until


class ChessCls:

    def __init__(self, model = 'TrainedModels/50Epoch.pt') :
        self.model = model
        self.img = None
        self.dict = dict()

    def getChessBoardArray(self,img_path):
        boardlist = [["" for i in range(0, 8)] for j in range(0, 8)]

        model = YOLO(self.model)  # pretrained YOLOv8n model
        
        self.img = Image.open(img_path)

        #detecded corners
        corners_image, detected_corners = GL.find_corners_hough_transform('TestImages/8ff752f9ed443e6e49d495abfceb2032_jpg.rf.c3e91277eea99c26328e39a6f0285189.jpg')

        #pretrained model
        result = model(self.img)[0]

        #coordination of each cls box
        boxes_coor = result.boxes.xywh.round().int()
        boxes_cls = result.boxes.cls

        print(boxes_coor.numel())

        for i in range(boxes_coor.size(0)):
           
            x = boxes_coor[i][0]
            y = boxes_coor[i][1]
            w = boxes_coor[i][2]
            h = boxes_coor[i][3]
            class_name = self.getClsName(int(boxes_cls[i].item()))

            print(class_name)
            print(boxes_coor[i])

    #Using it to debug, 
    def testLocation(self, img_path):

        model = YOLO(self.model)  # pretrained YOLOv8n model
        
        self.img = Image.open(img_path)

        #detected corners on the image
        corners_image, detected_corners = GL.find_corners_hough_transform(img_path)

        #Sort Corners to 2d Array()
        corners_2D = GL.sort_corners(detected_corners)

        #flip the 2d Array to adapt Board State wirte by Adam
        corners_2D_fliped = [subarray[::-1] for subarray in corners_2D]

        #prediction result
        result = model(self.img)[0]
        boxes_coor = result.boxes.xywh.round().int()
        boxes_cls = result.boxes.cls

        result.show()

        #board state 2Darray 
        return_board = [["" for i in range(0, 8)] for j in range(0, 8)]

        for i in range(boxes_coor.size(0)):
           
            x = boxes_coor[i][0]
            y = boxes_coor[i][1] - 10 #box has width
            w = boxes_coor[i][2]
            h = boxes_coor[i][3]

            class_name = self.getClsName(int(boxes_cls[i].item()))
            


            draw = ImageDraw.Draw(self.img)
            #draw the dot
            dot_x, dot_y = Until.get_bottom_center_abs(x, y, w, h)
            chess_coordinates = GL.findGrid(corners_2D_fliped, dot_x, dot_y)

            return_board[chess_coordinates[1]][chess_coordinates[0]] = class_name
            board_x = chess_coordinates[0]
            board_y = chess_coordinates[1]
            # draw the text next to the dot
            text_x, text_y = dot_x + 10, dot_y + 5
            font = ImageFont.truetype("Helvetica", 16)

            #draw the coordinate information under the class name
            coor_text_x, coor_text_y = text_x, text_y + 20
            
            #draw the coor of board
            board_text_x, board_text_y = coor_text_x, coor_text_y + 20
            
            board_text = "bx: " + str(board_x) + " by: " + str(board_y)
            img_coor ="x: " + str(int(x))+ " y: " + str(int(y))

            #drawing
            draw.text((coor_text_x, coor_text_y), img_coor, fill='red', font=font)
            draw.text((text_x, text_y), class_name, fill='red', font=font)
            draw.text((board_text_x, board_text_y), board_text, fill='red', font=font)
            draw.ellipse((dot_x, dot_y, dot_x + 5, dot_y + 5), fill = 'red')
           

        self.img.show()
        return return_board

    def getClsName(self,index:int):
        ClsNameList = ['BBI', 'BBI', 'BKI', 'BKN', 'BPA', 'BQE', 'BRO', 'WBI', 'WKI', 'WKN', 'WPA', 'WQE', 'WRO']

        return ClsNameList[index]




    


def main():
    GridLocatortest()


def GridLocatortest():
    classfier = ChessCls()
    classfier.testLocation('TestImages/8ff752f9ed443e6e49d495abfceb2032_jpg.rf.c3e91277eea99c26328e39a6f0285189.jpg')

if __name__ == '__main__' :
    main()