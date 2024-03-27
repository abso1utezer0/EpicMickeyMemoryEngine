import os
import sys
import time
import discord
from discord import app_commands

# add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import epicmickeymemoryengine as emme
import epicmickeymemoryengine.states.game as game
import epicmickeymemoryengine.lua.wrappers as lua_wrapper
import epicmickeymemoryengine.lua.communicator as lua

# set the path to the token.txt file here
token_path = r"C:\Users\thise\source\repos\EpicMickeyMemoryEngine\examples\token.txt"

# check if token.txt exists
if not os.path.exists(token_path):
    print("token.txt not found, please create a token.txt file with the bot token.")
    sys.exit(1)

# read the token from token.txt
with open(token_path, "r") as token_file:
    token = token_file.read().strip()

# set the path to the game files here (used for error checking movies)
game_path = r"C:\Users\thise\Documents\epic_mickey_clean\DATA\files"

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(1134200376275513475))

@client.event
async def on_message(message):
    if message.channel.id == 1220727456865194087:
        if message.author.id != client.user.id:
            emme.hook()
            # stop the message from being shown if the game is loading, paused, or in a cutscene
            # this ensures we dont softlock the game
            if game.is_loading() or game.is_paused() or game.is_in_cutscene():
                return
            message.content = ''.join([i if ord(i) < 128 else ' ' for i in message.content])
            lua_wrapper.bark(message=message.content, show_time=5, icon_name="", title=message.author)
            emme.unhook()

@tree.command(
    name="exec_lua",
    description="Execute a lua script",
    guild=discord.Object(1134200376275513475)
)
async def exec_lua(interaction:discord.Interaction, lua_snippet: str):
    emme.hook()
    if game.is_loading() or game.is_paused() or game.is_in_cutscene():
        emme.unhook()
        await interaction.response.send_message("The game is loading, paused, or in a cutscene, please wait.")
        return
    # replace any unicode characters with "\charcode"
    lua_snippet = ''.join([i if ord(i) < 128 else f"\\{ord(i)}" for i in lua_snippet])
    lua.execute_lua(lua_snippet)
    emme.unhook()
    await interaction.response.send_message(f"{interaction.user.mention} executed a lua script:\n```lua\n{lua_snippet}\n```")

# lua_file - execute a lua script from a file
@tree.command(
    name="exec_lua_file",
    description="Execute a lua script from a file",
    guild=discord.Object(1134200376275513475)
)
async def exec_lua_file(interaction:discord.Interaction, file: discord.Attachment):
    emme.hook()
    if game.is_loading() or game.is_paused() or game.is_in_cutscene():
        emme.unhook()
        await interaction.response.send_message("The game is loading, paused, or in a cutscene, please wait.")
        return
    # temp path is current directory
    temp_lua_path = os.path.join(os.getcwd(), "temp.lua")
    # save the file to temp.lua in the current directory
    with open(temp_lua_path, "wb") as temp_file:
        await file.save(temp_file)
    # execute the file
    lua.execute_lua_file(temp_lua_path)
    emme.unhook()
    # @{author} executed a lua script: \n```lua\n{contents of file}\n```
    lua_contents = open(temp_lua_path, "r").read()
    await interaction.response.send_message(f"{interaction.user.mention} executed a lua script:\n```lua\n{lua_contents}\n```")

@tree.command(
    name="ask",
    description="Ask a question",
    guild=discord.Object(1134200376275513475)
)
async def ask(interaction:discord.Interaction, question: str, answer1: str, answer2: str):
    emme.hook()
    if game.is_loading() or game.is_paused() or game.is_in_cutscene():
        emme.unhook()
        await interaction.response.send_message("The game is loading, paused, or in a cutscene, please wait.")
        return
    # display name of the user who asked the question
    username = interaction.user.display_name
    lua_wrapper.yes_no_dialog_box(question=question, answer1=answer1, answer2=answer2, icon_name="", title=username)
    emme.unhook()
    # show that the question was asked
    await interaction.response.send_message(f"{interaction.user.mention} asked: \"{question}\"")
    response = None
    # wait for the response
    while response == None:
        emme.hook()
        response = lua_wrapper.get_dialog_box_response()
        emme.unhook()
    if response == "Yes":
        response = answer1
    elif response == "No":
        response = answer2
    await interaction.followup.send(f"Player answered: {response}")

