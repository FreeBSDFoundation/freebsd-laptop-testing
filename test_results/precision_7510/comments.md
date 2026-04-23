## Dell Precision 7510

## Tested and working
- keyboard
- touchpad
- hard drive 
- audio (output)

## To be confirmed
- webcam
- bluetooth
- wireless

## Additional information
Of course, from a superuser's perspective, installing a system built from "blocks" is a great adventure. However, if FreeBSD is to reach a wider audience, including laptop users, we must work on making the installation easier and more automated. There is great potential in this OS, so let’s make it better.

As far as I know, another issue is graphics switching. Currently, only one GPU can work at a time, which is a problem for hybrid graphics. I also noticed some dependency issues in certain applications; pkg seems to struggle with that.

If you need more logs or information from my FreeBSD setup, let me know. I am excited to help develop this OS and provide you with useful data. I believe that making the system more user-friendly will help it grow. 

## Fastfetch

```                        `        
  ` `.....---.......--.```   -/     -------
  +o   .--`         /y:`      +.    Host: Precision 7510
   yo`:.            :o      `+-     Kernel: FreeBSD 15.0-RELEASE-p5
    y/               -/`   -o/      Uptime: 13 mins
   .-                  ::/sy+:.     Packages: 1277 (pkg)
   /                     `--  /     Shell: sh
  `:                          :`    Display (LGD04B9): 1920x1080 in 16", 60 Hz [Built-in]
  `:                          :`    DE: KDE Plasma 6.5.5
   /                          /     WM: KWin (X11)
   .-                        -.     WM Theme: Breeze
    --                      -.      Theme: Breeze (Dark) [Qt], Raleigh [GTK2], Adwaita [GTK3]
     `:`                  `:`       Icons: breeze-dark [Qt], breeze [GTK2], breeze-dark [GTK3/4]
       .--             `--.         Font: Noto Sans (10pt) [Qt], Sans (11pt) [GTK2], Noto Sans (10pt) [GTK3/4]
          .---.....----.            Cursor: breeze (24px)
                                    Terminal: konsole 25.12.1
                                    CPU: Intel(R) Core(TM) i7-6820HQ (8) @ 3.60 GHz
                                    GPU 1: Intel HD Graphics 530 [Integrated]
                                    GPU 2: NVIDIA Quadro M2000M [Discrete]
                                    Memory: 3.95 GiB / 31.63 GiB (12%)
                                    Swap: 0 B / 12.00 GiB (0%)
                                    Disk (/): 8.84 GiB / 449.38 GiB (2%) - zfs
                                    Disk (/zroot): 96.00 KiB / 440.53 GiB (0%) - zfs
                                    Local IP (em0): 192.168.8.149/24
                                    Battery (DELL RDYCT14): 73% (2 hours, 24 mins remaining) [Discharging]
                                    Locale: C.UTF-8
