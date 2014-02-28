import pygame, sys
from pygame.locals import *#do i need this?
from twisted.internet import reactor

#set by Setup():
Main = None#the main class

#GameGlobals:
print "Initalizing pygame..."
pygame.init()
pygame.font.init()
pygame.display.set_caption("Twitch plays GBA")
#Output = pygame.display.set_mode((427,240))
Window = pygame.display.set_mode((1280,720))
Output = pygame.Surface((427, 240)).convert()

anarchyBG = pygame.image.load("graphics/anarchy.png").convert()
democracyBG = pygame.image.load("graphics/democracy.png").convert()
Commands = {}#loaded by Setup()

pIndicator = pygame.image.load("graphics/politics-indicator.png").convert_alpha()
pCurrent = pygame.image.load("graphics/current.png").convert_alpha()

prev = None#to see if a screen update is required

#make colors load from config file!
class Text():
	def __init__(self):
		self.Font = pygame.font.Font("graphics/font.fon", 12)#make this support other filetypes as well
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
Text = Text()

def MainLoop():#like the mainloop, but an event triggered by twisted instead
	global Main, Commands, prev
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
	
	#figure wether to update the frame or not:
	if Main.inputs <> prev:
		prev = Main.inputs[:]
		
		Output.blit(democracyBG if Main.Mode else anarchyBG, (0, 0))
		
		#blit time
		
		
		#blit inputs
		for i, (user, cmd) in enumerate(Main.inputs[-15 + (7*Main.Mode):][::-1]):
			Output.blit(Text.Create(user), (262, 223 - 12*i))
			Output.blit(Commands[cmd], (423-Commands[cmd].get_width(), 226 - 12*i))
			
		#blit democracy stuff
		if Main.dBuffer:
			for i, (cmd) in enumerate(sorted(Main.dBuffer.keys(), key=Main.dBuffer.get)[:6][::-1]):
				#Output.blit(Text.Create(cmd), (262, 67 + 12*i))
				Output.blit(Commands[cmd], (264+8, 70 + 12*i))
				
				count = Text.Create(str(Main.dBuffer[cmd]))
				Output.blit(count, (423-count.get_width() - 8, 67 + 12*i))
		if Main.command:
			w = (674 - Commands[Main.command].get_width()) / 2
			
			Output.blit(pCurrent, (w, 58))
			
			#Output.blit(Text.Create(Main.command), (w+11, 55))
			Output.blit(Commands[Main.command], (w+13, 58))
			
		#blit politics bar
		Output.blit(pIndicator, (297 + Main.Politics * 73 / 500, 41))
		
		#update screen:
		pygame.transform.scale(Output, (1280, 720), Window)
		pygame.display.flip()

def Setup(main):
	global Main, Commands
	reactor.callLater(1.0/30.0, MainLoop)
	Main = main
	for i in Main.Commands:
		Commands[i] = pygame.image.load("graphics/cmd/%s.png" % i).convert_alpha()
	Commands["anarchy"] = pygame.image.load("graphics/cmd/anarchy.png").convert_alpha()
	Commands["democracy"] = pygame.image.load("graphics/cmd/democracy.png").convert_alpha()