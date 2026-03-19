The Realtek ethernet NIC on the laptop wouldn't work out of the box and required manually loading the `re` driver using `kld_list="if_re"` inside of `rc.conf`. 
