# Mathematics Game
# Given multiple expressions and operations,
# you must produce a specified number

import pygame,sys,random
from operator import attrgetter
from pygame.locals import *
from time import sleep

##########
# Colors #
##########

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)

################
# Choice Lists #
################

op_lst = ['+','-','*','/']
num_lst = [str(x) for x in range(101)]


#######################
# Operator Dictionary #
#######################

op_dic = {'+':'+','-':'–','*':'•','/':'÷'}
rev_op_dic = {value:key for key,value in op_dic.items()}


#############################
# Back-track Recording List #
#############################

back_track_lst = []


#################
# Sprite Groups #
#################

choice_group = pygame.sprite.Group()
selected_group = pygame.sprite.Group()
eqn_group = pygame.sprite.Group()
timer_group = pygame.sprite.Group()



def pick_choices(num_num):
    '''
    Randomly chooses operators & numbers from 
    corresponding lists given a number of 
    operators
    '''

    chosen_lst = []
    for i in range(num_num):
        chosen_lst.append(random.choice(num_lst))
        chosen_lst.append(random.choice(op_lst))
        if i == num_num-1:
            chosen_lst.append(random.choice(num_lst))
    return chosen_lst



def check_int(eval_exp_part):
    '''
    Returns True if eval_exp_part
    is an integer or 0.0
    '''
    if isinstance(eval_exp_part,float):
        print('exp is a float')
        print(eval_exp_part)
        if eval_exp_part != 0.0:
            print('exp is a non-zero float')
            whole_num_index = 0
            str_value = str(eval_exp_part)
            for i in range(len(str_value)):
                if str_value[i] == '.':
                    whole_num_index = i
            decimal = str_value[whole_num_index+1:]
            print(decimal)
            for digit in decimal:
                if digit != '0':
                    print("It is Not the answer")
                    return False
            return True
        return True
    return True

    



def pos_choices(len_chosen_lst):
    '''
    Returns a list of positions for 
    the choice blocks
    '''
    start_pos = [(screen.get_width()/2.-20)-130*(len_chosen_lst/2),450]   #[175,400]
    pos_lst = []
    for i in range(len_chosen_lst):
        pos_lst.append(start_pos[:])
        start_pos[0] += 150
    return pos_lst



def pos_eqn(len_places):
    '''
    Returns a list of positions for
    the places, equal sign, and 
    an evaluated number
    '''
    start_pos = [(screen.get_width()/2.-20)-80*(len_places/2+1),280]    # [70,300]
    pos_lst = []
    for temp in range(len_places+1):
        pos_lst.append(start_pos[:])
        start_pos[0] += 100
    start_pos[0] -= 30
    pos_lst.append(start_pos[:])
    return pos_lst




def check_eval(eval_str):
    '''
    Checks whether evaluated term 
    is equal to the value
    '''

    try:
        if eval(eval_str) == value:
            return True
        return False
    except:
        return False


def choice_click_update(eval_str,choice,counter,choice_group,selected_group,places_pos_lst):
    '''
    Updates when choice block is
    clicked
    '''
    if choice.string in rev_op_dic:
        eval_str += rev_op_dic[choice.string]
    else:
        eval_str += choice.string
    choice.update_click(choice.rect.topleft,places_pos_lst[counter])
    selected_group.add(choice)
    selected_group.draw(screen)
    counter += 1
    pygame.display.update()
    return eval_str,counter


def eval_wrong(back_track_lst,selected_group):
    '''
    Re-places the selected choices to their
    original positions
    '''
    sorted_selected_group_lst = sorted(selected_group.sprites(),key=lambda x:x.rect.topleft)
    for i in range(len(back_track_lst)):
        sorted_selected_group_lst[i].rect.topleft = tuple(back_track_lst[i])




#################
# Sprite Places #
#################

class Place(pygame.sprite.Sprite):

    def __init__(self,screen,string,start_pos,color,bcolor=None):

        super(Place,self).__init__()

        self.screen = screen
        self.string = string
        self.start_pos = tuple(start_pos)
        self.color = color
        self.bcolor = bcolor
        self.image = font.render(self.string,True,self.color,self.bcolor)
        self.rect = self.image.get_rect(topleft=self.start_pos)
        self.center = self.rect.center




##################
# Sprite Choices #
##################


class Choice(pygame.sprite.Sprite):

    def __init__(self,screen,string,start_pos,color,bcolor=None):

        super(Choice,self).__init__()

        self.screen = screen
        self.string = string
        self.start_pos = tuple(start_pos)
        self.color = color
        self.bcolor = bcolor
        self.image = font.render(self.string,True,self.color,self.bcolor)
        self.rect = self.image.get_rect(topleft=self.start_pos)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.center = self.rect.center


    def button_highlight(self):
        '''
        Given a matrix of [text,pos] and placement of 
        underscore, highlights a choice by bliting new
        text
        '''
        self.image = font.render(self.string,False,GREY)
        self.screen.blit(self.image,self.start_pos)

    def button_unhighlight(self):

        self.image = font.render(self.string,False,WHITE)
        self.screen.blit(self.image,self.start_pos)

    def update_click(self,old_pos,new_pos):

        self.rect.center = (new_pos[0]+62/2,new_pos[1]+67/2.)
        black_patch = pygame.Surface((self.width,self.height))
        black_patch.fill(BLACK)
        self.screen.blit(black_patch,old_pos)
        pygame.display.update()


################
# Sprite Timer #
################

