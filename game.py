import win32com.client as comclt
import win32api, win32con
from twisted.internet import reactor

class Game:
	
	def __init__(self, Main):
		self.Main = Main
		self.wsh = comclt.Dispatch("WScript.Shell")
		
		self.commands = {}#self.commands[chat input] = "button to press"
		
		#read commands:
		f = open("keyconfig.txt", "r")
		for i in f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n"):
			if i:
				if "=" in i:
					key, data = i.split("=")[:2]
					#self.commands[key] = data
					self.commands[key] = ord(data.upper())
		f.close()
		self.activate()
	def activate(self):
		self.wsh.AppActivate("VisualBoyAdvance")
		reactor.callLater(5, self.activate)
	def Command(self, cmd):
		self.wsh.AppActivate("VisualBoyAdvance")
		win32api.keybd_event(self.commands[cmd], 0, 0, 0)
		reactor.callLater(0.08, self._release, cmd)
	def _release(self, cmd):
		win32api.keybd_event(self.commands[cmd], 0, win32con.KEYEVENTF_KEYUP, 0)
		