import re

command_group = 1

def processLine(line):
   regex = re.compile("\s*(.*?)\s*(?://.*)?")
   match = re.match(regex, line)
   if match:
       command = match.group(command_group)
       if command.startswith("@"):
           processACommand(command)
       else:
           processCCommand(command)
    file.write("\n")

def processACommand(command):
    regex = re.compile("@\d+")
    match =re.match(regex, command)
    if match:
        turnToBinary(command[1:])
    else:

def turnToBinary(numString):
    num = int(numString)
    numberGroup = []
    while(num > 1):
        if num%2 == 0:
            numberGroup.append(0)
            num = num/2
        else:
            numberGroup.append(1)
            num = (num-1)/2
    if num%2 == 0:
        numberGroup.append(0)
    else:
        numberGroup.append(1)
    numberGroup.sort(reverse=True)
    for char in numberGroup:
        file.write(char)

file=0
