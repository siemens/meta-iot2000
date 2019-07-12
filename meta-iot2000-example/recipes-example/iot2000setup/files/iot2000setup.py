#!/usr/bin/env python3

from snack import *
import time
from subprocess import call
from subprocess import Popen, PIPE
from subprocess import check_output
import subprocess
import os
import os.path
import stat
import mraa
import sys
import time
from shutil import copyfile

sys.settrace


class ansicolors:
	clear = '\033[2J'
	blue = '\033[1;34m'
	reset = '\033[0m'

interfacesConfig = """# /etc/network/interfaces -- configuration file for ifup(8), ifdown(8)
 
# The loopback interface
auto lo
iface lo inet loopback

"""
dhcpTemplate = """auto [interfaceName]
iface [interfaceName] inet dhcp

"""
staticTemplate = """auto [interfaceName]
iface [interfaceName] inet static
	address [ip]
	netmask 255.255.255.0

"""

wirelessDhcpTemplate = """allow-hotplug wlan0
auto wlan0
iface wlan0 inet dhcp
	wpa-conf /etc/wpa_supplicant.conf

"""
wirelessStaticTemplate = """allow-hotplug wlan0
auto wlan0
iface wlan0 inet static
	address [ip]
	netmask 255.255.255.0
	wpa-conf /etc/wpa_supplicant.conf

"""

wpaFileTemplate = '''ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
update_config=1

network={
	key_mgmt=[type]
	ssid="[ssid]"
	psk="[passwd]"
}'''

repoFileTemplate = '''src/gz all http://[host]/ipk/all
src/gz i586-nlp-32 http://[host]/ipk/i586-nlp-32
src/gz i586-nlp-32-intel-common http://[host]/ipk/i586-nlp-32-intel-common
src/gz iot2000 http://[host]/ipk/iot2000
'''

# Ofono Context Header
apnHeaderStr = "        AccessPointName = "
userHeaderStr = "        Username = "
pwdHeaderStr = "        Password = "

class TopMenu:
	def __init__(self):
		# Use dmidecode to determine device type (IOT2040/IOT2000)
		task = subprocess.Popen("/usr/sbin/dmidecode -t 11 | awk 'NR==8' | cut -f 2 -d :", stdout=subprocess.PIPE, shell=True)
		device = task.stdout.read().decode().lstrip().rstrip()

		self.deviceIsIot2020 = False
		if (device == "IOT2020"):
			self.deviceIsIot2020 = True

	def show(self):
		self.gscreen = SnackScreen()

		menuItems = [
			("OS Settings", OsSettings(self)), 
			("Networking", Networking(self)), 
			("Software", SoftwareSettings(self))]

		menuItems.append(("Peripherals", Peripherals(self)))

		title = "IOT2000 Setup"

		action, selection = ListboxChoiceWindow(
			self.gscreen, 
			title, "", 
			menuItems, 
			[('Quit', 'quit', 'ESC')])


		if(action == 'quit'):
			self.gscreen.finish()
			exit()
		selection.show()

class OsSettings:
	def __init__(self, topmenu):
		self.currentHostname = subprocess.check_output("hostname").decode()
		self.topmenu = topmenu
		self.finish = False

	def show(self):
		while(True and not self.finish):
			action, selection = ListboxChoiceWindow(
				self.topmenu.gscreen, 
				"OS Settings", "",
				[("Change Hostname", self.ChangeHostname),
				 ("Change Password", self.ChangePassword),
				 ("Change Timezone", self.ChangeTimezone)],
				[('Back', 'back', 'ESC')])
			if(action == 'back'):
				return
			selection()

	def ChangeHostname(self):
		ret = EntryWindow(
			self.topmenu.gscreen,
			"Change Host Name",
			"",
			[("Host Name:", self.currentHostname)],
			1,
			70, 50,
			[('OK'), ('Cancel', 'cancel', 'ESC')],
			None)
		if (ret[0] == "ok"):
			subprocess.Popen(["hostname", ret[1][0].rstrip()], stdout=open(os.devnull, 'wb'))
			with open("/etc/hostname", "w") as textfile:
				textfile.write(ret[1][0].rstrip())
			self.finish = True

	def ChangePassword(self):
		self.topmenu.gscreen.finish()
		print(ansicolors.clear) # Clear console 
		subprocess.call("passwd")
		self.finish = True

	def ChangeTimezone(self):
		with open("/usr/share/zoneinfo/zone1970.tab") as zonetab:
			zones = [(zone.split()[2], zone.split()[2]) \
				 for zone in zonetab.readlines() \
				 if not zone.startswith('#')]

		with open("/etc/timezone") as timezone:
			defaultzone = timezone.readline().strip()
		if not (defaultzone, defaultzone) in zones:
			defaultzone = None

		action, selection = ListboxChoiceWindow(
				self.topmenu.gscreen, 
				"Select Timezone", "",
				sorted(zones),
				[("Cancel", "cancel", "ESC")],
				scroll=1, height=20, default=defaultzone)
		if (action == 'cancel'):
			return

		with open("/etc/timezone", "w") as timezone:
			timezone.write(selection + "\n")

		try:
			os.remove("/etc/localtime")
		except FileNotFoundError:
			pass
		os.symlink("/usr/share/zoneinfo/" + selection, "/etc/localtime")

