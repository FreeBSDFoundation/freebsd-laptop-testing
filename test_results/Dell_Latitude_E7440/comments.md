FreeBSD was quite difficult to install on this laptop for me, compared to my ThinkPad T430, which I submitted results for earlier.

Endless reports of my touchscreen disconnecting:

ugen1.5: <ELAN Touchscreen> at usbus1 
usbhid0 on uhub2
usbhid0: <ELAN Touchscreen>, class 0/0, rev 2.00/0.11, addr 5> on usbus1
hidbus0: <HID bus> on usbhid0
hmt0: <ELAN Touchscreen> on hidbus0
hmt0: Multitouch touchscreen with 0 external buttons
hnt0: 10 contacts with [WH] properties. Report range [0:0] - [3968:2240] 
ugen1.5: <ELAN Touchscreen> at usbus1 (disconnected)
hmd0: detached
hidusb0: detached
usbhid0: detached

And it would repeatedly cycle these messages, trying to connect every couple of seconds.
So I had to install FreeBSD on this laptop using ttyv1 because that was interrupting my view of the installer.
Also, logging in normally required me to use ttyv1 as well for the same reason.

Fedora MATE 44 works just fine with the touchscreen, by comparison.
