# Mathematics Game
# Given multiple expressions and operations,
# you must produce a specified number

## TO-DO LIST

'''
1. Scoring system
2. Clock, Feedback position Rearrangement
'''

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
num_lst = [str(x) for x in range(100)]


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




def check_eval(eval_str,value):
    '''
    Checks whether evaluated term 
    is equal to the value
    '''

    try:
        if eval(eval_str) == value:
            print('evaluated')
            return True
        print('different')
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
    print("sorted_selected_group_lst: "+str(len(sorted_selected_group_lst)))
    print("back_track_lst: "+str(len(back_track_lst)))
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
        black_patch = pygame.Surface((self.width,self.height))
        black_patch.fill(BLACK)
        self.screen.blit(black_patch,self.start_pos)
        self.screen.blit(self.image,self.start_pos)

    def button_unhighlight(self):

        self.image = font.render(self.string,False,WHITE)
        black_patch = pygame.Surface((self.width,self.height))
        black_patch.fill(BLACK)
        self.screen.blit(black_patch,self.start_pos)
        self.screen.blit(self.image,self.start_pos)

    def update_click(self,old_pos,new_pos):

        self.rect.center = (new_pos[0]+79/2.,new_pos[1]+67/2.)
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

# if __name__ == '__main__':

pygame.init()
screen = pygame.display.set_mode((1200,700))
font = pygame.font.SysFont('Comic Sans MS',60)
screen.fill(BLACK)

clock = pygame.time.Clock()


#############
# Main Page #
#############

def main_page():

    screen.fill(BLACK)

    title_font = pygame.font.SysFont('Comic Sans MS',130)
    option_font = pygame.font.SysFont('Comic Sans MS',30)

    title = title_font.render("Exisosi",True,WHITE)
    screen.blit(title,(screen.get_width()/2.-title.get_width()/2.,120))

    instruct = option_font.render("How do I play?",True,WHITE)
    screen.blit(instruct,(screen.get_width()/2.-instruct.get_width()/2.,350))
    instruct_cursor = option_font.render("How do I play?",True,GREY)

    easy = option_font.render("Easy",True,WHITE)
    screen.blit(easy,(screen.get_width()/2.-easy.get_width()/2.,410))
    easy_cursor = option_font.render("Easy",True,GREY)

    medium = option_font.render("Medium",True,WHITE)
    screen.blit(medium,(screen.get_width()/2.-medium.get_width()/2.,470))
    medium_cursor = option_font.render("Medium",True,GREY)

    hard = option_font.render("Hard",True,WHITE)
    screen.blit(hard,(screen.get_width()/2.-hard.get_width()/2.,530))
    hard_cursor = option_font.render("Hard",True,GREY)


    pygame.display.update()


    options_lst = [instruct,easy,medium,hard]
    options_cursor_lst = [instruct_cursor,easy_cursor,medium_cursor,hard_cursor]
    options_pos_lst = [[screen.get_width()/2.-instruct.get_width()/2.,350],
                       [screen.get_width()/2.-easy.get_width()/2.,410],
                       [screen.get_width()/2.-medium.get_width()/2.,470],
                       [screen.get_width()/2.-hard.get_width()/2.,530]]
    # black_patch = pygame.Surface((second_surface.get_width(),second_surface.get_height()))
    # black_patch.fill(BLACK)

    while True:

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        pygame.display.update()
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            for i in range(len(options_pos_lst)):
                if (options_pos_lst[i][0] <= mouse_pos[0] <= options_pos_lst[i][0]+options_lst[i].get_width() and
                    options_pos_lst[i][1] <= mouse_pos[1] <= options_pos_lst[i][1]+options_lst[i].get_height()):
                    black_patch = pygame.Surface((options_lst[i].get_width(),options_lst[i].get_height()))
                    black_patch.fill(BLACK)
                    screen.blit(black_patch,options_pos_lst[i])
                    screen.blit(options_cursor_lst[i],options_pos_lst[i])
                    if i == 0 and event.type == MOUSEBUTTONUP:
                        instruct_page()
                    elif event.type == MOUSEBUTTONUP:
                        accuracy_mode(BLACK,WHITE,GREY,
                                      op_lst,num_lst,op_dic,rev_op_dic,
                                      choice_group,
                                      selected_group,eqn_group,timer_group,(i+2)**2)
                else:
                    screen.blit(options_lst[i],options_pos_lst[i])

####################
# Instruction Page #
####################

