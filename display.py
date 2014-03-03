import pygame, sys, time
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from twisted.internet import reactor

#set by Setup():
Main = None#the class in main.py
Settings = None#the class in main.py
Game = None#the class in game.py

#GameGlobals:
print "Initalizing pygame..."
pygame.init()
pygame.font.init()
pygame.display.set_caption("Twitch plays GBA")
Window = pygame.display.set_mode((427, 240))
Output = pygame.Surface((427, 240)).convert()

anarchyBG = pygame.image.load("graphics/anarchy.png").convert()
democracyBG = pygame.image.load("graphics/democracy.png").convert()
Commands = {}#loaded by Setup()

pIndicator = pygame.image.load("graphics/politics-indicator.png").convert_alpha()
pCurrent = pygame.image.load("graphics/current.png").convert_alpha()

prev = None#to see if a screen update is required

class Text():
	def __init__(self):
		global Settings
		self.Font = pygame.font.Font(Settings.font, 12)#make this support other filetypes as well
	def Create(self, String, Color=(255, 255, 255)):
		return self.Font.render(String, True, Color)
	def CreateShadowed(self, String, Color1=(16, 24, 32), Color2=(160, 160, 160)):
		size = self.Font.size(String)
		out = pygame.Surface((size[0]+1,size[1]+1)).convert_alpha()
		out.fill((0, 0, 0, 0))
		
		shadow = self.Font.render(String, True, Color2)
		out.blit(shadow, (0, 1))
		out.blit(shadow, (1, 0))
		out.blit(shadow, (1, 1))
		
		out.blit(self.Font.render(String, True, Color1), (0, 0))
		
		return out

def MakeTime():
	t = int(time.time() - Settings.epoch + 0.5)
	
	d = t / (60*60*24)
	t = t % (60*60*24)
	
	h = t / (60*60)
	t = t % (60*60)
	
	m = t / (60)
	
	s = t % (60)
	
	timestamp = "%id%ih%im%is" % (d, h, m, s)
	UTC = time.strftime("utc%M:%S")
	return timestamp, UTC

def MainLoop():#like the mainloop, but an event triggered by twisted instead
	global Main, Settings, Commands, prev
	global anarchyBG, democracyBG, pIndicator, pCurrent
	
	#Framerate
	#maybe not fixed?
	reactor.callLater(1.0/30.0, MainLoop)
	
	#update window frame:
	pygame.event.pump()
	Events = pygame.event.get()
	for i in Events:
		if i.type == QUIT:
			reactor.stop()
		if i.type == KEYDOWN:
			if i.key == K_ESCAPE:
				Game.ToggleActivity()
	
	#figure wether to update the frame or not:
	timestamp, UTC = MakeTime()
	if (Main.inputs, Main.command, timestamp) <> prev:
		prev = (Main.inputs[:], Main.command, timestamp)
		
		#blit BG:
		Output.blit(democracyBG if Settings.Mode else anarchyBG, (0, 0))
		
		#blit time:
		text = Text.CreateShadowed("%s   %s" % (timestamp, UTC), Settings.cTime1, Settings.cTime2)
		w = text.get_width() - 1
		Output.blit(text, (132-w/2, 37))
		
		#blit inputs:
		for i, (user, cmd) in enumerate(Main.inputs[-15 + (7*Settings.Mode):][::-1]):
			Output.blit(Text.Create(user, Settings.cInputs), (262, 223 - 12*i))
			Output.blit(Commands[cmd], (423-Commands[cmd].get_width(), 226 - 12*i))
		
		#blit democracy stuff:
		if Settings.Mode:
			if Main.dBuffer:
				for i, (cmd) in enumerate(sorted(Main.dBuffer.keys(), key=Main.dBuffer.get)[:6][::-1]):
					#Output.blit(Text.Create(cmd, Settings.cInputs), (262, 67 + 12*i))
					Output.blit(Commands[cmd], (264+8, 70 + 12*i))
					
					count = Text.Create(str(Main.dBuffer[cmd]), Settings.cInputs)
					Output.blit(count, (423-count.get_width() - 8, 67 + 12*i))
			if Main.command:
				x = (674 - Commands[Main.command].get_width()) / 2
				
				Output.blit(pCurrent, (x, 58))
				
				#Output.blit(Text.Create(Main.command, Settings.cInputs), (w+11, 55))
				Output.blit(Commands[Main.command], (x+13, 58))
			
		#blit politics bar indicator:
		Output.blit(pIndicator, (297 + Settings.Politics * 73 / Settings.pScale, 41))
		
		#update window:
		pygame.transform.scale(Output, Settings.size, Window)
		pygame.display.flip()

def Setup(main, settings, game):
	global Main, Settings, Game, Commands, Text, Window
	Main = main
	Settings = settings
	Game = game
	Text = Text()
	
	Window = pygame.display.set_mode(Settings.size)
	
	reactor.callLater(1.0/30.0, MainLoop)
	
	for i in Main.Commands:
		Commands[i] = pygame.image.load("graphics/cmd/%s.png" % i).convert_alpha()
	Commands["anarchy"] = pygame.image.load("graphics/cmd/anarchy.png").convert_alpha()
	Commands["democracy"] = pygame.image.load("graphics/cmd/democracy.png").convert_alpha()