/*
 * Don't try this at home...
 *
 * Copyright (c) Siemens AG, 2016
 *
 * Authors:
 *  Jan Kiszka <jan.kiszka@siemens.com>
 *
 * This work is licensed under the terms of the GNU GPL, version 2.  See
 * the COPYING file in the top-level directory.
 *
 * Derived from drivers/mfd/intel_qrk_gip_gpio.c of meta-intel-galileo
 */

#include <linux/module.h>
#include <linux/pci.h>
#include <linux/uio_driver.h>

#define GIP_GPIO_BAR		1

#define SCH_GPIOBASE		0x44
#define SCH_GPIO_IO_SIZE	64

static struct pci_dev *gip_dev;
static struct pci_dev *sch_dev;
static struct uio_info uio_gip;
static struct uio_info uio_sch;
static void __iomem *gip_reg_base;

int init_module(void)
{
	resource_size_t start, len;
	unsigned int base_addr_cfg;
	int err;

	gip_dev = pci_get_device(PCI_VENDOR_ID_INTEL, 0x0934, NULL);
	if (!gip_dev)
		return -ENODEV;

	start = pci_resource_start(gip_dev, GIP_GPIO_BAR);
	len = pci_resource_len(gip_dev, GIP_GPIO_BAR);

	gip_reg_base = ioremap_nocache(start, len);
	if (!gip_reg_base) {
		err = -EFAULT;
		goto err_gip_devput;
	}

	uio_gip.mem[0].addr = start;
	uio_gip.mem[0].internal_addr = gip_reg_base;
	uio_gip.mem[0].size = len;
	uio_gip.mem[0].memtype = UIO_MEM_PHYS;
	uio_gip.mem[0].name = "gpio_regs";
	uio_gip.name = "gpio uio";
	uio_gip.version = "0.0.1";

	err = uio_register_device(&gip_dev->dev, &uio_gip);
	if (err)
		goto err_gip_unmap;

	sch_dev = pci_get_device(PCI_VENDOR_ID_INTEL,
				 PCI_DEVICE_ID_INTEL_QUARK_X1000_ILB, NULL);
	if (!sch_dev) {
		err = -ENODEV;
		goto err_gip_unregister;
	}

	pci_read_config_dword(sch_dev, SCH_GPIOBASE, &base_addr_cfg);
	if (!(base_addr_cfg & (1 << 31))) {
		err = -EIO;
		goto err_sch_devput;
	}

	uio_sch.port[0].start = (unsigned short)base_addr_cfg;
	uio_sch.port[0].size = SCH_GPIO_IO_SIZE;
	uio_sch.port[0].porttype = UIO_PORT_X86;
	uio_sch.port[0].name = "gpio_regs";
	uio_sch.name = "sch_gpio";
	uio_sch.version = "0.0.1";

	err = uio_register_device(&sch_dev->dev, &uio_sch);
	if (err)
		goto err_sch_devput;

	return 0;

err_sch_devput:
	pci_dev_put(gip_dev);
err_gip_unregister:
	uio_unregister_device(&uio_gip);
err_gip_unmap:
	iounmap(gip_reg_base);
err_gip_devput:
	pci_dev_put(gip_dev);
	return err;
}

void cleanup_module(void)
{
	uio_unregister_device(&uio_sch);
	pci_dev_put(sch_dev);

	uio_unregister_device(&uio_gip);
	iounmap(gip_reg_base);
	pci_dev_put(gip_dev);
}

MODULE_LICENSE("GPL");
