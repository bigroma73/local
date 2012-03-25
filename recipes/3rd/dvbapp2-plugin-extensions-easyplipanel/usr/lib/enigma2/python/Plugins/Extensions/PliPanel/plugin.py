#by 2boom 4bob@ua.fm 2011-12
from Screens.Screen import Screen
from Screens.PluginBrowser import PluginBrowser
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Label import Label
from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Tools.Directories import fileExists
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from os import environ
import os
import gettext
import SimpleCardServ
import minstall
import backup
import tools

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

class easyPanel(Screen):
	skin = """
<screen name="PliPanel" position="center,160" size="750,370" title="Easy Panel for Pli">
<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
<widget source="Redkey" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
<widget source="Greenkey" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<ePixmap position="340,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
<widget source="Yellowkey" render="Label" position="340,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<ePixmap position="505,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/blue.png" alphatest="blend" />
<widget source="Bluekey" render="Label" position="505,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="menu" render="Listbox" position="15,10" size="720,300" scrollbarMode="showOnDemand">
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
<ePixmap position="675,331" size="70,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/info.png" zPosition="2" alphatest="blend" />
</screen>"""

	def __init__(self, session):
		self.session = session

		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions", "EPGSelectActions"],

		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"info": self.infoKey,
			"green": self.keyGreen,
			"yellow": self.keyYellow,
			"blue": self.keyBlue,
			
		})
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("Softcam"))
		self["Yellowkey"] = StaticText(_("Tools"))
		self["Bluekey"] = StaticText(_("Install"))
		self.list = []
		self["menu"] = List(self.list)
#		self.firststart()
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/softcam.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/cardserver.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/tools.png"))
		backuppng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/backup.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/install.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/addon.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/system.png"))
		self.list.append((_("Simple Softcam/Cardserver"),"com_one", _("Start, Stop, Restart Sofcam/Cardserver"), onepng))
		self.list.append((_("Service Tools"),"com_two", _("Manage swap, ntp, unmount, script, info ..."), twopng ))
		self.list.append((_("System Tools"),"com_six", _("kernel modules manager, manage ftp, samba ..."), sixpng ))
		self.list.append((_("Full back-up and setting on USB/HDD"),"com_tree", _("Full 1:1 back-up and back-up setting"), backuppng ))
		self.list.append((_("Manual Installer/Uninstaller"),"com_four", _("install/uninstall local .ipk & .tar.gz files from /tmp"), treepng))
		self.list.append((_("Plugin Browser"),"com_five", _("Install & Remove Plugins, Addons, Softcams"), fourpng))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "com_one":
				self.session.open(SimpleCardServ.SoftcamPanel)
				
			elif returnValue is "com_two":
				self.session.open(tools.ToolsScreen)
					
			elif returnValue is "com_tree":
				self.session.open(backup.BackupSuite)
				
			elif returnValue is "com_four":
				self.session.open(minstall.IPKToolsScreen)
				
			elif returnValue is "com_five":
				self.session.open(PluginBrowser)
				
			elif returnValue is "com_six":
				self.session.open(tools.SystemScreen)
				
			else:
				print "\n[PliPanel] cancel\n"
				self.close(None)

	def keyBlue (self):
		self.session.open(minstall.IPKToolsScreen)
				
	def keyYellow (self):
		self.session.open(tools.ToolsScreen)
		
	def keyGreen (self):
		self.session.open(SimpleCardServ.emuSel, "softcam")
	
	def infoKey (self):
		self.session.openWithCallback(self.mList,info)
		
