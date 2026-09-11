FreeBSD 16.0-CURRENT as of 12/09/2026 (d m y)

Ethernet works wonderfully, but Realtek 8852CE wifi causes system to hang
when attempting to setup wifi device. System even may hang during boot at
linker 32 bit something after that (although, i haven't installet 32 bit 
compatibility libraries). fsck from LiveCD helps.

Radeon 660M works without issues.

About battery. After enabling powerd (w roughly default options) and
setting cstate to Cmax (sysctl hw.acpi.cpu.cx_lowest=Cmax) at least 4/5 of
usual lifetime before recharge can be expected.

Builtin audio dynamic work is not consistent between reboots, usually
aren't workin' at all. Following may or may not help (Microphone stops working
with this, you still need to manually switch sink after plugging headphones)

/boot/device.hints:
    hint.hdaa.1.nid20.config="as=1 seq=0 device=Speaker"
    hint.hdaa.1.nid18.config="as=2 seq=0 device=Mic"

Volume is really low, this may help a bit:
/etc/sysctl.conf:
    hw.snd.vpc_0db=5
    $ mixer vol=100

Hwprobe shows that bluetooth is working but I haven't f****d around with
it, so dunno.

Backlight and some FN keys are working after loading acpi_ibm module,
though can't tell if every key is working.

Even though laptop doesn't support S3 sleep, suspend_to_idle is kinda
workin' ok after a little configuration.

Suspect could be used as main OS on this laptop, if you could not
configure audio it will be sad though.
