#!/usr/bin/env python3
import math
import os
import time
from colorama import init, Fore, Style

init(autoreset=True)

debug_mode = False
mode = "text_to_bf"

def stabilizator(value, max_adjustment=10):
    best_pair = None
    best_score = float('inf')

    for adjustment in range(-max_adjustment, max_adjustment + 1):
        adjusted_value = value + adjustment
        if adjusted_value <= 0:
            continue
        for i in range(2, int(adjusted_value ** 0.5) + 1):
            if adjusted_value % i == 0:
                factor1 = i
                factor2 = adjusted_value // i
                factor_diff = abs(factor1 - factor2)
                score = abs(adjustment) * 10 + factor_diff
                if score < best_score:
                    best_score = score
                    best_pair = (factor1, factor2, -adjustment)

    if not best_pair:
        return (1, value, 0)
    return best_pair

def text_to_brainfuck(text):
    bf_code = ""
    if debug_mode:
        print(f"{Fore.YELLOW}DEBUG: Converting text to Brainfuck...\n")
    for char in text:
        value = 0 if char == ' ' else ord(char)
        a, b, diff = stabilizator(value)
        if debug_mode:
            print(f"{Fore.CYAN}{char} ({value}) → {a} x {b} (Diff: {diff})")
        loop = "+" * a + "[>" + "+" * b + "<-]>"

        if diff > 0:
            loop += "+" * abs(diff)
        elif diff < 0:
            loop += "-" * abs(diff)

        bf_code += loop + ".>"
    return bf_code

def brainfuck_to_text(code):
    tape = [0] * 30000
    pointer = 0
    output = ""
    i = 0
    loop_stack = []
    while i < len(code):
        command = code[i]
        if command == '>':
            pointer += 1
        elif command == '<':
            pointer -= 1
        elif command == '+':
            tape[pointer] = (tape[pointer] + 1) % 256
        elif command == '-':
            tape[pointer] = (tape[pointer] - 1) % 256
        elif command == '.':
            output += chr(tape[pointer])
        elif command == ',':
            pass  # Not used here
        elif command == '[':
            if tape[pointer] == 0:
                open_brackets = 1
                while open_brackets != 0:
                    i += 1
                    if code[i] == '[':
                        open_brackets += 1
                    elif code[i] == ']':
                        open_brackets -= 1
            else:
                loop_stack.append(i)
        elif command == ']':
            if tape[pointer] != 0:
                i = loop_stack[-1]
            else:
                loop_stack.pop()
        i += 1
    return output

def banner():
    print(Fore.RED + Style.BRIGHT + """
         ,--.                                       
       ,--.'|                                       
   ,--,:  : |                          ,---,        
,`--.'`|  ' :                        ,---.'|        
|   :  :  | |                        |   | :        
:   |   \ | :   ,---.     ,---.      |   | |        
|   : '  '; |  /     \   /     \   ,--.__| |        
'   ' ;.    ; /    /  | /    /  | /   ,'   |        
|   | | \   |.    ' / |.    ' / |.   '  /  |        
'   : |  ; .''   ;   /|'   ;   /|'   ; |:  |        
|   | '`--'  '   |  / |'   |  / ||   | '/  '        
'   : |      |   :    ||   :    ||   :    :|        
;   |.'       \   \  /  \   \  /  \   \  /          
'---'          `----'    `----'    `----'           
    ,---,.                                          
  ,'  .'  \                      ,--,               
,---.' .' |  __  ,-.           ,--.'|         ,---, 
|   |  |: |,' ,'/ /|           |  |,      ,-+-. /  |
:   :  :  /'  | |' | ,--.--.   `--'_     ,--.'|'   |
:   |    ; |  |   ,'/       \  ,' ,'|   |   |  ,"' |
|   :     \'  :  / .--.  .-. | '  | |   |   | /  | |
|   |   . ||  | '   \__\/: . . |  | :   |   | |  | |
'   :  '; |;  : |   ," .--.; | '  : |__ |   | |  |/ 
|   |  | ; |  , ;  /  /  ,.  | |  | '.'||   | |--'  
|   :   /   ---'  ;  :   .'   \;  :    ;|   |/      
|   | ,'          |  ,     .-./|  ,   / '---'       
`----'             `--`---'     ---`-'              


       Brainfuck <-> Text Bi-Directional Translator
    """)

def main_loop():
    global debug_mode, mode
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        print(Fore.CYAN + f"Mode: {mode.upper()}    Debug Mode: [{'✔' if debug_mode else ' '}]")
        print(Fore.YELLOW + "Commands: [1] Toggle Debug  [2] Switch Mode  [3] Exit\n")

        if mode == "text_to_bf":
            user_input = input(Fore.GREEN + "Text > ")
            if user_input == "1":
                debug_mode = not debug_mode
                continue
            elif user_input == "2":
                mode = "bf_to_text"
                continue
            elif user_input == "3":
                break
            print(Fore.WHITE + "\nBrainfuck:\n" + Fore.BLUE + text_to_brainfuck(user_input))
        else:
            user_input = input(Fore.GREEN + "Brainfuck > ")
            if user_input == "1":
                debug_mode = not debug_mode
                continue
            elif user_input == "2":
                mode = "text_to_bf"
                continue
            elif user_input == "3":
                break
            print(Fore.WHITE + "\nOutput:\n" + Fore.GREEN + brainfuck_to_text(user_input))

        input(Fore.MAGENTA + "\nPress ENTER to continue...")

if __name__ == "__main__":
    main_loop()
