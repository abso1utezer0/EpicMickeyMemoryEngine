from epicmickeymemoryengine.lua.communicator import get_lua
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