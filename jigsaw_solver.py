import numpy as np
import cv2
import os
import glob
import random
import sys

# Main function used to instaniate the image, replace path with your own directory.

def main():

    path = os.getcwd()
    path += '/nyc_images'
    t = Tile(0,0, random.randrange(0, len([n for n in os.listdir(path) if os.path.join(path, n)])))
    pixels = 100

    x = 'n'

    while (x != 'y'):
        islands = []
        t = Tile(0,0, random.randrange(0, len([n for n in os.listdir(path) if os.path.join(path, n)])))

        test = Image(t, pixels, path)
        test.map_image()

        # while(test.max_images < 0):
        #     test.clear_map()
        #     t = Tile(0,0, random.randrange(0, len([n for n in os.listdir(path) if os.path.join(path, n)])))
        #     test = Image(t, pixels, path)
        #     test.map_image()
        test.print_map()
     #   for i in range(len(test.map_indices)):
     #       for j in range(len(test.map_indices[i])-1):
     #           if (test.map_indices[i][j].x + 1 != test.map_indices[i][j+1].x):
     #               print("Image:", str(38*i + j + 1), "to", str(38*i + test.map_indices[i][j+1].x + abs(test.map_indices[i][0].x) - 1) , "is missing")

        print('\nDoes the output look correct (type y to end): ')
        x = input()



# Load all png images in current pwd/images, make sure to make changes if not pngs or the directory
# isn't /images

def load_images(path):
    gray_images = []
    images = [cv2.imread(file) for file in glob.glob(path + "/*.png")]
    for i in range(len(images)):
            gray = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
            gray_images.append(gray)
    return images, gray_images


# A load function to pick the pictues in a nonrandom order //Used only for testing

def load_test_images(path):
    images = []
    gray_images = []
    x_val = 0
    y_val = 1
    c = 0
    images.append(cv2.imread(path + "/0.png"))
    images.append(cv2.imread(path + "/1.png"))
    images.append(cv2.imread(path + "/2.png"))
    images.append(cv2.imread(path + "/3.png"))
    images.append(cv2.imread(path + "/4.png"))
    images.append(cv2.imread(path + "/5.png"))
    images.append(cv2.imread(path + "/6.png"))
    images.append(cv2.imread(path + "/7.png"))
    images.append(cv2.imread(path + "/8.png"))
    images.append(cv2.imread(path + "/9.png"))
    images.append(cv2.imread(path + "/10.png"))
    images.append(cv2.imread(path + "/11.png"))
    images.append(cv2.imread(path + "/12.png"))
    images.append(cv2.imread(path + "/13.png"))
    images.append(cv2.imread(path + "/14.png"))
    images.append(cv2.imread(path + "/15.png"))
    images.append(cv2.imread(path + "/16.png"))
    images.append(cv2.imread(path + "/17.png"))
    images.append(cv2.imread(path + "/18.png"))
    images.append(cv2.imread(path + "/19.png"))
    images.append(cv2.imread(path + "/20.png"))
    images.append(cv2.imread(path + "/21.png"))
    images.append(cv2.imread(path + "/22.png"))
    images.append(cv2.imread(path + "/23.png"))

    # for j in range(4):
    #     for i in range(6):
    #             #img_name = 'images_2/y: '+ str(y_val) + ' x: ' + str(x_val) + ".png"
    #             img_name = path + "/"+ str(c) + ".png"
    #             images.append(cv2.imread(img_name))
    #             x_val += 1
    #             c += 1
    #     y_val += 1
    #     x_val = 0
    for image in range(len(images)):
        gray = cv2.cvtColor(images[image], cv2.COLOR_BGR2GRAY)
        gray_images.append(gray)
    return images, gray_images


# Creating an object for each Tile that gives it an x val, y val, and index in the images list

class Tile:
    def __init__(self, y, x, index):
        self.x = x
        self.y = y
        self.index = index