def readFileLines(fileName, startLine):
	fileReading = open(fileName, 'r')
	return "".join(fileReading.readlines()[startLine:])

class Networking:
	def __init__(self, topmenu):
		self.topmenu = topmenu
		self.finish = False
		self.eth0HWPresent = True
		self.eth1HWPresent = not topmenu.deviceIsIot2020
		self.wifiHWPresent = os.path.isdir("/sys/class/net/wlan0")
		self.networkInterfaces = {'eth0': '', 'eth1': '', 'wlan0': ''}
		self.cellularInterface = []
		self.cellularSimInfo = {}

	def show(self):
		self.reconfigWifi = False
		self.interfaceFileChange = False
		self.newSettingsFile = interfacesConfig

		# Get Get current configurations of each interface
		self.getCurrentInterfaces(self.networkInterfaces)
		self.cellularInterface = iot2000Connman.getCellularTechnology()
		self.cellularSimInfo = iot2000Connman.getOfonoSimManager()

		# Show check box
		bb = ButtonBar(self.topmenu.gscreen, (("Ok", "ok"), ("Cancel", "cancel", "ESC")))
		ct = CheckboxTree(height=7, scroll=1, width=40)
		self.showCheckbox(ct)

		gridFormText = "Cross [*] to select active interfaces"
		g = GridForm(self.topmenu.gscreen, gridFormText, 1, 4)
		g.add(ct, 0, 1)
		g.add(bb, 0, 3, growx=1)
		result = g.runOnce()

		if (bb.buttonPressed(result) != "ok"):
			return;

		# Get user selection
		selectedOptions = ct.getSelection()
		eth0Enabled = "eth0" in selectedOptions
		eth1Enabled = "eth1" in selectedOptions
		wifiEnabled = "Wifi" in selectedOptions
		cellularEnabled = "Cellular" in selectedOptions

		# Show sub-config
		if eth0Enabled:
			proceed = self.showEthConfig("eth0")
		if eth1Enabled:
			proceed = self.showEthConfig("eth1")
		if wifiEnabled:
			proceed = self.showWifiConfig("wlan0")
		if cellularEnabled:
			proceed = self.showCellularConfig()
		if not proceed:
			return

		# Show new config
		wpa_conf = readFileLines("/etc/wpa_supplicant.conf", 4)
		self.cellularInterface = iot2000Connman.getCellularTechnology()
		infoText = "Interface config:" + "\n" \
				+ self.newSettingsFile \
				+ "wlan0 config: " + "\n" \
				+ "".join(wpa_conf) + "\n" \
				+ "cellular: " + str(cellularEnabled) + "\n" + "\n".join(self.cellularInterface)
		ret = ButtonChoiceWindow(
			self.topmenu.gscreen,
			"Press OK to enable New Config",
			infoText,
			[("OK", "ok"), ("Cancel", "cancel", "ESC")],
			50, 50,
			None)
		if (ret != "ok"):
			return

		# down unselected interfaces
		if not eth0Enabled:
			subprocess.call("/sbin/ifdown eth0", shell=True, stderr=open(os.devnull, 'wb'))
		if not eth1Enabled:
			subprocess.call("/sbin/ifdown eth1", shell=True, stderr=open(os.devnull, 'wb'))
		if not wifiEnabled:
			subprocess.call("/sbin/ifdown wlan0", shell=True, stderr=open(os.devnull, 'wb'))
		if not cellularEnabled:
			iot2000Connman.disconnectCellular()


		# Write interface file
		fileName = "/etc/network/interfaces"
		backupFileName = "/etc/network/interfaces.bak"
		copyfile(fileName, backupFileName)
		interfacesFile = open(fileName, 'w')
		interfacesFile.write(self.newSettingsFile)
		interfacesFile.close()

		# restartNetwork?
		newTempInterface = {'eth0': '', 'eth1': '', 'wlan0': ''}
		self.getCurrentInterfaces(newTempInterface)
		for key in self.networkInterfaces.keys():
			if newTempInterface[key] != self.networkInterfaces[key]:
				self.interfaceFileChange = True

		if self.interfaceFileChange or self.reconfigWifi:
			self.restartNetwork()

	def showEthConfig(self, interface):
		title = "Configure " + interface
		settings = [(interface, self.networkInterfaces[interface])]
		# ret is tuple type
		ret = EntryWindow(
			self.topmenu.gscreen,
			title,
			"Specify IP addresses for network interfaces, enter 'dhcp' to obtain address by DHCP.",
			settings,
			1,
			70, 50,
			['OK', ('Cancel', 'cancel', 'ESC')],
			None)

		if (ret[0] == "cancel"):
			return False

		# Update eth config
		self.updateNewInterfaceConfig(interface, ret[1][0].rstrip(), settings[0][1])

		return True

	def showWifiConfig(self, interface):
		title = "Configure " + interface
		settings = [(interface, self.networkInterfaces[interface]), ("Type:", "WPA-PSK"), ("SSID:", ""), ("Key:", "")]
		ret = EntryWindow(
			self.topmenu.gscreen,
			title,
			"Specify IP addresses for network interfaces, enter 'dhcp' to obtain address by DHCP.",
			settings,
			1,
			70, 50,
			['OK', ('Cancel', 'cancel', 'ESC')],
			None)

		if (ret[0] == "cancel"):
			return False

		# Update wifi interace
		self.updateNewInterfaceConfig(interface, ret[1][0].rstrip(), settings[0][1])

		# Update wpa config
		for i in range(1, len(settings)):
			if (ret[1][i] != settings[i][1]):
				self.reconfigWifi = True
				break

		wpaConfig = wpaFileTemplate.replace("[type]", ret[1][1].rstrip()).replace("[ssid]", ret[1][2].rstrip()).replace(
			"[passwd]", ret[1][3].rstrip())

		fileName = "/etc/wpa_supplicant.conf"
		backupFileName = "/etc/wpa_supplicant.conf.bak"
		copyfile(fileName, backupFileName)

		wpaFile = open(fileName, 'w')
		wpaFile.write(wpaConfig)
		wpaFile.close()

		return True

	def showCellularConfig(self):
		settings = []

		reconfigAPN = False
		apnDict = iot2000Connman.getOfonoAPN()
		settings.append(("APN:", apnDict[apnHeaderStr]))
		settings.append(("Username:", apnDict[userHeaderStr]))
		settings.append(("Password:", apnDict[pwdHeaderStr]))

		pinStr= self.cellularSimInfo['PinRequired']
		if pinStr == "puk":
			settings.append(("Puk:", ""))
			reconfigPin = True
		elif pinStr == "pin":
			settings.append(("Pin:", ""))
			reconfigPin = True
		elif pinStr == "none":
			reconfigPin = False

		title = "Configure Cellular"
		infoText = "SIM Setting for modem " + self.cellularSimInfo['ModemPath'] \
			+ "\n(leave empty when in doubt)"
		ret = EntryWindow(
			self.topmenu.gscreen,
			title,
			infoText,
			settings,
			1,
			70, 50,
			['OK', ('Cancel', 'cancel', 'ESC')],
			None)

		if (ret[0] == "cancel"):
			return False

		# Update APN config?
		for i in range(len(apnDict)):
			if (ret[1][i] != settings[i][1]):
				reconfigAPN = True
				break

		# Flow: disconnect---set params---connect
		if reconfigAPN or reconfigPin:
			iot2000Connman.disconnectCellular()

		if reconfigPin:
			iot2000Connman.configPin(ret[1][3].rstrip(), pinStr, self.cellularSimInfo['ModemPath'])
			time.sleep(1)
			self.cellularInterface = iot2000Connman.getCellularTechnology()

		iot2000Connman.connectCellular(ret[1][0].rstrip(), ret[1][1].rstrip(), ret[1][2].rstrip())

		return True

	def getInterfaceConfig(self, interface):
		lines = [line.rstrip('\n') for line in open('/etc/network/interfaces')]
		searchString = "auto " + interface
		for lineNumber in range(0, len(lines) - 1):
			if lines[lineNumber].startswith('#'):
				continue
			if (searchString in lines[lineNumber]):
				splitLine = lines[lineNumber].split()

				while (splitLine[0] != "iface"):
					lineNumber += 1
					splitLine = lines[lineNumber].split()
				mode = splitLine[3]
				if (mode == "dhcp"):
					return "dhcp"
				if (mode == "static"):
					while (splitLine[0] != "address"):
						lineNumber += 1
						splitLine = lines[lineNumber].split()
					return splitLine[1]
			lineNumber += 1
		return ""

	def getConfigString(self, interface, config):
		if ("wlan0" == interface):
			if ("dhcp" == config):
				return wirelessDhcpTemplate.replace("[interfaceName]", interface)
			else:
				return wirelessStaticTemplate.replace("[interfaceName]", interface).replace("[ip]", config)

		if ("dhcp" == config):
			return dhcpTemplate.replace("[interfaceName]", interface)
		else:
			return staticTemplate.replace("[interfaceName]", interface).replace("[ip]", config)

	def restartNetwork(self):
		self.topmenu.gscreen.finish()
		print(ansicolors.clear)  # Clear console
		print(ansicolors.reset)
		subprocess.call("/etc/init.d/networking restart", shell=True)

		if (self.wifiHWPresent):
			subprocess.call("/sbin/ifdown wlan0", shell=True)
			subprocess.call("/sbin/ifup wlan0", shell=True)

		self.finish = True

	def getCurrentInterfaces(self, networkDict):
		for key, value in networkDict.items():
			networkDict[key] = self.getInterfaceConfig(key)

	def showCheckbox(self, ct):
		eth0CrossBox = self.eth0HWPresent and len(self.networkInterfaces['eth0'])
		eth1CrossBox = self.eth1HWPresent and len(self.networkInterfaces['eth1'])
		wifiCrossBox = self.wifiHWPresent and len(self.networkInterfaces['wlan0'])

		cellularCrossBox = False
		if len(self.cellularInterface):
			if "  Connected = True" in self.cellularInterface:
				cellularCrossBox = True

		# Show checkbox in case that hardware is present
		if self.eth0HWPresent:
			ct.append("eth0", selected=eth0CrossBox)
		if self.eth1HWPresent:
			ct.append("eth1", selected=eth1CrossBox)
		if self.wifiHWPresent:
			ct.append("Wifi", selected=wifiCrossBox)
		if 'ModemPath' in self.cellularSimInfo:
			if len(self.cellularSimInfo['ModemPath']) > 0:
				ct.append("Cellular", selected=cellularCrossBox)

	def updateNewInterfaceConfig(self, interface, newConfig, oldConfig):
		# Invalid newConfig if it is blank
		if len(newConfig) > 0:
			self.newSettingsFile += self.getConfigString(interface, newConfig)
		elif len(oldConfig) > 0:
			self.newSettingsFile += self.getConfigString(interface, oldConfig)


