# EpicMickeyMemoryEngine
 A Python library for manipulating Epic Mickey (1) while the game is running.

## Installation

Replace the _Dynamic.pak and globalscripts.pak files in the packfiles folder of your Epic Mickey installation with the ones provided in the root of this repository. Next, add the following to the beginning of ConfigFiles.ini (or ConfigOverride.ini):

```ini
LuaToExecute=.
LuaOut=.
```

Then, hook into the game using the provided Python library and you're good to go!