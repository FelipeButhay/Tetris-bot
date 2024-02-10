import pygame
import random

screen_x, screen_y = 1920, 1080
while False:
    try:
        resolution = input("resolution (x,y format): ").split(",")
        screen_x = int(resolution[0])
        screen_y = int(resolution[1]) 
        break
    except:
        pass
    
import tkinter as tk
resolution_screen = tk.Tk()
screen_x = resolution_screen.winfo_screenwidth()
screen_y = resolution_screen.winfo_screenheight()
         
square = (screen_y -90)//20
game_pos_x = (screen_x-square*10)//2
game_pos_y = 45

def remove_outs(list):
    nu_list = []
    for x in list:
        if not ((x[0][0]<0) or (x[0][0]>9) or (x[0][1]<0) or (x[0][1]>19)):
            nu_list.append(x)
    return nu_list

def only_pos(list):
    nu_list = []
    for x in list:
        nu_list.append(tuple(x[0]))
    return tuple(nu_list)

def full_line(frozen):
    for y in range(0,20):
        test_list = set((x, y) for x in range(0,10))
        frozen_set = set(only_pos(remove_outs(frozen)))
        if test_list.issubset(frozen_set):            
            for x in test_list:
                for xx in frozen[:]:
                    if x == xx[0]:
                        frozen.remove(xx)
                        break
            nu_frozen = []
            for xx in frozen:
                if (xx[0][1] < y) and (xx[0][1] != 20) and (xx[0][1] != -1) and (xx[0][0] != 10) and (xx[0][0] != -1):
                    nu_frozen.append(((xx[0][0], xx[0][1]+1), xx[1]))
                else:
                    nu_frozen.append(xx)
            return nu_frozen, 1
    return frozen, 0

def draw_all(screen, active, following, saved, frozen):
    screen.fill("black")
    pygame.draw.rect(screen, "white",(game_pos_x-15, game_pos_y-15, square*10+30, square*20+30), 0)
    pygame.draw.rect(screen, "black",(game_pos_x, game_pos_y, square*10, square*20), 0)
    
    pygame.draw.rect(screen, "white",(game_pos_x-15 + (10+3)*square, game_pos_y-15+square, square*6 + 30, square*5 + 30), 0)
    pygame.draw.rect(screen, "black",(game_pos_x + (10+3)*square, game_pos_y+square, square*6, square*5), 0)
    
    pygame.draw.rect(screen, "white",(game_pos_x-15 + (10+3)*square, game_pos_y-15+square*10, square*6 + 30, square*5 + 30), 0)
    pygame.draw.rect(screen, "black",(game_pos_x + (10+3)*square, game_pos_y+square*10, square*6, square*5), 0)
    
    pygame.draw.rect(screen, (30,30,30),(game_pos_x, game_pos_y, square*10, square*4), 0)
    frozen_print = remove_outs(frozen)
    if len(frozen_print) != 0:
        for x in frozen_print:
            pos_x = x[0][0]*square + game_pos_x
            pos_y = x[0][1]*square + game_pos_y
            pygame.draw.rect(screen, x[1],(pos_x, pos_y, square, square), 0)
    if not active == None:
        active.draw(screen)
    if not following == None:
        save_pos = following.pos
        following.pos = [14 + following.dims[0], 1 + following.dims[1]]
        following.draw(screen)
        following.pos = save_pos
    if not saved == None:
        save_pos = saved.pos
        saved.pos = [14 + saved.dims[0], 10 + saved.dims[1]]
        saved.draw(screen)
        saved.pos = save_pos
        
def write(screen, text, x, y, size, colour):
    font = pygame.font.Font(None, size)
    img = font.render(str(text), True, colour)
    screen.blit(img, (x,y))

def nu_p():
    rand_float = random.random()*sum(shape_weight)
    xx = 0
    for z,x in enumerate(shape_weight):
        xx += x
        if 0<=rand_float<xx:
            break             
    shape = shape_list[z]
    dims  = shape_dims[z]
    # colour = aux.colour_list[random.randint(0, len(aux.colour_list))-1]
    while True:
        colour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if sum(colour) > 340:
            break
    return piece([3,0], shape, colour, dims)

class piece:
    def __init__(self, position, shape, colour, dimensions):
        # 0,0 es la esquina superior izquierda
        self.pos = [position[0]+1,position[1]+1]
        self.fall = False
        self.colour = colour
        self.rotate = 0
        self.shape = shape
        self.rot = self.shape[self.rotate%4]
        self.dims = dimensions
        
    def refr(self):
        self.rot = self.shape[self.rotate%4]
        
    def draw(self, screen):
        for x in range(0, len(self.rot)):
            pos_x = self.pos[0]*square + self.rot[x][0]*square + game_pos_x
            pos_y = self.pos[1]*square + self.rot[x][1]*square + game_pos_y
            pygame.draw.rect(screen, self.colour,(pos_x, pos_y, square, square), 0)
            
    def check_colision(self, frozen):
        self.refr()
        for x in self.rot:
            x = (self.pos[0] + x[0], int(self.pos[1] + x[1]+0.99))
            # print(x, only_pos(frozen))
            if x in only_pos(frozen):
                return True
        else:
            return False
        
        
