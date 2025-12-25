from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np, copy
import json

with open(r'data/replacer.json', 'r') as replacer_file:
    json_file = json.load(replacer_file)
    replacer = json_file['map']['path_finder']    


class Finder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid_matrix = copy.deepcopy(self.matrix)
        self.zero_one_matrix = []
        self.zero_one_row = []

        for y in range(len(self.matrix)):
            self.zero_one_row = []
            for x in range(len(self.matrix[0])):
                item = matrix[y][x]
                sh_app = replacer[item]
                self.zero_one_row.append(sh_app)
            self.zero_one_matrix.append(self.zero_one_row)
        
            
    def Find(self, startX, startY, endX, endY, last_gpos):
        self.zero_one_matrix2 = copy.deepcopy(self.zero_one_matrix)
        self.zero_one_matrix2[7][12] = '0'
        self.zero_one_matrix2[7][10] = '0'
        self.zero_one_matrix2[last_gpos[1]][last_gpos[0]] = '0'

        self.finder = AStarFinder()
        self.grid = Grid(matrix=self.zero_one_matrix2)
        self.startG = self.grid.node(startX, startY)
        self.endG = self.grid.node(endX, endY)

        path_main, _ = self.finder.find_path(self.startG, self.endG, self.grid)
        path = []
        for item in path_main:
            s_add = (item.x, item.y)
            path.append(s_add)

        return path
