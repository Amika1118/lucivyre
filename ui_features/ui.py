import os

def lines(count):
    for i in range(count):
        print("-", end="")
    print()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")