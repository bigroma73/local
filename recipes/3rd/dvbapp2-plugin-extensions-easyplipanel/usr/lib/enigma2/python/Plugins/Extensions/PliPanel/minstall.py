#by 2boom 2011 IPK Tools 4bob@ua.fm 
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
	
class IPKToolsScreen(Screen):
	skin = """
	<screen name="ipktoolsscreen" position="center,160" size="750,370" title="IPK Tools">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,358" zPosition="1" size="230,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" transparent="1" alphatest="on" />
	<widget source = "key_red" render="Label" position="20,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source = "key_green" render="Label" position="190,328" zPosition="2" size="230,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="710,300" >
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
			"ok": self.OK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.restartGUI,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Restart GUI"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/tar.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/ipk1.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/ipk.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/clear.png"))
		self.list.append((_("bh.tgz, tar.gz, nab.tgz installer"),"one", _("install bh.tgz, tar.gz, nab.tgz from /tmp"), onepng ))
		self.list.append((_("ipk packets installer"),"two", _("install ipk packets from /tmp"), twopng ))
		self.list.append((_("advanced ipk packets installer"),"tree", _("-force-overwrite install ipk packets from /tmp"), twopng ))
		self.list.append((_("install extensions"),"six", _("install extensions from feed"), twopng ))
		self.list.append((_("ipk packets remover"),"four", _("remove & advanced remove ipk packets"), treepng ))
		self.list.append((_("clear /tmp"),"five", _("remove *.ipk & *.tar.gz & *.bh.tgz & *.nab.tgz from /tmp"), fivepng))
		self["menu"].setList(self.list)
		
	def exit(self):
		self.close()
		
	def restartGUI(self):
		os.system("killall -9 enigma2")

	def OK(self):
		item = self["menu"].getCurrent()[1]
		if item is "one":
			self.session.openWithCallback(self.mList,InstallTarGZ)
		elif item is "two":
			self.session.openWithCallback(self.mList,InstallIpk)
		elif item is "tree":
			self.session.openWithCallback(self.mList,AdvInstallIpk)
		elif item is "four":
			self.session.openWithCallback(self.mList,RemoveIPK)
		elif item is "five":
			os.system("rm /tmp/*.tar.gz /tmp/*.bh.tgz /tmp/*.ipk /tmp/*.nab.tgz")
			self.mbox = self.session.open(MessageBox,_("*.tar.gz & *.bh.tgz & *.ipk removed"), MessageBox.TYPE_INFO, timeout = 4 )
		elif item is "six":
			self.session.openWithCallback(self.mList,downfeed)
#######################################################################################
class InstallTarGZ(Screen):
	skin = """
<screen name="install tar.gz" position="center,160" size="750,370" title="Select install files">
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
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" transparent="1" alphatest="on" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="360,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="360,328" zPosition="2" size="200,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.okInst,
				"green": self.okInst,
				"red": self.cancel,
				"yellow": self.okInstAll,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Install All"))
		
	def nList(self):
		self.list = []
		ipklist = os.popen("ls -lh  /tmp/*.tar.gz /tmp/*.bh.tgz /tmp/*.nab.tgz")
		ipkminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/tarmini.png"))
		for line in ipklist.readlines():
			dstring = line.split("/")
			try:
				endstr = len(dstring[0] + dstring[1]) + 2
				self.list.append((line[endstr:], dstring[0], ipkminipng))
			except:
				pass
		self["menu"].setList(self.list)
		
	def okInst(self):
		try:
			item = self["menu"].getCurrent()
			name = item[0]
			self.session.open(Console,title = _("Install tar.gz, bh.tgz, nab.tgz"), cmdlist = ["tar -C/ -xzpvf /tmp/%s" % name])
		except:
			pass
			
	def okInstAll(self):
			ipklist = os.popen("ls -1  /tmp/*.tar.gz /tmp/*.bh.tgz")
			self.session.open(Console,title = _("Install tar.gz, bh.tgz, nab.tgz"), cmdlist = ["tar -C/ -xzpvf /tmp/*.tar.gz", "tar -C/ -xzpvf /tmp/*.bh.tgz", "tar -C/ -xzpvf /tmp/*.nab.tgz"])

	def cancel(self):
		self.close()
########################################################################################
class InstallIpk(Screen):
	skin = """
<screen name="install ipk" position="center,160" size="750,370" title="Select install files">
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
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" transparent="1" alphatest="on" />
	<widget source="key_red"  render="Label" position="20,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_green"  render="Label" position="190,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="360,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow"  render="Label" position="360,328" zPosition="2" size="200,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.okInst,
				"green": self.okInst,
				"red": self.cancel,
				"yellow": self.okInstAll,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Install All"))
		
	def nList(self):
		self.list = []
		ipklist = os.popen("ls -lh  /tmp/*.ipk")
		ipkminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/ipkmini.png"))
		for line in ipklist.readlines():
			dstring = line.split("/")
			try:
				endstr = len(dstring[0] + dstring[1]) + 2
				self.list.append((line[endstr:], dstring[0], ipkminipng))
			except:
				pass
		self["menu"].setList(self.list)
		
	def okInst(self):
		try:
			item = self["menu"].getCurrent()
			name = item[0]
			self.session.open(Console,title = "Install ipk packets", cmdlist = ["opkg install /tmp/%s" % name])
		except:
			pass
			
	def okInstAll(self):
		name = "*.ipk"
		self.session.open(Console,title = "Install ipk packets", cmdlist = ["opkg install /tmp/%s" % name])
		
	def cancel(self):
		self.close()
##########################################################################################################
class AdvInstallIpk(Screen):
	skin = """
