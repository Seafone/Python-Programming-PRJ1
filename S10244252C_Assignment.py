#Isaac Khoo S10244252C P16
import random


# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }

defender_list = ['ARCHR', 'WALL']  #list of defender
monster_list = ['ZOMBI', 'WWOLF']  #list of monster

defenders = {'ARCHR': {'name': 'Archer', #dictionary of ARCHR
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       },
             
             'WALL': {'name': 'Wall',   #dictionary of WALL
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      }
             }

monsters = {'ZOMBI': {'name': 'Zombie',   #dictionary of ZOMBI
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',   #dictionary of WWOLF
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      }
            }

field = [ [None, None, None, None, None, None, None],       #list of field
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]


#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------
def draw_field():                                                                                           #draw field
    num_rows = len(field)
    num_columns = len(field[0])
    print("{:^2}{:^6}{:^6}{:^6}".format("","1","2","3"))                                                   #prints column number
    
    print(" ", end = '')                                                                                    #prints horizontal of field
    for column in range(num_columns):
        print('+-----', end='')
    print("+")
    
    letters = ['A','B','C','D','E']                                                                         #list of letters for row
    for row in range(num_rows):                                                                             
        print(letters[row], end='')                                                                         #print letters for each row
        for column in field[row]:                                                       
            if column != None:                                                                               
                print("|{:5}".format(column[0]),end = '')                                                   
            else:
                print("|{:5}".format(" "), end= '')                                                         
        print("|")
        print(" ", end = '')
        for column in field[row]:
            if column != None:
                if column[0] in defender_list:
                    print("|{:>2}/{:<2}".format(column[1],defenders[column[0]]["maxHP"]),end = '')          #formats hp of defenders on bottom of box
                elif column[0] in monster_list:
                    print("|{:>2}/{:<2}".format(column[1],monsters[column[0]]["maxHP"]),end = '')           #formats hp of monsters on bottom of box
            else:
                print("|{:5}".format(" "), end= '')
        print("|")
        print(" ", end = '')
        for column in range(num_columns):                                                                   #print verticle of column
            print("+-----",end= '')
        print("+")
    
    return
#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print('Turn {}     Threat = [          ]     Danger Level {}'.format(game_vars['turn'], game_vars['danger_level']))  #print and format turn, threat and danger level
    print('Gold = {}     Monsters killed = {}/{}'.format(game_vars['gold'],game_vars['monsters_killed'],game_vars['monster_kill_target'])) #print and format gold and monsters killed
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):
    if int(position[1]) > 3:                   #if position inputed is outside of range."position is invalid" is printed gold is returned and user is sent back to buy menu
        print('Position is invalid!')
        game_vars['gold']+= defenders[unit_name]['price']
        buy_unit(field,game_vars)
        
    else:                               
        capitalise = position[0].upper()                #capitalises input value and indexs it to the number list to get position on the field and places unit on field with hp
        number_list = ['A','B','C','D','E']
        row = number_list.index(capitalise)
        if field[row][int(position[1])-1] == None:
            field[row][(int(position[1])-1)] = [unit_name, defenders[unit_name]['maxHP']]
            return True
        
        else:
            print('Position is invalid')                #if position is taken unit is not replaced. Gold is returned and user is sent back to buy menu
            game_vars['gold']+= defenders[unit_name]['price']
            buy_unit(field,game_vars)
        

        


