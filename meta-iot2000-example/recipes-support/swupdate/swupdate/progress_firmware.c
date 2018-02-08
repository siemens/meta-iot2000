/*
 * Author: Christian Storm
 * Copyright (C) 2018, Siemens AG
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc.
 */

#include <progress.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

static int connect2swupdate(bool retry)
{
	struct sockaddr_un servaddr;
	int connfd = socket(AF_LOCAL, SOCK_STREAM, 0);
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sun_family = AF_LOCAL;
	strcpy(servaddr.sun_path, SOCKET_PROGRESS_PATH);
	do {
		if (connect(connfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) == 0) {
			break;
		}
		if (retry == false) {
			fprintf(stderr, "progress_firmware :: no connection to SWUpdate, exiting.\n");
			exit(1);
		}
		usleep(10000);
	} while (true);
	fprintf(stdout, "progress_firmware :: connected to SWUpdate IPC.\n");
	return connfd;
}

int main(void)
{
	struct progress_msg msg;
	int connfd = -1;
	while (true) {
		if (connfd < 0) {
			connfd = connect2swupdate(true);
		}

		if (read(connfd, &msg, sizeof(msg)) != sizeof(msg)) {
			fprintf(stdout, "progress_firmware :: short read, connection closing..\n");
			close(connfd);
			connfd = -1;
			continue;
		}

		if (msg.status == DONE) {
			fprintf(stdout, "progress_firmware :: firmware installed, rebooting.\n");
			if (system("reboot") < 0) {
				fprintf(stderr,
					"progress_firmware :: reboot failed, please reset the board manually.\n");
			}
		}
	}
}