class SoftwareSettings:
	def __init__(self, topmenu):
		self.topmenu = topmenu
		self.finish = False

	def show(self):
		while(True and not self.finish):
			action, selection = ListboxChoiceWindow(
				self.topmenu.gscreen, 
				"Software", "",
				[("Set Package Repository", self.setRepo),("Manage Packages", self.changePackages),("Manage Autostart Options", self.changeAutostart)],
				[('Back', 'back', 'ESC')])
			if(action == 'back'):
				return
			selection()

	def setRepo(self):
		ret = EntryWindow(
			self.topmenu.gscreen,
			"Please enter a valid address for a opkg package repository (IP or host name only).",
			"",
			[("Host Address:", "")],
			1,
			70, 50,
			['OK', ('Cancel', 'cancel', 'ESC')],
			None)
		if(ret[0] != "ok"):
			return
		opkgConfig = repoFileTemplate.replace("[host]", ret[1][0].rstrip())
		with open("/etc/opkg/iot2000.conf", "w") as textfile:
			textfile.write(opkgConfig)

		self.topmenu.gscreen.finish()
		print(ansicolors.clear) # Clear console
		print(ansicolors.reset)
		finish = True

	def changePackages(self):
		### Edit here ###
		# Contains all potential candidates for removal
		packageList = ["galileo-target", "nodejs", "tcf-agent"]
		###
		
		bb = ButtonBar(self.topmenu.gscreen, (("Ok", "ok"), ("Cancel", "cancel")))
		ct = CheckboxTree(height = 10, scroll = 1,width=40)

		# Iterate through list of removal candidates and check if they are 
		# actually installed.
		task = subprocess.Popen("/usr/bin/opkg list-installed", stdout=subprocess.PIPE, shell=True)
		installedPackages = task.stdout.read().decode()

		numberOfRemovablePackages = 0
		for package in packageList:
			if (package in installedPackages):
				ct.append(package)
				numberOfRemovablePackages += 1

		g = GridForm(self.topmenu.gscreen, "Select Packages to Remove", 1, 4)
		l = Label("Use 'Space' to select the packages you want to remove.")
		g.add(l, 0, 0, growy=1, growx=1, padding=(1,1,1,1))
		g.add(ct, 0, 1)
		g.add(bb, 0, 3, growx = 1)
		result = g.runOnce()
		
		removeList = ''
		if (bb.buttonPressed(result) != "ok" or numberOfRemovablePackages < 1):
			return;
		# Build list of selected packages
		selectedPackages = ct.getSelection()
		for package in selectedPackages:
			removeList = removeList + package + '* '
		
		ret = ButtonChoiceWindow(
			self.topmenu.gscreen,
			"Remove Packages",
			"Are you sure you want to remove the following packages: \n\n" + removeList,
			buttons=[("OK", "ok"), ("Cancel", "cancel", "ESC")],
			width=40)

		if (ret != "ok"):
			return

		removeList = "/usr/bin/opkg --force-removal-of-dependent-packages remove " + removeList
		self.topmenu.gscreen.finish()
		print(ansicolors.clear)
		print(ansicolors.reset)
		subprocess.call(removeList, shell=True)
		self.finish = True

	def changeAutostart(self):
		nodeRedEnabled = self.serviceEnabled("node-red")
		sshEnabled = self.serviceEnabled("sshd")
		mosquittoEnabled = self.serviceEnabled("mosquitto")
		galileoEnabled = self.serviceEnabled("galileod")
		tcfEnabled = self.serviceEnabled("tcf-agent")

		bb = ButtonBar(self.topmenu.gscreen, (("Ok", "ok"), ("Cancel", "cancel", "ESC")))
		ct = CheckboxTree(height = 7, scroll = 1,width=40)

		ct.append("Node-RED", "node-red", selected=nodeRedEnabled)
		ct.append("SSH Server", "ssh", selected=sshEnabled)
		ct.append("Mosquitto Broker", "mosquitto", selected=mosquittoEnabled)
		ct.append("Galileo Arduino Runtime", "galileo", selected=galileoEnabled)
		ct.append("TCF Debugger Agent", "tcf", selected=tcfEnabled)

		g = GridForm(self.topmenu.gscreen, "Autostart Services", 1, 4)
		g.add(ct, 0, 1)
		g.add(bb, 0, 2, growx = 1)
		result = g.runOnce()
		if (bb.buttonPressed(result) != "ok"):
			return;

		selectedOptions = ct.getSelection()

		nodeRedEnabledNew = "node-red" in selectedOptions
		sshEnabledNew = "ssh" in selectedOptions
		mosquittoEnabledNew = "mosquitto" in selectedOptions
		galileoEnabledNew = "galileo" in selectedOptions
		tcfEnabledNew = "tcf" in selectedOptions

		if (nodeRedEnabled != nodeRedEnabledNew):
			self.update_rc("node-red", nodeRedEnabledNew)
		if (sshEnabled != sshEnabledNew):
			self.update_rc("sshd", sshEnabledNew)
		if (mosquittoEnabled != mosquittoEnabledNew):
			self.update_rc("mosquitto", mosquittoEnabledNew)
		if (galileoEnabled != galileoEnabledNew):
			self.update_rc("galileod", galileoEnabledNew)
		if (tcfEnabled != tcfEnabledNew):
			self.update_rc("tcf-agent", tcfEnabledNew)

	def update_rc(self, service, enable):
		with open(os.devnull, 'wb') as devnull:
			if (enable):
				subprocess.call("update-rc.d %s defaults" % service, shell=True, stdout=devnull)
				subprocess.call("/etc/init.d/%s start" % service, shell=True, stdout=devnull)
			else:
				subprocess.call("/etc/init.d/%s stop" % service, shell=True, stdout=devnull)
				subprocess.call("update-rc.d -f %s remove" % service, shell=True, stdout=devnull, stderr=devnull)

	def serviceEnabled(self, service):
		task = subprocess.Popen("/etc/init.d/%s status" % service, stdout=subprocess.PIPE, shell=True)
		taskReturn = task.stdout.read().decode().lstrip().rstrip()
		return "running" in taskReturn

