# -*- coding: utf-8 -*-

"""
# Library maskpass with two functions askpass and advpass.
## askpass
     askpass uses standard library to get non blocking input and
     returns the password.
     askpass doesn't work in some IDEs like Spyder.
## advpass
     advpass uses pynput to get text and returns the password.
     advpass works in both console and also in Spyder. Not sure
     if it works in other IDEs.

"""

from .methods.without_pynput import askpass
from .methods.with_pynput import advpass

__all__ = ["askpass", "advpass"]

if __name__ == "__main__":
    print(advpass(mask="*", suppress=True))
    input("Press enter to exit...")
