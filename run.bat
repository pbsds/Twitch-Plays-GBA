REM This is only used to make sure FFSPLIT use the pygame window instead of the terminal window, and start the emulator
REM But remember to uncheck the "pause when inactive" in the emulator, as it's not stored in the config

start vba/VisualBoyAdvanceM.exe vba/game.gba
python main.py