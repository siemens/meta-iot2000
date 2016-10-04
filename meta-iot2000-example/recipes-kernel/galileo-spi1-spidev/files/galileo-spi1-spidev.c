/*
 * Register spidev userspace driver with SPI channel 1
 *
 * Copyright (c) Siemens AG, 2016
 *
 * Authors:
 *  Jan Kiszka <jan.kiszka@siemens.com>
 *
 * This work is licensed under the terms of the GNU GPL, version 2.  See
 * the COPYING file in the top-level directory.
 */

#include <linux/module.h>
#include <linux/spi/pxa2xx_spi.h>
#include <linux/spi/spi.h>

static struct spi_device *spi_device;

/* Option to allow GPIO 10 to be used for SPI1 chip-select */
static int gpio_cs;

module_param(gpio_cs, int, S_IRUGO | S_IWUSR);
MODULE_PARM_DESC(gpio_cs, "Enable GPIO chip-select for SPI channel 1");

static struct pxa2xx_spi_chip qrk_ffrd_spi_1_cs_0 = {
	.gpio_cs = 10,
};

static struct spi_board_info spi1_dev_gpiocs = {
	.modalias = "spidev",
	.chip_select = 0,
	.controller_data = &qrk_ffrd_spi_1_cs_0,
	.max_speed_hz = 50000000,
	.bus_num = 169,
};

static struct spi_board_info spi1_dev = {
	.modalias = "spidev",
	.chip_select = 0,
	.controller_data = NULL,
	.max_speed_hz = 50000000,
	.bus_num = 169,
};

int init_module(void)
{
	struct spi_board_info *info;
	struct spi_master *master;

	if (gpio_cs)
		info = &spi1_dev_gpiocs;
	else
		info = &spi1_dev;

	master = spi_busnum_to_master(info->bus_num);
	if (!master)
		return -EINVAL;

	spi_device = spi_new_device(master, info);
	put_device(&master->dev);
	if (!spi_device)
		return -EPERM;

	return 0;
}

void cleanup_module(void)
{
	spi_unregister_device(spi_device);
}

MODULE_LICENSE("GPL");
