# -*- coding: utf-8 -*-

import maskpass
print("Password input using getch (limited features).")
print(f"Entered password is {maskpass.askpass(mask='*')}", end="\n\n")
print("Now without any echo (like in Unix).")
print(f"Password is {maskpass.askpass(mask='')}", end="\n\n")
print("Now using pynput, press Ctrl to reveal while typing, press again to unreveal.")
print(f"The password is {maskpass.advpass(mask='*')}")
