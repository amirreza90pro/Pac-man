import math
import time, pygame, pyautogui, random, zipfile
import keyboard
from matplotlib import pyplot
import math as ma
from PIL import Image
import copy, path_finder
import numpy as np
import pickle

screenWidth = 1366
screenHeight = 700

pygame.init()
root = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pac-Man')

fps = 80

def move(character, speed, dir): # pacman move
    if dir == 'r' : character.x += speed
    elif dir == 'l' : character.x -= speed
    elif dir == 'd' : character.y += speed
    elif dir == 'u' : character.y -= speed


def x_y(x, y, f):
    return f[y][x]


def pillow_to_pygame(image_pillow):
    return pygame.image.fromstring(image_pillow.tobytes(), image_pillow.size, image_pillow.mode)


def generate_number_for_map(lf):
    print('generate_number_for_map')
    f = copy.deepcopy(lf)
    for y in range(len(lf)):
        for x in range(len(lf[0])):
            if lf[y][x] == '#':
                # Check surrounding walls
                up = lf[y-1][x]
                down = lf[y+1][x]
                right = lf[y][x+1]
                left = lf[y][x-1]

                # Create the number based on the walls
                number = f"{'1' if up == '#' else '0'}{'1' if down == '#' else '0'}{'1' if right == '#' else '0'}{'1' if left == '#' else '0'}"
                # Replace the '#' with the number
                f[y][x] = number
    return f


def info(gpos, main_map): # up, down, right, left info
    x = gpos[0]
    y = gpos[1]

    up = main_map[y - 1][x]
    down = main_map[y + 1][x]
    left = main_map[y][x - 1]
    right = main_map[y][x + 1]

    return (up, down, right, left)


def canMove(gpos, dir, main_map):
    x = gpos[0]
    y = gpos[1]

    up = main_map[y-1][x]
    down = main_map[y+1][x]
    left = main_map[y][x-1]
    right = main_map[y][x+1]

    if dir == 'r' and right == '#':
        return False
    elif dir == 'l' and left == '#':
        return False
    elif dir == 'u' and up == '#':
        return False
    elif dir == 'd' and down == '#':
        return False
    else:
        return True


def canRotation(gpos, dir, to, main_map):
    x = gpos[0]
    y = gpos[1]

    up = main_map[y-1][x]
    down = main_map[y+1][x]
    left = main_map[y][x-1]
    right = main_map[y][x+1]

    if dir == 'r':
        if to == 'd' and down != '#':
            return True

        if to == 'u' and up != '#':
            return True

        if to == 'l' and left != '#':
            return True

    elif dir == 'l':
        if to == 'd' and down != '#':
            return True

        if to == 'u' and up != '#':
            return True

        if to == 'r' and right != '#':
            return True

    elif dir == 'u':
        if to == 'd' and down != '#':
            return True

        if to == 'l' and left != '#':
            return True

        if to == 'r' and right != '#':
            return True

    elif dir == 'd':
        if to == 'u' and up != '#':
            return True

        if to == 'l' and left != '#':
            return True

        if to == 'r' and right != '#':
            return True

    else:
        return False


def distance(xy, xy2):
    x1 = xy[0]
    y1 = xy[1]
    x2 = xy2[0]
    y2 = xy2[1]

    if x1 > x2:
        z1 = x1 - x2
    else:
        z1 = x2 - x1

    if y1 > y2:
        z2 = y1 - y2
    else:
        z2 = y2 - y1

    d2 = (z1 ** 2) +  (z2 ** 2)
    return math.sqrt(d2)


def GiveMePinkyTargetPos(main_map, pacman_gpos, pacman_dir):
    pass


def ListToStr(_list_):
    string = ''
    for item in _list_:
        string += str(item)
    return string

def ghosts_soft_moving(ghost, dir):
    if dir == 'left' : ghost.x -= 1
    elif dir == 'right' : ghost.x += 1
    elif dir == 'up' : ghost.y -= 1
    elif dir == 'down' : ghost.y += 1


