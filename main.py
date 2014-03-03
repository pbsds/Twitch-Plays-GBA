from twisted.internet import reactor
from ConfigParser import ConfigParser
import time
import twitch, game, display

class Settings:
	def __init__(self):
		print "Reading data.ini..."
		f = open("data.ini")
		self.ini = ConfigParser()
		self.ini.readfp(f)
		f.close()
		
		#Twitch:
		self.username = self.ini.get("twitch", "username")
		self.Oauth = self.ini.get("twitch", "oauth")#can be generated at http://twitchapps.com/tmi/
		self.channel = self.ini.get("twitch", "channel")
		
		self.host = "irc.twitch.tv" if not self.ini.has_option("twitch", "host") else self.ini.get("twitch", "host")
		self.port = 6667 if not self.ini.has_option("twitch", "port") else self.ini.getint("twitch", "port")
		
		#Politics:
		self.Mode = 1 * (self.ini.get("politics", "mode") == "democracy")
		self.Politics = self.ini.getint("politics", "votes")
		self.pScale = self.ini.getint("politics", "vote_scale")
		self.VotingTime = self.ini.getfloat("politics", "democracy_votingtime")
		
		#Style:
		self.size = map(int, self.ini.get("style", "render_resolution").split("x"))
		self.cInputs = self.ini.get("style", "inputs_color")[-6:]
		self.cInputs = (int(self.cInputs[:2], 16), int(self.cInputs[2:4], 16), int(self.cInputs[4:6], 16))
		self.cTime1 = self.ini.get("style", "time_color")[-6:]
		self.cTime1 = (int(self.cTime1[:2], 16), int(self.cTime1[2:4], 16), int(self.cTime1[4:6], 16))
		self.cTime2 = self.ini.get("style", "time_color_shadow")[-6:]
		self.cTime2 = (int(self.cTime2[:2], 16), int(self.cTime2[2:4], 16), int(self.cTime2[4:6], 16))
		self.font = self.ini.get("style", "font")
		
		#time:
		self.epoch = time.time() - self.ini.getint("time", "time")
		
		#emulator
		self.eTitle = self.ini.get("emulator", "title")
		
		reactor.callLater(60*5, self.Save)
	def Save(self):
		reactor.callLater(60*5, self.Save)
		
		#store to self.ini
		self.ini.set("time", "time", str(int(time.time() - self.epoch)))
		self.ini.set("politics", "mode", "democracy" if self.Mode else "anarchy")
		self.ini.set("politics", "votes", str(self.Politics))
		
		#make savestate:
		Game.save()
		
		#store to file
		f = open("data.ini", "w")
		self.ini.write(f)
		f.close()

class Main:
	def __init__(self):
		global Settings
		
		self.Commands = []#strings of the accepted commands, to be filled later in execution
		
		self.inputs = []#the stdout of commands
		self.dBuffer = {}#democrachy
		self.command = None
		
		reactor.callLater(0.5, self.Step)
	def MSGRecieved(self, username, msg):
		global Settings
		msg = msg.lower()
		
		if msg in self.Commands:
			self.inputs.append((username, msg))
			
			if Settings.Mode == 0:#anarchy
				Game.Command(msg)
			else:
				self.dBuffer[msg] = self.dBuffer.get(msg, 0) + 1
		elif msg == "anarchy":
			self.inputs.append((username, msg))
			if Settings.Politics > 0: Settings.Politics -= 1
			if Settings.Politics < Settings.pScale/5 and Settings.Mode == 1:
				print "Changed to Anarchy!"
				Settings.Mode = 0
		elif msg == "democracy":
			self.inputs.append((username, msg))
			if Settings.Politics < Settings.pScale-1: Settings.Politics += 1
			if Settings.Politics >= Settings.pScale*4/5 and Settings.Mode == 0:
				print "Changed to Democracy!"
				Settings.Mode = 1
				self.command = None
	def Step(self):#do stuff in democracy
		global Settings
		reactor.callLater(Settings.VotingTime, self.Step)
	
		#clean
		self.inputs = self.inputs[-20:]
		
		#democracy
		if Settings.Mode:
			self.command = max(self.dBuffer.keys(), key=self.dBuffer.get) if self.dBuffer.keys() else None
			self.dBuffer.clear()
			
			if self.command:
				Game.Command(self.command)

Settings = Settings()
Main = Main()

Game = game.Game(Main, Settings.eTitle)
Main.Commands = Game.commands.keys()#now is later
twitch.Connect(Settings.host, Settings.port, Settings.channel, Settings.username, Settings.Oauth, Main.MSGRecieved)

display.Setup(Main, Settings, Game)

reactor.run()

print "Exiting..."
Settings.Save()