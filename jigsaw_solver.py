#from scipy.ndimage import filters
#from PIL import Image, ImageChops
#import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import glob
import random

def main():
    t = Tile(0,0, random.randrange(0, 303)) #len([n for n in os.listdir('.') if os.path.isfile(n)])))
    print('Random Starting Image:', t.index)
    test = Image(10, t, 100)
    test.map_image()

    #print('Does out.png look correct (type y to end): ')
    #x = input()
    #while (x != 'y'):
    #    t = Tile(0,0, random.randrange(0, 303)) #len([n for n in os.listdir('.') if os.path.isfile(n)])))
    #    print('Random Starting Image:', t.index)
    #    test = Image(10, t, 100)
    #    test.map_image()

    #    print('Does out.png look correct (type y to end): ')
    #    x = input()
     
    for i in range(len(test.map_indices)):
        print("\n")
        for j in range(len(test.map_indices[i])):
            print(test.map_indices[i][j].y, test.map_indices[i][j].x, test.map_indices[i][j].index, end="   ")
    

    #for i in range(304):
    #     print(test.compare_tile(i, 's'))


def load_images():
    gray_images = []
    images = [cv2.imread(file) for file in glob.glob("images/*.png")]
    for i in range(len(images)):
            gray = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
            gray_images.append(gray)
    return images, gray_images


def load_test_images():
    images = []
    gray_images = []
    x_val = 0
    y_val = 1
    c = 0
    for j in range(8):
        for i in range(38):
                #img_name = 'images_2/y: '+ str(y_val) + ' x: ' + str(x_val) + ".png"
                img_name = 'images_xy/' + str(c) + ".png"
                images.append(cv2.imread(img_name))
                x_val += 1
                c += 1
        y_val += 1
        x_val = 0
    for image in range(len(images)):
        gray = cv2.cvtColor(images[image], cv2.COLOR_BGR2GRAY)
        gray_images.append(gray)
    return images, gray_images

class Tile:
    def __init__(self, y, x, index):
        self.x = x
        self.y = y
        self.index = index


