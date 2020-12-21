# -*- coding: utf-8 -*-

import maskpass
print("Password input using getch (limited features).")
print("Entered password is", maskpass.askpass(mask="*"), end="\n\n")
print("Now without any echo (like in Unix).")
print("Password is", maskpass.askpass(mask=""), end="\n\n")
print("Now using pynput, press Ctrl to reveal while typing, press again to unreveal.")
print("The password is", maskpass.advpass(mask="*"))
print("Now without echo in advpass, Ctrl reveal works here too.")
print("The password is ", maskpass.advpass(mask=""))
