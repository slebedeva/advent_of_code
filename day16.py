# classes for d16 puzzle

import numpy as np

# matrix as object
class InputMatrix:
    """ Stores the array of mirrors and the path of lasers """
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.mat = np.array([[char for char in line] for line in f.read().splitlines()])
        self.mask = np.zeros(self.mat.shape, dtype=bool)
        #mask of two steps before:
        self.past = np.zeros(self.mat.shape, dtype=bool)
        # initiate list of lasers
        #self.lasers = [] #provide it as external list


    def update(self, lasers):
        """ Update boolean mask after moving all lasers once one by one """

        # move each laser
        for i,laser in enumerate(lasers):
            laser.move()

        # check if coord still valid and write mask only then
        # separate it here because the list of lasers may have changed after the move!
        to_remove = []
        for i,laser in enumerate(lasers):
            if laser.check():
                self.mask[tuple(laser.coord)]=True
            # if it is off the edge record and clean
            else:
                to_remove.append(i)
        # check all lasers and kick out invalid
        for i in to_remove:
            del lasers[i]
        #self.lasers = [laser for laser in self.lasers if laser.check()]

# laser as object
class Laser:
    # helper to flip axis/direction (class attribute)
    flip_dict={0:1, 1:0, '+':'-', '-':'+'}

    def __init__(self, input_matrix: InputMatrix, coord=[0,0], ax=1, direction='+'):
        self.coord=coord
        self.ax=ax
        self.direction=direction
        self.input_matrix=input_matrix
        # add yourself to the list of beams in your matrix
        # self.input_matrix.lasers.append(self)
        # update your input matrixes mask to True at your start posiiton
        self.input_matrix.mask[tuple(self.coord)] = True

    def check(self):
        """Checks if coordinates are over the edge"""
        if (self.coord[0] < 0) or (self.coord[1] < 0) or (self.coord[0] >= self.input_matrix.mat.shape[0]) or (self.coord[1] >= self.input_matrix.mat.shape[1]): #if I have 10 lines last index is 9
            return False
        else:
            return True

    def update_coord(self):
        """ Moves laser by one step depending on set properties """
        self.coord[self.ax] = eval(str(self.coord[self.ax])+self.direction+'1')
        #self.check()

    def split(self):
        """ Creates a copy at the same place with different direction """
        print('splitting')
        return Laser(self.input_matrix, self.coord.copy(),
                     self.ax, Laser.flip_dict[self.direction])

    def move(self):
        """ Updates laser properties according to rules and calls update_coord() """

        # current char defines the rule
        current_char = self.input_matrix.mat[tuple(self.coord)]

        # case: goes straight on
        if (current_char == '.') or (current_char == '-' and self.ax == 1) or (current_char == '|' and self.ax == 0):
            self.update_coord()

        # case: deflects 90 degrees
        elif current_char == '/':
            # it will flip axis and direction
            self.ax = Laser.flip_dict[self.ax]
            self.direction = Laser.flip_dict[self.direction]
            self.update_coord()
        elif current_char == '\\':
            # it will flip axis
            self.ax = Laser.flip_dict[self.ax]
            self.update_coord()

        # case: split beam # this is actually a combination of \ and /
        elif (current_char == '-' and self.ax == 0) or \
            (current_char == '|' and self.ax == 1):
            self.ax = Laser.flip_dict[self.ax]
            newlaser = self.split()
            print(f'newlaser coord: {newlaser.coord}')
            self.update_coord()
            print(f'old laser coord: {self.coord}')
            newlaser.update_coord()
            print(f'new laser coord: {newlaser.coord}')
