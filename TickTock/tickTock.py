# Mathematics Game
# Given multiple expressions and operations,
# you must produce a specified number

import pygame,sys,random
from operator import attrgetter
from pygame.locals import *

##########
# Colors #
##########

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)


##########
# Images #
##########

bgi_main = pygame.image.load("tickTock_bgi.jpg")
plus_img = pygame.image.load("plus_img.png")
minus_img = pygame.image.load("minus_img.png")
mult_img = pygame.image.load("mult_img.png")
div_img = pygame.image.load("div_img.png")
print(type(bgi_main))

################
# Choice Lists #
################

op_lst = ['+','-','*','/']
op_dic = {'+':'+','-':'–','*':'•','/':'÷'}
num_lst = [str(x) for x in range(101)]


####################
# Dictionary Lists #
####################





#############
# Functions #
#############

def pick_choices(num_num):
    '''
    Randomly chooses operators & numbers from 
    corresponding lists given the number of 
    numbers
    '''
    chosen_num_lst = []
    chosen_op_lst = []
    for i in range(num_num):
        chosen_num_lst.append(random.choice(num_lst))
        chosen_op_lst.append(random.choice(op_lst))
        if i == num_num-1:
            chosen_num_lst.append(random.choice(num_lst))
    return chosen_num_lst,chosen_op_lst

def make_exp(chosen_num_lst,chosen_op_lst):
    '''
    Given two lists (number & operator), returns
    a string of expressions
    '''
    exp = ''
    random.shuffle(chosen_num_lst)
    random.shuffle(chosen_op_lst)
    len_op_lst = len(chosen_op_lst)
    for i in range(len_op_lst):
        exp += chosen_num_lst[i]
        exp += chosen_op_lst[i]
        if i == len_op_lst-1:
            exp += chosen_num_lst[len_op_lst]
    return exp

def exp_eval(exp):
    '''
    Returns a value of an expression
    '''
    return eval(exp)


def make_num_img(chosen_num_lst,chosen_op_lst):
    '''
    Given two sub-lists of numbers & operators, returns
    lists of corresponding pygame images
    '''
    num_img_lst = []
    op_img_lst = []
    # font = pygame.font.SysFont('Times New Roman,Arial',30)
    for num in chosen_num_lst:
        text = font.render(num,True,WHITE,GREY)
        num_img_lst.append(text)
    for op in chosen_op_lst:
        text = font.render(op_dic[op],True,WHITE,GREY)
        op_img_lst.append(text)
    return num_img_lst,op_img_lst



def make_dic(chosen_num_lst,chosen_op_lst,num_img_lst,op_img_lst):
    '''
    Given three lists (number & operator & image), 
    returns a dictionary of the form 
    {'image':'string'}
    '''
    dic = {}
    for i in range(len(num_img_lst)):
        dic[num_img_lst[i]] = chosen_num_lst[i]
    for j in range(len(op_img_lst)):
        dic[op_img_lst[j]] = chosen_op_lst[j]
    return dic

def blit_places_and_equal(len_dic,value):
    '''
    Blits placeholders (underscores) 
    for len_dic times
    '''
    start_pos = [70,300]
    places_pos_lst = []
    for temp in range(len_dic):
        text = blit_text('__',tuple(start_pos))
        print(text.get_width())
        print(text.get_height())
        places_pos_lst.append(start_pos[:]) 
        start_pos[0] += 80
    screen.blit(font.render('=',True,WHITE),tuple(start_pos))
    start_pos[0] += 50
    screen.blit(font.render(str(int(value)),True,WHITE),tuple(start_pos))
    pygame.display.update()
    return places_pos_lst

def blit_text(string,pos):
    '''
    Blits string on the screen at
    a given position
    '''
    text = font.render(string,True,WHITE)
    screen.blit(text,pos)
    pygame.display.update()
    return text

def blit_num_and_op(dic):
    '''
    Given a dictionary {'img':'string'},
    blits each texts on the screen
    '''
    start_pos = [175,400]
    pos_lst = []
    for text in (chosen_num_lst+chosen_op_lst):
        # screen.blit(text,tuple(start_pos))
        pos_lst.append(start_pos[:])
        start_pos[0] += 80
        # print(pos_lst)
    # pygame.display.update()
    return pos_lst

def button_highlighter(place_num):
    '''
    Given a matrix of [text,pos] and placement of 
    underscore, highlights a choice by bliting new
    text
    '''
    # choices_pos_lst[place_num][0].set_colorkey(GREY)
    # screen.blit(choices_pos_lst[place_num][0],
    #             choices_pos_lst[place_num][1])
    # pygame.display.update()
    counter = 0
    for value in dic.values():
        if counter == place_num:
            if value in op_dic:
                value = op_dic[value]
            text = font.render(value,True,RED)
            screen.blit(text,choices_pos_lst[place_num])
            pygame.display.update()
        counter += 1

    # dic_lst = list(dic)
    # dic_lst[place_num].fill(RED)
    # dic_lst[place_num].blit()
    # screen.blit(dic_lst[place_num],
    #             tuple(choices_pos_lst[place_num]))
    # pygame.display.update()