def instruct_page():

    screen.fill(BLACK)

    expl_title_font = pygame.font.SysFont("Comic Sans MS",80)
    expl_font = pygame.font.SysFont("Comic Sans MS",40)
    expl_title = expl_title_font.render("How To Play",True,WHITE)
    line1 = expl_font.render("1. Choose one of the modes you wish to play",True,WHITE)
    line2 = expl_font.render("2. Click all choices to complete a given equation",True,WHITE)
    line3 = expl_font.render("3. Try to complete it before the time runs out!",True,WHITE)
    main_menu = expl_font.render("Main Menu",True,WHITE)
    main_menu_cursor = expl_font.render("Main Menu",True,GREY)

    screen.blit(expl_title,(screen.get_rect()[2]/2.-expl_title.get_width()/2.,40))
    screen.blit(line1,(screen.get_rect()[2]/2.-line1.get_width()/2.,240))
    screen.blit(line2,(screen.get_rect()[2]/2.-line2.get_width()/2.,360))
    screen.blit(line3,(screen.get_rect()[2]/2.-line3.get_width()/2.,480))

    main_menu_pos = (screen.get_rect()[2]/2.-main_menu.get_width()/2.,580)
    screen.blit(main_menu,main_menu_pos)
    pygame.display.update()


            
    while True:

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (main_menu_pos[0]<=mouse_pos[0]<=main_menu_pos[0]+main_menu.get_width() and
                main_menu_pos[1]<=mouse_pos[1]<=main_menu_pos[1]+main_menu.get_height()):
                black_patch = pygame.Surface((main_menu.get_width(),main_menu.get_height()))
                black_patch.fill(BLACK)
                screen.blit(black_patch,main_menu_pos)
                screen.blit(main_menu_cursor,main_menu_pos)
                if event.type == MOUSEBUTTONUP:
                    main_page()
            else:
                screen.blit(main_menu,main_menu_pos)






######################
# Accuracy Mode Page #
######################


def accuracy_mode(BLACK,WHITE,GREY,op_lst,num_lst,op_dic,rev_op_dic,
                  choice_group,selected_group,eqn_group,timer_group,game_num):


    # Clearing screen

    screen.fill(BLACK)


#############################
# Initialization: Variables #
#############################
    
    # back_track_lst

    back_track_lst = []


    # Initializing Clear button
    
    clear_start_pos = (900,100)
    clear_button = font.render("CLEAR",True,WHITE)
    screen.blit(clear_button,clear_start_pos)
    clear_button_cursor = font.render("CLEAR",True,GREY)

    # Initializing Main Menu button

    
    main_menu = font.render("Main Menu",True,WHITE)
    main_menu_pos = (screen.get_width()/2.-main_menu.get_width()/2.,550)
    screen.blit(main_menu,main_menu_pos)
    main_menu_cursor = font.render("Main Menu",True,GREY)

    # Initializing Choice and Place blocks

    check = False

    num_op = 2
    num_places = num_op*2+1

    while not check:
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
    print(value)

    # timer = Timer(screen,str(clock),(1000,200),WHITE)
    # timer_group.add(timer)
    # timer_group.draw(screen)

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
        print(place.rect)
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

    second = 1000

    second_surface = font.render('0'+str(second)[0]+':'+str(second)[1:3],True,WHITE)
    screen.blit(second_surface,(250,150))

    # Black Patch to cover up timer

    black_patch = pygame.Surface((second_surface.get_width()+20,second_surface.get_height()+20))
    black_patch.fill(BLACK)

    # Black Patch to cover up Clear button

    black_patch_clear = pygame.Surface((clear_button.get_width(),clear_button.get_height()))
    black_patch_clear.fill(BLACK)

    # Black Patch to cover up Main Menu button

    black_patch_main_menu = pygame.Surface((main_menu.get_width(),main_menu.get_height()))
    black_patch_main_menu.fill(BLACK)    

    # Initializing Wrong Feedback Message

    wrong_feedback = font.render("Try Again",True,WHITE)

    # Black Patch to cover up wrong feedback

    black_patch_wrong_feedback = pygame.Surface((wrong_feedback.get_width(),
                                                wrong_feedback.get_height()))
    screen.blit(black_patch_wrong_feedback,(50,25))

    pygame.display.update()


