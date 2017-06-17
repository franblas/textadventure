from utils import bcolors

def statusbar((k, val)):
    remaining = val % 10
    if val == 100: remaining = 10
    color = None
    if val > 66:
        color = bcolors.OKGREEN
    elif val <= 66 and val > 33:
        color = bcolors.WARNING
    else:
        color = bcolors.FAIL
    return k + ': ' + color + str(val) + '%' + bcolors.ENDC

def global_status(pos, room_id, inventory, status, equipment):
    plop = ''
    idash, ispace = '-'*11, ' '*5
    if pos == 1:
        plop += "+" + bcolors.OKBLUE + idash + bcolors.ENDC + "+\n"
        plop += "|"+(ispace*2+' ')+"|"+ispace+"Room "+str(room_id)+" \n"
        plop += "|"+ispace+"^"+ispace+"|"+ispace+""+'  '.join([statusbar(s) for s in status])+"\n"
        plop += "|"+(ispace*2+' ')+"|"+ispace+"Bag: "+', '.join(inventory)+"\n"
        plop += "+"+idash+"+"+ispace+"Equipment: "+', '.join(equipment.values())+"\n"
    elif pos == 0:
        plop += "+"+idash+"+\n"
        plop += bcolors.OKBLUE + "|" + bcolors.ENDC + ""+(ispace*2+' ')+"|"+ispace+"Room "+str(room_id)+" \n"
        plop += bcolors.OKBLUE + "|" + bcolors.ENDC + ""+ispace+"<"+ispace+"|"+ispace+""+'  '.join([statusbar(s) for s in status])+"\n"
        plop += bcolors.OKBLUE + "|" + bcolors.ENDC + ""+(ispace*2+' ')+"|"+ispace+"Bag: "+', '.join(inventory)+"\n"
        plop += "+"+idash+"+"+ispace+"Equipment: "+', '.join(equipment.values())+"\n"
    elif pos == 2:
        plop += "+"+idash+"+\n"
        plop += "|"+(ispace*2+' ')+""+bcolors.OKBLUE+"|"+bcolors.ENDC+""+ispace+"Room "+str(room_id)+" \n"
        plop += "|"+ispace+">"+ispace+""+bcolors.OKBLUE+"|"+bcolors.ENDC+""+ispace+""+'  '.join([statusbar(s) for s in status])+"\n"
        plop += "|"+(ispace*2+' ')+""+bcolors.OKBLUE+"|"+bcolors.ENDC+""+ispace+"Bag: "+', '.join(inventory)+"\n"
        plop += "+"+idash+"+"+ispace+"Equipment: "+', '.join(equipment.values())+"\n"
    elif pos == 3:
        plop += "+"+idash+"+\n"
        plop += "|"+(ispace*2+' ')+"|"+ispace+"Room "+str(room_id)+" \n"
        plop += "|"+ispace+"v"+ispace+"|"+ispace+""+'  '.join([statusbar(s) for s in status])+"\n"
        plop += "|"+(ispace*2+' ')+"|"+ispace+"Bag: "+', '.join(inventory)+"\n"
        plop += "+" + bcolors.OKBLUE + idash + bcolors.ENDC + "+"+ispace+"Equipment: "+', '.join(equipment.values())+"\n"
    else:
        plop += "+"+idash+"+\n"
        plop += "|"+(ispace*2+' ')+"|"+ispace+"Room "+str(room_id)+" \n"
        plop += "|"+ispace+"+"+ispace+"|"+ispace+""+'  '.join([statusbar(s) for s in status])+"\n"
        plop += "|"+(ispace*2+' ')+"|"+ispace+"Bag: "+', '.join(inventory)+"\n"
        plop += "+"+idash+"+"+ispace+"Equipment: "+', '.join(equipment.values())+"\n"
    return plop

def top_interface(status, pos_map, room_id, inventory, equipment):
    ispace, idash = 22, 69
    print "\n"+(" "*ispace)+"A small Adventure"+(" "*ispace)
    print ("_"*idash)+"\n"
    print global_status(pos_map, room_id, inventory, status, equipment)
    print ("_"*idash)+"\n"