#	def firststart(self):
#		if not fileExists("/etc/init.d/busybox-cron"):
#			os.system("opkg update && opkg install busybox-cron")
#		if not fileExists("/usr/bin/ntpdate"):
#			os.system("opkg update && opkg install ntpdate")
##########################################################################################
class info(Screen):
	skin = """
<screen name="info" position="center,105" size="600,570" title="E-Panel for OpenPli">
	<ePixmap position="20,562" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,532" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="MemoryLabel" render="Label" position="20,375" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="SwapLabel" render="Label" position="20,400" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="FlashLabel" render="Label" position="20,425" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="memTotal" render="Label" position="180,375" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="swapTotal" render="Label" position="180,400" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="flashTotal" render="Label" position="180,425" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="deviceLabel" render="Label" position="20,250" size="200,22" font="Regular; 20" halign="left" foregroundColor="#aaaaaa" />
	<widget source="device" render="Label" position="20,275" zPosition="2" size="560,88" font="Regular;20" halign="left" valign="top" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Hardware" render="Label" position="230,10" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Image" render="Label" position="230,35" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Kernel" render="Label" position="230,60" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="EnigmaVersion" render="Label" position="230,110" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="HardwareLabel" render="Label" position="20,10" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="ImageLabel" render="Label" position="20,35" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="KernelLabel" render="Label" position="20,59" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="EnigmaVersionLabel" render="Label" position="20,110" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="nimLabel" render="Label" position="20,145" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="nim" render="Label" position="20,170" zPosition="2" size="500,66" font="Regular;20" halign="left" valign="top" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="driver" render="Label" position="230,85" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="driverLabel" render="Label" position="20,85" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<eLabel position="30,140" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,242" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,367" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,454" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="230,494" size="320,2" backgroundColor="#aaaaaa" />
	<ePixmap position="20,463" size="180,47" zPosition="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/2boom.png" alphatest="blend" />
	<widget source="panelver" render="Label" position="470,463" zPosition="2" size="100,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="plipanel" render="Label" position="215,463" zPosition="2" size="250,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="cardserver" render="Label" position="350,528" zPosition="2" size="225,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="cardserverLabel" render="Label" position="215,528" zPosition="2" size="130,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="softcam" render="Label" position="350,503" zPosition="2" size="225,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="softcamLabel" render="Label" position="215,503" zPosition="2" size="130,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.cancel,
			"ok": self.cancel,
			})
		self["key_red"] = StaticText(_("Close"))
		self["MemoryLabel"] = StaticText(_("Memory:"))
		self["SwapLabel"] = StaticText(_("Swap:"))
		self["FlashLabel"] = StaticText(_("Flash:"))
		self["memTotal"] = StaticText()
		self["swapTotal"] = StaticText()
		self["flashTotal"] = StaticText()
		self["device"] = StaticText()
		self["deviceLabel"] = StaticText(_("Devices:"))
		self["Hardware"] = StaticText()
		self["Image"] = StaticText()
		self["Kernel"] = StaticText()
		self["nim"] = StaticText()
		self["nimLabel"] = StaticText(_("Detected NIMs:"))
		self["EnigmaVersion"] = StaticText()
		self["HardwareLabel"] = StaticText(_("Hardware:"))
		self["ImageLabel"] = StaticText(_("Image:"))
		self["KernelLabel"] = StaticText(_("Kernel Version:"))
		self["EnigmaVersionLabel"] = StaticText(_("Last Upgrade:"))
		self["driver"] = StaticText()
		self["driverLabel"] = StaticText(_("Driver Version:"))
		self["plipanel"] = StaticText(_("E-Panel for OpenPli Ver:"))
		self["panelver"] = StaticText()
		self["softcamLabel"] = StaticText(_("Softcam:"))
		self["softcam"] = StaticText()
		self["cardserverLabel"] = StaticText(_("Cardserver:"))
		self["cardserver"] = StaticText()
		self.memInfo()
		self.FlashMem()
		self.devices()
		self.mainInfo()
		self.verinfo()
		self.emuname()
		
	def emuname(self):
		if fileExists("/etc/init.d/softcam"):
			try:
				soft = os.popen("/etc/init.d/softcam info")
				for line in soft:
					self["softcam"].text = line
				soft.close()
			except:
				self["softcam"].text = _("Not Active")
		else:
			self["softcam"].text = _("Not Installed")
		if fileExists("/etc/init.d/cardserver"):
			try:
				card = os.popen("/etc/init.d/cardserver info")
				for line2 in card:
					self["cardserver"].text = line2
				card.close()
			except:
				self["cardserver"].text = _("Not Active")
		else:
			self["cardserver"].text = _("Not Installed")
		
	def devices(self):
		list = ""
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				hdd = hddlist[count][1]
				if int(hdd.free()) > 1024:
					list += ((_("%s  %s  (%d.%03d GB free)\n") % (hdd.model(), hdd.capacity(), hdd.free()/1024 , hdd.free()%1024)))
				else:
					list += ((_("%s  %s  (%03d MB free)\n") % (hdd.model(), hdd.capacity(),hdd.free())))
		else:
			hddinfo = _("none")
		self["device"].text = list
		
	def mainInfo(self):
		listnims = ""
		self["Hardware"].text = about.getHardwareTypeString()
		self["Image"].text = about.getImageTypeString()
		self["Kernel"].text = about.getKernelVersionString()
		self["EnigmaVersion"].text = about.getImageVersionString()
		nims = nimmanager.nimList()
		for count in range(len(nims)):
			if count < 4:
				listnims += "%s\n" % nims[count]
			else:
				listnims += "\n"
		self["nim"].text = listnims
		try:
			drv = os.popen("opkg info *-dvb-modules")
			for line in drv:
				if line.find("Version:") > -1:
					self["driver"].text = line.split()[1]
			drv.close()
		except:
			self["driver"].text = " "

	def memInfo(self):
		mem = open("/proc/meminfo", "r")
		for line in mem:
			if line.find("MemTotal:") > -1:
				memtotal = line.split()[1]
			elif line.find("MemFree:") > -1:
				memfree = line.split()[1]
			elif line.find("SwapTotal:") > -1:
				swaptotal =  line.split()[1]
			elif line.find("SwapFree:") > -1:
				swapfree = line.split()[1]
		self["memTotal"].text = _("Total: %s Kb  Free: %s Kb") % (memtotal, memfree)
		self["swapTotal"].text = _("Total: %s Kb  Free: %s Kb") % (swaptotal, swapfree)
		mem.close()
		
	def FlashMem(self):
		flash = os.popen("df | grep root")
		for line in flash:
			self["flashTotal"].text = _("Total: %s Kb  Free: %s Kb") % (line.split()[1], line.split()[3])
		flash.close()
		
	def verinfo(self):
		ipklist = os.popen("opkg list-installed")
		for line in ipklist.readlines():
			if line.find("easyplipanel") != -1:
				try:
					self["panelver"].text = line[len(line.split()[0]) + 2:]
				except:
					self["panelver"].text = " "
		ipklist.close()
		
	def cancel(self):
		self.close()
		
		
####################################################################
	
def main(session, **kwargs):
	session.open(easyPanel)

def Plugins(**kwargs):
	return PluginDescriptor(
			name=_("E-Panel for Pli"),
			description= _("simple tools for Pli image"),
			where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
			icon="epp.png",
			fnc=main)

