# by 2boom 2011-2012 4bob@ua.fm 
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigSelection, ConfigSubsection, ConfigYesNo
from Components.ConfigList import ConfigListScreen
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap
from Screens.PluginBrowser import PluginBrowser
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.Screen import Screen
from Components.Label import Label
from enigma import eTimer
from Components.Language import language
from Components.Sources.StaticText import StaticText
from Tools.Directories import fileExists
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ
import os
import gettext

adress = "http://gisclub.tv/gi/softcam/SoftCam.Key"
pluginpath = "/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/"
ownbiss = "own.biss"

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("PliPanel", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/PliPanel/locale"))

def _(txt):
	t = gettext.dgettext("PliPanel", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
####################################################################
config.plugins.nclsw = ConfigSubsection()
config.plugins.nclsw.activeserver = ConfigText(default = "NotSelected")
####################################################################
######################################################################################
config.plugins.SoftCamUdp = ConfigSubsection()
config.plugins.SoftCamUdp.addbiss = ConfigSelection(default = "No", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
config.plugins.SoftCamUdp.path = ConfigSelection(default = "/usr/keys/", choices = [
		("/usr/keys/", "/usr/keys/"),
		("/etc/keys/", "/etc/keys/"),
		("/etc/tuxbox/config/", "/etc/tuxbox/config/"),
		("/etc/tuxbox/config/oscam-stable/", "/etc/tuxbox/config/oscam-stable/"),
		])
config.plugins.SoftCamUdp.keyname = ConfigSelection(default = "SoftCam.Key", choices = [
		("SoftCam.Key", "SoftCam.Key"),
		("oscam.keys", "oscam.keys"),
		("oscam.biss", "oscam.biss"),
		])
######################################################################################
class emuSel(Screen):
	skin = """
<screen name="emuSel" position="center,160" size="750,370" title="Select SoftCam or CardServer">
<widget source="menu" render="Listbox" position="15,10" size="720,250" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" transparent="1" alphatest="on" />
	<ePixmap position="360,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" transparent="1" alphatest="on" />
	<ePixmap position="530,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/blue.png" transparent="1" alphatest="on" />
	<widget name="key_red" position="20,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget name="key_green" position="190,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget name="key_yellow" position="360,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget name="key_blue" position="530,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""

	def __init__(self, session, emu):
		self.emutype = emu
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.selemulist()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"green": self.start,
				"red": self.stop,
				"yellow": self.restart,
				"blue": self.install,
			},-1)
		self.list = [ ]
		self["key_red"] = Label(_("Stop"))
		self["key_green"] = Label(_("Start"))
		self["key_yellow"] = Label(_("ReStart"))
		self["key_blue"] = Label(_("Install"))
		
	def selemulist(self):
		self.list = []
		camdlist = os.popen("ls -1 /etc/init.d/%s.*" % self.emutype)
		if self.emutype == "softcam":
			actpng = "emuact.png"
			defpng = "emumini.png"
		else:
			actpng = "cardact.png"
			defpng = "cardmini.png"
		for line in camdlist:
			if self.emuversion(line) == self.emucurrent():
				softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/%s" % actpng))
			else:
				softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/%s" % defpng))
			try:
				if line.find("%s.None" % self.emutype) == -1:
					self.list.append((line.split("/")[3], self.emuversion(line), softpng))
			except:
				pass
		camdlist.close()
		self["menu"].setList(self.list)
		
	def emuversion(self, what):
		emuname = " "
		emu = os.popen("%s info" % what.split("\n")[0])
		for line in emu.readlines():
			emuname = line 
		emu.close()
		return emuname
		
	def emucurrent(self):
		emuname = " "
		emu = os.popen("/etc/init.d/%s info" % self.emutype)
		for line in emu.readlines():
			emuname = line 
		emu.close()
		return emuname
		
	def start(self):
		if self["menu"].getCurrent()[1] != self.emucurrent():
			os.system("/etc/init.d/%s stop" % self.emutype)
			if fileExists("/etc/init.d/%s" % self.emutype):
				os.unlink("/etc/init.d/%s" % self.emutype)
			os.symlink("/etc/init.d/%s" % self["menu"].getCurrent()[0][:-1], "/etc/init.d/%s" % self.emutype)
			os.chmod("/etc/init.d/%s" % self.emutype, 0777)
			os.system("/etc/init.d/%s start" % self.emutype)
			self.mbox = self.session.open(MessageBox, _("Please wait, starting %s" % self["menu"].getCurrent()[0][:-1]), MessageBox.TYPE_INFO, timeout = 4 )
			self.selemulist()
		
	def stop(self):
		item = self.emucurrent()
		if item != " ":
			os.system("/etc/init.d/%s stop" % self.emutype)
			os.unlink("/etc/init.d/%s" % self.emutype)
			if not fileExists("/etc/init.d/%s.None" % self.emutype):
				os.system("echo -e '# Placeholder for no cam' >> /etc/init.d/%s.None" % self.emutype)
			os.symlink("/etc/init.d/%s.None" % self.emutype, "/etc/init.d/%s" % self.emutype)
			os.chmod("/etc/init.d/%s" % self.emutype, 0777)
			self.mbox = self.session.open(MessageBox, _("Please wait, stoping %s" % item), MessageBox.TYPE_INFO, timeout = 4 )
			self.selemulist()
		
	def restart(self):
		item = self.emucurrent()
		if item != " ":
			os.system("/etc/init.d/%s restart" % self.emutype)
			self.mbox = self.session.open(MessageBox,_("Please wait, restarting %s" % self.emucurrent()), MessageBox.TYPE_INFO, timeout = 4 )
		
	def install(self):
		self.session.openWithCallback(self.selemulist,installCam, self.emutype)
		
	def ok(self):
		if self["menu"].getCurrent()[1] != self.emucurrent():
			self.start()
		
	def cancel(self):
		self.close()
#####################################################################################################
class installCam(Screen):
	skin = """
<screen name="installCam" position="center,160" size="750,370" title="insatall">
<widget source="menu" render="Listbox" position="15,10" size="720,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap name="red" position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap name="green" position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" transparent="1" alphatest="on" />
	<widget name="key_red" position="20,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget name="key_green" position="190,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""
	  
	def __init__(self, session, emu):
		self.emutype = emu
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.feedlist()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"green": self.setup,
				"red": self.cancel,
			},-1)
		self.list = [ ]
		self["key_red"] = Label(_("Close"))
		self["key_green"] = Label(_("Install"))
		
	def feedlist(self):
		self.list = []
		os.system("opkg update")
		camdlist = os.popen("opkg list enigma2-plugin-softcams-*")
		softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/emumini.png"))
		for line in camdlist.readlines():
			dstring = line.split()
			try:
				endstr = len(dstring[0]) + len(dstring[1]) + len(dstring[2]) + len(dstring[3]) + 4 
				if self.emutype == "softcam":
					if line.find("cardserver") == -1:
						self.list.append(("%s %s %s" % (dstring[0], dstring[1], dstring[2]), line[endstr:], softpng))
				else:
					if line.find("%s" % self.emutype) > -1:
						self.list.append(("%s %s %s" % (dstring[0], dstring[1], dstring[2]), line[endstr:], softpng))
			except:
				self.list.append((_("Error dowload SoftCam list"), _("Check your internet connection"), softpng))
		camdlist.close()
		self["menu"].setList(self.list)
		
	def ok(self):
		self.setup()
		
	def setup(self):
		os.system("opkg install -force-reinstall %s" % self["menu"].getCurrent()[0])
		self.mbox = self.session.open(MessageBox, _("%s is installed" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		
	def cancel(self):
		self.close()

#################################################
class SoftcamPanel(Screen):
	skin = """
<screen name="SoftcamPanel" position="center,160" size="750,370" title="softcam/cardserver Panel">
<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
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
			"green": self.Restart,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("ReStart Both"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()
		
	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/softcam.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/cardserver.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/ecminfo.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/soft.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/newsw.png"))
		self.list.append((_("Simple Softcam"),"com_one", _("Start, Stop, Restart Sofcam"), onepng))
		self.list.append((_("Simple Cardserver"),"com_two", _("Start, Stop, Restart Cardserver"), twopng))
		self.list.append((_("newcamd.list Switcher"),"com_five", _("Switch newcamd.list with remote conrol"), fivepng))
		self.list.append((_("ecm.info Viewer"),"com_four", _("ecm.info file viewer"), fourpng))
		self.list.append((_("SoftCam.Key Updater"),"com_tree", _("update Softcam.key from internet"), treepng))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "com_one":
				self.session.openWithCallback(self.mList,emuSel, "softcam")
			elif returnValue is "com_two":
				self.session.openWithCallback(self.mList,emuSel, "cardserver")
			elif returnValue is "com_tree":
				self.session.open(SoftcamUpd)
			elif returnValue is "com_four":
				self.session.open(ecminfoScreen)
			elif returnValue is "com_five":
				self.session.open(NCLSwp)
		else:
				print "\n[PliPanel] cancel\n"
				self.close(None)

	def Restart(self):
		if fileExists("/etc/init.d/softcam"):
			os.system("/etc/init.d/softcam stop")
		if fileExists("/etc/init.d/cardserver"):
			os.system("/etc/init.d/cardserver stop")
			os.system("/etc/init.d/cardserver start")
		if fileExists("/etc/init.d/softcam"):
			os.system("/etc/init.d/softcam start")
		if fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			msg  = _("Restarting ...")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout = 4 )
###############################################################################################
class ecminfoScreen(Screen):
	skin = """
<screen name="ecminfoview" position="center,160" size="750,370" title="ecm.info viewer">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="20,10" size="710,310" font="Console;22" />
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
		self["key_red"] = StaticText(_("Close"))
		self["text"] = ScrollLabel("")
		self.list = []
		self["menu"] = List(self.list)
		self.listecm()
		self.Timer = eTimer()
		self.Timer.callback.append(self.listecm)
		self.Timer.start(1000*4, False)
		
	def exit(self):
		self.close()
	
	def listecm(self):
		list = ""
		try:
			ecmfiles = open("/tmp/ecm.info", "r")
			for line in ecmfiles:
				list += line
			self["text"].setText(list)
			ecmfiles.close()
		except:
			pass
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
		
###############################################################################################
class SoftcamUpd(ConfigListScreen, Screen):
	skin = """
<screen name="SoftcamUpd" position="center,160" size="750,370" title="SoftCam.Key Updater">
		<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
		<widget source="Redkey" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
		<widget source="Greenkey" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="340,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
		<widget source="Yellowkey" render="Label" position="340,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="505,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/blue.png" alphatest="blend" />
		<widget source="Bluekey" render="Label" position="505,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.list = []
		self.list.append(getConfigListEntry(_("Path to save keyfile"), config.plugins.SoftCamUdp.path))
		self.list.append(getConfigListEntry(_("Name of keyfile"), config.plugins.SoftCamUdp.keyname))
		self.list.append(getConfigListEntry(_("Add own biss in keyfile"), config.plugins.SoftCamUdp.addbiss))
		ConfigListScreen.__init__(self, self.list)
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("Save"))
		self["Yellowkey"] = StaticText(_("Download"))
		self["Bluekey"] = StaticText(_("Changelog"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.downkey,
			"blue": self.keyBlue,
			"ok": self.save
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)
	
	def save(self):
		for i in self["config"].list:
			i[1].save()
		self.mbox = self.session.open(MessageBox,(_("Saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def keyBlue (self):
		self.session.open(ChangelogScreen)
		
	def downkey(self):
		try:
			os.system("wget -P /tmp %s" % ( adress))
			if config.plugins.SoftCamUdp.addbiss.value == "1":
				if fileExists("%s%s" % (pluginpath,ownbiss)):
					os.system("cp %s%s /tmp/%s" % (pluginpath, ownbiss, ownbiss))
					os.system("cat /tmp/%s /tmp/SoftCam.Key > /tmp/keyfile.tmp" % (ownbiss))
					os.system("rm /tmp/SoftCam.Key")
			else:
				os.system("mv /tmp/SoftCam.Key /tmp/keyfile.tmp")
			if fileExists("%s%s" % (config.plugins.SoftCamUdp.path.value, config.plugins.SoftCamUdp.keyname.value)):
				if config.plugins.SoftCamUdp.keyname.value == "SoftCam.Key":
					os.system("cp %s%s %s%s.old" % (config.plugins.SoftCamUdp.path.value, config.plugins.SoftCamUdp.keyname.value, config.plugins.SoftCamUdp.path.value, config.plugins.SoftCamUdp.keyname.value[:-4]))
				else:
					os.system("cp %s%s %s%s.old" % (config.plugins.SoftCamUdp.path.value, config.plugins.SoftCamUdp.keyname.value, config.plugins.SoftCamUdp.path.value, config.plugins.SoftCamUdp.keyname.value[:-5]))
				os.system("rm %s%s" % (config.plugins.SoftCamUdp.path.value, config.plugins.SoftCamUdp.keyname.value))
			os.system("cp /tmp/keyfile.tmp %s%s" % (config.plugins.SoftCamUdp.path.value, config.plugins.SoftCamUdp.keyname.value))
			os.chmod(("%s%s" % (config.plugins.SoftCamUdp.path.value, config.plugins.SoftCamUdp.keyname.value)), 0644)
			os.system("rm /tmp/keyfile.tmp")
			os.system("rm /tmp/%s" % (ownbiss))
			self.mbox = self.session.open(MessageBox,(_("%s downloaded Successfull" % config.plugins.SoftCamUdp.keyname.value)), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			os.system("cp /usr/keys/SoftCam.old /usr/keys/SoftCam.Key")
			self.mbox = self.session.open(MessageBox,(_("%s downloaded UnSuccessfull" % config.plugins.SoftCamUdp.keyname.value)), MessageBox.TYPE_INFO, timeout = 4 )
######################################################################################
class ChangelogScreen(Screen):
	skin = """
<screen name="changelog" position="center,160" size="750,370" title="Changelog">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="15,10" size="720,300" font="Console;20" />
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
		self["text"] = ScrollLabel("")
		self.meminfoall()
		
	def exit(self):
		self.close()
		
	def meminfoall(self):
		list = " "
		os.system("wget -P /tmp/ %s.txt" % (adress[:-4]))
		try:
			meminfo = open("/tmp/SoftCam.txt", "r")
			for line in meminfo:
				list += line
			self["text"].setText(list)
			meminfo.close()
			os.system("rm /tmp/SoftCam.txt")
		except:
			try:
				self.mbox = self.session.open(MessageBox,(_("%s") % (adress)), MessageBox.TYPE_INFO, timeout = 4)
			except:
				pass
			list = " "
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], 
		{ "cancel": self.close,
		"up": self["text"].pageUp,
		"left": self["text"].pageUp,
		"down": self["text"].pageDown,
		"right": self["text"].pageDown,
		}, -1)
######################################################################################
class NCLSwp(Screen):
	skin = """
<screen name="NewCamdListSwitchpanel" position="center,155" size="750,460" title="newcamd.list Switcher">
	<ePixmap position="20,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" alphatest="blend" />
	<widget source="Redkey" render="Label" position="20,425" zPosition="2" size="170,30" font="Regular; 19" halign="center" valign="center" backgroundColor="background" foregroundColor="white" transparent="1" />
	<ePixmap position="190,455" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" alphatest="blend" />
	<widget source="Greenkey" render="Label" position="190,425" zPosition="2" size="200,30" font="Regular; 19" halign="center" valign="center" backgroundColor="background" foregroundColor="white" transparent="1" />
	<ePixmap position="390,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" alphatest="blend" />
	<widget source="Yellowkey" render="Label" position="390,425" zPosition="2" size="170,30" font="Regular; 19" halign="center" valign="center" backgroundColor="background" foregroundColor="white" transparent="1" />
	<ePixmap position="560,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/blue.png" alphatest="blend" />
	<widget source="Bluekey" render="Label" position="560,425" zPosition="2" size="170,30" font="Regular; 19" halign="center" valign="center" backgroundColor="background" foregroundColor="white" transparent="1" />
	<widget source="list" render="Listbox" position="15,10" size="720,200" scrollbarMode="showOnDemand">
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
	<widget source="readServ" render="Label" zPosition="2" position="324,230" size="360,24" font="Regular; 20" halign="left" transparent="1" foregroundColor="foreground" /> 
	<widget source="Active" render="Label" zPosition="2" position="60,230" size="250,24" font="Regular; 20" halign="right" transparent="1" foregroundColor="#e9820c" />
	<eLabel position="265,295" size="60,22" text="Caid:" font="Regular; 19" foregroundColor="#aaaaaa" />
	<eLabel position="100,295" size="60,22" text="Prov:" font="Regular; 19" foregroundColor="#aaaaaa" />
	<eLabel position="409,295" size="80,22" text="Server:" font="Regular; 19" foregroundColor="#aaaaaa" />
	<eLabel position="265,325" size="60,22" text="Port:" font="Regular; 19" foregroundColor="#aaaaaa" />
	<eLabel position="425,325" size="65,22" text="Time:" font="Regular; 19" foregroundColor="#aaaaaa" />
	<eLabel position="100,325" size="60,22" text="Pid:" font="Regular; 19" foregroundColor="#aaaaaa" />
	<widget source="version" render="Label" zPosition="2" position="325,260" size="300,22" font="Regular; 19" halign="left" transparent="1" foregroundColor="foreground" />
	<eLabel position="85,283" size="570,2" backgroundColor="#aaaaaa" />
	<eLabel position="85,413" size="570,2" backgroundColor="#aaaaaa" />
	<widget source="pid" render="Label" position="160,325" size="80,22" font="Regular; 19" halign="left" backgroundColor="background" transparent="1" noWrap="1" foregroundColor="foreground" valign="center" /> 
	<widget source="source" render="Label" position="490,295" size="210,22" font="Regular; 19" halign="left" backgroundColor="background" transparent="1" noWrap="1" foregroundColor="foreground" valign="center" />
	<widget source="caid" render="Label" position="325,295" size="80,22" font="Regular; 19" halign="left" backgroundColor="background" transparent="1" noWrap="1" foregroundColor="foreground" valign="center" />
	<widget source="prov" render="Label" position="160,295" size="95,22" font="Regular; 19" halign="left" backgroundColor="background" transparent="1" noWrap="1" foregroundColor="foreground" valign="center" />
	<widget source="port" render="Label" position="325,325" size="80,22" font="Regular; 19" halign="left" backgroundColor="background" transparent="1" noWrap="1" foregroundColor="foreground" valign="center" />
	<widget source="time" render="Label" position="490,325" size="120,22" font="Regular; 19" halign="left" backgroundColor="background" transparent="1" noWrap="1" foregroundColor="foreground" valign="center" />
	<widget source="cw0" render="Label" zPosition="2" position="125,355" size="500,24" font="Regular; 19" halign="center" transparent="1" foregroundColor="foreground" />
	<widget source="cw1" render="Label" zPosition="2" position="125,380" size="500,24" font="Regular; 19" halign="center" transparent="1" foregroundColor="foreground" />
</screen>"""

	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.skin = NCLSwp.skin
		self.session = session
		self.list = []
		self["list"] = List(self.list)
		self.mList()
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions"],
		{	
			"ok": self.run,
			"red": self.close,
			"green": self.keyGreen,
			"yellow": self.keyYellow,
			"blue": self.keyBlue,
			"cancel": self.close
		}, -1)
		self["readServ"] = StaticText()
		self["Active"] = StaticText(_("Active Profile:"))
		self["Redkey"] = StaticText(_("Close"))
		self["Greenkey"] = StaticText(_("Restart MgCamd"))
		self["Yellowkey"] = StaticText(_("Ping"))
		self["Bluekey"] = StaticText(_("Trace"))
		self["readServ"]= StaticText(config.plugins.nclsw.activeserver.value)
		self["version"] = StaticText(self.mgcamdVersion())
		self["caid"] = StaticText()
		self["pid"] = StaticText()
		self["prov"] = StaticText()
		self["source"] = StaticText()
		self["port"] = StaticText()
		self["time"] = StaticText()
		self["cw0"] = StaticText()
		self["cw1"] = StaticText()
		self.ecminfo()
		self.Timer = eTimer()
		self.Timer.callback.append(self.ecminfo)
		self.Timer.start(1000*4, False)
		
	def ecminfo(self):
		try:
			ecmfile = open("/tmp/ecm.info", "r")
			for line in ecmfile:
				if line.lower().find("caid:") > -1:
					self["caid"].text = ("%0.4X" % int(line.split("\n")[0].split(" ")[-1],16))
				if line.find("pid:") > -1:
					self["pid"].text = ("%0.4X" % int(line.split("\n")[0].split(" ")[-1],16))
				if line.find("prov:") > -1:
					if line.split("\n")[0].split(" ")[-1][:2] == "0x":
						self["prov"].text = ("%0.6X" % int(line.split("\n")[0].split(" ")[-1],16))
					else:
						self["prov"].text = line.split("\n")[0].split(" ")[-1]
