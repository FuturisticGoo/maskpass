# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 05:16:41 2021

@author: FuturisticGoo
"""

#from maskpass.input_methods.cross_getch import CrossGetch

try:
    from .cross_getch import CrossGetch
except ImportError:
    from cross_getch import CrossGetch


def askpass(prompt="Enter Password: ", mask="*"):
    """
    Description
    ----------
    A simple function which can be used for asking password

    Parameters
    ----------
    prompt : String, optional
        DESCRIPTION. The default is "Enter Password: ".

    mask : String, optional
        DESCRIPTION. Masks the input password.
                     The default is "*", "" can be used for
                     no masking like in Unix passwords.
                     Single length string preferred, multi length string works.
    Raises
    ------
    KeyboardInterrupt
        When CTRL+C pressed while typing the password

    Returns
    -------
    Returns the entered password in string format.
    Returns empty string "" if ESC pressed

    """

    char = b""
    password_input = b""
    count = 0
    cross_getch = CrossGetch()

    print(prompt, end="", flush=True)

    while True:
        char = cross_getch.getch()
        if char == b"\x03":
            # Ctrl-C Character
            raise KeyboardInterrupt
        elif char == b"\x1b":
            # Escape character
            password_input = b""
            break
        elif char == b"\r":
            break
        elif char == b"\t":
            break
        elif char in [b"\x08", b"\x7f"]:
            if count != 0:
                print("\b \b"*len(mask), end="", flush=True)
                count -= 1
            password_input = password_input[:-1]
        else:
            print(mask, end="", flush=True)
            if mask != "":
                count += 1
            password_input += char
    print(flush=True)
    return password_input.decode()
