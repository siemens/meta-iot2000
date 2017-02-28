#!/usr/bin/python

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
from shutil import copyfile

networkConfigurationChanged = False
wifiEnabled = True
wifiInterfaceConfigured = True
deviceIsIot2020 = False

class ansicolors:
	clear = '\033[2J'
	blue = '\033[1;34m'
	reset = '\033[0m'
def initScreen():
	global gscreen
	gscreen = SnackScreen()
	
def displayStartScreen():
	global wifiEnabled
	global deviceIsIot2020
	
	initScreen()
	
	# Use dmidecode to determine device type (IOT2040/IOT2000)
	task = subprocess.Popen("/usr/sbin/dmidecode -t 11 | awk 'NR==8' | cut -f 2 -d :", stdout=subprocess.PIPE, shell=True)
	device = task.stdout.read().lstrip().rstrip()
		
	# Check if WLAN hardware is available	
	wifiEnabled = os.path.isdir("/sys/class/net/wlan0")
	
	# Check if WLAN network interface is available
	with open("/etc/network/interfaces", "r") as interfacesFile:
		interfacesContent=interfacesFile.read()
	
	wifiInterfaceConfigured = "wlan" in interfacesContent
	
	title = device + " Setup"
	menuItems = [	"Change Root Password", "Change Host Name",
					"Configure Network Interfaces",
					"Set up OPKG Repository",
					"Remove Unused Packages", "Advanced Options -->"]
		
	if (device == "IOT2020"):
		deviceIsIot2020 = True
	
	# Enable serial mode setting if device is IOT2040
	if (not deviceIsIot2020):	
		menuItems.append("Set Serial Mode") 
	if (wifiEnabled and wifiInterfaceConfigured):
		menuItems.append("Configure WLAN")
			
	action, selection = ListboxChoiceWindow(
		gscreen, 
		title, "", 
		menuItems, 
		[('Quit', 'quit', 'ESC')])

	if (action == 'quit'):
		gscreen.finish()
		if (networkConfigurationChanged == True):
			print(ansicolors.clear) # Clear console
			print(ansicolors.blue + "Restarting network services..." + ansicolors.reset + "\n")
			subprocess.call("/etc/init.d/networking restart", shell=True)
			if (wifiEnabled):
				subprocess.call("/sbin/ifdown wlan0", shell=True)
				subprocess.call("/sbin/ifup wlan0", shell=True)
		
		exit()
	
	if selection == 0:
		changeRootPassword()
	elif selection == 1:
		changeHostName()
	elif selection == 2:
		configureNetworkInterfaces()
	elif selection == 3:
		configureOpkgRepository()
	elif selection == 4:
		removeUnusedPackages()
	elif selection == 5:
		advancedOptions()
	elif selection == 6:
		if (not deviceIsIot2020):
			configureSerial()
		elif (wifiEnabled and wifiInterfaceConfigured):
			configureWLAN()
	elif selection == 7:
		configureWLAN()

def changeSshServerSetting(status):
	if (status == "on"):
		subprocess.call("update-rc.d -f sshd defaults", shell=True, stdout=open(os.devnull, 'wb'))
		subprocess.call("/etc/init.d/sshd start", shell=True, stdout=open(os.devnull, 'wb'))
	elif (status == "off"):
		subprocess.call("/etc/init.d/sshd stop", shell=True, stdout=open(os.devnull, 'wb'))
		subprocess.call("update-rc.d -f sshd remove", shell=True, stdout=open(os.devnull, 'wb'))

def registerLaunchScript(status, fileName, scriptcontent):
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

def advancedOptions():
	task = subprocess.Popen("/etc/init.d/sshd status", stdout=subprocess.PIPE, shell=True)
	taskReturn = task.stdout.read().lstrip().rstrip()
	sshEnabled = "running" in taskReturn
	
	noderedAutostartEnabled = os.path.isfile("/etc/init.d/launch_node-red.sh")
	mosquittoAutostartEnabled = os.path.isfile("/etc/init.d/launch_mosquitto.sh")
	
	bb = ButtonBar(gscreen, [("Done", "done", "ESC")])
	ct = CheckboxTree(height = 7, scroll = 1,width=40)

	ct.append("Auto Start node-red", selected=noderedAutostartEnabled)
	ct.append("SSH Server Enabled", selected=sshEnabled)
	ct.append("Auto Start Mosquitto Broker", selected=mosquittoAutostartEnabled)

	g = GridForm(gscreen, "Advanced Options", 1, 4)
	g.add(ct, 0, 1)
	g.add(bb, 0, 3, growx = 1)
	result = g.runOnce()
	selectedOptions = ct.getSelection()

	noderedAutostartEnabledNew = "Auto Start node-red" in selectedOptions
	sshEnabledNew = "SSH Server Enabled" in selectedOptions
	mosquittoAutostartEnabledNew = "Auto Start Mosquitto Broker" in selectedOptions
	
	if (noderedAutostartEnabled != noderedAutostartEnabledNew):
		if ("Auto Start node-red" in selectedOptions):
			registerLaunchScript("on", "launch_node-red.sh", "#!/bin/sh\nsu root -c \"/usr/bin/node /usr/lib/node_modules/node-red/red >/dev/null\" &")
		else:
			registerLaunchScript("off", "launch_node-red.sh", "")
			
	if (sshEnabled != sshEnabledNew):
		if ("SSH Server Enabled" in selectedOptions):
			changeSshServerSetting("on")
		else:
			changeSshServerSetting("off")

	if (mosquittoAutostartEnabled != mosquittoAutostartEnabledNew):
		if ("Auto Start Mosquitto Broker" in selectedOptions):
			registerLaunchScript("on", "launch_mosquitto.sh", "#!/bin/sh\nsu root -c \"/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf -d &>/dev/null\" ")

			fileName = "/etc/mosquitto/mosquitto.conf"
			initFile = open(fileName, 'w')
			initFile.write("user root")
			initFile.close()
		else:
			registerLaunchScript("off", "launch_mosquitto.sh", "")

	displayStartScreen()

