#!/usr/bin/env python3
from __future__ import absolute_import, print_function, unicode_literals

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

# Wired interfaces
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
	
class TopMenu:
	def __init__(self):
		
		# Use dmidecode to determine device type (IOT2040/IOT2000)
		task = subprocess.Popen("/usr/sbin/dmidecode -t 11 | awk 'NR==8' | cut -f 2 -d :", stdout=subprocess.PIPE, shell=True)
		device = task.stdout.read().lstrip().rstrip()

		self.deviceIsIot2020 = False
		if (device == "IOT2020"):
			self.deviceIsIot2020 = True
	def show(self):
		self.gscreen = SnackScreen()

		menuItems = [
			("OS Settings", OsSettings(self)), 
			("Networking", Networking(self)), 
			("Software", SoftwareSettings(self))]

		if (not self.deviceIsIot2020):
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
				("Change Password", self.ChangePassword)], 
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

class Networking:
	def __init__(self, topmenu):
		self.topmenu = topmenu
		self.finish = False
		self.eth1present = not topmenu.deviceIsIot2020
		self.wifiPresent = os.path.isdir("/sys/class/net/wlan0")
	def show(self):
		menuItems = [("Configure Interfaces", self.configureInterfaces)]
		if(self.wifiPresent):
			menuItems.append(("Connect Wifi", self.configureWifi))
		while(True and not self.finish):
			action, selection = ListboxChoiceWindow(
				self.topmenu.gscreen, 
				"Networking", "",
				menuItems,
				[('Back', 'back', 'ESC')])
			if(action == 'back'):
				return
			selection()
	def configureInterfaces(self):
		interfaces = ["eth0"]
		if(self.eth1present):
			interfaces.append("eth1")
		if(self.wifiPresent):
			interfaces.append("wlan0")
		settings = []
		for entry in interfaces:
			settings.append((entry, self.getInterfaceConfig(entry)))
		ret = EntryWindow(
			self.topmenu.gscreen,
			"Configure Network Interfaces",
			"Specify IP addresses for network interfaces, enter 'dhcp' to obtain address by DHCP.",
			settings,
			1,
			70, 50,
			['OK', ('Cancel', 'cancel', 'ESC')],
			None)
			
		if(ret[0] == "cancel"):
			return;

		newValues = ret[1]
		settingsChanged = False
		newSettingsFile = interfacesConfig
		
		for i in range(len(settings)):
			if(newValues[i] != settings[i][1]):
				settingsChanged = True
			newSettingsFile += self.getConfigString(settings[i][0], newValues[i])
		if(not settingsChanged):
			return
		
		fileName = "/etc/network/interfaces"
		backupFileName = "/etc/network/interfaces.bak"
		copyfile(fileName, backupFileName)
		interfacesFile = open(fileName, 'w')
		interfacesFile.write(newSettingsFile)
		interfacesFile.close()
		
		self.restartNetwork()
	def getInterfaceConfig(self, interface):
		lines = [line.rstrip('\n') for line in open('/etc/network/interfaces')]
		for lineNumber in range(0, len(lines)-1):
			searchString = "auto " + interface

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
		if("wlan0" == interface):
			if("dhcp" == config):
				return wirelessDhcpTemplate.replace("[interfaceName]", interface)
			else:
				return wirelessStaticTemplate.replace("[interfaceName]", interface).replace("[ip]", config)
		if("dhcp" == config):
			return dhcpTemplate.replace("[interfaceName]", interface)
		else:
			return staticTemplate.replace("[interfaceName]", interface).replace("[ip]", config)
	def restartNetwork(self):
		self.topmenu.gscreen.finish()
		print(ansicolors.clear) # Clear console
		print(ansicolors.reset)
		subprocess.call("/etc/init.d/networking restart", shell=True)
		
		if(self.wifiPresent):
			subprocess.call("/sbin/ifdown wlan0", shell=True)
			subprocess.call("/sbin/ifup wlan0", shell=True)
		
		self.finish = True
	def configureWifi(self):
		ret = EntryWindow(
			self.topmenu.gscreen,
			"Configure WLAN",
			"",
			[("Type:", "WPA-PSK"), ("SSID:", ""), ("Key:", "")],
			1,
			70, 50,
			['OK', ('Cancel', 'cancel', 'ESC')],
			None)
		if(ret[0] != "ok"):
			return
		
		wpaConfig = wpaFileTemplate.replace("[type]", ret[1][0].rstrip()).replace("[ssid]", ret[1][1].rstrip()).replace("[passwd]", ret[1][2].rstrip())
		
		fileName = "/etc/wpa_supplicant.conf"
		
		backupFileName = "/etc/wpa_supplicant.conf.bak"
		copyfile(fileName, backupFileName)
		
		wpaFile = open(fileName, 'w')
		wpaFile.write(wpaConfig)
		wpaFile.close()
		
		self.restartNetwork()

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
		packageList = ["galileo-target", "nodejs", "tcf-agent"] 	# Contains all potential 
		# candidates for removal
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
		task = subprocess.Popen("/etc/init.d/sshd status", stdout=subprocess.PIPE, shell=True)
		taskReturn = task.stdout.read().decode().lstrip().rstrip()
		sshEnabled = "running" in taskReturn
		
		noderedAutostartEnabled = os.path.isfile("/etc/init.d/launch_node-red.sh")
		mosquittoAutostartEnabled = os.path.isfile("/etc/init.d/launch_mosquitto.sh")
		
		bb = ButtonBar(self.topmenu.gscreen, [("Done", "done", "ESC")])
		ct = CheckboxTree(height = 7, scroll = 1,width=40)

		ct.append("Auto Start node-red", selected=noderedAutostartEnabled)
		ct.append("SSH Server Enabled", selected=sshEnabled)
		ct.append("Auto Start Mosquitto Broker", selected=mosquittoAutostartEnabled)

		g = GridForm(self.topmenu.gscreen, "Advanced Options", 1, 4)
		g.add(ct, 0, 1)
		g.add(bb, 0, 3, growx = 1)
		result = g.runOnce()
		selectedOptions = ct.getSelection()

		noderedAutostartEnabledNew = "Auto Start node-red" in selectedOptions
		sshEnabledNew = "SSH Server Enabled" in selectedOptions
		mosquittoAutostartEnabledNew = "Auto Start Mosquitto Broker" in selectedOptions
		
		if (noderedAutostartEnabled != noderedAutostartEnabledNew):
			if ("Auto Start node-red" in selectedOptions):
				self.registerLaunchScript("on", "launch_node-red.sh", "#!/bin/sh\nsu root -c \"/usr/bin/node /usr/lib/node_modules/node-red/red >/dev/null\" &")
			else:
				self.registerLaunchScript("off", "launch_node-red.sh", "")
				
		if (sshEnabled != sshEnabledNew):
			if ("SSH Server Enabled" in selectedOptions):
				changeSshServerSetting("on")
			else:
				changeSshServerSetting("off")

		if (mosquittoAutostartEnabled != mosquittoAutostartEnabledNew):
			if ("Auto Start Mosquitto Broker" in selectedOptions):
				self.registerLaunchScript("on", "launch_mosquitto.sh", "#!/bin/sh\nsu root -c \"/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf -d &>/dev/null\" ")

				fileName = "/etc/mosquitto/mosquitto.conf"
				initFile = open(fileName, 'w')
				initFile.write("user root")
				initFile.close()
			else:
				self.registerLaunchScript("off", "launch_mosquitto.sh", "")
	def changeSshServerSetting(self, status):
		if (status == "on"):
			subprocess.call("update-rc.d -f sshd defaults", shell=True, stdout=open(os.devnull, 'wb'))
			subprocess.call("/etc/init.d/sshd start", shell=True, stdout=open(os.devnull, 'wb'))
		elif (status == "off"):
			subprocess.call("/etc/init.d/sshd stop", shell=True, stdout=open(os.devnull, 'wb'))
			subprocess.call("update-rc.d -f sshd remove", shell=True, stdout=open(os.devnull, 'wb'))
	def registerLaunchScript(self, status, fileName, scriptcontent):
		if (status == "on"):
			initFile = open("/etc/init.d/" + fileName, 'w')
			initFile.write(scriptcontent)
			initFile.close()

			st = os.stat("/etc/init.d/" + fileName)
			os.chmod("/etc/init.d/" + fileName, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

			subprocess.call("update-rc.d " + fileName + " defaults", shell=True, stdout=open(os.devnull, 'wb'))
			subprocess.call("/etc/init.d/" + fileName, shell=True, stdout=open(os.devnull, 'wb'))
		elif (status == "off"):
			subprocess.call("update-rc.d " + fileName + " remove", shell=True, stdout=open(os.devnull, 'wb'))
			os.remove("/etc/init.d/" + fileName)

class Peripherals:
	def __init__(self, topmenu):
		self.topmenu = topmenu
		self.finish = False
		self.comPortsPresent = os.path.isdir("/dev/ttyS2")
	def show(self):
		menuItems = [("Configure External COM Ports", self.configureComPorts), ("Show I/O Configuration", self.showIoConfiguration), ("Enable I2C on Pins A4 & A5", self.enableI2c), ("Enable SPI on Pins D10-D13", self.enableSpi), ("Enable UART0 on Pins D0 & D1", self.enableUart0)]
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
#repoFileTemplate
mainwindow = TopMenu()
while(True):
	mainwindow.show()