<screen name="Advanced install ipk" position="center,160" size="750,370" title="Select install files">
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
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" transparent="1" alphatest="on" />
	<widget source ="key_red"  render="Label" position="20,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_green"  render="Label" position="190,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="360,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source ="key_yellow"  render="Label" position="360,328" zPosition="2" size="200,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.okInst,
				"green": self.okInst,
				"red": self.cancel,
				"yellow": self.okInstAll,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Install All"))
		
	def nList(self):
		self.list = []
		ipklist = os.popen("ls -lh  /tmp/*.ipk")
		ipkminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/ipkmini.png"))
		for line in ipklist.readlines():
			dstring = line.split("/")
			try:
				endstr = len(dstring[0] + dstring[1]) + 2
				self.list.append((line[endstr:], dstring[0], ipkminipng))
			except:
				pass
		self["menu"].setList(self.list)
		
	def okInst(self):
		try:
			item = self["menu"].getCurrent()
			name = item[0]
			self.session.open(Console,title = _("Install ipk packets"), cmdlist = ["opkg install -force-overwrite -force-downgrade /tmp/%s" % name])
		except:
			pass
		
	def okInstAll(self):
		name = "*.ipk"
		self.session.open(Console,title = _("Install ipk packets"), cmdlist = ["opkg install -force-overwrite -force-downgrade /tmp/%s" % name])
		
	def cancel(self):
		self.close()
########################################################################################################
class RemoveIPK(Screen):
	skin = """
<screen name="RemoveIpk" position="center,100" size="750,570" title="Ipk remove">
<widget source="menu" position="15,10" render="Listbox" size="720,500">
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
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" transparent="1" alphatest="on" />
	<ePixmap position="360,558" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_red" render="Label" position="20,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_green" render="Label" position="190,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_yellow" render="Label" position="360,528" zPosition="2" size="200,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnInstall"))
		self["key_yellow"] = StaticText(_("Adv. UnInstall"))
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.Remove,
				"green": self.Remove,
				"red": self.cancel,
				"yellow": self.ARemove,
			},-1)
		
	def nList(self):
		self.list = []
		ipklist = os.popen("opkg list-installed")
		ipkminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/ipkmini.png"))
		for line in ipklist.readlines():
			dstring = line.split(" ")
			try:
				endstr = len(dstring[0]) + 2
				self.list.append((dstring[0], line[endstr:], ipkminipng))
			except:
				pass
		self["menu"].setList(self.list)
		
	def cancel(self):
		self.close()
		
	def Remove(self):
		item = self["menu"].getCurrent()
		name = item[0]
		os.system("opkg remove %s" % item[0])
		self.mbox = self.session.open(MessageBox, _("%s is UnInstalled" % item[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()

	def ARemove(self):
		item = self["menu"].getCurrent()
		os.system("opkg remove -force-remove %s" % item[0])
		self.mbox = self.session.open(MessageBox,_("%s is UnInstalled" % item[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()
#####################################################################################
class downfeed(Screen):
	skin = """
<screen name="downdown" position="center,100" size="750,570" title="insatall extensions from feed">
<widget source="menu" render="Listbox" position="15,10" size="720,500" scrollbarMode="showOnDemand">
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
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/PliPanel/images/green.png" transparent="1" alphatest="on" />
	<widget source="key_red" render="Label" position="20,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_green" render="Label" position="190,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.setup,
				"green": self.setup,
				"red": self.cancel,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		
	def nList(self):
		self.list = []
		os.system("opkg update")
		try:
			ipklist = os.popen("opkg list")
		except:
			pass
		png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/PliPanel/images/ipkmini.png"))
		for line in ipklist.readlines():
			dstring = line.split(" ")
			try:
				endstr = len(dstring[0] + dstring[1]+ dstring[2]+dstring[3]) + 4

				self.list.append((dstring[0]  + " " + dstring[1] + " " + dstring[2], line[endstr:], png))
			except:
				pass
		self["menu"].setList(self.list)
		
	def cancel(self):
		self.close()
		
	def setup(self):
		item = self["menu"].getCurrent()
		name = item[0]
		os.system("opkg install -force-reinstall %s" % name)
		msg  = _("%s is installed" % name)
		self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout = 4 )

##############################################################################
