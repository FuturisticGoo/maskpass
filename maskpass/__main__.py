# -*- coding: utf-8 -*-
"""
Simple example usage of the module maskpass
"""

import maskpass


print("Password input using getch (limited features).")
print("Entered password is", maskpass.askpass(mask="*"), end="\n\n")
print("Now without any echo (like in Unix).")
print("Password is", maskpass.askpass(mask=""), end="\n\n")
print("Now using pynput, press left Ctrl to reveal and unreveal while typing")
print("The password is", maskpass.advpass(mask="*"))
print("Now without echo in advpass, left Ctrl reveal works here too.")
print("The password is ", maskpass.advpass(mask=""))
