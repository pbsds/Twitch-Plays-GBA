from twisted.internet import reactor
from ConfigParser import ConfigParser
import twitch, game, display

class Settings:
	def __init__(self):
		print "Reading data.ini..."
		f = open("data.ini")
		ini = ConfigParser()
		ini.readfp(f)
		f.close()
		
		#Twitch:
		self.username = ini.get("twitch", "username")
		self.Oauth = ini.get("twitch", "oauth")#can be generated at http://twitchapps.com/tmi/
		self.channel = ini.get("twitch", "channel")
		
		self.host = "irc.twitch.tv" if not ini.has_option("twitch", "host") else ini.get("twitch", "host")
		self.port = 6667 if not ini.has_option("twitch", "port") else ini.getint("twitch", "port")
		
		#Politics:
		self.Mode = 1 * (ini.get("politics", "mode") == "democracy")
		self.Politics = ini.getint("politics", "votes")
		self.pScale = ini.getint("politics", "vote_scale")
		self.VotingTime = ini.getfloat("politics", "democracy_votingtime")
		
		#Style:
		self.scale = ini.getint("style", "render_scale")
		self.cInputs = ini.get("style", "inputs_color")[-6:]
		self.cInputs = (int(self.cInputs[:2], 16), int(self.cInputs[2:4], 16), int(self.cInputs[4:6], 16))
		self.font = ini.getint("style", "font")
		#self.
		
		self.epoch = time.gmtime() - ini.getint("time", "time")
		
		reactor.callLater(60*5, self.Save)
	def Save(self):
		reactor.callLater(60*5, self.Save)
		
		#store to ini
		ini.set("time", "time", str(time.gmtime() - self.epoch))
		pass
		
		#store to file
		pass
		
		pass#save game to savestate?

class Main:
	def __init__(self):
		global Settings
		
		self.Commands = []#strings of the accepted commands, to be filled later in execution
		
		self.inputs = []#the stdout of commands
		self.dBuffer = {}#democrachy
		self.command = None
		
		reactor.callLater(1.0, self.Step)
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
			if Settings.Politics < 100 and Settings.Mode == 1:
				print "Changed to Anarchy!"
				Settings.Mode = 0
		elif msg == "democracy":
			self.inputs.append((username, msg))
			if Settings.Politics < 499: Settings.Politics += 1
			if Settings.Politics >= 400 and Settings.Mode == 0:
				print "Changed to Democracy!"
				Settings.Mode = 1
				self.command = None
	def Step(self):#do stuff in democracy
		global Settings
		reactor.callLater(3.0, self.Step)
	
		#clean
		self.inputs = self.inputs[-30:]
		
		#democracy
		if Settings.Mode:
			self.command = max(self.dBuffer.keys(), key=self.dBuffer.get) if self.dBuffer.keys() else None
			self.dBuffer.clear()
			
			if self.command:
				Game.Command(self.command)

Settings = Settings()				
Main = Main()

Game = game.Game(Main)
Main.Commands = Game.commands.keys()#now is later
twitch.Connect(Settings.host, Settings.port, Settings.channel, Settings.username, Settings.Oauth, Main.MSGRecieved)

display.Setup(Main)

reactor.run()

print "Exiting..."
Settings.Save()