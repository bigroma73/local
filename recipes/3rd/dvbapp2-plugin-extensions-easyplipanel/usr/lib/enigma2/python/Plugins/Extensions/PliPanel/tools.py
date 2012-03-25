# by 2boom 4bob@ua.fm 2011-12
# swap on hdd by bigroma, scriptexecuter  by AliAbdul
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigSelection, ConfigSubsection, ConfigYesNo
from Components.ConfigList import ConfigListScreen
from Components.Harddisk import harddiskmanager
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Components.ScrollLabel import ScrollLabel
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigSelection, ConfigSubsection, ConfigYesNo
from Components.ConfigList import ConfigListScreen
from os import environ
import os
import gettext

global swapfile
swapfile = "/media/hdd/swapfile"
global Crashfile 
Crashfile = "21 "

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
######################################################################
config.plugins.CronMan = ConfigSubsection()
config.plugins.CronMan.min = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("5", "5"),
		("10", "10"),
		("15", "15"),
		("20", "20"),
		("25", "25"),
		("30", "30"),
		("35", "35"),
		("40", "40"),
		("45", "45"),
		("50", "50"),
		("55", "55"),
		])
config.plugins.CronMan.hour = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("0", "0"),
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
		("9", "9"),
		("10", "10"),
		("11", "11"),
		("12", "12"),
		("13", "13"),
		("14", "14"),
		("15", "15"),
		("16", "16"),
		("17", "17"),
		("18", "18"),
		("19", "19"),
		("20", "20"),
		("21", "21"),
		("22", "22"),
		("23", "23"),
		])
config.plugins.CronMan.dayofmonth = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
		("9", "9"),
		("10", "10"),
		("11", "11"),
		("12", "12"),
		("13", "13"),
		("14", "14"),
		("15", "15"),
		("16", "16"),
		("17", "17"),
		("18", "18"),
		("19", "19"),
		("20", "20"),
		("21", "21"),
		("22", "22"),
		("23", "23"),
		("24", "24"),
		("25", "25"),
		("26", "26"),
		("27", "27"),
		("28", "28"),
		("29", "29"),
		("30", "30"),
		("31", "31"),
		])
config.plugins.CronMan.month = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("1", _("Jan.")),
		("2", _("Feb.")),
		("3", _("Mar.")),
		("4", _("Apr.")),
		("5", _("May")),
		("6", _("Jun.")),
		("7", _("Jul")),
		("8", _("Aug.")),
		("9", _("Sep.")),
		("10", _("Oct.")),
		("11", _("Nov.")),
		("12", _("Dec.")),
		])
config.plugins.CronMan.dayofweek = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("0", _("Su")),
		("1", _("Mo")),
		("2", _("Tu")),
		("3", _("We")),
		("4", _("Th")),
		("5", _("Fr")),
		("6", _("Sa")),
		])
config.plugins.CronMan.command = ConfigText(default="/usr/bin/", visible_width = 70, fixed_size = False)
config.plugins.CronMan.every = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Min")),
		("2", _("Hour")),
		("3", _("Day of month")),
		("4", _("Month")),
		("5", _("Day of week")),
		])
#####################################################################
######################################################################################
config.plugins.TimeUdp = ConfigSubsection()
config.plugins.TimeUdp.onoff = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
config.plugins.TimeUdp.time = ConfigSelection(default = "30", choices = [
		("30", _("30 min")),
		("1", _("60 min")),
		("2", _("120 min")),
		("3", _("180 min")),
		("4", _("240 min")),
		])
config.plugins.TimeUdp.TransponderTime = ConfigSelection(default = "0", choices = [
		("0", _("Off")),
		("1", _("On")),
		])