#############
# Game Loop #
#############
    


    while check:
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            else:

                for i in range(len(choices_pos_lst)):
                    choice = sorted_choice_lst[i]
                    if ((choices_pos_lst[i][0]<=mouse_pos[0]<=choices_pos_lst[i][0]+sorted_choice_lst[i].width) and 
                        (choices_pos_lst[i][1]<=mouse_pos[1]<=choices_pos_lst[i][1]+sorted_choice_lst[i].height)):
                        if not (selected_group.has(choice)):
                            choice.button_highlight()
                            if event.type == MOUSEBUTTONUP:
                                choice.button_unhighlight()
                                # pygame.display.update()
                                back_track_lst.append(choice.rect.topleft)
                                eval_str,counter = choice_click_update(eval_str,choice,counter,choice_group,selected_group,places_pos_lst)
                    

                    else:
                        if not (selected_group.has(choice)):
                            choice.button_unhighlight()

                if (clear_start_pos[0]<=mouse_pos[0]<=clear_start_pos[0]+clear_button.get_width() and 
                    clear_start_pos[1]<=mouse_pos[1]<=clear_start_pos[1]+clear_button.get_height()):
                    
                    screen.blit(black_patch_clear,clear_start_pos)
                    screen.blit(clear_button_cursor,clear_start_pos) 
                    if event.type == MOUSEBUTTONUP:
                        eval_wrong(back_track_lst,selected_group)
                        selected_group.clear(screen,bgd)
                        selected_group.empty()
                        back_track_lst = []
                        eval_str = ''
                        choice_group.clear(screen,bgd)
                        eqn_group.draw(screen)
                        choice_group.draw(screen)
                        eqn_group.draw(screen)
                        counter = 0


                elif (main_menu_pos[0]<=mouse_pos[0]<=main_menu_pos[0]+main_menu.get_width() and 
                    main_menu_pos[1]<=mouse_pos[1]<=main_menu_pos[1]+main_menu.get_height()):
                    
                    screen.blit(black_patch_main_menu,main_menu_pos)
                    screen.blit(main_menu_cursor,main_menu_pos) 
                    if event.type == MOUSEBUTTONUP:
                        back_track_lst = []
                        choice_group.empty()
                        selected_group.empty()
                        eqn_group.empty()
                        timer_group.empty()
                        main_page()

                
                else:
                    screen.blit(black_patch_clear,clear_start_pos)
                    screen.blit(black_patch_main_menu,main_menu_pos)

                    screen.blit(clear_button,clear_start_pos)
                    screen.blit(main_menu,main_menu_pos)




        if counter == len(sorted_choice_lst):
            if check_eval(eval_str,value):
                game_num -= 1
                if game_num == 0:
                    screen.blit(black_patch_wrong_feedback,(50,25))
                    screen.blit(font.render("GENIUS!",True,WHITE),(50,25))
                    pygame.display.update()
                    while True:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                else:
                    screen.fill(BLACK)
                    back_track_lst = []
                    choice_group.empty()
                    selected_group.empty()
                    eqn_group.empty()
                    accuracy_mode(BLACK,WHITE,GREY,op_lst,num_lst,op_dic,rev_op_dic,
                                  choice_group,selected_group,
                                  eqn_group,timer_group,game_num)
        
            else:
                eval_wrong(back_track_lst,selected_group)
                screen.blit(wrong_feedback,(50,25))
                selected_group.clear(screen,bgd)
                selected_group.empty()
                back_track_lst = []
                eval_str = ''
                choice_group.clear(screen,bgd)
                choice_group.draw(screen)
                eqn_group.clear(screen,bgd)
                eqn_group.draw(screen)
                counter = 0
                # pygame.display.update()
        second -= .5
        if second < 10:
            second = '0'
            second_surface = font.render('00:0'+second,True,WHITE)
            screen.blit(second_surface,(250,150))
            pygame.display.update()
            check = False
        elif second < 100:
            second_surface = font.render('00:0'+str(second)[:1],True,WHITE)
        else:
            if second == 999.5:
                second = 600
            elif second == 1999.5:
                second = 1600
            else:
                if second >= 600:
                    second_surface = font.render('0'+str(second)[0]+':'+str(second)[1:3],True,WHITE)
                else:
                    second_surface = font.render('00:'+str(second)[:2],True,WHITE)
        screen.blit(black_patch,(250,150))
        screen.blit(second_surface,(250,150))
        
    if not check_eval(eval_str,value):
        screen.blit(black_patch_wrong_feedback,(50,25))
        screen.blit(font.render('Time Out',True,WHITE),(50,25))

        # print(main_menu.get_rect()) #(451~749,550~635)
        # print(main_menu_pos)
        while True:
            pygame.display.update()
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif (main_menu_pos[0]<=mouse_pos[0]<=main_menu_pos[0]+main_menu.get_width() and 
                    main_menu_pos[1]<=mouse_pos[1]<=main_menu_pos[1]+main_menu.get_height()):
                    screen.blit(black_patch_main_menu,main_menu_pos)
                    screen.blit(main_menu_cursor,main_menu_pos) 
                    if event.type == MOUSEBUTTONUP:
                        back_track_lst = []
                        choice_group.empty()
                        selected_group.empty()
                        eqn_group.empty()
                        timer_group.empty()
                        main_page()
                else:
                    screen.blit(black_patch_main_menu,main_menu_pos)
                    screen.blit(main_menu,main_menu_pos)



# if __name__ == "__main__":
main_page()
# instruct_page()
# accuracy_mode(BLACK,WHITE,GREY,op_lst,num_lst,op_dic,rev_op_dic,back_track_lst,choice_group,selected_group,eqn_group,timer_group,2)