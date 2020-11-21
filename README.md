THE FITHINATOR
==============

A small Python application designed to run on a RasPi and use an attached LCD screen to display FITH TF2 server data.

CONFIGURE
=========
Edit `config.yml`.  Comes with FITH servers pre-configured.

Default config location is `/boot/fithinator.yml` to allow editing the config via SD card.

INSTALL
=======
```
apt-get update
apt-get install python3-pygame
sudo pip3 install git+https://github.com/yesrod/fithinator.git
```

RUN
===
```
sudo python3 -m fithinator -c config.yml
```

Systemd script is provided under `systemd` for convenience.

CASE
====
A case is available at https://www.thingiverse.com/thing:4660995 that holds a Pi Zero W and an ILI9341 2.2" LCD module.