config.plugins.TimeUdp.cold = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
######################################################################################
class ToolsScreen(Screen):
	skin = """
		<screen name="toolscreen" position="center,160" size="750,370" title="Service Tools">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Greenkey" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />

	<widget source="menu" render="Listbox" position="15,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (120, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (130, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
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
			"green": self.GreenKey,
		})
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("HDD sleep"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/crash.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/info2.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/sat.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/unusb.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/script.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/ntp.png"))
		self.list.append((_("Crashlog viewer"),"com_one", _("view & remove crashlog files"), onepng ))
		self.list.append((_("System info"),"com_two", _("system info (free, dh -f)"), twopng ))
		self.list.append((_("Satellites.xml Downloader"),"com_tree", _("Download Satellites.xml from internet"), treepng ))
		self.list.append((_("Synchronization NTP"),"com_six", _("Synchronization ntp every 30 min,60 min,120 min, 240 min and Now"), sixpng ))
		self.list.append((_("UnMount USB"),"com_four", _("Unmount usb devices"), fourpng ))
		self.list.append((_("User Scripts"),"com_five", _("Start scripts from /usr/script"), fivepng ))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()
		
	def GreenKey(self):
		ishdd = os.popen("cat /proc/mounts")
		for line in ishdd:
			if line.find("/media/hdd") > -1:
				mountpointname = line.split(" ")
				os.system("hdparm -y %s" % (mountpointname[0]))
				self.mbox = self.session.open(MessageBox,_("HDD go sleep"), MessageBox.TYPE_INFO, timeout = 4 )

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "com_one":
				self.session.openWithCallback(self.mList,CrashLogScreen)
			elif returnValue is "com_two":
				self.session.openWithCallback(self.mList,Info2Screen)
			elif returnValue is "com_tree":
				self.session.openWithCallback(self.mList,DownScreen2)
			elif returnValue is "com_four":
				self.session.openWithCallback(self.mList,UsbScreen)
			elif returnValue is "com_five":
				self.session.openWithCallback(self.mList, ScriptScreen)
			elif returnValue is "com_six":
				self.session.openWithCallback(self.mList, NTPScreen)
			else:
				print "\n[BackupSuite] cancel\n"
				self.close(None)
###############################################################################
class ServiceMan(Screen):
	skin = """
