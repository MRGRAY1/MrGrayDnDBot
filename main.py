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
    with open('Names/male_names.txt', 'r') as file:
        names = file.read().split("\n")
    rand_name = names[random.randint(0, len(names) - 1)]
    print(rand_name)
    return "Male Name: " + rand_name
###/name_gen_m

####Name Gen Female
def name_gen_f():
    rand_name = ""
    with open('Names/female_names.txt', 'r') as file:
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

###get Boulder Parchment Shears
def getBPS(cmd, user):
    player1 = 0
    player2 = 0
    choices = ["Boulder", "Parchment", "Shears"]
    player2 = random.randint(1,99)
    player2 = player2 % 3
    final = ""

    if cmd == "b" or cmd == "boulder":
        player1 = 0
    elif cmd == "p" or cmd == "parchment":
        player1 = 1
    elif cmd == "s" or cmd == "shears":
        player1 = 2
    print (player1)
    print (player2)
    final += (f"\n" + user + " played: " + choices[player1])
    final += (f"\nBot played: " + choices[player2])
    if player1 == player2:
        final += (f"\n" + user + " and Bot Tied. Try Again.")
    elif (player1 == 0 and player2 == 1) or (player1 == 1 and player2 == 2) or (player1 == 2 and player2 == 0):
        final += (f"\n" + user + " Lost! Try Again.")
    elif (player1 == 0 and player2 == 2) or (player1 == 1 and player2 == 0) or (player1 == 2 and player2 == 1):
        final += (f"\n" + user + " Won! Good Job!")

    return final
###getBPS()

###Class Descriptions
def getClass():
    with open("Classes/classes.txt", 'r') as file:
        data = file.read()
    final = "Dungeons and Dragons Classes:\n"
    data = "```\n" + data + "\n```"
    final += data
    return final
###getClass()

###Class Decriptions
async def getClassDesc(cl, message):
    if cl == "barbarian":
        await message.channel.send("Barbarian:", file=discord.File("Classes/Barbarian.txt"))
    elif cl == "artificer":
        await message.channel.send("Artificer:", file=discord.File("Classes/Artificer.txt"))
    elif cl == "bard":
        await message.channel.send("Bard:", file=discord.File("Classes/Bard.txt"))
    elif cl == "cleric":
        await message.channel.send("Cleric:", file=discord.File("Classes/Cleric.txt"))
    elif cl == "druid":
        await message.channel.send("Druid:", file=discord.File("Classes/Druid.txt"))
    elif cl == "fighter":
        await message.channel.send("Fighter:", file=discord.File("Classes/Fighter.txt"))
    elif cl == "monk":
        await message.channel.send("Monk:", file=discord.File("Classes/Monk.txt"))
    elif cl == "paladin":
        await message.channel.send("Paladin:", file=discord.File("Classes/Paladin.txt"))
    elif cl == "ranger":
        await message.channel.send("Ranger:", file=discord.File("Classes/Ranger.txt"))
    elif cl == "rogue":
        await message.channel.send("Rogue:", file=discord.File("Classes/Rogue.txt"))
    elif cl == "sorcerer":
        await message.channel.send("Sorcerer:", file=discord.File("Classes/Sorcerer.txt"))
    elif cl == "warlock":
        await message.channel.send("Warlock:", file=discord.File("Classes/Warlock.txt"))
    elif cl == "wizard":
        await message.channel.send("Wizard:", file=discord.File("Classes/Wizard.txt"))
###getClassDesc()



#### Main get command function
async def get_cmd(message, user):
    cmd = message.content.lower().replace(".", "")
    final = ""
    error1 = "Unknown input. Do better. -Bot"
    fail = False
    

    if len(cmd) < 1:
        fail = True
    
    #(dis\s*[\-\+]\s*\d+)|(adv\s*[\-\+]\s*\d)|(dis)|(adv)
    if (re.match("\d+\s+\d+d\d+\s+dl", cmd) or re.match("\d+\s+\d+d\d+", cmd) or re.match("\d+d\d+\sdl", cmd) or re.match("\d+d\d+", cmd) or re.match("d\d+", cmd) or re.match("\d+\s+d\d", cmd)):
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
    elif (cmd == "b" or cmd == "p" or cmd == "s" or cmd == "boulder" or cmd == "parchment" or cmd == "shears"):
        final = getBPS(cmd, user)
    elif cmd == "class":
        final = getClass()
    elif (cmd =="barbarian" or cmd == "artificer" or cmd == "bard" or cmd == "cleric" or cmd == "druid" or
          cmd =="fighter" or cmd == "monk" or cmd =="paladin" or cmd == "ranger" or cmd == "rogue" or
          cmd =="sorcerer" or cmd == "warlock" or cmd == "wizard"):
        await getClassDesc(cmd, message)
    else:
        final = error1

    if final != "":
        await message.channel.send(final)
###/get_cmd


load_dotenv(".env")
client = discord.Client()
botkey = os.getenv("BOTKEY")
print (botkey)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    user = message.author.name
    if message.author == client.user:
        return
    elif message.content.startswith("."):
        #await message.channel.send(get_cmd(message, user))
        await get_cmd(message, user)

client.run(botkey)