# ask and execute - ask a question and execute a lua script based on the answer
@tree.command(
    name="ask_exec",
    description="Ask a question and execute a lua script based on the answer",
    guild=discord.Object(1134200376275513475)
)
async def ask_exec(interaction:discord.Interaction, question: str, answer1: str, answer2: str, lua1: str, lua2: str):
    emme.hook()
    if game.is_loading() or game.is_paused() or game.is_in_cutscene():
        emme.unhook()
        await interaction.response.send_message("The game is loading, paused, or in a cutscene, please wait.")
        return
    username = interaction.user.display_name
    lua_wrapper.yes_no_dialog_box(question=question, answer1=answer1, answer2=answer2, icon_name="", title=username)
    emme.unhook()
    # show that the question was asked
    await interaction.response.send_message(f"{interaction.user.mention} asked: \"{question}\"")
    response = None
    # wait for the response
    while response == None:
        emme.hook()
        response = lua_wrapper.get_dialog_box_response()
        emme.unhook()
    if response == "Yes":
        response = answer1
        lua_snippet = lua1
    elif response == "No":
        response = answer2
        lua_snippet = lua2
    await interaction.followup.send(f"Player answered: {response}")
    emme.hook()
    lua.execute_lua(lua_snippet)
    emme.unhook()

@tree.command(
    name="get",
    description="Get the value of a lua variable or expression",
    guild=discord.Object(1134200376275513475)
)
async def get(interaction:discord.Interaction, variable_name: str):
    emme.hook()
    if game.is_loading() or game.is_paused() or game.is_in_cutscene():
        emme.unhook()
        await interaction.response.send_message("The game is loading, paused, or in a cutscene, please wait.")
        return
    value = lua.get_lua(variable_name)
    emme.unhook()
    await interaction.response.send_message(f"Value of {variable_name}: {value}")

# audio_event - play an audio event
@tree.command(
    name="audio_event",
    description="Play an audio event",
    guild=discord.Object(1134200376275513475)
)
async def audio_event(interaction:discord.Interaction, event: str):
    emme.hook()
    if game.is_loading() or game.is_paused():
        emme.unhook()
        await interaction.response.send_message("The game is loading or paused, please wait.")
        return
    lua.execute_lua(f"AudioPostEventOn(GetPlayer(), \"{event}\")")
    emme.unhook()
    await interaction.response.send_message(f"{interaction.user.mention} played audio event: `{event}`")

# play movie - play a movie
@tree.command(
    name="play_movie",
    description="Play a movie",
    guild=discord.Object(1134200376275513475)
)
async def play_movie(interaction:discord.Interaction, movie: str):
    # movies path
    movies_path = os.path.join(game_path, "Movies")
    movie_path = os.path.join(movies_path, movie)
    # check to see if the movie exists
    if not os.path.exists(movie_path):
        await interaction.response.send_message(f"Movie not found: {movie}")
        return
    
    emme.hook()
    if game.is_loading() or game.is_paused() or game.is_in_cutscene() or game.is_movie_playing():
        emme.unhook()
        await interaction.response.send_message("The game is loading, paused, in a cutscene, or a movie is already playing, please wait.")
        return
    lua_wrapper.play_movie(movie)
    emme.unhook()
    await interaction.response.send_message(f"{interaction.user.mention} played movie: `{movie}`")

# get global files
@tree.command(
    name="get_files",
    description="Get a list of global files",
    guild=discord.Object(1134200376275513475)
)
async def get_files(interaction:discord.Interaction):
    emme.hook()
    files = game.get_files()
    emme.unhook()
    string = ""
    # must be 2000 characters or less
    for file in files:
        string += f"{file}\n"
    
    # remove any non-ascii characters
    string = ''.join([i if ord(i) < 128 else ' ' for i in string])
    
    # upload the file as a text file
    with open("files.txt", "w") as file:
        file.write(string)
    with open("files.txt", "rb") as file:
        await interaction.response.send_message("Global files:", file=discord.File(file, "files.txt"))
    
    # delete the file
    os.remove("files.txt")

