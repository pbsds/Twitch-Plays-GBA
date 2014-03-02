Twitch Plays GBA - by pbsds
======

This currently only works on a windows enviroment.
pywin32, pygame and twisted is needed for this to work to run.

This program is released under the AGLP3 license, found in license.md.
An online copy can be found here: http://www.gnu.org/licenses/agpl-3.0.html

How to use:
- Sut up a python 2.7 enviroment and install pywin32, pygame and twisted
- Download the latest Visual Boy Advance and store it to vba/VisualBoyAdvance.exe
- Put the game you want to play in vba/game.gba.
- Edit the visuals in graphics/ and display.py as you may please
- Set the preferences you need in data.ini
- run run.bat
- Set up your preffered streaming program, and make VBA overlay "Twitch Plays GBA" at x36, y=204, w=720, h=480
- Stream

Streaming:
I reccomend using Open Broadcaster Software (OBS) because of its stability and lightweightness.
You could also try out FFSPLIT which is easier to set up, but i personally find it too unstable.
If you need help setting up your streaming program, i reccomend you head on over to http://help.twitch.tv/customer/portal/topics/358640-broadcast-hardware-and-software/articles

The fonts used: http://www.dafont.com/pokemon-ruby-sapphi.font