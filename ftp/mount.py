from otautil import *

class Mount:
	'sudo mount -t cifs -o ro,username=xuzhaoyou,password=mobile#3 //192.168.8.206/data/data server'
	def __init__(self,localdir,server,username,password):
		self.server=server
		self.localdir=localdir
		self.username=username
		self.password=password

	def doMount(self):
		assert(self.server is not None)
		assert(self.localdir is not None)
		assert(self.username is not None)
		assert(self.password is not None)
		_,recode=runCommand("sudo mount -t cifs -o ro,username="+self.username+",password=" + self.password + " " + self.server + " " + self.localdir)
		if recode == 0:
			return True
		else:
			return False