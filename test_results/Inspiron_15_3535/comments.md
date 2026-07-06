## WiFi

rtw88 has always been a pain since installing [my laptop](probe_2026-07-06_15-37-31.txt) on FreeBSD 14.2.
* 14.2, 14.3, 15.0: was never able to finish an rsync LAN backup: something freezes wlan0, trying to ifconfig it down doesn't even return.
* 14.2 and 14.3 were relatively quick to catch an AP; 15.0 regressed, with sometimes dozens of minutes before getting authenticated. The more APs there are all around, the slowest it succeeds (at home with 2 or 3 APs it can take as "low" as 2 minutes before being connected). It may have to do with the "6 s delay" that is identified as a (still unresolved) weakness of rtw88 and rtw89.
* 14.2 and 14.3 (maybe 15.0?) still needed `compat.linuxkpi.skb.mem_limit=1` in `/boot/loader.conf`. Removing it went from stable 2 MB/s transfer rates to unstable rates, from stalled to max 600 KB/s.

Waiting for Bjoern A. Zeeb's great efforts on net80211 (e.g. [status report from June](https://github.com/FreeBSDFoundation/status-updates/blob/main/Bjoern_Zeeb/2026-06.md#misc)).

## Graphics

Wayfire totally usable.

## Browsing

Heavily animated pages (e.g. LinkedIn, or blog pages with many ads flickering all over) could get the entire system to freeze. While upgrading from 14.3 to 15.0 I removed core dumps and ulimit -m 512: now only Firefox gets killed.
Probably memory-related (OOM kills), but wondering if there could be a bad interaction with network (graphic pages generally have Javascript, but many network requests too).

## Battery

No sleep mode supported from 14.2 to 15.0.
Ended up with a manual script to go low consumption: `ifconfig wlan0 down ; backlight 0 ; /etc/rc.d/power_profile 0x00 ; killall -STOP firefox`: this makes the laptop go to 2.5 - 3.5 W (as told by `acpiconf -i 0 | grep Present.rate`)

## User Experience

Custom Wayfire bindings to get keyboard's light up and down, and volume up and down, to nearly work: in `.config/wayfire.ini`:
```
[command]
repeatable_binding_volume_down = <super> KEY_F2
command_volume_down = mixer vol=-5%
repeatable_binding_volume_up = <super> KEY_F3
command_volume_up = mixer vol=+5%
repeatable_binding_light_down = <super> KEY_F6
command_light_down = backlight - 10
repeatable_binding_light_up = <super> KEY_F7
command_light_up = backlight + 10
```
