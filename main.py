from twisted.internet import reactor
import twitch, game, display

#todo: make these values be read from config file

username = "pbsds"
Oauth = "oauth:123456789"#can be generated at http://twitchapps.com/tmi/
channel = "twitchplayspokemon"
#channel = username

#host = "irc.twitch.tv"
host = "199.9.252.26"
port = 6667

class Main:
	def __init__(self):
		self.Commands = []#strings of the accepted commands, to be filled later in execution
		
		self.Mode = 0
		self.Politics = 350# <100 = anarchy and >=400 = democracy
		#self.Politics = 250# <100 = anarchy and >=400 = democracy
		
		self.inputs = []#the stdout of commands
		self.dBuffer = {}#democrachy
		self.command = None
		
		reactor.callLater(1.0, self.Step)
	def MSGRecieved(self, username, msg):
		msg = msg.lower()
		
		if msg in self.Commands:
			self.inputs.append((username, msg))
			
			if self.Mode == 0:#anarchy
				Game.Command(msg)
			else:
				self.dBuffer[msg] = self.dBuffer.get(msg, 0) + 1
		elif msg == "anarchy":
			self.inputs.append((username, msg))
			if self.Politics > 0: self.Politics -= 1
			if self.Politics < 100 and self.Mode == 1:
				print "Changed to Anarchy!"
				self.Mode = 0
		elif msg == "democracy":
			self.inputs.append((username, msg))
			if self.Politics < 499: self.Politics += 1
			if self.Politics >= 400 and self.Mode == 0:
				print "Changed to Democracy!"
				self.Mode = 1
				self.command = None
	def Step(self):#do stuff in democracy
		reactor.callLater(3.0, self.Step)
	
		#clean
		self.inputs = self.inputs[-30:]
		
		#democracy
		if self.Mode:
			self.command = max(self.dBuffer.keys(), key=self.dBuffer.get) if self.dBuffer.keys() else None
			self.dBuffer.clear()
			
			if self.command:
				Game.Command(self.command)
		
Main = Main()

Game = game.Game(Main)
Main.Commands = Game.commands.keys()#now is later
twitch.Connect(host, port, channel, username, Oauth, Main.MSGRecieved)

display.Setup(Main)

reactor.run()