def changeRootPassword():
	gscreen.finish()
	print(ansicolors.clear) # Clear console 
	
	subprocess.call(["passwd", "root"])
	displayStartScreen()

def removeUnusedPackages():
	### Edit here ###
	packageList = ["galileo-target", "nodejs", "tcf-agent"] 	# Contains all potential 
												# candidates for removal
	###
	
	bb = ButtonBar(gscreen, (("Ok", "ok"), ("Cancel", "cancel")))
	ct = CheckboxTree(height = 10, scroll = 1,width=40)

	# Iterate through list of removal candidates and check if they are 
	# actually installed.
	task = subprocess.Popen("/usr/bin/opkg list-installed", stdout=subprocess.PIPE, shell=True)
	installedPackages = task.stdout.read()
	
	numberOfRemovablePackages = 0
	for package in packageList:
		if (package in installedPackages):
			ct.append(package)
			numberOfRemovablePackages += 1

	g = GridForm(gscreen, "Select Packages to Remove", 1, 4)
	l = Label("Use 'Space' to select the packages you want to remove.")
	g.add(l, 0, 0, growy=1, growx=1, padding=(1,1,1,1))
	g.add(ct, 0, 1)
	g.add(bb, 0, 3, growx = 1)
	result = g.runOnce()
	
	removeList = ''
	if (bb.buttonPressed(result) == "ok" and numberOfRemovablePackages > 0):
		# Build list of selected packages
		selectedPackages = ct.getSelection()
		for package in selectedPackages:
			removeList = removeList + package + '* '
		
		ret = ButtonChoiceWindow(
			gscreen,
			"Remove Packages",
			"Are you sure you want to remove the following packages: \n\n" + removeList,
			buttons=[("OK", "ok"), ("Cancel", "cancel", "ESC")],
			width=40)
		
		if (ret == "ok"):	
			removeList = "/usr/bin/opkg --force-removal-of-dependent-packages remove " + removeList
			gscreen.finish()
			print(ansicolors.clear) # Clear console 
			print(ansicolors.blue + "Removing selected packages..." + ansicolors.reset + "\n")
			subprocess.call(removeList, shell=True)

	displayStartScreen()


def getSerialModeForPort(port):
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
	
