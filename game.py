from random import randint
from utils import bcolors, clear_screen, load_data
from interface import top_interface
from sprites import *

#         north (1)
#             |
# west (0)--- + ---east (2)
#             |
#         south (3)
def next_map_pos(map_pos, direction):
    # direction = left/right/back
    if direction == 'left':
        if map_pos == 0: return 3
        return map_pos - 1
    elif direction == 'right':
        if map_pos == 3: return 0
        return map_pos + 1
    elif direction == 'back':
        map_pos += 2
        if map_pos == 4:
            return 0
        elif map_pos == 5:
            return 1
        else:
            return map_pos
    else:
        return map_pos

def mob_system_init():
    return {
        'is_mob': False,
        'current_mob': None,
        'mob_round': 0
    }

def character_init():
    return {
        'life': 100,
        'stamina': 100,
        'mana': 100,
        'damage': 2,
        'armor': 0
    }

def equipment_init():
    return {
        'weapon': '',
        'armor': '',
        'special': ''
    }

def clear_mob():
    global mob
    mob = mob_system_init()

def equip_obj(obj):
    global objects_data, equipment
    obj_data = objects_data[obj]
    obj_kind = obj_data['etype']
    if equipment[obj_kind] == '':
        inventory.remove(obj)
        equipment[obj_data['etype']] = obj
    else:
        inventory.remove(obj)
        inventory.append(equipment[obj_data['etype']])
        equipment[obj_data['etype']] = obj

############################################################################
############################################################################
############################################################################

directions = ['left', 'right', 'back']
global_cmds = ['examine', 'use', 'equip']
mobs_actions = ['hit', 'leave']
objects_data = load_data('data/objects.json')
mob = mob_system_init()
character = character_init()
inventory, equipment = [], equipment_init()

def loop():
    global character, mob, inventory, equipment
    room_nb, pos_map = 0, 2
    global_msg = ''
    rooms = load_data('data/rooms.json')

    while True:
        room = rooms[room_nb]

        clear_screen()
        top_interface(
            (('Life',character['life']), ('Stamina',character['stamina']), ('Mana',character['mana'])),
            pos_map=pos_map,
            room_id=room['id'],
            inventory=inventory,
            equipment=equipment
        )

        available_actions = list()
        if mob['is_mob']:
            if mob['current_mob'] == None:
                mob_id = randint(0,len(room['mobs'])-1)
                mob['current_mob'] = dict(room['mobs'][mob_id])
            if mob['mob_round'] == 0:
                print global_msg + '\n' + mob['current_mob']['msg']
            else:
                print global_msg
            print eval(room['mobs'][mob_id]['mob'])
            available_actions += mobs_actions
            mob['mob_round'] += 1
        else:
            print (global_msg or room['msg'])
            print eval(room['walls'][pos_map])
            if room['actions'][pos_map]:
                available_actions = list(room['actions'][pos_map] + global_cmds)
            else:
                available_actions = list(global_cmds)
            available_actions += directions

        print 'Choose an action: ' + ' / '.join(available_actions) + '\n'
        action_input = raw_input('> Your action: ')

        if not action_input: continue
        action = action_input.lower().strip()

        mobs_dice_roller = randint(0,11)
        if mobs_dice_roller % 2 == 0 and mob['is_mob'] == False and len(room['mobs']) > 0 and action != 'open door':
            mob['is_mob'] = True
        else:
            pass

        if action in mobs_actions and action in available_actions:
            if action == 'hit':
                loose_life = mob['current_mob']['damage'] - character['armor']
                if loose_life >= 0:
                    character['life'] -= loose_life
                else:
                    loose_life = 0
                mob['current_mob']['life'] -= character['damage']
                global_msg = 'You hit the mob by '+str(character['damage'])+' damages and lose '+str(loose_life)+' life point(s).\n'
                # TODO: remove this sentence (the chara should have a special ability to know this ?)
                global_msg += 'Mob\'s life remaining: ' + str(mob['current_mob']['life'])
            elif action == 'leave':
                clear_mob()
                global_msg = 'You left the combat !'
                continue
            else:
                pass

            if mob['current_mob']['life'] <= 0:
                clear_mob()
                global_msg = 'You defeat the mob !'

        elif action == 'open door' and 'open door' in available_actions:
            door = room['doors'][pos_map]
            door_status, door_for_room = door['status'], door['for_room']
            if door_status == 'opened':
                global_msg = ''
                room_nb = door_for_room
            elif door_status == 'closed' and ('key_' + str(door_for_room)) in inventory:
                global_msg = ''
                door['status'] = 'opened'
                door_other_side = next(index for (index, d) in enumerate(rooms[door_for_room]['doors']) if d['for_room'] == room['id'])
                rooms[door_for_room]['doors'][door_other_side]['status'] = 'opened'
                room_nb = door_for_room
            else:
                global_msg = 'The door seems locked ...'

        elif action == 'examine' and 'examine' in available_actions:
            objs = room['reviews'][pos_map]
            if objs:
                for obj in objs:
                    if obj not in inventory: inventory.append(obj)
                global_msg = 'You found ' + bcolors.BOLD + ', '.join(objs) + bcolors.ENDC + ' and put them into your bag.'
            else:
                global_msg = 'Nothing found here.'

        elif action in room['secrets'][pos_map]:
            objs = room['secrets_reviews'][pos_map]
            if objs:
                for obj in objs:
                    if obj not in inventory: inventory.append(obj)
                global_msg = 'You found ' + bcolors.BOLD + ', '.join(objs) + bcolors.ENDC + ' and put them into your bag.'
            else:
                global_msg = 'Nothing found here.'

        elif 'use' in action and 'use' in available_actions:
            obj = action.split(' ')[1]
            clear_mob()
            if obj not in inventory or 'key_' in obj or objects_data[obj]['type'] != 'usable':
                global_msg = 'You cannot use ' + obj + ' !'
            else:
                exec objects_data[obj]['action'] in globals()
                inventory.remove(obj)
                global_msg = objects_data[obj]['msg']

        elif 'equip' in action and 'equip' in available_actions:
            obj = action.split(' ')[1]
            clear_mob()
            if obj not in inventory or 'key_' in obj or objects_data[obj]['type'] != 'equipable':
                global_msg = 'You cannot equip ' + obj + ' !'
            else:
                exec objects_data[obj]['action'] in globals()
                global_msg = objects_data[obj]['msg']

        elif 'talk' in action and 'talk' in available_actions:
            clear_mob()
            talk = room['talk'][pos_map]
            if talk: global_msg = '. '.join(talk)

        elif action in directions and action in available_actions:
            global_msg = ''
            pos_map = next_map_pos(pos_map, action)

        else:
            global_msg = 'You cannot perform this action !'


if __name__ == "__main__":
    loop()
