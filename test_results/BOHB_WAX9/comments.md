# Notes 
This is my first report on trying FreeBSD on my Huawei Matebook D15. I have not used it as a daily driver with any operating system. I won it in 2021, and since then have left it untouched because I have used other computers. I installed different operating systems from time to time, but there were always some difficulties, especially with brightness control and the sound card.   

## Brightness 
Brightness control works as expected after installing `drm-kmod` (adding the `i915kms` kernel module to `/etc/rc.conf`), `xorg`, and `xfce4`, and adding my standard user account (not root) to the `video` group. I set the brightness with the backlight program. I have tried FreeBSD in the past on this machine and brightness control did not work. Now it works, so this is a positive progress.

## Desktop Environment 
I use XFCE4. I created .xinitrc in my home directory 
containing the line `ck-launch-session dbus-launch --exit-with-session startxfce4`. I start it with the command `startxfce4`.

## Networking
Networking was configured automatically during the installation and works.

## Sound
Sound does not work. I followed the steps of chapter 9.2 `Setting Up The Sound Card` from the handbook.
In order to load the `snd_driver` at boot time, I placed
`snd_driver_load` into /boot/loader.conf.

I then executed dmesg | grep pcm: 
pcm0: <Intel Kaby Lake (HDMI/DP 8ch)> at nid 3 on hdaa0
pcm0: <Intel Kaby Lake (HDMI/DP 8ch)> at nid 3 on hdaa0
pcm0: <Intel Kaby Lake (HDMI/DP 8ch)> at nid 3 on hdaa0
pcm0: <Intel Kaby Lake (HDMI/DP 8ch)> at nid 3 on hdaa0

I then executed cat /dev/sndstat:
Installed devices:
pcm0: <Intel Kaby Lake (HDMI/DP 8ch)> (play) default
No devices installed from userspace.

If I execute beep, this process hangs for some seconds and then terminates, but no noise is produced. 

The output of mixer: 
pcm0:mixer: <Intel Kaby Lake (HDMI/DP 8ch)> on hdaa0 (play) (default)
    vol       = 1.00:1.00     pbk
    pcm       = 1.00:1.00     pbk

I then executed ls -all /dev/dsp:
crw-rw-rw-  1 root wheel 0x42 Sep 11 10:43 /dev/dsp

I then executed fstat | grep dsp. It produced no output.

Then I started pacmd. I entered the following commands inside pacmd:

list-cards: 
0 card(s) available.

list-sinks:
1 sink(s) available.
  * index: 0
	name: <oss_output.dsp0>
	driver: <module-oss.c>
	flags: HARDWARE HW_VOLUME_CTRL LATENCY 
	state: SUSPENDED
	suspend cause: IDLE
	priority: 0
	volume: front-left: 65536 / 100%,   front-right: 65536 / 100%
	        balance 0.00
	base volume: 65536 / 100%
	volume steps: 101
	muted: no
	current latency: 0.00 ms
	max request: 16 KiB
	max rewind: 0 KiB
	monitor source: 0
	sample spec: s16le 2ch 44100Hz
	channel map: front-left,front-right
	             Stereo
	used by: 0
	linked by: 0
	fixed latency: 92.88 ms
	module: 6
	properties:
		device.string = "/dev/dsp0"
		device.api = "oss"
		device.description = "0 - Intel Kaby Lake (HDMI/DP 8ch)"
		device.access_mode = "mmap"
		device.buffering.buffer_size = "16384"
		device.buffering.fragment_size = "4096"
		device.icon_name = "audio-card"

list-sources:
1 source(s) available.
  * index: 0
	name: <oss_output.dsp0.monitor>
	driver: <module-oss.c>
	flags: DECIBEL_VOLUME LATENCY 
	state: SUSPENDED
	suspend cause: IDLE
	priority: 1000
	volume: front-left: 65536 / 100% / 0.00 dB,   front-right: 65536 / 100% / 0.00 dB
	        balance 0.00
	base volume: 65536 / 100% / 0.00 dB
	volume steps: 65537
	muted: no
	current latency: 0.00 ms
	max rewind: 0 KiB
	sample spec: s16le 2ch 44100Hz
	channel map: front-left,front-right
	             Stereo
	used by: 0
	linked by: 0
	fixed latency: 92.88 ms
	monitor_of: 0
	module: 6
	properties:
		device.description = "Monitor of 0 - Intel Kaby Lake (HDMI/DP 8ch)"
		device.class = "monitor"
		device.icon_name = "audio-input-microphone"



## Miscellaneous 
I have not tested the microphone and webcam. The keyboard has no backlight. 
In general, I have little experience in using this laptop with any OS. 

## Contact
Feel free to reach out if you have tried running FreeBSD on a Huawei Matebook D15 and ran into issues. We can compare configuration files and try to troubleshoot together. If you need further information (output from programs etc.), please contact me.  
