# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

class TwitchListener(irc.IRCClient):
	def __init__(self, nick, password):
		self.nickname = nick
		self.password = password
	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		print "TwitchListener connected"
	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		print "TwitchListener disconnected"
	#====
	def signedOn(self):
		self.join(self.factory.channel)
	def joined(self, channel):
		print "TwitchListener joined", self.factory.channel
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

#sets up the connection to the twisted reactor:
def Connect(host, port, channel, username, Oauth, SendTo):
	reactor.connectTCP(host, port, TwitchListenerFactory(channel, username, Oauth, SendTo))