<screen name="Serviceman" position="center,160" size="750,370" title="Service Manager">

	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_yellow" render="Label" position="360,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (10, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 29
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "DirectionActions"],

		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.stopservice,
			"green": self.startservice,
			"yellow": self.restartservice,
		})
		self["key_red"] = StaticText(_("Stop"))
		self["key_green"] = StaticText(_("Start"))
		self["key_yellow"] = StaticText(_("ReStart"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		self.list.append((_("Manage Networking service"), "networking"))
		self.list.append((_("Manage Ftp service"), "vsftpd"))
		self.list.append((_("Manage Internet superserver (inetd)"), "inetd"))
		self.list.append((_("Manage Samba service"), "samba"))
		self.list.append((_("Manage Syslog/klogd service"), "syslog"))
		self.list.append((_("Manage Dropbear SSH service"), "dropbear"))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"cancel": self.close}, -1)

	def restartservice(self):
		try:
			os.system("/etc/init.d/%s restart" % (self["menu"].getCurrent()[1]))
			self.session.open(MessageBox, _("Restarting %s service" % self["menu"].getCurrent()[1]), type = MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.session.open(MessageBox, _("UnSuccessfull") , type = MessageBox.TYPE_INFO, timeout = 4 )
			
	def startservice(self):
		try:
			os.system("/etc/init.d/%s start" % (self["menu"].getCurrent()[1]))
			self.session.open(MessageBox, _("Starting %s service" % self["menu"].getCurrent()[1]), type = MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.session.open(MessageBox, _("UnSuccessfull"), type = MessageBox.TYPE_INFO, timeout = 4 )
			
	def stopservice(self):
		try:
			os.system("/etc/init.d/%s stop" % (self["menu"].getCurrent()[1]))
			self.session.open(MessageBox, _("Stoping %s service" % self["menu"].getCurrent()[1]), type = MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.session.open(MessageBox, _("UnSuccessfull"), type = MessageBox.TYPE_INFO, timeout = 4 )
			
	def cancel(self):
		self.close()
####################################################################
class SwapScreen(Screen):
	skin = """
		<screen name="swapscreen" position="center,160" size="750,370" title="Swap on USB/HDD">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
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

	def __init__(self, session, swapdirect):
		self.swapfile = swapdirect
		self.session = session
		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.CfgMenuDo,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["Redkey"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()

	def isSwapPossible(self):
		f = open("/proc/mounts", "r")
		for line in f:
			fields= line.rstrip('\n').split()
			if fields[1] == "%s" % self.swapfile[:10]:
				if fields[2] == 'ext2' or fields[2] == 'ext3' or fields[2] == 'ext4' or fields[2] == 'vfat':
					return 1
				else:
					return 0
		return 0
		
	def isSwapRun(self):
		try:
			f=os.popen('cat /proc/swaps')
			for line in f:
				if line.find(self.swapfile) > -1:
					return 1
			return 0
		except:
			pass
			
	def isSwapSize(self):
		try:
			f = os.popen('ls -lh %s/swapfile*' % self.swapfile[:10])
			for line in f:
				if line.find("%s/swapfile" % self.swapfile[:10]) > - 1:
					return line.split()[4]
		except:
			pass
			
	def makeSwapFile(self, size):
		try:
			os.system("dd if=/dev/zero of=%s bs=1024 count=%s" % (self.swapfile, size))
			os.system("mkswap %s" % (self.swapfile))
			self.mbox = self.session.open(MessageBox,_("Swap file created"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		except:
			pass
	
	def CfgMenu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/swapminion.png"))
		if self.isSwapPossible():
			if os.path.exists(self.swapfile):
				if self.isSwapRun() == 1:
					self.list.append((_("Swap off"),"5", (_("Swap on %s off (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minisonpng))
				else:
					self.list.append((_("Swap on"),"4", (_("Swap on %s on (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
					self.list.append((_("Remove swap"),"7",( _("Remove swap on %s (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
			else:
				self.list.append((_("Make swap"),"11", _("Make swap on %s (128MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"12", _("Make swap on %s (256MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"13", _("Make swap on %s (512MB)") % self.swapfile[7:10].upper(), minispng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.CfgMenuDo, "cancel": self.close}, -1)
			
	def CfgMenuDo(self):
		m_choice = self["menu"].getCurrent()[1]
		if m_choice is "4":
			try:
				runname = os.popen("cat /proc/swaps | grep swapfile")
				for line in runname:
					if  line.find("swapfile") > -1:
						os.system("swapoff %s" % (line.split()[0]))
				runname.close()
			except:
				pass
			os.system("swapon %s" % (self.swapfile))
			os.system("sed -i '/swap/d' /etc/fstab")
			os.system("echo -e '%s/swapfile swap swap defaults 0 0' >> /etc/fstab" % self.swapfile[:10])
			self.mbox = self.session.open(MessageBox,_("Swap file started"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		elif m_choice is "5":
			os.system("swapoff %s" % (self.swapfile))
			os.system("sed -i '/swap/d' /etc/fstab")
			self.mbox = self.session.open(MessageBox,_("Swap file stoped"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		elif m_choice is "11":
			self.makeSwapFile("131072")

		elif m_choice is "12":
			self.makeSwapFile("262144")

		elif m_choice is "13":
			self.makeSwapFile("524288")

		elif m_choice is "7":
			os.system("rm %s" % (self.swapfile))
			self.mbox = self.session.open(MessageBox,_("Swap file removed"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
			
	def exit(self):
		self.close()
####################################################################
class UsbScreen(Screen):
	skin = """
<screen name="unmountrgscreen" position="center,160" size="750,370" title="Unmount manager">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_yellow" render="Label" position="360,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 2), # index 4 is the pixmap
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
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.CfgMenu,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnMount"))
		self["key_yellow"] = StaticText(_("reFresh"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/usbico.png"))
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				hdd = hddlist[count][1]
				devpnt = self.devpoint(hdd.mountDevice())
				if hdd.mountDevice() != '/media/hdd':
					if devpnt != None:
						if int(hdd.free()) > 1024:
							self.list.append(("%s" % hdd.model(),"%s  %s  %s (%d.%03d GB free)" % (devpnt, self.filesystem(hdd.mountDevice()),hdd.capacity(), hdd.free()/1024 , hdd.free()%1024 ), minipng, devpnt))
						else:
							self.list.append(("%s" % hdd.model(),"%s  %s  %s (%03d MB free)" % (devpnt, self.filesystem(hdd.mountDevice()), hdd.capacity(),hdd.free()), minipng, devpnt))
		else:
			hddinfo = _("none")
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		try:
			item = self["menu"].getCurrent()[3]
			os.system("umount -f %s" % item)
			self.mbox = self.session.open(MessageBox,_("Unmounted %s" % item), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			pass
			#self.mbox = self.session.open(MessageBox,_("Unmounted %s Unsucessfull" % item), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def filesystem(self, mountpoint):
		try:
			fsystem = os.popen("cat /proc/mounts | grep %s" % mountpoint).readline()
			list = fsystem.split()
			return "%s  %s" % (list[2], list[3][:2])
		except:
			pass
			
	def devpoint(self, mountpoint):
		try:
			dsystem = os.popen("df -h | grep %s" % mountpoint).readline()
			list = dsystem.split()
			return list[0]
		except:
			pass
			
	def hddpresent(self):
		try:
			hddpr = os.popen("df -h | grep /media/hdd").readline()
			if hddpr.split()[-1] == "/media/hdd":
				return 1
			else:
				return 0
		except:
			pass
			
	def exit(self):
		self.close()
		
####################################################################
class ScriptScreen(Screen):
	skin = """
	<screen position="center,160" size="750,370" title="Script Executer" >
		<widget name="list" position="20,10" size="710,305" scrollbarMode="showOnDemand" />
		<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
		<widget source="Redkey" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		
		try:
			list = os.listdir("/usr/script")
			list = [x[:-3] for x in list if x.endswith('.sh')]
		except:
			list = []
		self["list"] = MenuList(list)
		self["Redkey"] = StaticText(_("Close"))
		self["actions"] = ActionMap(["OkCancelActions","ColorActions"], {"ok": self.run, "red": self.exit, "cancel": self.close}, -1)

	def run(self):
		script = self["list"].getCurrent()
		if script is not None:
			name = ("/usr/script/%s.sh" % script)
			os.chmod(name, 0755)
			self.session.open(Console, script.replace("_", " "), cmdlist=[name])
	
	def exit(self):
		self.close()
########################################################################
class NTPScreen(ConfigListScreen, Screen):
	skin = """
<screen name="TimeUpdater" position="center,160" size="750,370" title="NtpTime Updater">
		<widget position="15,10" size="720,200" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
		<widget source="red_key" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
		<widget source="green_key" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="340,358" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
		<widget source="yellow_key" render="Label" position="340,328" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.list = []
		self.list.append(getConfigListEntry(_("NtpTime Updater"), config.plugins.TimeUdp.onoff))
		self.list.append(getConfigListEntry(_("Set time to update"), config.plugins.TimeUdp.time))
		self.list.append(getConfigListEntry(_("Set Transponder time update"), config.plugins.TimeUdp.TransponderTime))
		self.list.append(getConfigListEntry(_("Cold start synchronization"), config.plugins.TimeUdp.cold))
		ConfigListScreen.__init__(self, self.list)
		self["red_key"] = StaticText(_("Close"))
		self["green_key"] = StaticText(_("OK"))
		self["yellow_key"] = StaticText(_("Update Now"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.UpdateNow,
			"ok": self.save
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
	
	def save(self):
		path = "/etc/cron/crontabs/root"
		if config.plugins.TimeUdp.onoff.value == "0":
			if fileExists(path):
				os.system("sed -i '/pool.ntp.org/d' %s" % path)
		if config.plugins.TimeUdp.onoff.value == "1":
			if fileExists(path):
				os.system("sed -i '/pool.ntp.org/d' %s" % path)
			if config.plugins.TimeUdp.time.value == "30":
				os.system("echo -e '/%s * * * *    /usr/bin/ntpdate -b -s -u pool.ntp.org' >> %s" % (config.plugins.TimeUdp.time.value, path))
			else:
				os.system("echo -e '* /%s * * *    /usr/bin/ntpdate -b -s -u pool.ntp.org' >> %s" % (config.plugins.TimeUdp.time.value, path))
		if fileExists(path):
			os.chmod("%s" % path, 0644)
		if config.plugins.TimeUdp.TransponderTime.value == "0": 
			config.misc.useTransponderTime.value = False
			config.misc.useTransponderTime.save()
		else:
			config.misc.useTransponderTime.value = True
			config.misc.useTransponderTime.save()
		if config.plugins.TimeUdp.cold.value == "0":
			if fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.system("rm /etc/rcS.d/S42ntpdate.sh")
		else:
			if not fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.system("echo -e '#!/bin/sh\n\n[ -x /usr/bin/ntpdate ] && /usr/bin/ntpdate -b -s -u pool.ntp.org\n\nexit 0' >> /etc/rcS.d/S42ntpdate.sh")
			if fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.chmod("/etc/rcS.d/S42ntpdate.sh", 0755)
		for i in self["config"].list:
			i[1].save()
		self.close()
			
	def UpdateNow(self):
		os.system("/usr/bin/ntpdate -b -s -u pool.ntp.org")
		self.mbox = self.session.open(MessageBox,_("Synchronized"), MessageBox.TYPE_INFO, timeout = 4 )
####################################################################
class SystemScreen(Screen):
	skin = """
		<screen name="systemtools" position="center,160" size="750,370" title="System Tools">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (120, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (130, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
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
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/kernel.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/serviceman.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/swap.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/cron.png"))
		self.list.append((_("Kernel Modules Manager"),"com_one", _("load & unload kernel modules"), onepng))
		self.list.append((_("Service Manager"),"com_two", _("Start, Stop, Restart system services"), twopng))
		self.list.append((_("Cron Manager"),"com_five", _("Is a time-based job scheduler"), fivepng))
		self.list.append((_("Manage Swap"),"com_four", _("Start, Stop, Create, Remove Swap file on HDD"), fourpng ))
		self.list.append((_("Manage Swap"),"com_tree", _("Start, Stop, Create, Remove Swap file on USB"), fourpng ))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "com_one":
				self.session.openWithCallback(self.mList,KernelScreen)
			elif returnValue is "com_two":
				self.session.openWithCallback(self.mList,ServiceMan)
			elif returnValue is "com_four":
				global swapfile
				self.session.openWithCallback(self.mList,SwapScreen, "/media/hdd/swapfile")
			elif returnValue is "com_tree":
				global swapfile
				self.session.openWithCallback(self.mList,SwapScreen, "/media/usb/swapfile")
			elif returnValue is "com_five":
				self.session.openWithCallback(self.mList,CrontabMan)
			else:
				print "\n[BackupSuite] cancel\n"
				self.close(None)
###############################################################################
class KernelScreen(Screen):
	skin = """
<screen name="kernelscreen" position="center,100" size="750,570" title="Kernel Modules Manager">
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,528" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Greenkey" render="Label" position="185,528" zPosition="2" size="210,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,558" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<ePixmap position="390,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="Yellowkey" render="Label" position="390,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="Bluekey" render="Label" position="560,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="560,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/blue.png" transparent="1" alphatest="on" />
	<widget source="menu" render="Listbox" position="20,10" size="710,500" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
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
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
		})
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("Load/UnLoad"))
		self["Yellowkey"] = StaticText(_("LsMod"))
		self["Bluekey"] = StaticText(_("Reboot"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def BlueKey(self):
		os.system("reboot")
		
	def YellowKey(self):
		self.session.openWithCallback(self.CfgMenu,lsmodScreen)
		
	def IsRunnigModDig(self, what):
		modrun = os.popen ("lsmod | grep %s" % (what[:-4]))
		for line in modrun:
			if line.find(what[:-4]) > -1:
				return 1
				break
		return 0
		
	def CfgMenu(self):
		self.list = []
		DvrName = os.popen("modprobe -l -t drivers")
		for line in DvrName:
			kernDrv = line.split("/")
			if self.IsRunnigModDig(kernDrv[-1]) == 1:
				minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/kernelminimem.png"))
				self.list.append((kernDrv[-1],line,minipng, "1"))
			else:
				minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/kernelmini.png"))
				self.list.append((kernDrv[-1],line,minipng, "0"))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.Ok, "cancel": self.close}, -1)

	def Ok(self):
		item = self["menu"].getCurrent()
		isrunning = item[3]
		nlist = item[0]
		if item[3] == "0":
			os.system(("modprobe %s" % (nlist[:-4])))
			os.system(("echo %s>/etc/modutils/%s" % (nlist[:-4],nlist[:-4])))
			os.chmod(("/etc/modutils/%s" % (nlist[:-4])), 0644)
			os.system("update-modules")
			self.mbox = self.session.open(MessageBox,(_("Loaded %s") % (nlist)), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			os.system(("rmmod%s" % (" " + nlist[:-4])))
			os.system(("rm /etc/modutils/%s" % (nlist[:-4])))
			os.system("update-modules")
			self.mbox = self.session.open(MessageBox,(_("UnLoaded %s") % (nlist)), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def exit(self):
		self.close()
####################################################################
class lsmodScreen(Screen):
	skin = """
<screen name="lsmodscreen" position="center,100" size="750,570" title="Kernel Drivers in Memory">
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,528" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,10" size="710,500" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
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
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			})
		self["Redkey"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		DvrName = os.popen("lsmod")
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/kernelminimem.png"))
		for line in DvrName:
			item = line.split(" ")
			size = line[:28].split(" ")
			minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/kernelminimem.png"))
			if line.find("Module") != 0:
				self.list.append((item[0],( _("size: %s  %s") % (size[-1], item[-1])), minipng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)

	def exit(self):
		self.close()
####################################################################
class CrashLogScreen(Screen):
	skin = """
<screen name="crashlogscreen" position="center,160" size="750,370" title="View or Remove Crashlog files">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<widget source="Greenkey" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="Yellowkey" render="Label" position="360,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="Bluekey" render="Label" position="530,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="530,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/blue.png" transparent="1" alphatest="on" />
	<widget source="menu" render="Listbox" position="20,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
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
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
			})
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("View"))
		self["Yellowkey"] = StaticText(_("Remove"))
		self["Bluekey"] = StaticText(_("Remove All"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		crashfiles = os.popen("ls -lhe /media/hdd/enigma2_crash*.log /media/usb/enigma2_crash*.log")
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/crashmini.png"))
		for line in crashfiles:
			item = line.split(" ")
			name = item[-1].split("/")
			self.list.append((name[-1][:-5],("%s %s %s %s %s" % ( item[-7], item[-4], item[-5], item[-2], item[-3])), minipng, ("/%s/%s/" % (name[-3],name[-2]))))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		item = self["menu"].getCurrent()
		global Crashfile
		try:
			Crashfile = item[3] + item[0] + ".log"
			self.session.openWithCallback(self.CfgMenu,LogScreen)
		except:
			Crashfile = " "
	
	def YellowKey(self):
		item = self["menu"].getCurrent()
		try:
			file = item[3] + item[0] + ".log"
			os.system("rm %s"%(file))
			self.mbox = self.session.open(MessageBox,(_("Removed %s") % (file)), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Failed remove")), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def BlueKey(self):
		try:
			os.system("rm /media/hdd/enigma2_crash*.log /media/usb/enigma2_crash*.log")
			self.mbox = self.session.open(MessageBox,(_("Removed All Crashlog Files") ), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Failed remove")), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def exit(self):
		self.close()
####################################################################
class LogScreen(Screen):
	skin = """
<screen name="crashlogview" position="center,80" size="1170,600" title="View Crashlog file">
	<ePixmap position="20,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,590" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<widget source="Greenkey" render="Label" position="190,560" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="390,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
	<widget source="Yellowkey" render="Label" position="390,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="10,10" size="1150,542" font="Console;22" />
</screen>"""

	def __init__(self, session):
		self.session = session

		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
			})
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("Restart GUI"))
		self["Yellowkey"] = StaticText(_("Save"))
		self["text"] = ScrollLabel("")
		self.listcrah()
		
	def exit(self):
		self.close()
	
	def GreenKey(self):
		os.system("killall -9 enigma2")
		
	def YellowKey(self):
		outname = Crashfile.split("/")
		os.system("gzip %s" % (Crashfile))
		os.system("mv %s.gz /tmp" % (Crashfile))
		self.mbox = self.session.open(MessageBox,(_("%s.gz created in /tmp") % (outname[-1] )), MessageBox.TYPE_INFO, timeout = 4)
		
	def listcrah(self):
		list = " "
		crashfiles = open(Crashfile, "r")
		for line in crashfiles:
			if line.find("Traceback (most recent call last):") != -1:
				for line in crashfiles:
					list += line
					if line.find("]]>") != -1:
						break
		self["text"].setText(list)
		crashfiles.close()
		global Crashfile
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
######################################################################################
class DownScreen2(Screen):
	skin = """
	<screen name="downscreen2" position="center,160" size="750,370" title="Satellites.xml Downloader">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<widget source="Greenkey" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 2), # index 4 is the pixmap
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
			"green": self.reboot,
		})
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("Reboot"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		satpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/satmini.png"))
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/satellites.ini"):
			webname = open("/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/satellites.ini", "r")
			for line in webname:
				adrstr = line.split("/")
				try:
					self.list.append((adrstr[2], _("download from: %s") %(adrstr[2]), satpng, line ))
				except:
					break
			webname.close()
		self["menu"].setList(self.list)

	def exit(self):
		self.close()

	def keyOK(self, webadr = None):
		if webadr == None:
			webadr = self["menu"].getCurrent()[3]
			zipname = webadr.split("/")
			if fileExists("/etc/tuxbox/satellites.xml"):
				if fileExists("/etc/tuxbox/satellites.old"):
					os.system("rm /etc/tuxbox/satellites.old")
				os.system("cp /etc/tuxbox/satellites.xml /etc/tuxbox/satellites.old")
				os.system("rm /etc/tuxbox/satellites.xml")
				try:
					os.system("wget -P /etc/tuxbox/ %s" % (webadr[:-2]))
					if fileExists("/etc/tuxbox/%s.zip" % (zipname[-1][:-6])):
						os.system("unzip -o /etc/tuxbox/%s -d /etc/tuxbox/" % (zipname[-1][:-2]))
						os.system("rm /etc/tuxbox/%s" % (zipname[-1][:-2]))
					elif fileExists("/etc/tuxbox/%s.tar.gz" % (zipname[-1][:-9])):
						os.system("tar -xzf /etc/tuxbox/%s -C /etc/tuxbox/" % (zipname[-1][:-2]))
						os.system("cp /etc/tuxbox/%s/satellites.xml /etc/tuxbox/" % (zipname[-1][:-9]))
						#os.system("rm /etc/tuxbox/%s/satellites.xml" % (zipname[-1][:-9]))
						os.system("rm -r /etc/tuxbox/%s" % (zipname[-1][:-9]))
						os.system("rm /etc/tuxbox/%s" % (zipname[-1][:-2]))
					os.chmod("/etc/tuxbox/satellites.xml", 0644)
					self.mbox = self.session.open(MessageBox,(_("satellite.xml downloaded Successfull")), MessageBox.TYPE_INFO, timeout = 4)
				except:
					os.system("cp /etc/tuxbox/satellites.old /etc/tuxbox/satellites.xml")
					self.mbox = self.session.open(MessageBox,(_("satellite.xml downloaded UnSuccessfull")), MessageBox.TYPE_INFO, timeout = 4)
				
	def reboot(self):
		os.system("reboot")
###############################################################################
class Info2Screen(Screen):
	skin = """
<screen name="info2view" position="center,100" size="890,560" title="System Info">
	<ePixmap position="20,548" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,518" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="15,10" size="860,500" font="Console;20" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"ok": self.exit,
			})
		self["Redkey"] = StaticText(_("Close"))
		self["text"] = ScrollLabel("")
		self.meminfoall()
		
	def exit(self):
		self.close()
		
	def meminfoall(self):
		list = " "
		try:
			os.system("free>/tmp/mem && echo>>/tmp/mem && df -h>>/tmp/mem")
			meminfo = open("/tmp/mem", "r")
			for line in meminfo:
				list += line
			self["text"].setText(list)
			meminfo.close()
			os.system("rm /tmp/mem")
		except:
			list = " "
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
######################################################################################
class CrontabMan(Screen):
	skin = """
<screen name="cronscreen" position="center,160" size="750,370" title="CtronTab Manager">
	<ePixmap position="20,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="red_key" render="Label" position="20,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="green_key" render="Label" position="195,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="195,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<widget source="yellow_key" render="Label" position="370,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="370,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="15,15" size="720,288" scrollbarMode="showOnDemand">
		<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (10, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 29
	}
			</convert>
		</widget>
</screen>"""
	
	def __init__(self, session):
		self.session = session

		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
		})
		self["red_key"] = StaticText(_("Close"))
		self["green_key"] = StaticText(_("Add tabs"))
		self["yellow_key"] = StaticText(_("Remove tabs"))
		self.list = []
		self["menu"] = List(self.list)
		self.cMenu()

	def cMenu(self):
		self.list = []
		count = 0
		if fileExists("/etc/cron/crontabs/root"):
			cron = open("/etc/cron/crontabs/root", "r")
			for line in cron:
				count = count + 1
				self.list.append((line, count))
			cron.close()
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.Ok, "cancel": self.close}, -1)

	def Ok(self):
		self.close()
		
	def GreenKey(self):
		self.session.openWithCallback(self.cMenu,CrontabManAdd)

	
	def YellowKey(self):
		try:
			os.system("sed -i %sd /etc/cron/crontabs/root" % str(self["menu"].getCurrent()[1]))
		except:
			pass
		self.cMenu()
		
	def exit(self):
		self.close()
