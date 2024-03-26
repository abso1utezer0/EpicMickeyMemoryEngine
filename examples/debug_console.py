import os
import sys
# add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import epicmickeymemoryengine.states.game as game
import epicmickeymemoryengine.lua.communicator as lua
import epicmickeymemoryengine as emme

def main():
    print("Epic Mickey Lua Debug Console\n")

    while True:
        # get the input
        command = input(">>> ")
        # if it is "exit", break the loop
        if command in ["exit", "quit"]:
            break
        # hook the game
        emme.hook()
        if not emme.is_hooked():
            print("The game is not running, please start it.")
            continue
        if game.is_loading():
            print("The game is loading, please wait.")
            continue
        if game.is_paused():
            print("The game is paused or in a menu, commands will not be executed.")
            continue
        # execute the command
        lua.execute_lua(command)
        # unhook the game
        emme.unhook()

if __name__ == "__main__":
    main()