def set_dir(gpos, target_gpos):
    if target_gpos[0] - gpos[0] == -1 : return 'left'
    elif target_gpos[0] - gpos[0] == 1 : return 'right'
    elif target_gpos[1] - gpos[1] == -1 : return 'up'
    elif target_gpos[1] - gpos[1] == 1 : return 'down'
    
    
class all:
    class map:
        def setup(self):
            self.main_map = [
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],
                ["S", "S", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", " ", "#", "#", " ", "#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", "#", " ", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", " ", "#", "#", " ", "#", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#", "#", " ", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", "#", "#", "#", " ", "#", "#", "#", "S", "#", "S", "#", "#", "#", " ", "#", "#", "#", "#", "S", "S"],
                ["S", "S", "S", "S", "S", "#", " ", "#", "S", "S", "S", "S", "S", "S", "S", "#", " ", "#", "S", "S", "S", "S", "S"],
                ["S", "#", "#", "#", "#", "#", " ", "#", "S", "#", "#", "S", "#", "#", "S", "#", " ", "#", "#", "#", "#", "#", "S"],
                ["T", "S", "S", "S", "S", "S", " ", "S", "S", "#", "S", "B", "S", "#", "S", "S", " ", "S", "S", "S", "S", "S", "T"],
                ["S", "#", "#", "#", "#", "#", " ", "#", "S", "#", "#", "#", "#", "#", "S", "#", " ", "#", "#", "#", "#", "#", "S"],
                ["S", "S", "S", "S", "S", "#", " ", "#", "S", "S", "S", "S", "S", "S", "S", "#", " ", "#", "S", "S", "S", "S", "S"],
                ["S", "S", "#", "#", "#", "#", " ", "#", "S", "#", "#", "#", "#", "#", "S", "#", " ", "#", "#", "#", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", " ", "#", "#", " ", "#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", "#", " ", "#", "S", "S"],
                ["S", "S", "#", " ", " ", "#", " ", " ", " ", " ", " ", "@", " ", " ", " ", " ", " ", "#", " ", " ", "#", "S", "S"],
                ["S", "S", "#", "#", " ", "#", " ", "#", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#", " ", "#", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", " ", "#", "#", "#", "#", "#", "#", " ", "#", " ", "#", "#", "#", "#", "#", "#", " ", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "S", "S"],
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"]
             ]



        main_map = [
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],
                ["S", "S", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", "D", "#", "#", " ", "#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", "#", "D", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", " ", "#", "#", " ", "#", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#", "#", " ", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", "#", "#", "#", " ", "#", "#", "#", "S", "#", "S", "#", "#", "#", " ", "#", "#", "#", "#", "S", "S"],
                ["S", "S", "S", "S", "S", "#", " ", "#", "S", "S", "S", "S", "S", "S", "S", "#", " ", "#", "S", "S", "S", "S", "S"],
                ["S", "#", "#", "#", "#", "#", " ", "#", "S", "#", "#", "S", "#", "#", "S", "#", " ", "#", "#", "#", "#", "#", "S"],
                ["T", "S", "S", "S", "S", "S", " ", "S", "S", "#", "S", "B", "S", "#", "S", "S", " ", "S", "S", "S", "S", "S", "T"],
                ["S", "#", "#", "#", "#", "#", " ", "#", "S", "#", "#", "#", "#", "#", "S", "#", " ", "#", "#", "#", "#", "#", "S"],
                ["S", "S", "S", "S", "S", "#", " ", "#", "S", "S", "S", "S", "S", "S", "S", "#", " ", "#", "S", "S", "S", "S", "S"],
                ["S", "S", "#", "#", "#", "#", " ", "#", "S", "#", "#", "#", "#", "#", "S", "#", " ", "#", "#", "#", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", " ", "#", "#", " ", "#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", "#", " ", "#", "S", "S"],
                ["S", "S", "#", "D", " ", "#", " ", " ", " ", " ", " ", "@", " ", " ", " ", " ", " ", "#", " ", "D", "#", "S", "S"],
                ["S", "S", "#", "#", " ", "#", " ", "#", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#", " ", "#", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", " ", "#", "#", "#", "#", "#", "#", " ", "#", " ", "#", "#", "#", "#", "#", "#", " ", "#", "S", "S"],
                ["S", "S", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", "S", "S"],
                ["S", "S", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "S", "S"],
                ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"]
             ]


        map = []
        ghosts_map = []
        array_map = []

        m_0000 = pygame.image.load(r'resourse\Main pack\walls\0000.png')
        m_0001 = pygame.image.load(r'resourse\Main pack\walls\0001.png')
        m_0010 = pygame.image.load(r'resourse\Main pack\walls\0010.png')
        m_0011 = pygame.image.load(r'resourse\Main pack\walls\0011.png')
        m_0100 = pygame.image.load(r'resourse\Main pack\walls\0100.png')
        m_0101 = pygame.image.load(r'resourse\Main pack\walls\0101.png')
        m_0110 = pygame.image.load(r'resourse\Main pack\walls\0110.png')
        m_0111 = pygame.image.load(r'resourse\Main pack\walls\0111.png')
        m_1000 = pygame.image.load(r'resourse\Main pack\walls\1000.png')
        m_1001 = pygame.image.load(r'resourse\Main pack\walls\1001.png')
        m_1010 = pygame.image.load(r'resourse\Main pack\walls\1010.png')
        m_1011 = pygame.image.load(r'resourse\Main pack\walls\1011.png')
        m_1100 = pygame.image.load(r'resourse\Main pack\walls\1100.png')
        m_1101 = pygame.image.load(r'resourse\Main pack\walls\1101.png')
        m_1111 = pygame.image.load(r'resourse\Main pack\walls\1111.png')
        m_1110 = pygame.image.load(r'resourse\Main pack\walls\1110.png')



    class pacman:
        pacmap = []


        fm = 0.08
        mode = 0.08
        sprite = 1
        direction = 'r'
        speed = 2


        pr1 = pygame.image.load(r'resourse\Main pack\pacman\right\r1.png')
        pr2 = pygame.image.load(r'resourse\Main pack\pacman\right\r2.png')
        pr3 = pygame.image.load(r'resourse\Main pack\pacman\right\r3.png')
        pr4 = pygame.image.load(r'resourse\Main pack\pacman\right\r4.png')

        pl1 = pygame.image.load(r'resourse\Main pack\pacman\left\l1.png')
        pl2 = pygame.image.load(r'resourse\Main pack\pacman\left\l2.png')
        pl3 = pygame.image.load(r'resourse\Main pack\pacman\left\l3.png')
        pl4 = pygame.image.load(r'resourse\Main pack\pacman\left\l4.png')

        pu1 = pygame.image.load(r'resourse\Main pack\pacman\up\u1.png')
        pu2 = pygame.image.load(r'resourse\Main pack\pacman\up\u2.png')
        pu3 = pygame.image.load(r'resourse\Main pack\pacman\up\u3.png')
        pu4 = pygame.image.load(r'resourse\Main pack\pacman\up\u4.png')

        pd1 = pygame.image.load(r'resourse\Main pack\pacman\down\d1.png')
        pd2 = pygame.image.load(r'resourse\Main pack\pacman\down\d2.png')
        pd3 = pygame.image.load(r'resourse\Main pack\pacman\down\d3.png')
        pd4 = pygame.image.load(r'resourse\Main pack\pacman\down\d4.png')

        size = pr1.get_height()

        gpos = (11, 16)
        x, y = gpos[0] * size, gpos[1]*size

        
    
    class dots:
        p1 = pygame.image.load(r'resourse\Main pack\dots\1.png')
        p2 = pygame.image.load(r'resourse\Main pack\dots\2.png')
        p4 = pygame.image.load(r'resourse\Main pack\dots\4.png')
        p5 = pygame.image.load(r'resourse\Main pack\dots\5.png')
        p6 = pygame.image.load(r'resourse\Main pack\dots\6.png')
        p7 = pygame.image.load(r'resourse\Main pack\dots\7.png')

        dotCounter = 0

        size = p1.get_height()
        
        class super_dots:
            p3 = pygame.image.load(r'resourse\Main pack\dots\3.png')
            size = p3.get_height()
            


    class ghosts:
        RandomSpotsYouCanGo = []
        class blinky:
            mode = 'chase'
            
            pr = pygame.image.load(r'resourse\Main pack\ghosts\blinky\r.png')
            pl = pygame.image.load(r'resourse\Main pack\ghosts\blinky\l.png')
            pf = pygame.image.load(r'resourse\Main pack\ghosts\blinky\f.png')
            p_Frightened_mode = pygame.image.load(r'resourse\Main pack\ghosts\Frightened\1.png')
            p_eated = pygame.image.load(r'resourse\Main pack\ghosts\eated\1.png')

            block = pygame.image.load(r'resourse\Main pack\rosekane_148.png')

            size = pr.get_height()
            pre = 10

            gpos = (11, 10)
            last_gpos = (10, 10)
            x, y = gpos[0] * size, gpos[1]*size
            speed = 10
            dir = 'up'
            
            max_scared_timer = 450
            scared_timer = 0
            
            home_gpos = (11, 10)
            scatter_mode_path = [(17, 4), (17, 2)]
            whitch_scatter_mode_im_in = 0
            


class gui:
    class render:
        wall_rendering = {
            '0000' : all.map.m_0000,
            '0001' : all.map.m_0001,
            '0010' : all.map.m_0010,
            '0011' : all.map.m_0011,
            '0100' : all.map.m_0100,
            '0101' : all.map.m_0101,
            '0110' : all.map.m_0110,
            '0111' : all.map.m_0111,
            '1000' : all.map.m_1000,
            '1001' : all.map.m_1001,
            '1010' : all.map.m_1010,
            '0010' : all.map.m_0010,
            '1011' : all.map.m_1011,
            '1100' : all.map.m_1100,
            '1101' : all.map.m_1101,
            '1110' : all.map.m_1110,
            '1111' : all.map.m_1111,
        }

        wall_rendering_map = []


all = all()
GUI = gui()
Render = GUI.render()
c_map = all.map()
c_map.setup()
all.pacman.pacmap = all.map.main_map
class_blinky = all.ghosts.blinky()

# setups
 # map
all.map.map = generate_number_for_map(c_map.main_map)
all.map.ghosts_map = generate_number_for_map(c_map.main_map)
blinky_path = [all.ghosts.blinky.gpos, all.ghosts.blinky.gpos, all.ghosts.blinky.gpos]
with open(r'data\random spots for ghosts.bin', 'br') as random_spots_file : all.ghosts.RandomSpotsYouCanGo = pickle.load(random_spots_file)

# << #tab >>

array_map = []
for y in c_map.map:
    array_map.append(np.array(y))
c_map.array_map = np.array(array_map).copy()
del(array_map)

# << #tab >>

wall_rendering_map = []
row_of_rendering_map = []

for y_render_setup in range(len(c_map.map)):
    row_of_rendering_map = []
    for x_render_setup in range(len(c_map.map[0])):
        item  = c_map.map[y_render_setup][x_render_setup]

        if item == 'S' or item == ' ' or item == 'T' or item == 'B' or item == '@' :
            row_of_rendering_map.append(' ')

        else:
            should_app = Render.wall_rendering[item]
            row_of_rendering_map.append(should_app)
    wall_rendering_map.append(row_of_rendering_map)

all.map.wall_rendering_map = wall_rendering_map
del(wall_rendering_map)

finder = path_finder.Finder(all.map.main_map)
target_path = [all.ghosts.blinky.gpos, all.ghosts.blinky.gpos, all.ghosts.blinky.gpos, all.ghosts.blinky.gpos]
frame_timer = 0
# main loop
runing = True
if __name__ == '__main__':
    while runing:
        root.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False

        frame_timer += 1
        all.ghosts.blinky.scared_timer += 1
        # pacman teleprot
        x = all.pacman.gpos[0]
        y = all.pacman.gpos[1]

        is_pacman_find = False
        is_blinky_find = False

        if all.pacman.gpos == (21, 10):
            # remove pacman
            all.map.map[all.pacman.gpos[1]][all.pacman.gpos[0]] = ' '

            # tp and update pacman pos
            all.map.map[10][2] = '@'
            all.pacman.gpos = (2, 10)
            all.pacman.x = 2 * all.pacman.size
            all.pacman.y = 10 * all.pacman.size

        elif all.pacman.gpos == (1, 10):
            # remove pacman
            all.map.map[all.pacman.gpos[1]][all.pacman.gpos[0]] = ' '

            # replace pacman with dot
            all.map.map[10][20] = '@'

            # update pacman pos
            all.pacman.gpos = (20, 10)
            all.pacman.x = 20 * all.pacman.size
            all.pacman.y = 10 * all.pacman.size
        

        if all.ghosts.blinky.gpos == (21, 10):
            # remove blinky
            all.map.map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]] = ' '

            # tp and update pacman pos
            all.map.map[10][2] = 'B'
            all.ghosts.blinky.gpos = (2, 10)
            all.ghosts.blinky.x = 2 * all.ghosts.blinky.size
            all.ghosts.blinky.y = 10 * all.ghosts.blinky.size

        elif all.ghosts.blinky.whitch_scatter_mode_im_in == (1, 10):
            # remove pacman
            all.map.map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]] = ' '

            # replace pacman with dot
            all.map.map[10][20] = 'B'

            # update pacman pos
            all.ghosts.blinky.gpos = (20, 10)
            all.ghosts.blinky.x = 20 * all.ghosts.blinky.size
            all.ghosts.blinky.y = 10 * all.ghosts.blinky.size


        # pacman dir
        if pygame.key.get_pressed()[pygame.K_d] and all.pacman.y % all.pacman.size == 0  and canRotation(all.pacman.gpos, all.pacman.direction, 'r', all.map.main_map):
            all.pacman.direction = 'r'
        elif pygame.key.get_pressed()[pygame.K_a] and all.pacman.y % all.pacman.size == 0 and canRotation(all.pacman.gpos, all.pacman.direction, 'l', all.map.main_map):
            all.pacman.direction = 'l'
        elif pygame.key.get_pressed()[pygame.K_w] and all.pacman.x % all.pacman.size == 0 and canRotation(all.pacman.gpos, all.pacman.direction, 'u', all.map.main_map):
            all.pacman.direction = 'u'
        elif pygame.key.get_pressed()[pygame.K_s] and all.pacman.x % all.pacman.size == 0 and canRotation(all.pacman.gpos, all.pacman.direction, 'd', all.map.main_map):
            all.pacman.direction = 'd'


        # can pacman move
        if canMove(all.pacman.gpos, all.pacman.direction, all.map.main_map):
            move(all.pacman, all.pacman.speed, all.pacman.direction)

        # rendering 
          # walls 
        for y_render in range(len(all.map.wall_rendering_map)):
            for x_render in range(len(all.map.wall_rendering_map[0])):
                item = all.map.wall_rendering_map[y_render][x_render] 
                if not(item == ' ' or item == 'B'): root.blit(item, (20 * x_render, 20 * y_render))
            
            # render dots
            main_map_row = np.array(all.map.main_map[y_render])
            where_dots = list(np.where(main_map_row == ' ')[0])
            all.dots.dotCounter += len(where_dots)

            for x_dots in where_dots:
                root.blit(all.dots.p2, (x_dots * all.dots.size, y_render * all.dots.size))
                
                
            # render super dots
            main_map_row = np.array(all.map.main_map[y_render])
            where_dots = list(np.where(main_map_row == 'D')[0])
            
            for x_dots in where_dots:
                root.blit(all.dots.super_dots.p3, (x_dots * all.dots.super_dots.size, y_render * all.dots.super_dots.size))



            # pacman
            where_pacman = list(np.where(main_map_row == '@')[0])
            if len(where_pacman) != 0:  
                # render pacman
                bx = all.pacman.x
                by = all.pacman.y

                if all.pacman.direction == 'r':
                    if round(all.pacman.sprite) == 1: root.blit(all.pacman.pr1, (bx, by))
                    elif round(all.pacman.sprite) == 2: root.blit(all.pacman.pr2, (bx, by))
                    elif round(all.pacman.sprite) == 3: root.blit(all.pacman.pr3, (bx, by))
                    elif round(all.pacman.sprite) == 4: all.pacman.sprite = 3 ; all.pacman.mode = -all.pacman.fm ; root.blit(all.pacman.pr3, (bx, by))
                    elif round(all.pacman.sprite) == 0: all.pacman.sprite = 2 ; all.pacman.mode = all.pacman.fm ; root.blit(all.pacman.pr1, (bx, by))
                elif all.pacman.direction == 'l':
                    if round(all.pacman.sprite) == 1: root.blit(all.pacman.pl1, (bx, by))
                    elif round(all.pacman.sprite) == 2: root.blit(all.pacman.pl2, (bx, by))
                    elif round(all.pacman.sprite) == 3: root.blit(all.pacman.pl3, (bx, by))
                    elif round(all.pacman.sprite) == 4: all.pacman.sprite = 3 ; all.pacman.mode = -all.pacman.fm ; root.blit(all.pacman.pl3, (bx, by))
                    elif round(all.pacman.sprite) == 0: all.pacman.sprite = 2 ; all.pacman.mode = all.pacman.fm ; root.blit(all.pacman.pl1, (bx, by))
                elif all.pacman.direction == 'u':
                    if round(all.pacman.sprite) == 1: root.blit(all.pacman.pu1, (bx, by))
                    elif round(all.pacman.sprite) == 2: root.blit(all.pacman.pu2, (bx, by))
                    elif round(all.pacman.sprite) == 3: root.blit(all.pacman.pu3, (bx, by))
                    elif round(all.pacman.sprite) == 4: all.pacman.sprite = 3 ; all.pacman.mode = -all.pacman.fm ; root.blit(all.pacman.pu3, (bx, by))
                    elif round(all.pacman.sprite) == 0: all.pacman.sprite = 2 ; all.pacman.mode = all.pacman.fm ; root.blit(all.pacman.pu1, (bx, by))
                elif all.pacman.direction == 'd':
                    if round(all.pacman.sprite) == 1: root.blit(all.pacman.pd1, (bx, by))
                    elif round(all.pacman.sprite) == 2: root.blit(all.pacman.pd2, (bx, by))
                    elif round(all.pacman.sprite) == 3: root.blit(all.pacman.pd3, (bx, by))
                    elif round(all.pacman.sprite) == 4: all.pacman.sprite = 3 ; all.pacman.mode = -all.pacman.fm ; root.blit(all.pacman.pd3, (bx, by))
                    elif round(all.pacman.sprite) == 0: all.pacman.sprite = 2 ; all.pacman.mode = all.pacman.fm ; root.blit(all.pacman.pd1, (bx, by))
                all.pacman.sprite += all.pacman.mode

                if not(is_pacman_find) and all.pacman.x % all.pacman.size == 0 and all.pacman.y % all.pacman.size == 0:
                    # move pacman
                    pcx = where_pacman[0]
                    pcy = y_render
                    
                    all.map.map[pcy][pcx] = 'S'
                    all.map.main_map[pcy][pcx] = 'S'
                    if all.map.main_map[all.pacman.y // all.pacman.size][all.pacman.x // all.pacman.size] == 'D': all.ghosts.blinky.cared_timer = 0 ; all.ghosts.blinky.mode = 'Frightened' ; all.ghosts.blinky.scared_timer = 0
                    all.map.map[all.pacman.y // all.pacman.size][all.pacman.x // all.pacman.size] = '@'
                    all.map.main_map[all.pacman.y // all.pacman.size][all.pacman.x // all.pacman.size] = '@'
                    all.pacman.gpos = (all.pacman.x // all.pacman.size, all.pacman.y // all.pacman.size)
                    is_pacman_find = True
            
        # blinky
        if all.ghosts.blinky.mode == 'chase' or all.ghosts.blinky.mode == 'scatter':
            root.blit(all.ghosts.blinky.pf, (all.ghosts.blinky.x, all.ghosts.blinky.y))
        elif all.ghosts.blinky.mode == 'Frightened':
            root.blit(all.ghosts.blinky.p_Frightened_mode, (all.ghosts.blinky.x, all.ghosts.blinky.y))
        else:
            root.blit(all.ghosts.blinky.p_eated, (all.ghosts.blinky.x, all.ghosts.blinky.y))
        # root.blit(all.ghosts.blinky.block, (all.ghosts.blinky.last_gpos[0]*20, all.ghosts.blinky.last_gpos[1]*20))
        
        
        # checks
        # check win
        if all.dots.dotCounter == 0:
            print('you win')
            runing = False
        all.dots.dotCounter = 0


        
        if all.pacman.gpos == all.ghosts.blinky.gpos:
            # check lose
            if all.ghosts.blinky.mode == 'chase' or all.ghosts.blinky.mode == 'scatter':
                print('exit')
                runing = False
            
            else:
                all.ghosts.blinky.mode = 'eated'
                        
        
        if all.ghosts.blinky.mode == 'chase':
        # Move blinky
            if frame_timer >= all.ghosts.blinky.speed:
                # find the path
                target_path = finder.Find(all.ghosts.blinky.gpos[0], all.ghosts.blinky.gpos[1], all.pacman.gpos[0], all.pacman.gpos[1], all.ghosts.blinky.last_gpos)
                try: go_to = target_path[1]
                except : go_to = all.ghosts.blinky.gpos

                all.ghosts.blinky.dir = set_dir(all.ghosts.blinky.gpos, target_path[2])
                
                blinky_text_list1 = all.map.ghosts_map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]]
                blinky_text_list2 = list(blinky_text_list1)
                all.map.ghosts_map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]] = ListToStr(blinky_text_list2)
                del blinky_text_list1
                del blinky_text_list2
                    
                gridX = go_to[0]
                gridY = go_to[1]

                all.ghosts.blinky.last_gpos = copy.deepcopy(all.ghosts.blinky.gpos)

                # Move the blinky
                all.ghosts.blinky.gpos = (gridX, gridY)
                all.ghosts.blinky.x = gridX * 20
                all.ghosts.blinky.y = gridY * 20
                all.map.ghosts_map[gridX][gridY] += 'B'

                frame_timer = 0
        
        
        elif frame_timer >= 11:
            if all.ghosts.blinky.mode == 'scatter':
                # Move blinky
                # find the path
                if target_path[(len(target_path)-1)] == all.ghosts.blinky.gpos:
                    all.ghosts.blinky.whitch_scatter_mode_im_in += 1
                    if all.ghosts.blinky.whitch_scatter_mode_im_in == len(all.ghosts.blinky.scatter_mode_path) : all.ghosts.blinky.whitch_scatter_mode_im_in = 0
                    
                    
                target_path = finder.Find(all.ghosts.blinky.gpos[0], all.ghosts.blinky.gpos[1], all.ghosts.blinky.scatter_mode_path[all.ghosts.blinky.whitch_scatter_mode_im_in][0], all.ghosts.blinky.scatter_mode_path[all.ghosts.blinky.whitch_scatter_mode_im_in][1], all.ghosts.blinky.last_gpos)
                try: go_to = target_path[1]
                except : go_to = all.ghosts.blinky.gpos
                
                all.ghosts.blinky.dir = set_dir(all.ghosts.blinky.gpos, go_to)
                    
                blinky_text_list1 = all.map.ghosts_map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]]
                blinky_text_list2 = list(blinky_text_list1)
                all.map.ghosts_map[all.ghosts.blinky.gpos[cared_timer1]][all.ghosts.blinky.gpos[0]] = ListToStr(blinky_text_list2)
                del blinky_text_list1
                del blinky_text_list2
                        
                gridX = go_to[0]
                gridY = go_to[1]

                all.ghosts.blinky.last_gpos = copy.deepcopy(all.ghosts.blinky.gpos)

                # Move the blinky
                all.ghosts.blinky.gpos = (gridX, gridY)
                all.ghosts.blinky.x = gridX * 20
                all.ghosts.blinky.y = gridY * 20
                all.map.ghosts_map[gridX][gridY] += 'B'

                frame_timer = 0
                
                
            elif all.ghosts.blinky.mode == 'Frightened':
                # blinky
                # find the path
                target = random.choice(all.ghosts.RandomSpotsYouCanGo)
                target_path = finder.Find(all.ghosts.blinky.gpos[0], all.ghosts.blinky.gpos[1], target[0], target[1], all.ghosts.blinky.last_gpos)
                try: go_to = target_path[1]
                except : go_to = all.ghosts.blinky.gpos
                
                all.ghosts.blinky.dir = set_dir(all.ghosts.blinky.gpos, go_to)
                
                blinky_text_list1 = all.map.ghosts_map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]]
                blinky_text_list2 = list(blinky_text_list1)
                all.map.ghosts_map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]] = ListToStr(blinky_text_list2)
                del blinky_text_list1
                del blinky_text_list2
                    
                gridX = go_to[0]
                gridY = go_to[1]

                all.ghosts.blinky.last_gpos = copy.deepcopy(all.ghosts.blinky.gpos)

                # Move the blinky
                all.ghosts.blinky.gpos = (gridX, gridY)
                all.ghosts.blinky.x = gridX * 20
                all.ghosts.blinky.y = gridY * 20
                all.map.ghosts_map[gridX][gridY] += 'B'
                
                if all.ghosts.blinky.scared_timer >= all.ghosts.blinky.max_scared_timer: all.ghosts.blinky.mode = 'chase'
                
                frame_timer = 0
                
            if all.ghosts.blinky.mode == 'eated':
                # Move blinky
                # find the path         
                target_path = finder.Find(all.ghosts.blinky.gpos[0], all.ghosts.blinky.gpos[1], all.ghosts.blinky.home_gpos[0], all.ghosts.blinky.home_gpos[1], all.ghosts.blinky.last_gpos)
                try: go_to = target_path[1]
                except : go_to = all.ghosts.blinky.gpos
                if go_to == all.ghosts.blinky.gpos: all.ghosts.blinky.mode = 'chase'
                
                all.ghosts.blinky.dir = set_dir(all.ghosts.blinky.gpos, go_to)
                    
                blinky_text_list1 = all.map.ghosts_map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]]
                blinky_text_list2 = list(blinky_text_list1)
                all.map.ghosts_map[all.ghosts.blinky.gpos[1]][all.ghosts.blinky.gpos[0]] = ListToStr(blinky_text_list2)
                del blinky_text_list1
                del blinky_text_list2
                        
                gridX = go_to[0]
                gridY = go_to[1]

                all.ghosts.blinky.last_gpos = copy.deepcopy(all.ghosts.blinky.gpos)

                # Move the blinky
                all.ghosts.blinky.gpos = (gridX, gridY)
                all.ghosts.blinky.x = gridX * 20
                all.ghosts.blinky.y = gridY * 20
                all.map.ghosts_map[gridX][gridY] += 'B'
                
                frame_timer = 0
                
        ghosts_soft_moving(all.ghosts.blinky, all.ghosts.blinky.dir)

        
        

        all.dots.dotCounter = 0
        pygame.display.flip()
        pygame.time.Clock().tick(fps)


