# Integration testing checklist

## Sanity checks

- [ ] Boot fresh FreeBSD release image to the installer

    **Instructions**
    1. fetch https://download.freebsd.org/releases/amd64/amd64/ISO-IMAGES/15.0/FreeBSD-15.0-RELEASE-amd64-memstick.img.xz
    2. xz -d FreeBSD-15.0-RELEASE-amd64-memstick.img.xz
    3. dd if=FreeBSD-15.0-RELEASE-amd64-memstick.img of=<desired USB device> bs=1M
    4. Plug in the USB drive to target computer
    5. Poweron target computer and ensure that UEFI boot targets the USB drive

- [ ] Validate disk encryption related options in the installer

    **Criteria**
    * Installer must indicate that the UEFI partition will not be encrypted.

- [ ] Install with disk encryption enabled and the KDE desktop environment (all other settings default)

    **Criteria**
    * Both Auto-on-ZFS and Auto-on-UFS installs succeed with no errors observed

- [ ] Reboot

    **Criteria**
    * Disk decryption password prompt during boot must succeed

- [ ] Test suspend/resume on the SDDM login screen

    **Instructions**
    1. Close and reopen laptop lid (since zzz is not available without a terminal in SDDM)

    **Criteria**
    * Must not bypass authentication
    * Must not add any extra text character input to any form fields

- [ ] Laptop-specific hardware indicator (e.g. LED blinking, etc.) functions during suspend/resume

- [ ] Login with user credentials

- [ ] Continuously switch between suspend/resume

    **Instructions**
    1. Close and reopen laptop lid erratically

    **Criteria**
    * No visual errors observed
    * No errors observed in dmesg or /var/log/messages

- [ ] TODO PLACEHOLDER FOR HIBERNATION TESTS

- [ ] Verify that resuming the hibernated system requires a password to decrypt the disk

    **Criteria**
    * The boot loader must require a valid password

- [ ] Accessing the internet works out-of-the-box

    **Instructions**
    1. Navigate to https://freebsd.org with a graphical web browser

    **Criteria**
    * No connection issues

- [ ] OpenGL and Vulkan test utilities are accelerated

    **Instructions**
    1. Run glxgears and vkcube in a terminal

    **Criteria**
    * Both utilities must report running on the GPU at the target monitor refresh rate

- [ ] Hardware accelerated video works out of the box

    **Instructions**
    1. Run `vainfo` in a terminal
    2. Open firefox and navigate to https://about:support
    3. Navigate to https://tools.woolyss.com/html5-audio-video-tester and click on a video from each codec supported by the laptop. Then run `radeontop` (AMD only) in a terminal and observe the 'video decoder' percentage"

    **Criteria**
    * vainfo must report codec capabilities successfully
    * firefox must show codecs as ""supported"" in about:support page
    * radeontop must show "video decoder" active (>0%) during video workload

- [ ] Suspend/resume during hardware-accelerated video playback

    **Instructions**
    1. Close and reopen laptop lid a few times while a video is playing

    **Criteria**
    * Must not produce any audio/video artifacts or crashes after resume
    * No errors observed in `dmesg` or /var/log/messages

- [ ] HDMI output works seamlessly with KDE Plasma

    **Instructions**
    1. Plug in HDMI
    2. Press super+p and cycle through various display configuration options

    **Criteria**
    * All display configurations must work as expected

- [ ] Sound server switches to HDMI audio when plugged in

    **Instructions**
    1. Plug in HDMI
    2. Run `wpctl status`
    3. Play any sound (e.g. through Firefox or `pw-play`)

    **Criteria**
    * Default sink should be the HDMI audio device
    * Sound should come from HDMI output device

- [ ] Closing the laptop lid with HDMI connected will either sleep/resume OR switch to clamshell mode

    **Instructions**
    1. Plug in HDMI monitor and wait for video output to show on screen
    2. Go to power settings and test two scenarios: one with _"sleep/resume on laptop lid even when external monitor is connected_, and one without

    **Criteria**
    * Both configurations should work as expected

- [ ] Suspend/resume with USB peripherals

    **Instructions**
    1. Test all and any USB devices available with erratic suspend/resume cycles

- [ ] Suspend/resume does not require disk decryption upon resume

    **Criteria**
    * Sleep/resume should work as normal

- [ ] Ensure offline disk security

    **Instructions**
    1. Shutdown the test system
    2. Flash an mfsBSD image onto a USB stick
    3. Boot into mfsBSD and attempt to mount the internal disk that contains the FreeBSD encrypted disk install

    **Criteria**
    * Root partition is neither mountable nor readable offline

- [ ] Windows VM survives suspend/resume cycles

- [ ] USB network tethering of a smartphone to a laptop should work

- [ ] VMs of all popular guest linux distributions survive suspend/resume cycles

    **Criteria**
    * Debian
    * Fedora
    * Alpine Linux
    * (optional) Arch Linux

- [ ] The laptop saves significantly more power while suspended than active in idle

    **Criteria**
    * (subjective?) The system must resume successfully _days later_ and lose very little power over that time

- [ ] The laptop consumes no (negligible) power while hibernated

    **Criteria**
    * (subjective?) * The system must wake from hibernation successfully _weeks later_ and lose very little power over that time

- [ ] Wifi 6E reaches gigabit speed

    **Instructions**
    1. Set router to 6GHz with a bandwidth of 160MHz
    2. On another host (connected by at least 2.5Gb ethernet), start an iperf3 server
    3. On the laptop, measure iperf3 client speeds to the host

    **Criteria**
    * Must observe at least 1Gbps between the two hosts

## User Stories (high level testing scenarios)

- [ ] The laptop should last through an 8-hour workday on a single charge
    https://github.com/FreeBSDFoundation/proj-laptop/issues/6

- [ ] The user can close the lid, store the laptop in a backpack, and open the lid hours later to resume working.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/7

- [ ] The laptop should automatically connect to known Wi-Fi networks without requiring the user to manually reconnect each time.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/4

- [ ] FreeBSD should have a simple recommended process or tool to identify available WiFi networks, choose one to connect to, and provide a passphrase.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/3

- [ ] The user can connect their laptop to the internet through their mobile phone when travelling.

- [ ] Suspending the laptop while a VM is running should not affect the VM's state upon resume.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/9

- [ ] Graphical applications (such as games and media content creation tools) should run smoothly on the laptop at the screen refresh rate or higher.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/11
    https://github.com/FreeBSDFoundation/proj-laptop/issues/13

- [ ] The user can share their screen on all popular browsers and other applications that request the webcam.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/14

- [ ] Sound should seamlessly switch to headphones when plugged in, and back to speakers when plugged out.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/15

- [ ] The user can use multi-finger touchpad gestures in the desktop environment.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/18

- [ ] All of the laptop's specialty keyboard buttons (e.g. brightness, volume, etc.) work correctly and can be bound in the desktop environment.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/19

- [ ] Windows VMs can be run on the laptop.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/21

- [ ] A new user can install FreeBSD easily and jump into a graphical desktop environment on the next boot.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/25

- [ ] A user can connect to an external monitor or projector using HDMI while using the desktop environment's display settings to configure it.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/27

- [ ] The laptop can enter and resume from hibernation mode with no change to its operating state.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/29

- [ ] All modern wifi standards (wifi 5, 6, and 6E) are supported on the laptop, with 6/6E providing an actual observed speed of 1Gbps or more.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/34
