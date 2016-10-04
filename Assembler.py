import re
import sys

command_group = 1
dest_group = 1
comp_with_dest_group = 2
jmp_with_dest_group = 3
comp_no_dest_group = 1
jmp_no_dest_group = 2
output_suffix = "hack"
no_dest_string = "000"
suffix_length = 3
current_group = 16
with_dest_regex = re.compile("([AMD]{1,3})=([^;]{1,3});?(.*)")
no_dest_regex = re.compile("([^;]{1,3});?(.*)")
general_regex = re.compile("[^/\n(]+")
new_symbol_regex = re.compile("\(([^\d].*)\)")
symbol_regex = re.compile("@([^/]+)")
comp_dictionary = {"0":"0101010", "1":"0111111", "-1":"0111010",
                   "D":"0001100", "A":"0110000", "!D":"0001101",
                   "!A":"0110001", "-D":"0001111", "-A":"0110011",
                   "D+1":"0011111", "A+1":"0110111", "D-1":"0001110",
                   "A-1":"0110010", "D+A":"0000010", "D-A":"0010011",
                   "A-D":"0000111", "D&A":"0000000", "D|A":"0010101",
                   "M":"1110000", "!M":"1110001", "-M":"1110011",
                   "M+1":"1110111", "M-1":"1110010", "M+D":"1000010",
                   "D-M":"1010011", "M-D":"1000111", "D&M":"1000000",
                   "D|M":"1010101", "D+M":"1000010"}
dest_dictionary = {"M":"001", "D":"010", "MD":"011", "A":"100",
                   "AM":"101", "AD":"110", "AMD":"111"}
jmp_dictionary = {"JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100",
                  "JNE":"101", "JLE":"110", "JMP":"111", "":"000"}
symbols_dictionary = {"SP":"000000000000000", "LCL":"000000000000001",
                      "ARG":"000000000000010", "THIS":"000000000000011",
                      "THAT":"000000000000100", "R0":"000000000000000",
                      "R1":"000000000000001", "R2":"000000000000010",
                      "R3":"000000000000011", "R4":"000000000000100",
                      "R5":"000000000000101", "R6":"000000000000110",
                      "R7":"000000000000111", "R8":"000000000001000",
                      "R9":"000000000001001", "R10":"000000000001010",
                      "R11":"000000000001011", "R12":"000000000001100",
                      "R13":"000000000001101", "R14":"000000000001110",
                      "R15":"000000000001111", "SCREEN":"100000000000000",
                      "KBD":"110000000000000"}


def process_line(line):
    match = re.match(general_regex, line)
    if match:
        if line.startswith("@"):
            process_a_command(line)
        else:
            process_c_command(line)
        output.write("\n")


def process_a_command(command):
    output.write('0')
    regex = re.compile("@\d+")
    match = re.match(regex, command)
    if match:
        output.write(turn_to_binary(command[1:]))
    else:
        match = re.match(symbol_regex, line)
        name = match.group(command_group)
        if name in symbols_dictionary:
            output.write(symbols_dictionary[name])
        else:
            global current_group
            number = turn_to_binary(current_group)
            output.write(number)
            symbols_dictionary[name] = number
            current_group += 1
        

def turn_to_binary(decimal_number):
    num = int(decimal_number)
    binary_number = ""
    while num > 1:
        if num % 2 == 0:
            binary_number = "0" + binary_number
            num = num/2
        else:
            binary_number = "1" + binary_number
            num = (num-1)/2
    if num % 2 == 0:
        binary_number = "0" + binary_number
    else:
        binary_number = "1" + binary_number
    while len(binary_number) < 15:
        binary_number = "0" + binary_number
    return binary_number


def process_c_command(command):
    output.write("111")
    if command.__contains__("="):
        process_with_dest(command)
    else:
        process_no_dest(command)


def process_with_dest(command):
    match = re.match(with_dest_regex, command)
    process_comp(match.group(comp_with_dest_group))
    process_dest(match.group(dest_group))
    process_jmp(match.group(jmp_with_dest_group))


def process_no_dest(command):
    match = re.match(no_dest_regex, command)
    process_comp(match.group(comp_no_dest_group))
    output.write(no_dest_string)
    process_jmp(match.group(jmp_no_dest_group))


def process_comp(comp):
    output.write(comp_dictionary[comp])


def process_dest(dest):
    output.write(dest_dictionary[dest])


def process_jmp(jmp):
    output.write(jmp_dictionary[jmp])


def space_filter(string):
    new_string = ""
    for char in string:
        if char is '/':
            break
        if char not in ["\s", '\n', '\t', ' ']:
            new_string = new_string + char
    return new_string


def check_for_symbols(lines):
    line_number = 0
    for i in range(len(lines)):
        lines[i] = space_filter(lines[i])
        if lines[i].startswith("("):
            match = re.match(new_symbol_regex, lines[i])
            symbols_dictionary[match.group(command_group)] = turn_to_binary(line_number)
        elif not (lines[i].startswith("/") or lines[i] is ''):
            line_number += 1

if __name__ == "__main__":
    source = open(sys.argv[1], 'r')
    output_name = sys.argv[1][:len(sys.argv[1])-suffix_length]
    output = open(output_name + output_suffix, 'w')
    lines = source.readlines()
    check_for_symbols(lines)
    for line in lines:
        process_line(line)
    source.close()
    output.close()


