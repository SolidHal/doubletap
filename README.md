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


# Why this project is depreciated

Through some testing, I found some issues with using two tap straps (really, these are issues with tap straps in general) versus using a "normal" physical keyboard

1) The lack of discrete feedback makes reliably typing difficult.

When you type a pattern, it is possible to have the straps vibrate indicating it recognized the input and provided the input to the connected device

But this vibration is less accurate than the feedback you receive while typing on a normal keyboard.

When typing, you get two forms of feedback

- tactile feedback that a key under a specific finger was pressed

- positional feedback, you can tell where your hand it on the keyboard and identify miss-presses long before you see the mispress on screen


2) reducing your hands to 1 input at a time is very inefficient

On a normal keyboard, each finger is a discrete input. While you press a key, you can move all of your other fingers into position to type the next characters.

This ability is lost entirely when using the tapstrap. Now instead of 2^10 inputs to the computer, you have 2^1.

This can be improved a bit by mapping common usages to single finger patterns, but there is a hard limit on how quickly you can tap a sequence of
single finger patterns since the tap strap needs to have some time window delay to detect pressing 2 one finger pattern versus a single 2 finger pattern.
normal keyboards do not have this restriction (besides modifier keys like control, alt, etc)


Because of this, I have not pursued the two tap strap idea further.
