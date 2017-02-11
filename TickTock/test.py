import random,pygame
from pygame.locals import *

op_lst = ['+','-','*','/']
num_lst = [str(x) for x in range(101)]

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

print(value)












