laptop info: Lenovo ThinkPad E-15 Gen 2, Intel Core i5 1135G7

known issues and bugs:
1. after resume from S3:
    * applications will take a long time to open on sway and internet will be
    gone with ping showing 100% packet loss -- `service netif restart` fixes
    both completely
    
    * the keyboard works mostly (input, etc. are fine) but:
        1. the CAPS-lock LED will be stuck in the on position (however, the
        CAPS state itself toggles fine)
        2. the XF86Audio{Raise/Lower}Volume keys don't work (they work before
        suspend)
        
        output of `kbdcontrol -d` and `kbdcontrol -i` are identical before and
        after suspend/resume
    
    * exactly once, it happened that the keyboard did not work at all (no
    input) after resume until I switched to a different vty and back; once I
    did, everything worked perfectly (i.e., even the caps/audio issue above did
    not happen) - I am still trying to replicate this.

1. bluetooth:
      loading ng_ubt does not make any bluetooth devices visible (i.e., no
      'ubt' related messages in /var/log/messages; like in FreeBSD Handbook
      34.7.1. Loading Bluetooth Support)

      I did not investigate any further

1. hybrid NVidia MX350 dGPU:
      the latest nvidia-drm-kmod pkg will *not* work (there will be kernel
      messages telling you to downgrade), you need to install
      nvidia-drm-kmod-580

      however, even with nvidia-drm-kmod-580, sway wm (wlr) reports
      /dev/dri/card0 as not being a DRM device

      I could not investigate further and am just using the integrated Intel
      GPU which works perfectly.

1. the laptop appears to run perceptibly hotter than on Linux; I have no
conjecture as to why.