shape_I = (((-1,0), (0,0), (1,0), (2,0)), ((0,-1), (0,0), (0,1), (0,2)), ((-1,1), (0,1), (1,1), (2,1)), ((1,-1), (1,0), (1,1), (1,2)))
shape_i = (((0,0), (1,0), ), ((0,0), (0,1),), ((0,1), (1,1)), ((1,0), (1,1)))
shape_O = tuple(((0,0), (1,0), (0,1), (1,1)) for x in range(0,4))
shape_plus = tuple(((0,0), (0,1), (0,-1), (1,0), (-1,0)) for x in range(0,4))
shape_U = (((0, 0), (-1, 0), (1, 0), (-1, 1), (1, 1)), ((0, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)), ((0, 0), (1, 0), (-1, 0), (1, -1), (-1, -1)), ((0, 0), (0, 1), (0, -1), (1, 1), (1, -1)))
shape_T = (((-1, 0), (0, 0), (1, 0), (0, 1)), ((0, -1), (0, 0), (0, 1), (-1, 0)), ((1, 0), (0, 0), (-1, 0), (0, -1)), ((0, 1), (0, 0), (0, -1), (1, 0)))
shape_L1 = (((-1, 0), (0, 0), (1, 0), (-1, 1)), ((0, -1), (0, 0), (0, 1), (-1, -1)), ((1, 0), (0, 0), (-1, 0), (1, -1)), ((0, 1), (0, 0), (0, -1), (1, 1))) 
shape_L2 = (((-1, 0), (0, 0), (1, 0), (1, 1)), ((0, -1), (0, 0), (0, 1), (-1, 1)), ((1, 0), (0, 0), (-1, 0), (-1, -1)), ((0, 1), (0, 0), (0, -1), (1, -1)))
shape_LL1 = (((-1, 0), (-1, 1), (0, 0), (1, 0), (2, 0)), ((0, -1), (-1, -1), (0, 0), (0, 1), (0, 2)), ((1, 0), (1, -1), (0, 0), (-1, 0), (-2, 0)), ((0, 1), (1, 1), (0, 0), (0, -1), (0, -2)))
shape_LL2 = (((-2, 0), (-1, 0), (0, 0), (1, 0), (1, 1)), ((0, -2), (0, -1), (0, 0), (0, 1), (-1, 1)), ((2, 0), (1, 0), (0, 0), (-1, 0), (-1, -1)), ((0, 2), (0, 1), (0, 0), (0, -1), (1, -1)))
shape_S1 = (((-1, 0), (0, 0), (0, 1), (1, 1)), ((0, -1), (0, 0), (-1, 0), (-1, 1)), ((1, 0), (0, 0), (0, -1), (-1, -1)), ((0, 1), (0, 0), (1, 0), (1, -1)))
shape_S2 = (((-1, 1), (0, 1), (0, 0), (1, 0)), ((-1, -1), (-1, 0), (0, 0), (0, 1)), ((1, -1), (0, -1), (0, 0), (-1, 0)), ((1, 1), (1, 0), (0, 0), (0, -1)))
shape_P1 = (((-1, 0), (0, 0), (1, 0), (0, 1), (1, 1)), ((0, -1), (0, 0), (0, 1), (-1, 0), (-1, 1)), ((1, 0), (0, 0), (-1, 0), (0, -1), (-1, -1)), ((0, 1), (0, 0), (0, -1), (1, 0), (1, -1)))
shape_P2 = (((-1, 0), (0, 0), (1, 0), (0, 1), (-1, 1)), ((0, -1), (0, 0), (0, 1), (-1, 0), (-1, -1)), ((1, 0), (0, 0), (-1, 0), (0, -1), (1, -1)), ((0, 1), (0, 0), (0, -1), (1, 0), (1, 1)))

shape_list  = (shape_I, shape_i, shape_O, shape_plus,   shape_U,   shape_T,  shape_L1, shape_L2, shape_LL1, shape_LL2,  shape_S1,  shape_S2,  shape_P1,  shape_P2,)
shape_dims = (   (1,2),   (1,2), (1,1.5),   (1.5, 2), (1.5,1.5), (1.5,1.5), (1.5,1.5),  (2,1.5),   (1,1.5),  (2, 1.5), (1.5,1.5), (1.5,1.5), (1.5,1.5), (1.5,1.5),)
shape_weight = (     1,     0.5,       1,        0.3,       0.4,         1,       0.5,      0.5,      0.35,      0.35,       0.5,       0.5,      0.35,      0.35,)

all_shape = []
for x,xx in zip(shape_list, shape_weight):
    all_shape.append((x, xx))

# colour_list = ((0,  41, 255), ( 33, 255,   0), "red", (255, 255, 0), "magenta", (230, 120, 0), 
#                (0, 209, 255), (190, 190, 190), (34, 141, 6), (112, 0, 181), (255, 0, 124), 
#                (0, 255, 151), (108,   0, 255), (255, 164, 0), (180, 0, 53) , (6, 119, 0))