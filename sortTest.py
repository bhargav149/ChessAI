
import copy
import Until

corner_list = [(294, 327), (1425, 1209), (1439, 337), (158, 1236), (985, 716), (950, 220), (1747, 856), (813, 1222), (628, 449), (1343, 714), (1632, 1205), (257, 577), (1707, 712), (416, 879), (1843, 1200), (1020, 1218), (1391, 121), (975, 577), (1670, 577), (601, 1226), (1523, 713), (385, 1231), (804, 717), (484, 105), (795, 219), (1572, 226), (1147, 577), (1117, 334), (1225, 1213), (1279, 335), (235, 720), (1604, 338), (430, 719), (996, 869), (1319, 577), (802, 577), (619, 718), (187, 1047), (1260, 223), (636, 218), (311, 215), (443, 577), (1493, 577), (1395, 1026), (958, 332), (464, 328), (1164, 715), (1007, 1033), (1555, 859), (1592, 1023), (1414, 224), (810, 1037), (211, 883), (608, 1040), (1793, 1019), (1367, 863), (1243, 118), (624, 577), (1203, 1030), (1104, 222), (966, 449), (1298, 449), (276, 449), (797, 331), (1464, 449), (613, 876), (632, 330), (1183, 866), (402, 1044), (474, 216), (328, 102), (1634, 449), (943, 113), (807, 873), (1544, 123), (1132, 449), (454, 449), (799, 449), (1091, 116), (640, 108), (794, 110)]
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
    
print(grid[7][7])
print(grid[7][8])
print(grid[8][7])
print(grid[8][8])



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
                print(difference)
                Smallest = difference
                Coor = (i,j)

    return Coor

print(findGrid(grid,1502,136))
            

    

    
