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
Window = pygame.display.set_mode((427,240))

anarchyBG = pygame.image.load("graphics/anarchy.png").convert()
#democracyBG = pygame.image.load("graphics/democracy.png").convert()
democracyBG = pygame.image.load("graphics/anarchy.png").convert()
Commands = {}#loaded by Setup()


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
	global Main, anarchyBG, democracyBG, Commands
	
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
	if 1 == 1:#huehuehue
		Window.blit(democracyBG if Main.Mode else anarchyBG, (0, 0))
		
		#blit time
		
		#blit inputs
		for i, (user, cmd) in enumerate(Main.inputs[-15:][::-1]):
			Window.blit(Text.Create(user), (264, 223 - 12*i))
			
			Window.blit(Commands[cmd], (423-Commands[cmd].get_width(), 225 - 12*i))
			
		
		#blit democrachy stuff
		
		
		#blit politics bar
		Main.Politics
		
		pygame.display.flip()

def Setup(main):
	global Main, Commands
	reactor.callLater(1, MainLoop)
	Main = main
	for i in Main.Commands:
		Commands[i] = pygame.image.load("graphics/cmd/%s.png" % i).convert_alpha()
	Commands["anarchy"] = pygame.image.load("graphics/cmd/anarchy.png").convert_alpha()
	Commands["democracy"] = pygame.image.load("graphics/cmd/democracy.png").convert_alpha()