def check_sprite(sprite_lst,sprite):

    if sprite in sprite_lst:
        return True

#################
# Sprite Places #
#################

class Place(pygame.sprite.Sprite):

    def __init__(self,screen,)



##################
# Sprite Choices #
##################


class Choice(pygame.sprite.Sprite):

    def __init__(self,screen,string,start_pos,color,bcolor=None):

        super(Choice,self).__init__()

        self.color = color
        self.bcolor = bcolor
        self.string = string
        self.image = font.render(self.string,True,color,bcolor)
        self.screen = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.start_pos = start_pos
        self.rect = self.image.get_rect(topleft=self.start_pos)
        # print(self.rect)
        # print(self.width)
        # print(self.height)
        # print(self.rect.centerx)
        # print(type(self.rect.bottomright))
        # self.rect.topleft = (40,40)
        # print(self.rect.bottomright)
        # self.rect.bottomright = (self.width+40,self.height+40)
        # self.rect.centerx = 40
        # self.rect.centery = 40
        # self.rect.bottomright = (20,20)
        # print(self.rect)
        # print(self.rect)

    def button_highlight(self):
        '''
        Given a matrix of [text,pos] and placement of 
        underscore, highlights a choice by bliting new
        text
        '''
        self.image = font.render(string,True,WHITE,GREY)

    def button_unhighlight(self):

        self.image = font.render(string,True,WHITE)

    def move_to_place(self,ed_start_pos):

        choice_group.remove(self)
        self.rect = self.image.get_rect(topleft=ed_start_pos)
        selected_group.add(self)
        

    def remove_from_place(self,ed_start_pos):

        selected_group.remove(self)
        self.rect = self.image.get_rect(topleft=ed_start_pos)
        choice_group.add(self)

    def __cmp__(self,other):

        return cmp(self.rect.x,other.rect.x)

    def update_click(self,old_pos,new_pos):

        self.rect.center = (new_pos[0]+42/2,new_pos[1]+45/2)
        black_patch = pygame.Surface((self.width,self.height))
        black_patch.fill(BLACK)
        self.screen.blit(black_patch,old_pos)
        # print(self.rect)
    
    def update_wrong(self,old_pos,new_pos):

        self.rect.center = (new_pos[0]+42/2,new_pos[1]+45/2)
        black_patch = pygame.Surface((self.width,self.height))
        black_patch.fill(BLACK)
        self.screen.blit(black_patch,old_pos)

def check_eval(eval_str):

    try:
        if eval(eval_str) == value:
            return True
        return False
    except:
        return False






##################
# Initialization #
##################