def configureSerial():
	portAction, portSelection = ListboxChoiceWindow(
		gscreen, 
		"Configure Serial Mode", "Select the serial port you want to configure and press 'Enter'.", 
		["X30", "X31"], 
		[('Cancel', 'cancel', 'ESC')])
	if (portSelection == 0):
		portName = "X30"
	else:
		portName = "X31"
	
	currentMode = getSerialModeForPort(portName)

	if (portAction != "cancel"):
		modes = ["RS232", "RS485", "RS422"]
		
		modeAction, modeSelection = ListboxChoiceWindow(
			gscreen, 
			"Configure Serial Mode", "Select a mode.", 
			modes, 
			[('Cancel', 'cancel', 'ESC')], default=currentMode)
		
		if (modeAction != "cancel"):
			persistentReturn = ButtonChoiceWindow(
				gscreen,
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
				initFile = open(fileName, 'w')
				initFile.write("#!/bin/sh\n" + switchCommand)
				initFile.close()
				
				st = os.stat(fileName)
				os.chmod(fileName, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
				subprocess.call("update-rc.d " + fileName + " defaults", shell=True, stdout=open(os.devnull, 'wb'))

				
	displayStartScreen()

def changeHostName():
	currentHostName = subprocess.check_output("hostname")
	
	ret = EntryWindow(
		gscreen,
		"Change Host Name",
		"",
		[("Host Name:", currentHostName)],
		1,
		70, 50,
		[('OK'), ('Cancel', 'cancel', 'ESC')],
		None)
		
	if (ret[0] == "ok"):
		subprocess.Popen(["hostname", ret[1][0].rstrip()], stdout=open(os.devnull, 'wb'))
		
	displayStartScreen()
	
def configureOpkgRepository():
	ret = EntryWindow(
		gscreen,
		"Configure OPKG Repository",
		"",
		[("Host Address:", "")],
		1,
		70, 50,
		['OK', ('Cancel', 'cancel', 'ESC')],
		None)
	
	fileTemplate = '''src/gz all http://[host]/ipk/all
src/gz i586-nlp-32 http://[host]/ipk/i586-nlp-32
src/gz i586-nlp-32-intel-common http://[host]/ipk/i586-nlp-32-intel-common
src/gz iot2000 http://[host]/ipk/iot2000
'''
	if (ret[0] == "ok"):
		opkgConfig = fileTemplate.replace("[host]", ret[1][0].rstrip())
		fileName = "/etc/opkg/iot2000.conf"
		
		opkgFile = open(fileName, 'w')
		opkgFile.write(opkgConfig)
		opkgFile.close()
						
	displayStartScreen()


def configureWLAN():
	global networkConfigurationChanged
	
	ret = EntryWindow(
		gscreen,
		"Configure WLAN",
		"",
		[("Type:", "WPA-PSK"), ("SSID:", ""), ("Key:", "")],
		1,
		70, 50,
		['OK', ('Cancel', 'cancel', 'ESC')],
		None)
	
	fileTemplate = '''ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
update_config=1

network={
	key_mgmt=[type]
	ssid="[ssid]"
	psk="[passwd]"
}'''

	if (ret[0] == "ok"):
		wpaConfig = fileTemplate.replace("[type]", ret[1][0].rstrip()).replace("[ssid]", ret[1][1].rstrip()).replace("[passwd]", ret[1][2].rstrip())
		
		fileName = "/etc/wpa_supplicant.conf"
		
		backupFileName = "/etc/wpa_supplicant.conf.bak"
		copyfile(fileName, backupFileName)
		
		wpaFile = open(fileName, 'w')
		wpaFile.write(wpaConfig)
		wpaFile.close()

		rv = ButtonChoiceWindow(
				gscreen,
				"Configure WLAN",
				"Your WLAN configuration has been changed. A backup of the old configuration can be found at: " + backupFileName,
				buttons=["OK"],
				width=40)
				
		networkConfigurationChanged = 1
	
	displayStartScreen()

def getNetworkInterfaceConfiguration(interface):
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
		
	return "dhcp"	

def configureNetworkInterfaces():
	global networkConfigurationChanged
	global wifiEnabled
	global deviceIsIot2020
	
	if deviceIsIot2020:
		interfaces = ([('eth0', getNetworkInterfaceConfiguration('eth0'))])
	else:
		interfaces = ([('eth0', getNetworkInterfaceConfiguration('eth0')) , ('eth1', getNetworkInterfaceConfiguration('eth1'))])
		
	if wifiEnabled:
		interfaces.append(('wlan0', getNetworkInterfaceConfiguration('wlan0')))
		
	ret = EntryWindow(
		gscreen,
		"Configure Network Interfaces",
		"Specify IP addresses for network interfaces, enter 'dhcp' to obtain address by DHCP.",
		interfaces,
		1,
		70, 50,
		['OK', ('Cancel', 'cancel', 'ESC')],
		None)
	
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
	
	i = 0
	for interface in interfaces:
		if (interface[0] == "wlan0"):
			if (ret[1][i] == "dhcp"):
				interfacesConfig = interfacesConfig + wirelessDhcpTemplate.replace("[interfaceName]", interface[0])
			else:
				interfacesConfig = interfacesConfig + wirelessStaticTemplate.replace("[interfaceName]", interface[0]).replace("[ip]", ret[1][i])
		else:
			if (ret[1][i] == "dhcp"):
				interfacesConfig = interfacesConfig + dhcpTemplate.replace("[interfaceName]", interface[0])
			else:
				interfacesConfig = interfacesConfig + staticTemplate.replace("[interfaceName]", interface[0]).replace("[ip]", ret[1][i])
		i += 1
	
	if (ret[0] == "ok"):
		fileName = "/etc/network/interfaces"
		backupFileName = "/etc/network/interfaces.bak"
		copyfile(fileName, backupFileName)
		interfacesFile = open(fileName, 'w')
		interfacesFile.write(interfacesConfig)
		interfacesFile.close()
		
		networkConfigurationChanged = 1
		rv = ButtonChoiceWindow(
				gscreen,
				"Configure Network Interfaces",
				"Your network interfaces have been reconfigured. A backup of the old configuration can be found at: " + backupFileName,
				buttons=["OK"],
				width=40)

	displayStartScreen()
	

displayStartScreen()	

