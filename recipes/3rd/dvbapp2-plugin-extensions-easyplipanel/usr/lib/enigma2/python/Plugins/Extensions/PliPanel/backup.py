# by 2boom 4bob@ua.fm 
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Label import Label
from Components.MenuList import MenuList
from Tools.Directories import fileExists
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ
import os
import gettext


lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("PliPanel", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/PliPanel/locale/"))

def _(txt):
	t = gettext.dgettext("PliPanel", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

TO_HDD = "/media/hdd/backupsettings"
TO_USB = "/media/usb/backupsettings"
#global DIRECT 
#DIRECT = " "
	
class BackupSuite(Screen):
	skin = """
		<screen name="backupsuite" position="center,160" size="750,370" title="Full 1:1 back-up in USB format on USB/HDD">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="toolpresent" render="Label" zPosition="2" position="25,250" size="700,25" font="Regular; 22" halign="center" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="710,203" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (120, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (130, 29), size = (680, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session

		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["Redkey"] = StaticText(_("Close"))
		self["toolpresent"] = StaticText(self.toolpresent())
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		backhddpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/bhdd.png"))
		backusbpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/busb.png"))
		backsetpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/bset.png"))
		self.list.append((_("Full back-up on USB/HDD"),"com_one", _("Full 1:1 back-up in USB format") + self.backupversion(), backhddpng))
		self.list.append((_("Full back-up to USB"),"com_two", _("Full 1:1 back-up in USB format") + self.backupversion(), backusbpng ))
		self.list.append((_("Back-up settings on HDD"),"com_tree", _("Back-up settings (sets, keys, boquets)"), backsetpng ))
		self.list.append((_("Back-up settings on USB"),"com_four", _("Back-up settings (sets, keys, boquets)"), backsetpng ))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "com_one":
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/BackupSuite-HDD/backup.sh"):
					self.session.open(Console, title = "Full back-up on HDD", cmdlist = [_("sh '/usr/lib/enigma2/python/Plugins/Extensions/BackupSuite-HDD/backup.sh' en_EN")])
				else:
					self.setupplugin()
				
			elif returnValue is "com_two":
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/BackupSuite-USB/backup.sh"):
					self.session.open(Console, title = "Full back-up on HDD", cmdlist = [_("sh '/usr/lib/enigma2/python/Plugins/Extensions/BackupSuite-USB/backup.sh' en_EN")])
				else:
					self.setupplugin()
					
			elif returnValue is "com_tree":
				#global DIRECT 
				#DIRECT = TO_HDD
				self.session.openWithCallback(self.mList,BackSett, TO_HDD)
			elif returnValue is "com_four":
				#global DIRECT 
				#DIRECT = TO_USB
				self.session.openWithCallback(self.mList,BackSett, TO_USB)
			else:
				print "\n[BackupSuite] cancel\n"
				self.close(None)

	def setupplugin(self):
		try:
			os.system("opkg update")
			os.system("opkg install enigma2-plugin-extensions-backupsuite")
			os.system("killall -9 enigma2")

		except:
			pass
			
	def backupversion(self):
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/BackupSuite-HDD/backup.sh"):
			ipklist = os.popen("opkg list-installed")
			for line in ipklist.readlines():
				dstring = line.split(" ")
				if line.find("backupsuite") != -1:
					try:
						return " - BackupSuite v.%s" % line[len(dstring[0]) + 2:]
					except:
						return " "
		else:
			i = _("Back-up suite not present, press OK for install it")
			return i
			ipklist.close()
			
	def toolpresent(self):
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/BackupSuite-HDD/backup.sh"):
			return " "
		else:
			i = _("Back-up suite not present, press OK for install it")
			return i
		
####################################################################
class BackSett(Screen):
	skin = """
		<screen name="backsetscreen1" position="center,160" size="750,370" title="Back-up settings on HDD/USB">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="red_key" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<widget source="green_key" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="340,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
	<widget source="yellow_key" render="Label" position="340,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="505,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/blue.png" alphatest="blend" />
	<widget source="blue_key" render="Label" position="505,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session, directpath):
		self.DIRECT = directpath
		self.session = session
		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.restorebkp,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.backupset,
			"yellow": self.restorebkp,
			"blue": self.removebkp,
		})
		self["red_key"] = StaticText(_("Close"))
		self["green_key"] = StaticText(_("BackUp"))
		self["yellow_key"] = StaticText(_("Restore"))
		self["blue_key"] = StaticText(_("Delete"))
		self.isbackupdir()
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def restorebkp(self):
		try:
			m_choice = self["menu"].getCurrent()[1]
			os.system("tar -C/ -xzpvf %s" % m_choice)
			self.mbox = self.session.open(MessageBox, "%s restored" % self.bkpfilename(), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox, "UnSuccesfull", MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def removebkp(self):
		try:
			m_choice = self["menu"].getCurrent()[1]
			os.system("rm %s" % m_choice)
			self.mbox = self.session.open(MessageBox, "%s removed" % self.bkpfilename(), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox, "UnSuccesfull", MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def backupset(self):
		try:
			os.system("tar czvf %s/%s.tar.gz /usr/keys/ /etc/enigma2/ /etc/tuxbox/ /etc/init.d/softcam.* /etc/init.d/cardserver.*" % ( self.DIRECT, self.bkpfilename()))
			self.mbox = self.session.open(MessageBox, "%s.tar.gz created" % self.bkpfilename(), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox, "UnSuccesfull", MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def isbackPossible(self):
		f = open("/proc/mounts", "r")
		for line in f:
			fields= line.rstrip('\n').split()
			if fields[1] == self.DIRECT[:-15]:
				if fields[2] == 'ext2' or fields[2] == 'ext3' or fields[2] == 'ext4' or fields[2] == 'fat32' or fields[2] == 'fat' or fields[2] == 'vfat':
					return 1
				else:
					return 0
		return 0
		f.close()
		
	def isbackupdir(self):
		if os.path.exists("%s" % self.DIRECT):
			return 1
		else:
			try:
				os.system("mkdir %s" % self.DIRECT)
			except:
				pass
		
	def bkpfilename(self):
		try:
			filename = os.popen("date").readline()
			fnamepart = filename.rstrip('\n').split()
			return "bkpsett_%s-%s-%s_%s%s" % (fnamepart[2], fnamepart[1], fnamepart[5], fnamepart[3].split(":")[0], fnamepart[3].split(":")[1])
			filename.close()
		except:
			pass
				
	def CfgMenu(self):
		self.list = []
		setpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/bsetmini.png"))
		if self.isbackPossible():
			try:
				bkpls = os.popen("ls %s/bkpsett*.tar.gz" % self.DIRECT)
				for line in bkpls:
					self.list.append((_("Back-up settings file"),line, (_("%s" )% (line[:-1])), setpng))
				bkpls.close()
			except:
				pass
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.restorebkp, "cancel": self.close}, -1)
			
	def exit(self):
		self.close()
##################################################################################################################