class Peripherals:
	def __init__(self, topmenu):
		self.topmenu = topmenu
		self.finish = False
		self.comPortsPresent = os.path.isdir("/dev/ttyS2")

	def show(self):
		menuItems = [("Show I/O Configuration", self.showIoConfiguration), ("Enable I2C on Pins A4 & A5", self.enableI2c), ("Enable SPI on Pins D10-D13", self.enableSpi), ("Enable UART0 on Pins D0 & D1", self.enableUart0)]
		if (not self.topmenu.deviceIsIot2020):
			menuItems.insert(0, ("Configure External COM Ports", self.configureComPorts))
		while(True and not self.finish):
			action, selection = ListboxChoiceWindow(
				self.topmenu.gscreen, 
				"Peripherals", "",
				menuItems,
				[('Back', 'back', 'ESC')])
			if(action == 'back'):
				return
			selection()

	def enableUart0(self):	
		u=mraa.Uart(0)
		self.showIoConfiguration()

	def enableSpi(self):
		s=mraa.Spi(0)
		self.showIoConfiguration()

	def enableI2c(self):
		x = mraa.I2c(0)
		self.showIoConfiguration()

	def showIoConfiguration(self):
		s = "       Pin     |  Function\n   ------------+------------\n"
		for i in range(0,20):
			s = s + "   IO" + "{:<10}".format(str(i))
			if (i == 0):
				if (self.getPinValue(45) == 1):
					s = s + "|   UART 0 RX"
				else:
					s = s + "|   GPIO"
			elif (i == 1):
				if (self.getPinValue(45) == 1):
					s = s + "|   UART 0 TX"
				else:
					s = s + "|   GPIO"
			if (i == 2):
				if (self.getPinValue(77) == 1):
					s = s + "|   UART 1 RX"
				else:
					s = s + "|   GPIO"
			elif (i == 3):
				if (self.getPinValue(76) == 1):
					s = s + "|   UART 1 TX"
				else:
					if (self.getPinValue(64) == 1):
						s = s + "|   PWM"
					else:
						s = s + "|   GPIO"
			if (i == 4):
				s = s + "|   GPIO"
			elif (i == 5):
				if (self.getPinValue(66) == 1):
					s = s + "|   PWM"
				else:
					s = s + "|   GPIO"
			if (i == 6):
				if (self.getPinValue(68) == 1):
					s = s + "|   PWM"
				else:
					s = s + "|   GPIO"
			elif (i == 7):
				s = s + "|   GPIO"	
			elif (i == 8):	
				s = s + "|   GPIO"
			elif (i == 9):
				s = s + "|   GPIO"
			elif (i == 10):
				if (self.getPinValue(74) == 1):
					s = s + "|   PWM"
				if (self.getPinValue(44) == 1):
					s = s + "|   SPI SS"
				else:
					s = s + "|   GPIO"
			elif (i == 11):
				if (self.getPinValue(44) == 1):
						s = s + "|   SPI MOSI"
				else:
					s = s + "|   GPIO"
			elif (i == 12):
				if (self.getPinValue(46) == 1):
					s = s + "|   SPI MISO"
				else:
					s = s + "|   GPIO"
			elif (i == 13):
				if (self.getPinValue(46) == 1):
					s = s + "|   SPI SCK"
				else:
					s = s + "|   GPIO"
			elif (i == 14):
				s = s + "|   GPIO/ADC0"
			elif (i == 15):
				s = s + "|   GPIO/ADC1"
			elif (i == 16):
				s = s + "|   GPIO/ADC2"
			elif (i == 17):	
				s = s + "|   GPIO/ADC3"
			elif (i == 18):	
				if (self.getPinValue(60) == 1):
					if (self.getPinValue(78) == 1):
						s = s + "|   GPIO"
					else:
						s = s + "|   ADC4"
				else:
					s = s + "|   I2C SDA"
			elif (i == 19):	
				if (self.getPinValue(60) == 1):
					if (self.getPinValue(79) == 1):
						s = s + "|   GPIO"
					else:
						s = s + "|   ADC5"
				else:
					s = s + "|   I2C SCL"

			s += "\n"

		rv = ButtonChoiceWindow( 
				self.topmenu.gscreen, 
				"I/O Configuration Overview", 
				s, 
				buttons=["Back"], 
				width=40) 

	def exportPin(self, pin):
		subprocess.call('echo -n "' + str(pin) + '" > /sys/class/gpio/export', shell=True, stderr=open(os.devnull, 'wb'), stdout=open(os.devnull, 'wb'))

	def pinDirection(self, pin, direction):
		if (direction == "in" or direction == "out"):
			subprocess.call('echo -n "' + str(direction) + '" > /sys/class/gpio/gpio' + str(pin) + '/direction', shell=True, stderr=open(os.devnull, 'wb'), stdout=open(os.devnull, 'wb'))

	def getPinValue(self, pin):
		self.exportPin(pin)
		return int(check_output(["cat", '/sys/class/gpio/gpio' + str(pin) +'/value']))		
	
	def configureComPorts(self):
		portAction, portSelection = ListboxChoiceWindow(
			self.topmenu.gscreen,
			"Configure Serial Mode", "Select the serial port you want to configure and press 'Enter'.",
			["X30", "X31"],
			[('Cancel', 'cancel', 'ESC')])
		if (portSelection == 0):
			portName = "X30"
		else:
			portName = "X31"

		currentMode = self.getSerialModeForPort(portName)

		if (portAction == "cancel"):
			return
		modes = ["RS232", "RS485", "RS422"]

		modeAction, modeSelection = ListboxChoiceWindow(
			self.topmenu.gscreen, 
			"Configure Serial Mode", "Select a mode.",
			modes, 
			[('Cancel', 'cancel', 'ESC')], default=currentMode)

		if (modeAction == "cancel"):
			return
		persistentReturn = ButtonChoiceWindow(
			self.topmenu.gscreen,
			"Configure Serial Mode",
			"Do you want to make your changes persistent? (Mode setting will be kept after reboot.) ",
			buttons=[("Yes", "yes"), ("No", "no", "ESC")],
			width=40)
		switchTool = '/usr/bin/switchserialmode'

		if (portSelection == 0):
			switchDeviceArg = '/dev/ttyS2'
		else:
			switchDeviceArg = '/dev/ttyS3'

		switchModeArg = modes[modeSelection].lower()
		switchCommand = switchTool + " " + switchDeviceArg + " " + switchModeArg
		subprocess.Popen([switchTool, switchDeviceArg, switchModeArg], stdout=open(os.devnull, 'wb'))

		if (persistentReturn == "yes"):
			fileName = "set_serial_mode_" + portName + ".sh"
			filePath = "/etc/init.d/" + fileName
			initFile = open(filePath, 'w')
			initFile.write("#!/bin/sh\n" + switchCommand)
			initFile.close()

			st = os.stat(filePath)
			os.chmod(filePath, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
			subprocess.call("update-rc.d " + fileName + " defaults", shell=True, stdout=open(os.devnull, 'wb'))

	def getSerialModeForPort(self, port):
		fileName = "/etc/init.d/set_serial_mode_" + port + ".sh"
		if (os.path.isfile(fileName)):
			lines = [line.rstrip('\n') for line in open(fileName)]
			selectedMode = lines[1].split()[2]

			if selectedMode == "rs232":
				return 0
			elif selectedMode == "rs485":
				return 1
			elif selectedMode == "rs422":
				return 2
		return 0

class connmanManager:
	def __init__(self):
		self.ethSupport = True
		self.wifiSupport = True
		self.cellularSupport = True
		self.bluetoothSupport = False

		self.connmanTechnologies = []
		self.connmanServices = []
		self.connmanSettings = ""
		self.connmanConfigs = ""
		self.cellularTechnology = []
		self.cellularContext = ""
		self.cellularCarrier = ""

	def isOfonoRunning(self):
		cellularOfono = False
		task = subprocess.Popen("ps aux | grep -v grep | grep -i ofonod", stdout=subprocess.PIPE, shell=True)
		if len(task.stdout.read().decode()) > 0:
			cellularOfono = True
		return cellularOfono

	def getOfonoSimManager(self):
		ofonoSimManager = {'Present': False, 'PinRequired': "none", 'LockedPins': False}

		task = subprocess.Popen("/usr/lib/ofono/test/list-modems", stdout=subprocess.PIPE, shell=True)
		ofonoModemInfo = task.stdout.read().decode()

		if len(ofonoModemInfo) > 0:
			if ofonoModemInfo.find("Present = 1") >= 0:
				ofonoSimManager['Present'] = True
			if ofonoModemInfo.find("LockedPins = pin") >= 0:
				ofonoSimManager['LockedPins'] = True
			if ofonoModemInfo.find("PinRequired = pin") >= 0:
				ofonoSimManager['PinRequired'] = "pin"
			elif ofonoModemInfo.find("PinRequired = puk") >= 0:
				ofonoSimManager['PinRequired'] = "puk"
			# Add dynamic ModemPath
			modemPathStart = ofonoModemInfo.index('[')
			modemPathEnd = ofonoModemInfo.index(']')
			modemPathStr = ofonoModemInfo[modemPathStart+2:modemPathEnd-1]
			ofonoSimManager['ModemPath'] = modemPathStr
		return ofonoSimManager

	def getOfonoAPN(self):
		apnDict = {apnHeaderStr:"", userHeaderStr:"", pwdHeaderStr:""}
		task = subprocess.Popen("/usr/lib/ofono/test/list-contexts", stdout=subprocess.PIPE, shell=True)
		ofonoContextList = task.stdout.read().decode().split('\n')
		for key in apnDict.keys():
			for i in range(len(ofonoContextList)):
				if ofonoContextList[i].find(key) >= 0:
					apnDict[key] = ofonoContextList[i][len(key):]
					break
		return apnDict

	def getConnmanTechnologies(self):
		self.connmanTechnologies = []
		self.cellularTechnology = []
		if self.isOfonoRunning():
			task = subprocess.Popen("/usr/bin/connmanctl technologies", stdout=subprocess.PIPE, shell=True)
			self.connmanTechnologies = task.stdout.read().decode().split('\n')
			for i in range(len(self.connmanTechnologies)):
				if self.connmanTechnologies[i].find('cellular') >= 0:
					self.cellularTechnology = self.connmanTechnologies[i: i + 6]
					break

	def getCellularTechnology(self):
		self.getConnmanTechnologies()
		return self.cellularTechnology

	def getCellularContext(self):
		self.cellularContext = ""
		self.cellularCarrier = ""
		task = subprocess.Popen("/usr/bin/connmanctl services", stdout=subprocess.PIPE, shell=True)
		self.connmanServices = task.stdout.read().decode().split()
		for i in range(len(self.connmanServices)):  # find the first cellular context
			if self.connmanServices[i].find('cellular') >= 0:
				self.cellularContext = self.connmanServices[i]
				self.cellularCarrier = self.connmanServices[i - 1]
				break

	def getConnmanSettings(self):
		file = open("/var/lib/connman/settings")
		self.connmanSettings = file.read()
		file.close()

	def connectCellular(self, apn, user, pwd):
		if not self.isOfonoRunning():
			print("ofono is not running")
		else:
			if len(self.cellularTechnology) > 0:
				# if modem need poweron
				if "  Powered = False" in self.cellularTechnology:
					self.powerOnCellular()

				# connect Cellular
				self.connectCellularContext()

				# real connected?
				if "  Connected = False" in self.getCellularTechnology():
					self.initCellular(apn, user, pwd)
			else:
				print("--No cellular technology!!!---")

	def initCellular(self, apn, user, pwd):
		print("The Cellular need initialization")
		internetContext = apn+" "+user+" "+pwd
		subprocess.call("/usr/lib/ofono/test/create-internet-context " + internetContext, shell=True,
				stderr=open(os.devnull, 'wb'))
		subprocess.call("/usr/lib/ofono/test/online-modem", shell=True, stderr=open(os.devnull, 'wb'))
		time.sleep(3)

		# connect Cellular
		self.connectCellularContext()

		# real connected?
		if "  Connected = False" in self.getCellularTechnology():
			print("Cellular connection is failed")

	def connectCellularContext(self):
		# get cellular service and context
		self.getCellularContext()
		# Connect cellularlo
		if len(self.cellularContext) > 0:
			subprocess.call("/usr/bin/connmanctl connect " + self.cellularContext, shell=True, stderr=open(os.devnull, 'wb'))

	def powerOnCellular(self):
		subprocess.call("/usr/bin/connmanctl enable cellular", shell=True, stderr=open(os.devnull, 'wb'))
		print("Cellular is in poweron, need to wait")
		time.sleep(5)

	def disconnectCellular(self):
		# get cellular service
		self.getCellularContext()
		subprocess.call("/usr/bin/connmanctl disconnect " + self.cellularContext, shell=True,
				stderr=open(os.devnull, 'wb'))

	def configPin(self, pinCode, pinStr, path):
		pinArgs = path + " " + pinStr + " " + pinCode
		subprocess.call("/usr/lib/ofono/test/enter-pin "+pinArgs, shell=True,
						stderr=open(os.devnull, 'wb'))
		subprocess.call("/usr/lib/ofono/test/unlock-pin "+pinArgs, shell=True,
						stderr=open(os.devnull, 'wb'))

iot2000Connman = connmanManager()

mainwindow = TopMenu()
while(True):
	mainwindow.show()