class Timer(pygame.sprite.Sprite):

    def __init__(self,screen,string,start_pos,color,bcolor=None):

        super(Timer,self).__init__()
        self.screen = screen
        self.string = string
        self.start_pos = tuple(start_pos)
        self.color = color
        self.bcolor = bcolor
        self.image = font.render(self.string,True,color,bcolor)
        self.rect = self.image.get_rect(topleft=self.start_pos)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.center = self.rect.center

    def timer_update(self,new_str):

        black_patch = pygame.Surface((self.width,self.height))
        black_patch.fill(BLACK)
        self.screen.blit(black_patch,self.start_pos)
        pygame.display.update()
        self.string = new_str
        self.image = font.render(self.string,True,self.color,self.bcolor)
        self.screen.blit(self.image,(self.width,self.height))
        pygame.display.update()








##########################
# Initialization: Pygame #
##########################

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((1200,700))
    font = pygame.font.SysFont('Times New Roman',60)
    screen.fill(BLACK)

    clock = pygame.time.Clock()







#############################
# Initialization: Variables #
#############################


    check = False

    num_op = 2
    num_places = num_op*2+1

    while not check:
        # print('loop again')
        chosen_lst = pick_choices(num_op)
        print(chosen_lst)
        try:
            print('here')
            exps = chosen_lst[0]
            index = 1
            while index < len(chosen_lst):
                exps += ''.join(chosen_lst[index:index+2])
                print(exps)
                value = eval(exps)
                print(value)
                if check_int(value):
                    check = True
                else:
                    index = len(chosen_lst)
                    check = False
                index += 2
        except ZeroDivisionError:
            print('no zeros')
            check = False


    choices_pos_lst = pos_choices(len(chosen_lst))
    places_pos_lst = pos_eqn(num_places)

    shuffled_chosen_lst = chosen_lst[:]
    random.shuffle(shuffled_chosen_lst)

    # Initializing Timer

    clock = pygame.time.Clock()
    print(clock)

    timer = Timer(screen,str(clock),(1000,200),WHITE)
    timer_group.add(timer)
    timer_group.draw(screen)

    pygame.display.update()

    # Adding choice blocks to choice_group

    for i in range(len(shuffled_chosen_lst)):
        if shuffled_chosen_lst[i] in op_dic:
            choice = Choice(screen,op_dic[shuffled_chosen_lst[i]],
                            choices_pos_lst[i],
                            WHITE)
            choice_group.add(choice)
        else:
            choice = Choice(screen,shuffled_chosen_lst[i],
                            choices_pos_lst[i],
                            WHITE)
            choice_group.add(choice)


    # Adding '__' blocks to eqn_group

    for j in range(len(places_pos_lst[:len(places_pos_lst)-2])):
        place = Place(screen,'__',places_pos_lst[j],WHITE)
        print(place.image.get_rect())
        eqn_group.add(place)

    # Adding '=' block to eqn_group

    equal = Place(screen,'=',places_pos_lst[-2],WHITE)
    eqn_group.add(equal)

    # Adding value block to eqn_group

    given_value = Place(screen,str(value),places_pos_lst[-1],
                        WHITE)
    eqn_group.add(given_value)

    # Initializing background

    bgd = pygame.Surface((screen.get_width(),screen.get_height()))
    bgd.fill(BLACK)

    # Initializing eval_str to record exps

    eval_str = ''

    # Initializing counter to record 
    # number of choices made

    counter = 0

    # Initializing a sorted choice list
    # by their positions

    sorted_choice_lst = choice_group.sprites()
    sorted_choice_lst = sorted(sorted_choice_lst,key=attrgetter('start_pos'))

    # Initializing a sorted eqn list 
    # by their positions

    choice_group.draw(screen)
    eqn_group.draw(screen)

    pygame.display.update()


    # Timer variable

    second = 30

    second_surface = font.render('00:'+str(second),True,WHITE)
    screen.blit(second_surface,(300,200))

    # Black Patch to cover up timer

    black_patch = pygame.Surface((second_surface.get_width(),second_surface.get_height()))
    black_patch.fill(BLACK)

    pygame.display.update()
#############
# Game Loop #
#############

    while True:
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            for i in range(len(choices_pos_lst)):
                choice = sorted_choice_lst[i]
                if ((choices_pos_lst[i][0]<=mouse_pos[0]<=choices_pos_lst[i][0]+sorted_choice_lst[i].width) and 
                    (choices_pos_lst[i][1]<=mouse_pos[1]<=choices_pos_lst[i][1]+sorted_choice_lst[i].height)):
                    if not (selected_group.has(choice)):
                        choice.button_highlight()
                        if event.type == MOUSEBUTTONUP:
                            choice.button_unhighlight()
                            pygame.display.update()
                            back_track_lst.append(choice.rect.topleft)
                            eval_str,counter = choice_click_update(eval_str,choice,counter,choice_group,selected_group,places_pos_lst)
                else:
                    if not (selected_group.has(choice)):
                        choice.button_unhighlight()

        if counter == len(sorted_choice_lst):
            if check_eval(eval_str):
                screen.blit(font.render("GENIUS!",True,WHITE),(50,100))
            else:
                eval_wrong(back_track_lst,selected_group)
                screen.blit(font.render("YOU DUMB!",True,WHITE),(50,100))
                selected_group.clear(screen,bgd)
                selected_group.empty()
                back_track_lst = []
                eval_str = ''
                choice_group.draw(screen)
                eqn_group.draw(screen)
                counter = 0
                pygame.display.update()
        second -= 1
        second_surface = font.render('00:'+str(second),True,WHITE)
        screen.blit(black_patch,(300,200))
        screen.blit(second_surface,(300,200))
        # timer_group.clear(screen,bgd)
        # timer.timer_update(str(clock))
        # sleep(1)
        pygame.display.update()
