import win32api, win32con, win32com.client
from twisted.internet import reactor
import time

#Maybe save game to savestate every once in a while?

class Game:
	def __init__(self, Main, eTitle):
		self.Main = Main
		self.eTitle = eTitle
		self.wsh = win32com.client.Dispatch("WScript.Shell")
		self.on = True
		
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
	def activate(self):#to keep the window focused
		if self.on: 
			self.wsh.AppActivate(self.eTitle)
		reactor.callLater(5, self.activate)
	def save(self):#called by Settings in main.py
		if self.on:
			#self.wsh.AppActivate(self.eTitle)
			win32api.keybd_event(0x10, 0, 0, 0)#shift
			win32api.keybd_event(0x70, 0, 0, 0)#F1
			time.sleep(0.08)#or else it won't work on shutdown
			#self.wsh.AppActivate(self.eTitle)
			win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)#shift release
			win32api.keybd_event(0x70, 0, win32con.KEYEVENTF_KEYUP, 0)#F1 release
	def Command(self, cmd):
		if self.on:
			#self.wsh.AppActivate(self.eTitle)
			win32api.keybd_event(self.commands[cmd], 0, 0, 0)
			reactor.callLater(0.08, self._release, self.commands[cmd])
	def _release(self, VK):
		#self.wsh.AppActivate(self.eTitle)
		win32api.keybd_event(VK, 0, win32con.KEYEVENTF_KEYUP, 0)
	def ToggleActivity(self):
		self.on = not self.on
		print "Keypressing turned", "on!" if self.on else "off!"