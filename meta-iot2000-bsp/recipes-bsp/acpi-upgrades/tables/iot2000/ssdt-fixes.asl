DefinitionBlock ("ssdt-fixes.aml", "SSDT", 5, "SsgPmm", "CpuPm", 17)
{
    /* What we hijacked */

    External (_PR_.CPU0, DeviceObj)

    Scope (\)
    {
        Name (PDC0, 0x80000000)
    }

    Scope (\_PR.CPU0)
    {
        Method (_PDC, 1, NotSerialized)  // _PDC: Processor Driver Capabilities
        {
            CreateDWordField (Arg0, 0x08, CAP0)
            Store (CAP0, PDC0)
        }
    }

    /* Fixes */

    External (\_SB.PCI0.SPI0, DeviceObj)
    External (\_SB.PCI0.GIP0.GPO, DeviceObj)
    External (\_SB.PCI0.PEX1, DeviceObj)

    Scope (\_SB.PCI0.SPI0)
    {
        Name (_CRS, ResourceTemplate () {
            GpioIo (Exclusive, PullUp, 0, 0, IoRestrictionOutputOnly,
                    "\\_SB.PCI0.GIP0.GPO", 0) {0}
        })

        Name (_DSD, Package () {
            ToUUID("daffd814-6eba-4d8c-8a91-bc9bbf4aa301"),
            Package () {
                Package () {
                    "cs-gpios", Package () {^SPI0, 0, 0, 0},
                },
            }
        })
    }

    Scope (\_SB.PCI0.PEX1)
    {
        Device (EXR0)
        {
            Name (_ADR, 0x00000000)
            Name (_STA, 0x0F)
        }
    }

    Scope (\_SB)
    {
        Device (LEDR)
        {
            Name (_HID, "PRP0001")

            Name (_CRS, ResourceTemplate () {
                GpioIo (Exclusive, PullNone, 0, 0, IoRestrictionOutputOnly,
                    "\\_SB.PCI0.PEX1.EXR0", 0) {0}
            })

            Name (_DSD, Package () {
                ToUUID("daffd814-6eba-4d8c-8a91-bc9bbf4aa301"),
                Package () {
                    Package () {"compatible", "gpio-leds"},
                },
                ToUUID("dbb8e3e6-5886-4ba6-8795-1319f52a966b"),
                Package () {
                    Package () {"led-0", "LED0"},
                }
            })

            Name (LED0, Package () {
                ToUUID("daffd814-6eba-4d8c-8a91-bc9bbf4aa301"),
                Package () {
                    Package () {"label", "mpio_uart_led:red:user"},
                    Package () {"gpios", Package () {^LEDR, 0, 0, 0}},
                    Package () {"linux,default-state", "off"},
                    Package () {"linux,default-trigger", "none"},
                    Package () {"linux,retain-state-suspended", 1},
                }
            })
        }
    }
}
