/*
 * Don't ask...
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
#include <linux/platform_device.h>

#define PLATFORM_NAME	"GalileoGen2"

static struct platform_device *pd;

static struct platform_driver galileo_platform_driver = {
	.driver		= {
		.name	= PLATFORM_NAME,
	},
};

int init_module(void)
{
	int err;

	err = platform_driver_register(&galileo_platform_driver);

	pd = platform_device_register_simple(PLATFORM_NAME, -1, NULL, 0);
	if (IS_ERR(pd)) {
		platform_driver_unregister(&galileo_platform_driver);
		return PTR_ERR(pd);
	}

	return 0;
}

void cleanup_module(void)
{
	platform_device_unregister(pd);
	platform_driver_unregister(&galileo_platform_driver);
}

MODULE_LICENSE("GPL");