####################################################################
class CrontabManAdd(ConfigListScreen, Screen):
	skin = """
<screen name="CrontabManAdd" position="center,160" size="750,370" title="add tabs" >
		<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
		<widget source="Redkey" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
		<widget source="Greenkey" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />

</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.list = []
		self.list.append(getConfigListEntry(_("Min"), config.plugins.CronMan.min))
		self.list.append(getConfigListEntry(_("Hour"), config.plugins.CronMan.hour))
		self.list.append(getConfigListEntry(_("Day of month"), config.plugins.CronMan.dayofmonth))
		self.list.append(getConfigListEntry(_("Month"), config.plugins.CronMan.month))
		self.list.append(getConfigListEntry(_("Day of week"), config.plugins.CronMan.dayofweek))
		self.list.append(getConfigListEntry(_("Command"), config.plugins.CronMan.command))
		self.list.append(getConfigListEntry(_("Every"), config.plugins.CronMan.every))
		ConfigListScreen.__init__(self, self.list)
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("Add"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.ok,
			"ok": self.ok
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	
	def ok(self):
		everymin = ""
		everyhour = ""
		everydayofmonth = ""
		everymonth = ""
		everydayofweek = ""
		if config.plugins.CronMan.min.value != '*' and config.plugins.CronMan.every.value == '1':
			everymin = '/'
		elif config.plugins.CronMan.hour.value != '*' and config.plugins.CronMan.every.value == '2':
			everyhour = '/'
		elif config.plugins.CronMan.dayofmonth.value != '*' and config.plugins.CronMan.every.value == '3':
			everydayofmonth = '/'
		elif config.plugins.CronMan.month.value != '*' and config.plugins.CronMan.every.value == '4':
			everymonth = '/'
		elif config.plugins.CronMan.dayofweek.value != '*' and config.plugins.CronMan.every.value == '5':
			everydayofweek = '/'
			
		if config.plugins.CronMan.min.value == '*' and config.plugins.CronMan.hour.value == '*' and config.plugins.CronMan.dayofmonth.value == '*' and config.plugins.CronMan.month.value == '*' and  config.plugins.CronMan.dayofweek.value == '*':
			print ("error")
		else:
			os.system("echo -e '%s%s %s%s %s%s %s%s %s%s    %s' >> /etc/cron/crontabs/root" % (everymin, config.plugins.CronMan.min.value,
																				everyhour, config.plugins.CronMan.hour.value, 
																				everydayofmonth, config.plugins.CronMan.dayofmonth.value,
																				everymonth, config.plugins.CronMan.month.value,
																				everydayofweek, config.plugins.CronMan.dayofweek.value,
																				config.plugins.CronMan.command.value))
		for i in self["config"].list:
			i[1].cancel()
		self.close()
####################################################################