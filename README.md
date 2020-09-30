# doubletap

an attempt at using the tap python sdk to map a pair of taps

need the following packages:
sudo apt-get install bluez-tools libbluetooth-dev

need user to be in the bluetooth group: 

```
sudo usermod -G bluetooth -a <username>
#and can reload groups in this shell by running: 
su - $USER
```

need to enable developer mode in the tapmanager
