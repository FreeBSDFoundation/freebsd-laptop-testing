# User experience notes - ThinkPad X1 Carbon Gen 4 (20FB0069MN)

Tested with KDE Plasma 6 (X11 session) on top of SDDM, FreeBSD 15.1-RELEASE.

## Display power management (DPMS) causes a full system hang
Setting Plasma's "Turn off screen" timeout (Power Management settings)
causes a complete system freeze requiring a hard reboot. This appears
related to known i915kms/drm-kmod display power-state issues on this
chipset (Intel HD Graphics 520 / Skylake-U). Workaround: leave
"Turn off screen" set to "Do nothing".

## Suspend (S3) works, but is hidden from the Plasma UI
`acpiconf -s 3` suspends and resumes the laptop correctly. However,
Plasma's Power Management page does not offer a "Suspend" option at
all, and ConsoleKit2's `CanSuspend` D-Bus method incorrectly returns
"no". Root cause: PowerDevil registers its own inhibitor with the
reason string `handle-suspend-key`, and ConsoleKit2 appears to treat
the substring "suspend" in any active inhibitor as a real block on
suspending - even though this is PowerDevil's own, expected
inhibitor. This means suspend is unusable from the GUI on a stock
setup, despite working perfectly at the hardware/kernel level.

Workaround used: a sudoers NOPASSWD rule for `/usr/sbin/acpiconf -s 3`
combined with a custom KDE global shortcut. For lid-close and
inactivity-based suspend, a custom devd(8) script with a delay timer
was used instead of Plasma's built-in suspend handling.

## Shutdown/Restart missing from Plasma's logout menu
By default, ConsoleKit2 reports `active = FALSE` for the X11/SDDM
session (`ck-list-sessions`), even after adding `pam_ck_connector.so`
to SDDM's PAM session stack. As a result, PowerDevil hides the
Shutdown/Restart buttons. Workaround: a custom polkit rule granting
`wheel` group members the `org.freedesktop.consolekit.system.stop`
and `.restart` actions directly, bypassing the broken active-session
check.

## Wi-Fi works at the driver level, but KDE's "Wi-Fi & Internet"
## settings page shows no networks
The `iwm0` (Intel Wireless 8260) device works fine at the driver
level. However, KDE's native Wi-Fi system settings page (plasma-nm)
never shows any networks, because the real freedesktop.org
NetworkManager daemon it depends on is not available on FreeBSD.
Workaround: installed `networkmgr` (the GhostBSD tray-icon network
manager) as a separate application instead.

## Bluetooth
Reported as NOT DETECTED by the probe tool, despite `ng_bluetooth`,
`ng_hci`, and `ng_ubt` kernel modules being loaded. Not investigated
further in this session.
