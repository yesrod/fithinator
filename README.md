THE FITHINATOR
==============

A small Python application designed to run on a RasPi and use an attached LCD screen to display FITH TF2 server data.

CONFIGURE
=========
Edit `config.yml`.  Comes with FITH servers pre-configured.

Default config location is `/boot/fithinator.yml` to allow editing the config via SD card.

INSTALL
=======
Ensure that `dtparam=spi=on` is uncommented in `/boot/config.txt`, then reboot.

```
sudo apt-get update
sudo apt-get install python3-pygame python3-wheel
sudo python3 -m pip install git+https://github.com/yesrod/fithinator.git
```

Newer versions of Python will complain about externally managed environments.  To install on Bookworm and up, use a venv.
```
sudo apt-get update
sudo apt-get install python3-pygame python3-wheel
python3 -m venv ~/.fithinator/
sudo ~/.fithinator/bin/python3 -m pip install git+https://github.com/yesrod/fithinator.git
```

It is recommended to disable powersaving on Bookworm and up, as NetworkManager turns it on by default, and it will cause the Pi to disconnect randomly.
```
sudo nmcli c modify <connection name> 802-11-wireless.powersave 2
```

RUN
===
```
# native
sudo python3 -m fithinator -c /boot/config.yml

# in venv
sudo ~/.fithinator/bin/python3 -m fithinator -c /boot/config.yml
```

Systemd script is provided under `systemd` for convenience.

CASE
====
A case is available at https://www.thingiverse.com/thing:4660995 that holds a Pi Zero W and an ILI9341 2.2" LCD module.
