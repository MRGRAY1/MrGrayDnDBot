import discord
import os
import re
import random
from dotenv import load_dotenv

###Displays help page
def get_help():
    with open('help.txt', 'r') as file:
        data = file.read()
    data = "```\n" + data + "\n```"
    return data
###/get_help

#def get_members(message):
#  #x = server.members
#  #print('This message will be displayed on the screen.')
#
#  with open('members.txt', 'w') as f:
#    for member in client.guilds.members:
#      #print('This message will be displayed on the screen.', file=f)
#      #print(member, file=f) # you'll just #print out Member objects your way.
#  return 1


####Roll dice that is in a set
def roll_dice(num_of_dice, dice_type, roll_set):
    dice_roll = 0
    all_dice = []
    dice_line = []
    num_of_dice = int(num_of_dice)
    dice_type = int(dice_type)
    roll_set = int(roll_set)

    for i in range(roll_set):
        dice_line = []
        for x in range(num_of_dice):
            if dice_type == 0:
                dice_roll = 0
            else:
                dice_roll = random.randint(1, dice_type)
            dice_line.append(dice_roll)
        all_dice.append(dice_line)
    return all_dice
###/roll_dice


####Get set of dice and total
def get_total(dice_set, drop_low):
    total = 0
    final = ""
    dice_set.sort(reverse=True)
    if drop_low:
        del dice_set[-1]
    for i in range(len(dice_set)):
        total += int(dice_set[i])
    #print(total)
    #print(dice_set)
    final += "\n["
    #print(str(len(dice_set)))
    for x in range(len(dice_set)):
        final += str(dice_set[x])
        if x < len(dice_set) - 1:
            final += ", "
    final += "] = " + str(total)

    return final
###/get_total

####Determine how many dice to roll
def get_dice(cmd, user):
    roll_set = 1
    num_of_dice = "1"
    dice_type = ""
    all_sets = ""
    drop_low = False

    multiple_sets = False
    #print(cmd)
    if "dl" in cmd:
        value = cmd[:-2]
        value = value.rstrip()
        #print(value)
        drop_low = True
    else:
        value = cmd
    #print(value)
    value = value.replace(" ", ",")
    value = value.replace("d", ',')
    #print(value)
    value = value.split(",")

    if " " in cmd:
        multiple_sets = True

    if multiple_sets:
        roll_set = value[0]
        if value[1] == "":
            num_of_dice = 1
        else:
            num_of_dice = value[1]
        dice_type = value[2]
    else:
        if value[0] == "":
            num_of_dice = 1
        else:
            num_of_dice = value[0]
        dice_type = value[1]

    final = roll_dice(num_of_dice, dice_type, roll_set)
    all_sets += user + " Rolled:"
    for i in range(len(final)):
        all_sets += get_total(final[i], drop_low)

    return all_sets
####/get_dice

####Name Gen Male
def name_gen_m():
    rand_name = ""
    with open('male_names.txt', 'r') as file:
        names = file.read().split("\n")
    rand_name = names[random.randint(0, len(names) - 1)]
    print(rand_name)
    return "Male Name: " + rand_name
###/name_gen_m

####Name Gen Female
def name_gen_f():
    rand_name = ""
    with open('female_names.txt', 'r') as file:
        names = file.read().split("\n")
    rand_name = names[random.randint(0, len(names) - 1)]
    print(rand_name)
    return "Female Name: " + rand_name
###/name_gen_f

####Get Adv/Dis
def AdvDis(advantage, cmd):
    roll_1 = random.randint(1, 20)
    roll_2 = random.randint(1, 20)
    High = 20
    Low = 1
    dropped = 1
    notDropped = 20
    final = ""
    positive = ""
    modifier = 0
    get_sign = 0
    value = cmd.replace(" ", "")
    print(str(value))

    if "+" in value:
        positive = " + "
        get_sign = value.index("+")
        modifier = value[get_sign + 1:]
        print(str(get_sign))

    elif "-" in value:
        positive = " - "
        get_sign = value.index("-")
        modifier = value[get_sign + 1:]

    print(str(positive) + str(modifier))

    if roll_1 > roll_2:
        High = roll_1
        Low = roll_2
    elif roll_1 < roll_2:
        Low = roll_1
        High = roll_2
    elif roll_1 == roll_2:
        High = Low = roll_1

    if advantage:
        final += ("\nRoll with Advantage:\n")
        final += ("Total is: " + str(High))
        dropped = Low
        notDropped = High
    elif not advantage:
        final += ("\nRoll with Disadvantage:\n")
        final += ("Total is: " + str(Low))
        dropped = High
        notDropped = Low

    if int(modifier) != 0:
        if positive == " + ":
            mtotal = notDropped + int(modifier)
        elif positive == " - ":
            mtotal = notDropped - int(modifier)
        final += (str(positive) + str(modifier))
        final += " = " + str(mtotal)

    final += ("\nDropped: " + str(dropped))

    #print(final)
    return final
###/AdvDis

#### Main get command function
async def get_cmd(message, user):
    cmd = message.content.lower().replace("&", "")
    final = " "
    error1 = "Unknown input. Do better. -Bot"
    fail = False

    if len(cmd) < 1:
        fail = True
    
    #(dis\s*[\-\+]\s*\d+)|(adv\s*[\-\+]\s*\d)|(dis)|(adv)
    if (re.match("\d+\s+\d+d\d+\s+dl", cmd) or re.match("\d+\s+\d+d\d+", cmd) or re.match("\d+d\d+\sdl", cmd) or re.match("\d+d\d+", cmd) or re.match("d\d+", cmd)):
        final = get_dice(cmd, user)
    elif cmd == "dis" or re.match("dis\s*[\-\+]\s*\d+", cmd):
        final = AdvDis(False, cmd)
    elif cmd == "adv" or re.match("adv\s*[\-\+]\s*\d", cmd):
        final = AdvDis(True, cmd)
    elif cmd == "help" or fail == True:
        final = get_help()
    elif cmd == "hello":
        final = "Hello! " + str(user)
    elif cmd == "gennamef":
        final = name_gen_f()
    elif cmd == "gennamem":
        final = name_gen_m()
    else:
        final = error1

    await message.channel.send(final)
###/get_cmd

load_dotenv(".env")
client = discord.Client()
botkey = os.getenv("BOTKEY")

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    user = message.author.name
    if message.author == client.user:
        return
    elif message.content.startswith("&"):
        #await message.channel.send(get_cmd(message, user))
        await get_cmd(message, user)

client.run(botkey)