class Image:
    def __init__(self, confidence, cur_image, pixels):
        self.images, self.gray_images = load_images()
        self.confidence = confidence
        self.cur_image = cur_image
        self.max_images = len(self.images)-1
        t = Tile(cur_image.y, cur_image.x, cur_image.index)
        self.map_indices = [[t]]
        self.first_img = cur_image.index
        self.hor = 0
        self.vert = 0
        self.pixels = pixels

    def compare_tile(self, index, direction):
        if (direction == 'n'):
            y1 = 0
            y2 = 99

        elif (direction == 's'):
            y1 = 99
            y2 = 0

        elif (direction == 'e'):
            x1 = 99
            x2 = 0

        elif (direction == 'w'):
            x1 = 0
            x2 = 99

        color = []
        cmp_img = []

        for image in range(len(self.gray_images)):
            c = 0
            for p in range(self.pixels):
                if (direction == 'n' or direction == 's'):
                    comp = [ self.gray_images[index][y1, p], self.gray_images[image] [y2, p] ]
                    color.append(comp)
                else:
                    comp = [ self.gray_images[index][p, x1], self.gray_images[image] [p, x2] ]
                    color.append(comp)
            for e in range(len(color)):
                    c = c + abs(int(color[e][0]) - int(color[e][1]))
            cmp_img.append(c/self.pixels)
            color.clear()
        minimum = min(cmp_img)
        return [minimum, cmp_img.index(minimum)]

    def place_image(self, tile):
        x = 0
        y = tile.y + abs(self.map_indices[0][0].y)

        if (y < 0):
            self.map_indices.insert(0, [tile])
            self.max_images -= 1

        elif (y >= len(self.map_indices)):
            self.map_indices.append([tile])
            self.max_images -= 1
        else:
            self.map_indices[y].append(tile)
    
    def sort_tiles(self):
        for row in self.map_indices:
            row.sort(key=lambda x: x.x)


    def get_img_index(self, y, x):
        count = 0
        for img in self.map_indices[y + abs(self.map_indices[0][0].y)]:
            if (x == img.x):
                return count
            count += 1

        return None

    def list_of_x(self):
        x_list = []
        for r in range(len(self.map_indices)):
            l = []
            for c in range(len(self.map_indices[r])):
                x = self.map_indices[r][c].x
                l.append(x)
            x_list.append(l)
        return(x_list)

    def list_of_images(self):
        index_list = []
        for r in range(len(self.map_indices)):
            l = []
            for c in range(len(self.map_indices[r])):
                x = self.images[self.map_indices[r][c].index]
                l.append(x)
            index_list.append(l)
        return(index_list)

    def map_image(self):

        north = True
        south = True

        while(north == True):
            con, index = self.compare_tile(self.cur_image.index, 'n')
            n_con, n_index = self.compare_tile(index, 's')
            if (n_index == self.cur_image.index):
                t = Tile(self.cur_image.y-1, self.cur_image.x, index)
                self.place_image(t)
                self.cur_image.index = index
                self.cur_image.y -= 1
                self.max_images -= 1
            else:
                self.cur_image.y = 0
                self.cur_image.index = self.first_img
                north = False

        while(south == True):
            con, index = self.compare_tile(self.cur_image.index, 's')
            n_con, n_index = self.compare_tile(index, 'n')
            if (n_index == self.cur_image.index):
                t = Tile(self.cur_image.y+1, self.cur_image.x, index)
                self.place_image(t)
                self.cur_image.index = index
                self.cur_image.y += 1
                self.max_images -= 1
            else:
                south = False


        for row in range(len(self.map_indices)):
            #print(self.map_indices[row][0].index, self.map_indices[row][0].y, self.map_indices[row][0].x)
            east = True
            self.cur_image.x = self.map_indices[row][0].x
            self.cur_image.y = self.map_indices[row][0].y
            self.cur_image.index = self.map_indices[row][0].index
            while(east == True):
                con, index = self.compare_tile(self.cur_image.index, 'e')
                n_con, n_index = self.compare_tile(index, 'w')
                if (n_index == self.cur_image.index):
                    t = Tile(self.cur_image.y, self.cur_image.x+1, index)
                    self.place_image(t)
                    self.cur_image.index = index
                    self.cur_image.x += 1
                    self.max_images -= 1
                else:
                    east = False
                # else:
                #     if (row != 0):
                #         is_above = False
                #         print(row)
                #         nor_con, nor_index = self.compare_tile(index, 'n')
                #         sou_con, sou_index = self.compare_tile(nor_index, 's')
                #         if (sou_index == index):
                #             for above_tile in self.map_indices[row-1]:
                #                 if (above_tile.index == nor_index):
                #                     print("check")
                #                     t = Tile(self.cur_image.y, self.cur_image.x+1, index)
                #                     r = self.map_indices[row]
                #                     r.append(t)
                #                     self.cur_image.index = index
                #                     self.cur_image.x += 1
                #                     self.max_images -= 1
                #                     is_above = True
                #             if (is_above == False):
                #                 east = False
                #         else:
                #             east = False
                # else:
                #     east = False

            west = True
            self.cur_image.x = self.map_indices[row][0].x
            self.cur_image.y = self.map_indices[row][0].y
            self.cur_image.index = self.map_indices[row][0].index
            while(west == True):
                con, index = self.compare_tile(self.cur_image.index, 'w')
                n_con, n_index = self.compare_tile(index, 'e')
                if (n_index == self.cur_image.index):
                    t = Tile(self.cur_image.y, self.cur_image.x-1, index)
                    self.place_image(t)
                    self.cur_image.index = index
                    self.cur_image.x -= 1
                    self.max_images -= 1
                else:
                    west = False
        x_list = self.list_of_x()
        for row in range(len(self.map_indices)-1):
            #print(self.map_indices[row])
            for x in range(len(self.map_indices[row])):
                self.cur_image.x = self.map_indices[row][x].x
                self.cur_image.y = self.map_indices[row][x].y
                self.cur_image.index = self.map_indices[row][x].index
                in_next_row = False
                if (self.map_indices[row][x].x not in x_list[row+1]):
                    con, index = self.compare_tile(self.cur_image.index, 's')
                    n_con, n_index = self.compare_tile(index, 'n')
                    if (n_index == self.cur_image.index):
                        t = Tile(self.cur_image.y+1, self.cur_image.x, index)
                        self.place_image(t)
                        self.max_images -= 1

        # x_list = self.list_of_x()
        # x_list_reversed = []
        # [x_list_reversed.append(i) for i in x_list[::-1]]
        # print(x_list_reversed)
        # for row in range((len(self.map_indices)-1) -1, -1, -1):
        #     #print(self.map_indices[row])
        #     for x in range(len(self.map_indices[row])):
        #         self.cur_image.x = self.map_indices[row][x].x
        #         self.cur_image.y = self.map_indices[row][x].y
        #         self.cur_image.index = self.map_indices[row][x].index
        #         in_next_row = False
        #         if (self.map_indices[row][x].x not in x_list_reversed[row-1]):
        #             con, index = self.compare_tile(self.cur_image.index, 'n')
        #             n_con, n_index = self.compare_tile(index, 's')
        #             if (n_index == self.cur_image.index):
        #                 t = Tile(self.cur_image.y-1, self.cur_image.x, index)
        #                 self.place_image(t)
        #                 self.max_images -= 1
            #print('Images left:', self.max_images)
            # for r in range(len(self.map_indices)-1):
            #     self.cur_image.x = self.map_indices[r][0].x
            #     self.cur_image.y = self.map_indices[r][0].y
            #     self.cur_image.index = self.map_indices[r][0].index
            #     if (len(self.map_indices[r]) < len(self.map_indices[r+1])):
            #         continue
            #     for c in range(len(self.map_indices[r])):
            #         n_val = False
            #         for next_row in range(len(self.map_indices[r+1])):
            #             if (self.map_indices[r][c].x != self.map_indices[r][next_row].x):
            #                 continue
            #             else:
            #                 n_val = True
            #         if (n_val == False):
            #             con, index = self.compare_tile(self.cur_image.index, 's')
            #             n_con, n_index = self.compare_tile(index, 'n')
            #             if (n_index == self.cur_image.index):
            #                 t = Tile(self.cur_image.y+1, self.cur_image.x, index)
            #                 self.map_indices[r+1].append(t)
            #                 self.cur_image.index = index
            #                 self.max_images -= 1
        self.sort_tiles()
        self.build_image()

    def build_image(self):
        rows = []
        # black_image = cv2.imread("black_image.png", cv2.IMREAD_COLOR)
        # b = black_image[0:self.pixels, 0:self.pixels]
        # self.images.append(b)
        # max_x = len(max(self.map_indices, key=len))
        #
        # for row in range(len(self.map_indices)):
        #     x_val = self.map_indices[row][0].x
        #     for column in range(len(self.map_indices[row])):
        #         if (self.map_indices[row][column].x != x_val):
        #             t = Tile(row, x_val, len(self.images)-1)
        #             self.place_image(t)
        #         x_val += 1

        im = self.list_of_images()

        for r in range(len(self.map_indices)):
            rows.append(cv2.hconcat(im[r]))

        out = cv2.vconcat(rows)
        cv2.imwrite('out.png', out)

if __name__=="__main__":
    main()