# load level - load a level
@tree.command(
    name="load_level",
    description="Load a level",
    guild=discord.Object(1134200376275513475)
)
async def load_level(interaction:discord.Interaction, level: str):
    # make sure the game isnt loading or paused
    emme.hook()
    if game.is_loading() or game.is_paused():
        emme.unhook()
        await interaction.response.send_message("The game is loading or paused, please wait.")
        return
    # if level doesnt have an extension, add .level
    if os.path.splitext(level)[1] == "":
        level += ".level"
    if os.path.split(level)[0] == "":
        level = os.path.join("Levels", level)
    level = level.replace("\\", "/")
    blacklisted_levels = [
        "Levels/AI_Test.level",
        "Levels/NPC_Test.level",
        "Levels/NPC_Test_2.level",
        "Levels/Main_Menu.level",
    ]
    for blacklisted_level in blacklisted_levels:
        if level.lower() == blacklisted_level.lower():
            await interaction.response.send_message(f"Could not load level `{level}` as it is blacklisted, either for missing assets or making the bot unhook from the game.")
            return
    files_in_memory = game.get_files()
    emme.unhook()
    # check if the level exists
    level_found = False
    for file in files_in_memory:
        if file.lower().endswith(f"{level.lower()}"):
            level_found = True
            break
    if not level_found:
        await interaction.response.send_message(f"Level not found: `{level}`")
        return
    emme.hook()
    lua_wrapper.clean_load_level(level)
    emme.unhook()
    await interaction.response.send_message(f"{interaction.user.mention} loaded a level: `{level}`")

# check if a movie is playing
@tree.command(
    name="movie_status",
    description="Check if a movie is playing",
    guild=discord.Object(1134200376275513475)
)
async def movie_status(interaction:discord.Interaction):
    emme.hook()
    status = game.is_movie_playing()
    emme.unhook()
    if status:
        await interaction.response.send_message("A movie is playing")
    else:
        await interaction.response.send_message("No movie is playing")

# get the cursor position
@tree.command(
    name="cursor_pos",
    description="Get the cursor position",
    guild=discord.Object(1134200376275513475)
)
async def cursor_pos(interaction:discord.Interaction):
    emme.hook()
    if game.is_loading() or game.is_paused() or game.is_in_cutscene():
        emme.unhook()
        await interaction.response.send_message("The game is loading, paused, or in a cutscene, please wait.")
        return
    cursor_pos = game.get_cursor_pos()
    emme.unhook()
    await interaction.response.send_message(f"Cursor position: {cursor_pos}")

# app to execute a message as a lua script
async def execute_lua_message(interaction:discord.Interaction, message: discord.Message):
    emme.hook()
    if game.is_loading() or game.is_paused() or game.is_in_cutscene():
        emme.unhook()
        await interaction.response.send_message("The game is loading, paused, or in a cutscene, please wait.")
        return
    message.content = ''.join([i if ord(i) < 128 else ' ' for i in message.content])
    snippet = message.content
    # if it begins with ```, remove that line
    lines = snippet.split("\n")
    if lines[0].startswith("```"):
        lines.pop(0)
    # if it ends with ```, remove that line
    if lines[-1].endswith("```"):
        lines.pop(-1)
    snippet = "\n".join(lines)
    snippet = snippet.replace("`", "")
    lua.execute_lua(snippet)
    emme.unhook()
    # link to the message
    await interaction.response.send_message(f"{interaction.user.mention} executed a lua script from message: {message.jump_url}")

execute_lua_message_context_menu = app_commands.ContextMenu(
    name="Execute as Lua",
    callback=execute_lua_message,
    guild_ids=[1134200376275513475]
)

# add the context menu
tree.add_command(execute_lua_message_context_menu)

client.run(token)