#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):
    print('What unit do you wish to buy?')                               #buy menu for units
    print('1.Archer ({} gold)'.format(defenders['ARCHR']['price']))
    print('2.Wall ({} gold)'.format(defenders['WALL']['price']))
    print('3.Don\'t buy')
    choice = int(input('Your choice? '))                                #input choice for menu
    if choice == 3:                                                     #if input is 3 then move on to next turn
        show_combat_menu(game_vars)
        pass
    else:
        if game_vars['gold'] - defenders[defender_list[choice-1]]['price'] < 0:             #if input is 1 or 2 but user does not have enough gold, then user is sent back to buy menu
            print('You do not have enough gold!')
            buy_unit(field,game_vars)
        else:
            position = input('Place Where? ')                                           #if input is 1 or 2, gold is deducted,input for position and placeunit() is run to place a unit
            game_vars['gold'] -= defenders[defender_list[choice-1]]['price']
            place_unit(field, position, defender_list[choice-1])

    return

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_name, field, row, column):
    number_list = ['A','B','C','D','E']
    for x in range(column,len(field[row])):
        if field[row][x] != None and (field[row][x][0] in monster_list):            #scans the entire column for monsters
            damage = random.randint(defenders[defender_name]['min_damage'], defenders[defender_name]['max_damage'] )    #damage randomiser for defender damage
            field[row][x][1] -= damage                                                                                  #defender does damage to monster in row
            print('Archer in lane {} shoots {} for {} damage!'.format(number_list[row],monsters[field[row][x][0]]['name'],damage,)) 
            if field[row][x][1] < 1 :                                                                                   #if monster dies
                print('{} dies!'.format(monsters[field[row][x][0]]['name']))                                            
                print('You gain {} gold as a reward.'.format(monsters[field[row][x][0]]['reward']))                       
                game_vars['gold']+=monsters[field[row][x][0]]['reward']                                                 #gold is gained
                field[row][x] = None                                                                                    # monster is removed
                game_vars['monsters_killed']+=1                                                                         #monsters_killed is updated
                game_vars['num_monsters']-=1                                                                            #number of monsters is reduced by 1

                





    return

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(field, row, column):
    number_list = ['A','B','C','D','E']
    zombie_move = monsters['ZOMBI']['moves']                            #moves of zombie
    werewolf_move = monsters['WWOLF']['moves']                          #moves of werewolf
    if field[row][column][0] == monster_list[1]:            #if werewolf crosses the left side of field game is lost
        if column-2 < 0 :                                 
            print('A {} has reached the city! All is lost!'.format(monsters[field[row][column][0]]['name']))
            print('You have lost the game. :(')
            quit() 
    
    elif field[row][column][0] == monster_list[0]:           #if zombie crosses the left side of field game is lost
        if column-1 < 0 :                                   
            print('A {} has reached the city! All is lost!'.format(monsters[field[row][column][0]]['name']))
            print('You have lost the game. :(')
            quit()                                                          #game ends

    if field[row][column][0] == monster_list[0]:                        #if monster in row is zombie    
        if field[row][column-zombie_move] == None:                      #nothing infront of zombie
            print('{} in lane {} advances!'.format(monsters[field[row][column][0]]['name'],number_list[row]))
            field[row][column-zombie_move] = field[row][column]         #a copy is made of zombie to the spot its advancing to
            field[row][column] = None                                   #zombie on previous spot is removed
    
    elif field[row][column][0] == monster_list[1]:          #if monster in row is werewolf
        if field[row][column-werewolf_move] == None:        #if nothing infront of werewolf
            if field[row][column-1] != None and (field[row][column-1][0] in defender_list): #if there is something infront of werewold and it is a defender
                damage = random.randint(monsters[field[row][column][0]]['min_damage'],monsters[field[row][column][0]]['max_damage']) #damage is random for werewolf
                field[row][column-1][1] -= damage                       #attacker takes damage
                if field[row][column-1][1] < 1 :                        #if attacker hp is less than 1
                    field[row][column-1] = None                         #attacker is removed
            else:                                                                                       #if not
                print('{} in lane {} advances!'.format(monsters[field[row][column][0]]['name'],number_list[row]))      
                field[row][column-werewolf_move] = field[row][column]              #a copy is made of werewolf to the spot its advancing to
                field[row][column] = None                                          #werewolf on previous spot is removed
        elif field[row][column-werewolf_move] != None and field[row][column-1] == None:
            print('{} in lane {} advances!'.format(monsters[field[row][column][0]]['name'],number_list[row]))
            field[row][column-1] = field[row][column]                   #werewolf copies itself 1 space before of obstacle
            field[row][column] = None                                   #werewolf behind it is removed
    
    elif field[row][column-1] != None and (field[row][column-1][0] in defender_list):                       #if obstacle infront of monster is a defender
        damage = random.randint(monsters[field[row][column][0]]['min_damage'],monsters[field[row][column][0]]['max_damage'])        #selects the random damage of monster
        field[row][column-1][1] -= damage                                                                   #defender takes damage from monster
        if field[row][column-1][1] < 1 :                                                                    #if defender hp is less than 1
            field[row][column-1] = None                                                                     #defender is removed
    
    elif field[row][column-1][0] == monster_list:                                                           #if obstacle blocing monster is a monster
        print('{} in lane {} is blocked from advancing'.format(monsters[field[row][column][0]]['name'],number_list[row]))   
        pass                                                                                                #nothing happens and monster is blocked from advancing
    

        
    return

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list):                  
    randomrow = random.randint(0,4)                             #selects random row for monster to spawn
    random_monster = random.randint(0,1)                        #selects random monster to be spawned
    hp = [monster_list[random_monster], monsters[monster_list[random_monster]]["maxHP"]]        #determine the hp of the randomly selected monster
    if game_vars['num_monsters'] == 0:                      #if monster on filed is 0
        field[randomrow][-1] = hp                           #spawns zombie on last column on field
        game_vars['num_monsters'] += 1                      #number of monster + 1
    


    return

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    save = open('C:/Users/isaac/OneDrive/Desktop/PRG ASSIGNMENT/'+'save.txt.', 'w')         #creates a new file to save at file location
    save_list=[]                                                                            #list to save variables
    save_list.append(game_vars)                                                             #variables appended to list
    for info in save_list:  
        save.write("{}".format(list(info.values())))                                        #variables in list are formatted
    save.write("\n")                                                                        #creates a new paragraph in file
    for items in field:
        row = []                                                                            #empty list for field
        for i in items:
            row.append(str(i))                                                              #appends the items in field to list
        save.writelines(".".join(row))                                                      #seperates the items in the file with a dot
        save.write("\n")                                                                    #creates a new paragraph for each row
    save.close()                                                                            #closes file
    print("Game saved.")                              

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game():                                            
    load = open('C:/Users/isaac/OneDrive/Desktop/PRG ASSIGNMENT/'+'save.txt.', 'r')     #file path to read file
    line = load.readlines()                                                             #read file
    save_variable = line[0].strip("\n").strip("[").strip("]").split(",")                
    save_field = line[1:]         
    count = 0
    for info in game_vars:                                                             #adding each variables in the file to the new game variables
        game_vars[info] = int(save_variable[count])
        count+=1
    for y in range(len(save_field)):                                                    #replacing the field in the new game
        temp = save_field[y].split(".")                                                 #splits each part of the field in the file
        for x in range(len(temp)):
            if temp[x].strip("\n") == "None":                                           #part of the field is none
                field[y][x] == None                                                     #part of field in new game is none
            else:
                unit = temp[x].strip("\n").strip("[").strip("]").split(",")
                field[y][x] = [unit[0].strip("'"),int(unit[1])]
    
    
    return

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1
    



