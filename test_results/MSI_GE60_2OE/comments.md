The laptop uses Hybrid nvidia + intel GPUs (nvidia uses legacy 470 driver)

the laptop runs with the intel GPU but It's not possible to use the nvidia gpu using 
"prime rendering ofload" due to lack of drm modesetting for 470 drivers under FreeBSD 
(I'm not sure If I could use something like bumblebee "A workaround for hybrid graphics that exists under linux")

See Also : https://forums.freebsd.org/threads/freebsd-on-legacy-nvidia-hybrid-laptop.101808

Note : I'm using GhostBSD 15 xfce (I'm not using KDE)

suspend seems to work when pressing suspend option graphically from xfce and the LED sleep indicator works

pressing the power button lightly shuts down the laptop completely instead of suspending/sleeping

when suspending I see TTY for a bit then it disappears

when closing the laptop lid and open it the screen goes black until I repeat the process (closing and opening the lid)

the mouse movement lags a bit after resume then continue to work fine (not sure If it shouldn't lag)

there are lots of things I havent test well
