import win32api, win32con, win32com.client
from twisted.internet import reactor

#Maybe save game to savestate every once in a while?

class Game:
	def __init__(self, Main):
		self.Main = Main
		self.wsh = win32com.client.Dispatch("WScript.Shell")
		
		self.commands = {}#self.commands[chat input] = "button to press"
		
		#read commands:
		f = open("vba/keyconfig.txt", "r")
		for i in f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n"):
			if i:
				if "=" in i:
					key, data = i.split("=")[:2]
					#self.commands[key] = data
					self.commands[key] = ord(data.upper())
		f.close()
		
		self.activate()
	def activate(self):#to keep the window focused during inactivity
		self.wsh.AppActivate("VisualBoyAdvance")
		reactor.callLater(5, self.activate)
	def Command(self, cmd):
		self.wsh.AppActivate("VisualBoyAdvance")
		win32api.keybd_event(self.commands[cmd], 0, 0, 0)
		reactor.callLater(0.08, self._release, cmd)
	def _release(self, cmd):
		win32api.keybd_event(self.commands[cmd], 0, win32con.KEYEVENTF_KEYUP, 0)
		