################################################################
				if line.find("source:") > -1:
					self["port"].text = line.split(")")[0].split("(")[-1].split(" ")[-1].split(":")[-1]
					self["source"].text = line.split(")")[0].split("(")[-1].split(" ")[-1].split(":")[0]
				elif line.find("from:") > -1:
					self["source"].text = line.split("\n")[0].split(" ")[-1]    
################################################################
				if line.find("msec") > -1:
					self["time"].text = ("%s msec" % line.split(" ")[0])
				elif line.find("ecm time:") >  -1:
					self["time"].text = line.split("\n")[0].split(" ")[-1]
				if line.find("cw0:") > -1:
					self["cw0"].text = line.split("\n")[0]
				if line.find("cw1:") > -1:
					self["cw1"].text = line.split("\n")[0]
			ecmfile.close()
		except:
			pass
		
	def mList(self):
		servinactpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/serv.png"))
		servactpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/servact.png"))
		self.list = []
		list = os.listdir("/usr/keys")
		for line in list:
			if line.find(".nl") > -1:
				if line[:-3] == config.plugins.nclsw.activeserver.value:
					self.list.append((line[:-3],_("server: %s" % (self.Adress(line))), servactpng))
				else:
					self.list.append((line[:-3],_("server: %s" % (self.Adress(line))), servinactpng))
		self["list"].setList(self.list)
		
	def run(self):
		config.plugins.nclsw.activeserver.value = self["list"].getCurrent()[0]
		config.plugins.nclsw.activeserver.save()
		os.system("cp /usr/keys/%s.nl /usr/keys/newcamd.list" %  self["list"].getCurrent()[0])
		os.chmod("/usr/keys/newcamd.list", 0644)
		self.session.open(MessageBox, _("Applying %s newcamd.list" % self["list"].getCurrent()[0]), type = MessageBox.TYPE_INFO, timeout = 4 )
		self.mList()
		self["readServ"].text = config.plugins.nclsw.activeserver.value

	def keyGreen (self):
	# PLI	
		if fileExists("/etc/init.d/softcam"):
			os.system("/etc/init.d/softcam stop")
			os.system("/etc/init.d/softcam start")
			self.session.open(MessageBox, _("MgCamd Restarted"), type = MessageBox.TYPE_INFO, timeout = 4 )
		
	def keyYellow (self):
		self.command("ping -c 5 %s" % self.Adress("newcamd.list"))
	
	def keyBlue (self):
		self.command("traceroute -m15 %s" % self.Adress("newcamd.list"))

	def Adress (self, nameserv):
		if fileExists("/usr/keys/%s" % (nameserv)):
			nameserver = open("/usr/keys/%s" % (nameserv), "r").readlines()
			for line in nameserver:
				if line.find("CWS = 127.0.0.1") == -1:
					if line.find("CWS = ") >= 0:
						return line.split()[2]
						break
					elif line.find("CWS_MULTIPLE = ") >= 0:
						return line.split()[2]
						break
		else:
			return " "
			
	def command(self, com):
		self.session.open(Console,_("start: %s") % (com), ["%s" % com])
		
	def mgcamdVersion(self):
		#Pli
		if fileExists("/etc/init.d/softcam"):
			try:
				f = os.popen("/etc/init.d/softcam info")
				for i in f.readlines():
					return i
			except:
				return None
		else:
			return None
			
####################################################################################