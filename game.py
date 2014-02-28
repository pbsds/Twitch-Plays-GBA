import win32com.client as comclt

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
					self.commands[key] = data
		f.close()
	def Command(self, cmd):
		#self.wsh.SendKeys(self.commands[cmd])
		pass