pygame.init()
size = (1200,700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("TickTock Game")

# screen.fill(WHITE)

font = pygame.font.SysFont('Arial',40)
# text = font.render("You are Correct!",True,WHITE)

# screen.blit(bgi_main,(0,0))
screen.fill(BLACK)

# block = Choice(screen,'what')
# screen.blit(plus_img,(25,400))
# screen.blit(minus_img,(150,400))
# screen.blit(mult_img,(325,400))
# screen.blit(div_img,(500,400))
# blit_text(' + ',(175,400))
# blit_text(' – ',(300,400))
# blit_text(' • ',(475,400))
# blit_text(' ÷ ',(650,400))
# blit_text(' = ',(750,400))
# blit_text(' __ ',(850,400))
# screen.blit(text,(600-text.get_rect().width/2,
#                   350-text.get_rect().height/2))
chosen_num_lst,chosen_op_lst = pick_choices(4)
# print(chosen_num_lst,chosen_op_lst)
exp = make_exp(chosen_num_lst,chosen_op_lst)
# print(exp)
value = exp_eval(exp)
# print(value)
num_img_lst,op_img_lst = make_num_img(chosen_num_lst,chosen_op_lst)
dic = make_dic(chosen_num_lst,chosen_op_lst,num_img_lst,op_img_lst)
# print(dic)
places_pos_lst = blit_places_and_equal(9,value)
# print(places_pos_lst)
choices_pos_lst = blit_num_and_op(dic)
print(choices_pos_lst)
pygame.display.update()

choice_group = pygame.sprite.Group()
selected_group = pygame.sprite.Group()

chosen_op_dis_lst = []
for op in chosen_op_lst:
    chosen_op_dis_lst.append(op_dic[op])

choice_str_lst = chosen_num_lst + chosen_op_dis_lst

for i in range(len(dic)):
    choice = Choice(screen,choice_str_lst[i],choices_pos_lst[i],WHITE,GREY)
    choice_group.add(choice)

sorted_choice_lst = sorted(choice_group.sprites(),key=attrgetter('start_pos'))
# for sprite in choice_group:
    # print(sprite.rect.bottomright)
# print(sorted_choice_lst[0].width)
# print(choice_group)
choice_group.draw(screen)
# print(choice_group.sprites())
# min_sprite = min(choice_group.sprites(),key=attrgetter('start_pos'))
# choice_group.remove(min_sprite)
# choice_group.draw(screen)
# selected_group.add(min_sprite)
# print(choice_group.)



#############
# Game Loop #
#############

print(choices_pos_lst[0][0]) #(175,215)
print(choices_pos_lst[0][0]+sorted_choice_lst[0].width)
print(choices_pos_lst[0][1]) #(400,445)
print(choices_pos_lst[0][1]+sorted_choice_lst[0].height)

bgd = pygame.Surface((screen.get_rect()[2],screen.get_rect()[3]))
bgd.fill(BLACK)

eval_str = ''
counter = 0
while True:
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()
    # print(mouse_pos)
    # print(mouse_pos) #(191,425)
    
        


        # button_highlighter(0)
        # 1
        # print('CLICKED!')
    # else:
        # 1
        # choices_pos_lst = blit_num_and_op(dic)
        # pygame.display.update()

        # pygame.display.update()
    # choices_pos_lst = blit_num_and_op(dic)
    pygame.display.update()
    # print(mouse_pos)
    for event in pygame.event.get():
        # print(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if ((choices_pos_lst[0][0]<=mouse_pos[0]<=choices_pos_lst[0][0]+sorted_choice_lst[0].width) and 
            (choices_pos_lst[0][1]<=mouse_pos[1]<=choices_pos_lst[0][1]+sorted_choice_lst[0].height)):
            choice = sorted_choice_lst[0]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1
        if ((choices_pos_lst[1][0]<=mouse_pos[0]<=choices_pos_lst[1][0]+sorted_choice_lst[1].width) and 
            (choices_pos_lst[1][1]<=mouse_pos[1]<=choices_pos_lst[1][1]+sorted_choice_lst[1].height)):
            choice = sorted_choice_lst[1]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1
        if ((choices_pos_lst[2][0]<=mouse_pos[0]<=choices_pos_lst[2][0]+sorted_choice_lst[2].width) and 
            (choices_pos_lst[2][1]<=mouse_pos[1]<=choices_pos_lst[2][1]+sorted_choice_lst[2].height)):
            choice = sorted_choice_lst[2]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1
        if ((choices_pos_lst[3][0]<=mouse_pos[0]<=choices_pos_lst[3][0]+sorted_choice_lst[3].width) and 
            (choices_pos_lst[3][1]<=mouse_pos[1]<=choices_pos_lst[3][1]+sorted_choice_lst[3].height)):
            choice = sorted_choice_lst[3]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1
        if ((choices_pos_lst[4][0]<=mouse_pos[0]<=choices_pos_lst[4][0]+sorted_choice_lst[4].width) and 
            (choices_pos_lst[4][1]<=mouse_pos[1]<=choices_pos_lst[4][1]+sorted_choice_lst[4].height)):
            choice = sorted_choice_lst[4]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1
        if ((choices_pos_lst[5][0]<=mouse_pos[0]<=choices_pos_lst[5][0]+sorted_choice_lst[5].width) and 
            (choices_pos_lst[5][1]<=mouse_pos[1]<=choices_pos_lst[5][1]+sorted_choice_lst[5].height)):
            choice = sorted_choice_lst[5]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1
        if ((choices_pos_lst[6][0]<=mouse_pos[0]<=choices_pos_lst[6][0]+sorted_choice_lst[6].width) and 
            (choices_pos_lst[6][1]<=mouse_pos[1]<=choices_pos_lst[6][1]+sorted_choice_lst[6].height)):
            choice = sorted_choice_lst[6]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1
        if ((choices_pos_lst[7][0]<=mouse_pos[0]<=choices_pos_lst[7][0]+sorted_choice_lst[7].width) and 
            (choices_pos_lst[7][1]<=mouse_pos[1]<=choices_pos_lst[7][1]+sorted_choice_lst[7].height)):
            choice = sorted_choice_lst[7]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1
        if ((choices_pos_lst[8][0]<=mouse_pos[0]<=choices_pos_lst[8][0]+sorted_choice_lst[8].width) and 
            (choices_pos_lst[8][1]<=mouse_pos[1]<=choices_pos_lst[8][1]+sorted_choice_lst[8].height)):
            choice = sorted_choice_lst[8]
            # print("INSIDE!")
            if event.type == MOUSEBUTTONUP and choice_group.has(choice):
                # print("CLICKED!")
                # choice_group.clear(screen,screen)
                eval_str += choice.string
                choice_group.remove(choice)
                choice.update_click(choice.rect.topleft,places_pos_lst[counter])
                choice_group.draw(screen)
                selected_group.add(choice)
                selected_group.draw(screen)
                counter += 1

        pygame.display.update()

    if counter == len(sorted_choice_lst):
        if check_eval(eval_str):
            screen.blit(font.render("GENIUS!",True,WHITE),(50,100))
        else:
            screen.blit(font.render("YOU DUMB!",True,WHITE),(50,100))
            selected_group.clear(screen,bgd)


    





