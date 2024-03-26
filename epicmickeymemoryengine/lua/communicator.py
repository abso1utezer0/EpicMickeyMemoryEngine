import dolphin_memory_engine
import time

def read_null_terminated_string(address, max_length=5000):
    string_bytes = dolphin_memory_engine.read_bytes(address, max_length)
    string = ""
    for byte in string_bytes:
        if byte == 0:
            break
        string += chr(byte)
    return string

def read_from_pointer(pointer_address, function, *args, **kwargs):
    address = read_u32(pointer_address)
    return function(address, *args, **kwargs)

def read_string(address, length):
    string_bytes = dolphin_memory_engine.read_bytes(address, length)
    string = ""
    for byte in string_bytes:
        string += chr(byte)
    return string

def read_u32(address):
    data = dolphin_memory_engine.read_bytes(address, 4)
    return int.from_bytes(data, byteorder='big')

def read_config_entry(address):
    key = read_from_pointer(address + 12, read_null_terminated_string)
    value = read_from_pointer(address + 16, read_null_terminated_string, 10000)
    #if value == "Effects/_Shared/UI_FadeIn_Ink_Splats_StartScreen.nif":
    #    print(hex(address + 16))
    #    exit()
    return (key, value)

def read_config_entries(address):
    entries = []
    while True:
        try:
            entry = read_config_entry(address)
            entries.append(entry)
            address += 36
        except:
            break
    return entries

def get_config_value(key):
    config_address = 0x80f36798
    entries = read_config_entries(config_address)
    for entry in entries:
        if entry[0] == key:
            return entry[1]
    return None

def write_config(address, key, value:str):
    # read thru the config entries until we find the key
    while True:
        read_key = read_from_pointer(address + 12, read_null_terminated_string)
        address += 36
        if read_key == key:
            break
    # write the value
    address = address - 20
    address = read_u32(address)
    # fixed length string of 10000, fill the rest with spaces (fill end)
    value = value.ljust(10000, " ")
    data = value.encode("ascii")
    dolphin_memory_engine.write_bytes(address, data)

def execute_lua(lua:str):
    # write the command to the config file
    write_config(0x80f36798, "LuaToExecute", lua)

def execute_lua_file(file_path:str):
    with open(file_path, "r") as lua_file:
        lua = lua_file.read()
    lua = lua.replace("\n", "~")
    print(lua)
    execute_lua(lua)

def get_lua(variable_name):
    execute_lua(f"SetConfigVariableString(GetPlayer(), \"LuaOut\", tostring({variable_name}))")
    value = "nil"
    while True:
        value = get_config_value("LuaOut")
        if value == ".":
            time.sleep(0.01)
        else:
            break
    while True:
        execute_lua(f"SetConfigVariableString(GetPlayer(), \"LuaOut\", \".\")")
        if get_config_value("LuaOut") == ".":
            break
        else:
            time.sleep(0.01)
    return value