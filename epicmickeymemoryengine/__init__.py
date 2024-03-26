import dolphin_memory_engine

def hook():
    """ Hook the memory engine """
    
    dolphin_memory_engine.hook()

def unhook():
    """ Unhook the memory engine """

    dolphin_memory_engine.un_hook()

def is_hooked() -> bool:
    """ Check if the memory engine is hooked """

    return dolphin_memory_engine.is_hooked()