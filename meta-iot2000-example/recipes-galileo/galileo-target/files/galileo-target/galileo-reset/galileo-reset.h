
/* 
 * Copyright(c) 2013 Intel Corporation.
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms and conditions of the GNU General Public License,
 * version 2, as published by the Free Software Foundation.
 *
 * This program is distributed in the hope it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 */

#ifndef gpio_reset_Header_h
#define gpio_reset_Header_h

#define GPIO_SYS_BASE_STRING "/sys/class/gpio"
#define GPIO_SYS_EXPORT_STRING "/sys/class/gpio/export"

//todo: make reset script an arg to the program
#define SKETCH_RESET_RELEASE_SCRIPT "/opt/cln/galileo/galileo_sketch_reset_script.sh"

#define GPIO_STRING_LEN 132 

#endif
