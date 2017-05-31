/*
 * Copyright (c) Siemens AG, 2017
 *
 * Authors:
 *  Sascha Weisenberger <sascha.weisenberger@siemens.com>
 *  Jan Kiszka <jan.kiszka@siemens.com>
 *
 * This file is subject to the terms and conditions of the MIT License.  See
 * COPYING.MIT file in the top-level directory.
 */

#include <linux/serial.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#ifndef SER_RS485_TERMINATE_BUS
#define SER_RS485_TERMINATE_BUS		(1 << 5)
#endif

static void print_usage(char *name)
{
	printf("Usage: %s DEVICE [MODE [-t|--terminate]]\n"
	       "\n"
	       "DEVICE\t\tThe device for which you want to switch the mode.\n"
	       "MODE\t\tThe mode you want to use: rs232, rs485, or rs422.\n"
	       "\t\tIf omitted, the current mode will be printed.\n"
	       "\n"
	       "Optional arguments:\n"
	       " -t, --terminate\tTerminate the RS422 or RS485 bus.\n"
	       "\n"
	       "Example: %s /dev/ttyS2 rs485 --terminate\n", name, name);
}

static void print_mode(struct serial_rs485 *rs485conf)
{
	const char *mode, *terminate;

	if (!(rs485conf->flags & SER_RS485_ENABLED)) {
		mode = "RS232";
		terminate = "";
	} else {
		if (rs485conf->flags & SER_RS485_RX_DURING_TX)
			mode = "RS422";
		else
			mode = "RS485";
		if (rs485conf->flags & SER_RS485_TERMINATE_BUS)
			terminate = ", terminating";
		else
			terminate = ", non-terminating";
	}

	printf("%s%s\n", mode, terminate);
}

static int get_mode(int file, char *device)
{
	struct serial_rs485 rs485conf;

	if (ioctl(file, TIOCGRS485, &rs485conf) < 0) {
		perror("Error");
		return 1;
	}

	printf("Mode of %s: ", device);
	print_mode(&rs485conf);

	return 0;
}

static int set_mode(int file, char *device, char *mode, char *option)
{
	struct serial_rs485 rs485conf;

	rs485conf.flags = 0;

	if (strcasecmp("rs485", mode) == 0) {
		rs485conf.flags |= SER_RS485_ENABLED;
	} else if (strcasecmp("rs422", mode) == 0) {
		rs485conf.flags |= SER_RS485_ENABLED | SER_RS485_RX_DURING_TX;
	} else if (strcasecmp("rs232", mode) != 0) {
		fprintf(stderr, "Invalid mode \"%s\"\n", mode);
		return 2;
	}

	if (option) {
		if (strcmp(option, "-t") == 0 ||
		    strcmp(option, "--terminate") == 0) {
			if (!(rs485conf.flags & SER_RS485_ENABLED)) {
				fprintf(stderr,
					"Termination not supported in RS232 "
					"mode\n");
				return 2;
			}
			rs485conf.flags |= SER_RS485_TERMINATE_BUS;
		} else {
			fprintf(stderr, "Invalid option \"%s\"\n", option);
			return 2;
		}
	}

	if (ioctl(file, TIOCSRS485, &rs485conf) < 0) {
		perror("Error");
		return 1;
	}

	printf("Successfully set %s to ", device);
	print_mode(&rs485conf);

	return 0;
}

int main(int argc, char *argv[])
{
	int file, ret;

	if (argc < 2 || argc > 4) {
		print_usage(argv[0]);
		return 2;
	}
	if (!strcmp(argv[1], "--help")) {
		print_usage(argv[0]);
		return 0;
	}

	file = open(argv[1], O_RDWR);
	if (file < 0) {
		perror("Error");
		return 1;
	}

	if (argc == 2)
		ret = get_mode(file, argv[1]);
	else
		ret = set_mode(file, argv[1], argv[2], argv[3]);

	close(file);

	return ret;
}