# Creates an image class with values inputted as the default confidence, current image to start,
# and the pixel count for each image which has to be identical for each image

class Image:

    # Initializes an image object with all the values below
    def __init__(self, cur_image, pixels, path):
        self.images, self.gray_images = load_images(path)
        self.cur_image = cur_image
        self.max_images = len(self.images)-1
        t = Tile(cur_image.y, cur_image.x, cur_image.index)
        self.map_indices = [[t]]
        self.first_img = cur_image.index
        self.pixels = pixels
        self.unused_images = []


    # comparison function needs an index to start with and a direction to compare the pixel values of all the other
    # images to in a north, east, south, west form
    def compare_tile(self, index, direction):
        if (direction == 'n'):
            y1 = 0
            y2 = self.pixels-1

        elif (direction == 's'):
            y1 = self.pixels-1
            y2 = 0

        elif (direction == 'e'):
            x1 = self.pixels-1
            x2 = 0

        elif (direction == 'w'):
            x1 = 0
            x2 = self.pixels-1

        color = []
        cmp_img = []


        # this loop is taking every other image in the directory loaded and checking every single pixel that
        # borders it on the side choosen. It them takes the absolute value of the difference between the grayscaled
        # version and averages that. Whatever image has the smallest average is the closest to bordering it.
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

    def print_map(self):
        for i in range(len(self.map_indices)):
            print("\n")
            for j in range(len(self.map_indices[i])):
                print(self.map_indices[i][j].y, self.map_indices[i][j].x, self.map_indices[i][j].index, end="   ")



    # This function determines where the tile should be placed in the mappings of the array
    def place_image(self, tile):
        x = 0
        y = tile.y + abs(self.map_indices[0][0].y)
        x_list = self.list_of_x()
        print(tile.index)
        if (tile.index in self.unused_images):
            self.unused_images.remove(tile.index)

        # adds a new row on top
        if (y < 0):
            self.map_indices.insert(0, [tile])
            self.max_images -= 1
        # adds a new row at the bottom
        elif (y >= len(self.map_indices)):
            self.map_indices.append([tile])
            self.max_images -= 1
        # adds an x values to a row
        else:
            self.map_indices[y].append(tile)
            self.sort_tiles()
            self.max_images -= 1

    def clear_map(self):
         self.map_indices.clear()

    # sorts all the rows by their x value
    def sort_tiles(self):
        for row in self.map_indices:
            row.sort(key=lambda x: x.x)

    #returns the number value for a tiles position in the 2D array, returns none if doesn't exist
    def get_img_index(self, y, x):
        count = 0
        for img in self.map_indices[y + abs(self.map_indices[0][0].y)]:
            if (x == img.x):
                return count
            count += 1
        return None


    # returns a list of the entire mapping but just the x values
    def list_of_x(self):
        x_list = []
        for r in range(len(self.map_indices)):
            l = []
            for c in range(len(self.map_indices[r])):
                x = self.map_indices[r][c].x
                l.append(x)
            x_list.append(l)
        return(x_list)


    # returns a list of the entire mapping but just the index values
    def list_of_images(self):
        index_list = []
        for r in range(len(self.map_indices)):
            l = []
            for c in range(len(self.map_indices[r])):
                x = self.images[self.map_indices[r][c].index]
                l.append(x)
            index_list.append(l)
        return(index_list)

    # maps out the entire image based on the starting one
    def map_image(self):
        # setting up a list that will 161show at the end which images haven't been used
        for i in range(len(self.images)):
            if i == self.cur_image.index:
                continue
            self.unused_images.append(i)

        print(self.unused_images)
        north = True
        south = True

        # goes and maps all the way up until it doesn't have enough confidence to place
        while(north == True):
            con, index = self.compare_tile(self.cur_image.index, 'n')
            n_con, n_index = self.compare_tile(index, 's')
            if (n_index == self.cur_image.index and index in self.unused_images):
                t = Tile(self.cur_image.y-1, self.cur_image.x, index)
                self.place_image(t)
                self.cur_image.index = index
                self.cur_image.y -= 1
            else:
                self.cur_image.y = 0
                self.cur_image.index = self.first_img
                north = False

        # goes and maps all the way down until it doesn't have enough confidence to place
        while(south == True):
            con, index = self.compare_tile(self.cur_image.index, 's')
            n_con, n_index = self.compare_tile(index, 'n')
            if (n_index == self.cur_image.index and index in self.unused_images):
                t = Tile(self.cur_image.y+1, self.cur_image.x, index)
                self.place_image(t)
                self.cur_image.index = index
                self.cur_image.y += 1

            else:
                south = False

        # for each row going up and down go and place images east and west all the way until it doesn't
        # have the confidence to anymore
        for row in range(len(self.map_indices)):
            # East half implementation
            east = True
            self.cur_image.x = self.map_indices[row][0].x
            self.cur_image.y = self.map_indices[row][0].y
            self.cur_image.index = self.map_indices[row][0].index
            while(east == True):
                con, index = self.compare_tile(self.cur_image.index, 'e')
                n_con, n_index = self.compare_tile(index, 'w')
                if (n_index == self.cur_image.index and index in self.unused_images):
                    t = Tile(self.cur_image.y, self.cur_image.x+1, index)
                    self.place_image(t)
                    self.cur_image.index = index
                    self.cur_image.x += 1

                else:
                    east = False

            # West half implementation
            west = True
            self.cur_image.x = self.map_indices[row][0].x
            self.cur_image.y = self.map_indices[row][0].y
            self.cur_image.index = self.map_indices[row][0].index
            while(west == True):
                con, index = self.compare_tile(self.cur_image.index, 'w')
                n_con, n_index = self.compare_tile(index, 'e')
                if (n_index == self.cur_image.index and index in self.unused_images):
                    t = Tile(self.cur_image.y, self.cur_image.x-1, index)
                    self.place_image(t)
                    self.cur_image.index = index
                    self.cur_image.x -= 1

                else:
                    west = False

        top = self.map_indices[0]
        bot = self.map_indices[-1]
        for c in range(len(self.map_indices[0])):
            # North half implementation

            north = True
            self.cur_image.x = top[c].x
            self.cur_image.y = top[c].y
            self.cur_image.index = top[c].index
            # goes and maps all the way up until it doesn't have enough confidence to place
            while(north == True):
                con, index = self.compare_tile(self.cur_image.index, 'n')
                n_con, n_index = self.compare_tile(index, 's')
                if (n_index == self.cur_image.index and index in self.unused_images):
                    t = Tile(self.cur_image.y-1, self.cur_image.x, index)
                    self.place_image(t)
                    self.cur_image.index = index
                    self.cur_image.y -= 1

                else:
                    north = False

        for col in range(len(self.map_indices[-1])):
            # south half implementation
            south = True
            self.cur_image.x = bot[col].x
            self.cur_image.y = bot[col].y
            self.cur_image.index = bot[col].index
            # goes and maps all the way down until it doesn't have enough confidence to place
            while(south == True):
                con, index = self.compare_tile(self.cur_image.index, 's')
                n_con, n_index = self.compare_tile(index, 'n')
                if (n_index == self.cur_image.index and index in self.unused_images):
                    t = Tile(self.cur_image.y+1, self.cur_image.x, index)
                    self.place_image(t)
                    self.cur_image.index = index
                    self.cur_image.y += 1

                else:
                    south = False

        # Add East and West tiles to the newly added rows on top and bottom
        for row in range(len(self.map_indices)):
            # East half implementation
            east = True
            self.cur_image.x = self.map_indices[row][-1].x
            self.cur_image.y = self.map_indices[row][-1].y
            self.cur_image.index = self.map_indices[row][-1].index
            while(east == True):
                con, index = self.compare_tile(self.cur_image.index, 'e')
                n_con, n_index = self.compare_tile(index, 'w')
                if (n_index == self.cur_image.index and index in self.unused_images):
                    t = Tile(self.cur_image.y, self.cur_image.x+1, index)
                    self.place_image(t)
                    self.cur_image.index = index
                    self.cur_image.x += 1

                else:
                    east = False

            # West half implementation
            west = True
            self.cur_image.x = self.map_indices[row][0].x
            self.cur_image.y = self.map_indices[row][0].y
            self.cur_image.index = self.map_indices[row][0].index
            while(west == True):
                con, index = self.compare_tile(self.cur_image.index, 'w')
                n_con, n_index = self.compare_tile(index, 'e')
                if (n_index == self.cur_image.index and index in self.unused_images):
                    t = Tile(self.cur_image.y, self.cur_image.x-1, index)
                    self.place_image(t)
                    self.cur_image.index = index
                    self.cur_image.x -= 1

                else:
                    west = False


        # Starting at the top row on a row to row basis fill in each row beneath with any x values that the
        # row below the current doesn't have
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
                    if (n_index == self.cur_image.index and index in self.unused_images):
                        t = Tile(self.cur_image.y+1, self.cur_image.x, index)
                        self.place_image(t)


        x_list = self.list_of_x()
        for row in range(len(self.map_indices)-1, 0, -1):
            for x in range(len(self.map_indices[row])):
                self.cur_image.x = self.map_indices[row][x].x
                self.cur_image.y = self.map_indices[row][x].y
                self.cur_image.index = self.map_indices[row][x].index
                in_next_row = False
                if (self.map_indices[row][x].x not in x_list[row-1]):
                    con, index = self.compare_tile(self.cur_image.index, 'n')
                    n_con, n_index = self.compare_tile(index, 's')
                    if (n_index == self.cur_image.index and index in self.unused_images):
                        t = Tile(self.cur_image.y-1, self.cur_image.x, index)
                        self.place_image(t)


        # This will sort the tiles by their x value
        self.sort_tiles()
        #self.print_map()
        self.build_image()

    # Fill holes and concatenate rows and then concatenate vertically to rebuild the image
    def build_image(self):
        rows = []
        black_image = cv2.imread("gray.PNG", cv2.IMREAD_COLOR)
        b = black_image[0:self.pixels, 0:self.pixels]
        self.images.append(b)
        max_x = max(self.map_indices, key=len)
        len_max_x = len(max(self.map_indices, key=len))
        x = max_x[0].x

        x_list = self.list_of_x()
        for row in range(len(self.map_indices)-1):
            #print(self.map_indices[row])
            for x in range(len(self.map_indices[row])):
                self.cur_image.x = self.map_indices[row][x].x
                self.cur_image.y = self.map_indices[row][x].y
                self.cur_image.index = self.map_indices[row][x].index
                in_next_row = False
                if (self.map_indices[row][x].x not in x_list[row+1]):
                    t = Tile(self.cur_image.y+1, self.cur_image.x, len(self.images)-1)
                    self.place_image(t)

        x_list = self.list_of_x()
        for row in range(len(self.map_indices)-1, 0, -1):
            for x in range(len(self.map_indices[row])):
                self.cur_image.x = self.map_indices[row][x].x
                self.cur_image.y = self.map_indices[row][x].y
                self.cur_image.index = self.map_indices[row][x].index
                in_next_row = False
                if (self.map_indices[row][x].x not in x_list[row-1]):
                    t = Tile(self.cur_image.y-1, self.cur_image.x, len(self.images)-1)
                    self.place_image(t)
        self.print_map()
        im = self.list_of_images()

        for r in range(len(self.map_indices)):
            rows.append(cv2.hconcat(im[r]))

        out = cv2.vconcat(rows)
        cv2.imwrite('out1.png', out)

if __name__=="__main__":
    main()
