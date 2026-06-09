# Dell Latitude 7490 comments
Almost all the hardware works as expected including the LTE broadband adapter. But the Bluetooth support lacks behind: the system is able to see the device and use the correct kernel module, it is possible to scan and see the Bluetooth devices nearby, and even the connection succeeds. However it is not possible to use Bluetooth devices: even when device is connected, neither Bluetooth mouse, nor Bluetooth headphones appear in devices list.

Next is the sample from `usbconfig` report:
```
ugen0.4: <AX210 Bluetooth Intel Corp.> at usbus0, cfg=0 md=HOST spd=FULL (12Mbps) pwr=ON (100mA)
ugen0.4.0: ubt0: <vendor 0x8087 product 0x0032, class 224/1, rev 2.01/0.00, addr 3>
```

