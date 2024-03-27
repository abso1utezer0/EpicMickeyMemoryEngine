from epicmickeymemoryengine.lua.communicator import execute_lua, get_lua

def bark(message, show_time=1, icon_name="", title="Title") -> None:
    """ Display a message to the player.

    ### Parameters
    1. `message` (`str`)
        The message to display.
    2. `show_time` (`int`, optional)
        The amount of time in seconds to display the message. Default is 1.
    3. `icon_name` (`str`, optional)
        The name of the icon to display with the message. Default is "".
    4. `title` (`str`, optional)
        The title of the message. Default is "Title".
    """

    execute_lua(f"Bark(GetPlayer(), \"{message}\", {show_time}, \"{icon_name}\", \"{title}\")")

def yes_no_dialog_box(question, answer1="Yes", answer2="No", icon_name="", title="Title") -> None:
    """ Display a dialog box with a question and two possible answers.
    
    ### Parameters
    1. `question` (`str`)
        The question to ask the player.
    2. `answer1` (`str`, optional)
        The text to display for the first answer. Default is "Yes".
    3. `answer2` (`str`, optional)
        The text to display for the second answer. Default is "No".
    4. `icon_name` (`str`, optional)
        The name of the icon to display in the dialog box. Default is "".
    5. `title` (`str`, optional)
        The title of the dialog box. Default is "Title".
    """

    execute_lua(f"YesNoDialogBox(\"{question}\", \"{answer1}\", \"{answer2}\", \"{icon_name}\", \"{title}\")")

def get_dialog_box_response() -> str:
    """ Get the response from a dialog box.

    ### Returns
    `str`
        The response from the dialog box. (Yes or No)
    """

    return get_lua("GetDialogResponse()")

def play_movie(movie_name:str) -> None:
    """ Play a movie.

    ### Parameters
    1. `movie_name` (`str`)
        The name of the movie to play.
    """

    execute_lua(f"PlayMovie(GetPlayer(), \"{movie_name}\")")

def get_ticket_count() -> int:
    """ Get the number of E-Tickets the player has.

    ### Returns
    `int`
        The number of E-Tickets the player has.
    """
    return int(get_lua("GetTicketCount()"))

def get_config_variable_string(variable_name:str) -> str:
    """ Get the value of a config variable.

    ### Parameters
    1. `variable_name` (`str`)
        The name of the variable to get the value of.

    ### Returns
    `str`
        The value of the config variable.
    """

    return get_lua(f"GetConfigVariableString(GetPlayer(), \"{variable_name}\")")

def set_config_variable_string(variable_name:str, value:str) -> None:
    """ Set the value of a config variable.

    ### Parameters
    1. `variable_name` (`str`)
        The name of the variable to set the value of.
    2. `value` (`str`)
        The value to set the variable to.
    """

    execute_lua(f"SetConfigVariableString(GetPlayer(), \"{variable_name}\", \"{value}\")")

def get_config_variable_bool(variable_name:str) -> bool:
    """ Get the value of a config variable.

    ### Parameters
    1. `variable_name` (`str`)
        The name of the variable to get the value of.

    ### Returns
    `bool`
        The value of the config variable.
    """

    return bool(get_lua(f"GetConfigVariableBool(GetPlayer(), \"{variable_name}\")"))

def set_config_variable_bool(variable_name:str, value:bool) -> None:
    """ Set the value of a config variable.

    ### Parameters
    1. `variable_name` (`str`)
        The name of the variable to set the value of.
    2. `value` (`bool`)
        The value to set the variable to.
    """

    execute_lua(f"SetConfigVariableBool(GetPlayer(), \"{variable_name}\", {str(value).lower()})")

def get_config_variable_float(variable_name:str) -> float:
    """ Get the value of a config variable.

    ### Parameters
    1. `variable_name` (`str`)
        The name of the variable to get the value of.

    ### Returns
    `float`
        The value of the config variable.
    """

    return float(get_lua(f"GetConfigVariableFloat(GetPlayer(), \"{variable_name}\")"))

def set_config_variable_float(variable_name:str, value:float) -> None:
    """ Set the value of a config variable.

    ### Parameters
    1. `variable_name` (`str`)
        The name of the variable to set the value of.
    2. `value` (`float`)
        The value to set the variable to.
    """

    execute_lua(f"SetConfigVariableFloat(GetPlayer(), \"{variable_name}\", {value})")

def get_game_time() -> float:
    """ Get the current game time.

    ### Returns
    `float`
        The current game time.
    """

    return float(get_lua("GetGameTime()"))

def set_percent_game_speed(speed:float) -> None:
    """ Set the game speed as a percentage of normal speed.

    ### Parameters
    1. `speed` (`float`)
        The speed to set the game to as a percentage of normal speed. (default % is 1.0)
    """

    execute_lua(f"SetPercentGameSpeed({speed})")

def clean_load_level(level_name:str) -> None:
    """ Load a level.

    ### Parameters
    1. `level_name` (`str`)
        The name of the level to load.
    """

    execute_lua(f"CleanLoadLevel(\"{level_name}\")")