#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
show_main_menu()                                                #shows main menu
choice = int(input('Your Choice? '))                            #input choice
if choice == 1:                                                 #if choice is 1 new game is begun
    play_game = True
    initialize_game()
elif choice == 2:                                               #if choice is 2 game is begun but load game is run and saved game file is loaded into the game
    play_game = True
    load_game()
    pass
else :                                                          #if choice is 3 game does not start
    play_game = False
    print("See You Next Time!")

while play_game == True:                                        #while game is begun
    spawn_monster(field,monster_list)                           #spawns monster
    draw_field()                                                #draws field
    game_vars['turn']+=1                                        #add 1 turn to variable 'turn'
    show_combat_menu(game_vars)                                 #shows combat menu
    combat_choice = int(input('Your Choice? '))                 #input choice
    if combat_choice == 4:                                      #if choice is 4 game is ended
        play_game = False
        print("See You Next Time!")
    elif combat_choice == 3:                                    #if choice is 3 game is saved
        save_game()
        game_vars['turn']-=1                                    # 1 turn is removed
    elif combat_choice == 1:                                    # if choice is 1
        buy_unit(field,game_vars)                               # buy unit is run
        for row in range(len(field)):                          
            for column in range(len(field[row])):             
                if field[row][column] != None and field[row][column][0] == 'ARCHR':         #if defender is in row
                    defender_attack(defender_list[0], field, row, column)                   #defender attacks
                elif field[row][column] != None and field[row][column][0] in monster_list:  #if monster is in row, 
                    monster_advance(field,row,column)                                       #monster advances
        game_vars['gold']+=1                                                                #gold is gained every round
    elif combat_choice == 2:                                                                #if choice is 2
        game_vars['gold']+=1                                                                #gold is gained every round
        for row in range(len(field)):                                                       
            for column in range(len(field[row])):
                if field[row][column] != None and field[row][column][0] == 'ARCHR':         #if defender is in row
                    defender_attack(defender_list[0], field, row, column)                   #defender attacks
                elif field[row][column] != None and field[row][column][0] in monster_list:  #if monster is in row,
                    monster_advance(field,row,column)                                       #monster advances
        pass
    if game_vars['monsters_killed'] == 20:                                                  #if monsters killed in the game reaches 20
        print('You have protected the city! You win!')                                      #prints that user has won
        play_game = False                                                                   #game ends
    
        
    


    
