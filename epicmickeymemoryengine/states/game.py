from epicmickeymemoryengine.lua.communicator import get_lua, read_null_terminated_string
import dolphin_memory_engine
import struct

def read_u32(address):
    data = dolphin_memory_engine.read_bytes(address, 4)
    return int.from_bytes(data, byteorder='big')

def read_bool(address):
    data = dolphin_memory_engine.read_bytes(address, 1)
    return bool(data[0])

def read_float(address):
    data = dolphin_memory_engine.read_bytes(address, 4)
    return struct.unpack('>f', data)[0]

def is_movie_playing():
    """ Check if a movie is playing """
    return read_bool(0x806fd2b7)

def is_paused():
    """ Check if gameplay is paused (pause menu or main menu) """
    return read_bool(0x807170c7)

def is_loading():
    """ Check if the game is loading """
    return not read_bool(0x811ac7b3)

def is_in_cutscene():
    """ Check if the game is in a cutscene """
    return not read_bool(0x80795856)

def get_cursor_x():
    """ Get the x position of the reticle (does not work in menus)"""
    return read_float(0x91316be4)

def get_cursor_y():
    """ Get the y position of the reticle (does not work in menus)"""
    return read_float(0x91316be8)

def get_cursor_pos():
    """ Get the position of the reticle (does not work in menus)"""
    return (get_cursor_x(), get_cursor_y())

def get_files():
    current_address = 0x90ac32b0
    def add_path_from_pointer(pointer_address):
        if pointer_address == 0:
            return
        path = ""
        try:
            path = read_null_terminated_string(pointer_address)
        except:
            pass
        if path != "":
            return path
    paths = []
    for i in range(1082):
        try:
            num1 = read_u32(current_address)
            num2 = read_u32(current_address + 4)
            num3 = read_u32(current_address + 8)
            data_offset = read_u32(current_address + 12)
            path1_offset = read_u32(current_address + 16)
            path2_offset = read_u32(current_address + 20)
            path3_offset = read_u32(current_address + 24)
            size1 = read_u32(current_address + 28)
            size2 = read_u32(current_address + 32)
            path1 = add_path_from_pointer(read_u32(path1_offset))
            path2 = add_path_from_pointer(path2_offset)
            path3 = add_path_from_pointer(path3_offset)
            paths.append(path1)
            paths.append(path2)
            paths.append(path3)
            current_address += 36
        except Exception as e:
            break
    # remove duplicates
    paths = list(set(paths))
    paths = [path for path in paths if path is not None]
    return paths