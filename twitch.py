# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

class TwitchListener(irc.IRCClient):
	def __init__(self, nick, password):
		self.nickname = nick
		self.password = password
		
		self.listening = False
	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		print "TwitchListener connected to Twitch IRC server"
	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		print "TwitchListener disconnected from Twitch IRC"
		self.listening = False
		reactor.callLater(10,self.factory.Reconnect)
	def JoinChannel(self):
		if not self.listening:
			reactor.callLater(5, self.JoinChannel)
			self.join(self.factory.channel)
	#====
	def signedOn(self):
		print "TwitchListener successfully signed on to Twitch IRC"
		self.JoinChannel()
	def joined(self, channel):
		print "TwitchListener joined", self.factory.channel
		self.listening = True
	def kickedFrom(self, channel, kicker, message):
		print "TwitchListener kicked from", channel
		if channel == self.factory.channel:
			self.listening = False
			self.JoinChannel()
	def privmsg(self, user, channel, msg):
		user = user.split('!', 1)[0]
		self.factory.SendTo(user, msg)
	#def noticed(self, user, channel, msg):
	#	self.privmsg(user, channel, msg)
	def action(self, user, channel, msg):
		pass
	#	user = user.split('!', 1)[0]
	#	print "* %s %s" % (user, msg)
	def alterCollidedNick(self, nickname):
		return nickname + '_'

class TwitchListenerFactory(protocol.ClientFactory):
	def __init__(self, channel, username, Oauth, SendTo):
		self.channel = channel
		self.username = username
		self.Oauth = Oauth
		self.SendTo = SendTo
	def buildProtocol(self, addr):
		p = TwitchListener(self.username, self.Oauth)
		p.factory = self
		return p
	def clientConnectionLost(self, connector, reason):
		connector.connect()
	def clientConnectionFailed(self, connector, reason):
		print "connection failed:", reason
		reactor.callLater(10,self.Reconnect)
	def Reconnect(self):
		print "Reconnecting to Twitch IRC server..."
		reactor.connectTCP(self.host, self.port, self)

#sets up the connection to the twisted reactor:
def Connect(host, port, channel, username, Oauth, SendTo):
	f = TwitchListenerFactory(channel, username, Oauth, SendTo)
	f.host = host
	f.port = port
	reactor.connectTCP(host, port, f)