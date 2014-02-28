from twisted.internet import reactor
import twitch, game, display

username = "pbsds"
Oauth = "oauth:d3qyvzeesizeomoe6kuscz6gyzyhsdq"#can be generated at http://twitchapps.com/tmi/
channel = "twitchplayspokemon"
#channel = username

host = "199.9.252.26"
#host = "irc.twitch.tv"
port = 6667

class Main:
	def __init__(self):
		self.Commands = []#strings of the accepted commands, to be filled later in execution
		
		self.Mode = 0
		self.Politics = 250# <100 = anarchy and >=400 = democracy
		
		self.dBuffer = {}#democrachy
		self.inputs = []#the stdout of commands
		
		reactor.callLater(1.0, self.Step)
	def MSGRecieved(self, username, msg):
		msg = msg.lower()
		
		if msg in self.Commands:
			self.inputs.append((username, msg))
			
			if self.Mode == 0:#anarchy
				Game.Command(msg)
			else:
				dBuffer[msg] = dBuffer.get(msg, default=0) + 1
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
	def Step(self):#do stuff in democracy
		reactor.callLater(1.0, self.Step)
	
		#clean
		self.inputs = self.inputs[-30:]
		
Main = Main()

Game = game.Game(Main)
Main.Commands = Game.commands.keys()#now is later
twitch.Connect(host, port, channel, username, Oauth, Main.MSGRecieved)

display.Setup(Main)

reactor.run()