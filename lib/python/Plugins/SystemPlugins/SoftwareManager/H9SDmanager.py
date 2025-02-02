from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from boxbranding import getMachineBuild
from Components.ActionMap import ActionMap
from Components.ChoiceList import ChoiceList, ChoiceEntryComponent
from Components.config import config
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.SystemInfo import SystemInfo
from Tools.BoundFunction import boundFunction
from enigma import getDesktop

def esHD():
	if getDesktop(0).size().width() > 1400:
		return True
	else:
		return False

class H9SDmanager(Screen):

	if esHD():
		skin = """
		<screen name="H9SDmanager" position="400,75" size="1125,1250" flags="wfNoBorder" backgroundColor="transparent">
		<eLabel name="b" position="0,0" size="1125,950" backgroundColor="#00ffffff" zPosition="-2" />
		<eLabel name="a" position="1,1" size="1122,947" backgroundColor="#00000000" zPosition="-1" />
		<widget source="Title" render="Label" position="90,15" foregroundColor="#00ffffff" size="720,75" halign="left" font="RegularHD; 28" backgroundColor="#00000000" />
		<eLabel name="line" position="1,90" size="1122,1" backgroundColor="#00ffffff" zPosition="1" />
		<eLabel name="line2" position="1,375" size="1122,6" backgroundColor="#00ffffff" zPosition="1" />
		<widget source="labe14" render="Label" position="3,120" size="1095,45" halign="center" font="RegularHD; 22" backgroundColor="#00000000" foregroundColor="#00ffffff" />
		<widget source="key_red" render="Label" position="45,300" size="225,45" noWrap="1" zPosition="1" valign="center" font="RegularHD; 20" halign="left" backgroundColor="#00000000" foregroundColor="#00ffffff" />
		<widget source="key_green" render="Label" position="300,300" size="225,45" noWrap="1" zPosition="1" valign="center" font="RegularHD; 20" halign="left" backgroundColor="#00000000" foregroundColor="#00ffffff" />
		<ePixmap pixmap="buttons/red_HD.png" position="55,300" size="225,60" alphatest="blend" />
		<ePixmap pixmap="buttons/green_HD.png" position="304,300" size="225,60" alphatest="blend" />
		</screen>"""
	else:
		skin = """
		<screen name="H9SDmanager" position="250,50" size="750,850" flags="wfNoBorder" backgroundColor="transparent">
		<eLabel name="b" position="0,0" size="750,650" backgroundColor="#00ffffff" zPosition="-2" />
		<eLabel name="a" position="1,1" size="748,648" backgroundColor="#00000000" zPosition="-1" />
		<widget source="Title" render="Label" position="60,10" foregroundColor="#00ffffff" size="480,50" halign="left" font="Regular; 28" backgroundColor="#00000000" />
		<eLabel name="line" position="1,60" size="748,1" backgroundColor="#00ffffff" zPosition="1" />
		<eLabel name="line2" position="1,250" size="748,4" backgroundColor="#00ffffff" zPosition="1" />
		<widget source="labe14" render="Label" position="2,80" size="730,30" halign="center" font="Regular; 22" backgroundColor="#00000000" foregroundColor="#00ffffff" />
		<widget source="key_red" render="Label" position="30,200" size="158,30" noWrap="1" zPosition="1" valign="center" font="Regular; 20" halign="left" backgroundColor="#00000000" foregroundColor="#00ffffff" />
		<widget source="key_green" render="Label" position="200,200" size="155,30" noWrap="1" zPosition="1" valign="center" font="Regular; 20" halign="left" backgroundColor="#00000000" foregroundColor="#00ffffff" />
		<ePixmap pixmap="buttons/red.png" position="35,200" size="150,40" alphatest="blend" />
		<ePixmap pixmap="buttons/green.png" position="205,200" size="150,40" alphatest="blend" />
		</screen>"""

	def __init__(self, session,menu_path=""):
		Screen.__init__(self, session)
		self.skinName = "H9SDmanager"
		screentitle = _("H9 SDcard manager")

		self.menu_path = menu_path
		if config.usage.show_menupath.value == 'large':
			self.menu_path += screentitle
			title = self.menu_path
			self["menu_path_compressed"] = StaticText("")
			self.menu_path += ' / '
		elif config.usage.show_menupath.value == 'small':
			title = screentitle
			condtext = ""
			if self.menu_path and not self.menu_path.endswith(' / '):
				condtext = self.menu_path + " >"
			elif self.menu_path:
				condtext = self.menu_path[:-3] + " >"
			self["menu_path_compressed"] = StaticText(condtext)
			self.menu_path += screentitle + ' / '
		else:
			title = screentitle
			self["menu_path_compressed"] = StaticText("")
		Screen.setTitle(self, title)
		self.title = screentitle
		self["labe14"] = StaticText(_("Press appropiate Init to move Nand root to SDcard."))
		self["key_red"] = StaticText(_("Reboot"))
		self["key_green"] = StaticText(_("Init SDcard"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"red": self.reboot,
			"green": self.SDInit,
			"ok": boundFunction(self.close, None),
			"cancel": boundFunction(self.close, None),
		}, -1)
		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(self.title)

	def SDInit(self):
		if SystemInfo["HasH9SD"]:
			self.TITLE = _("Init Zgemma H9 SDCARD - please reboot after use.")
			cmdlist = []
			cmdlist.append("opkg update")
			cmdlist.append("opkg install rsync")
			cmdlist.append("umount /dev/mmcblk0p1")
			cmdlist.append("dd if=/dev/zero of=/dev/mmcblk0p1 bs=1M count=150")
			cmdlist.append('mkfs.ext4 -L "H9-ROOTFS" /dev/mmcblk0p1')
			cmdlist.append("mkdir /tmp/mmc")
			cmdlist.append("mount /dev/mmcblk0p1 /tmp/mmc")
			cmdlist.append("mkdir /tmp/root")
			cmdlist.append("mount --bind / /tmp/root")
			cmdlist.append("rsync -aAX /tmp/root/ /tmp/mmc/")
			cmdlist.append("umount /tmp/root")
			cmdlist.append("umount /tmp/mmc")
			cmdlist.append("rmdir /tmp/root")
			cmdlist.append("rmdir /tmp/mmc")
			self.session.open(Console, title = self.TITLE, cmdlist = cmdlist, closeOnSuccess = True)
		else:
			self.close()

	def reboot(self):
		self.session.open(TryQuitMainloop, 2)

	def USBInit(self):
			self.TITLE = _("Init Zgemma H9 USB/SDA1 - please reboot after use.")
			cmdlist = []
			cmdlist.append("opkg update")
			cmdlist.append("opkg install rsync")
			cmdlist.append("umount /dev/mmcblk0p1")
			cmdlist.append("dd if=/dev/zero of=/dev/sda1 bs=1M count=150")
			cmdlist.append('mkfs.ext4 -L "H9-ROOTFS" /dev/sda1')
			cmdlist.append("mkdir /tmp/mmc")
			cmdlist.append("mount /dev/mmcblk0p1 /tmp/mmc")
			cmdlist.append("mkdir /tmp/root")
			cmdlist.append("mount --bind / /tmp/root")
			cmdlist.append("rsync -aAX /tmp/root/ /tmp/mmc/")
			cmdlist.append("umount /tmp/root")
			cmdlist.append("umount /tmp/mmc")
			cmdlist.append("rmdir /tmp/root")
			cmdlist.append("rmdir /tmp/mmc")
			self.session.open(Console, title = self.TITLE, cmdlist = cmdlist, closeOnSuccess = True)
