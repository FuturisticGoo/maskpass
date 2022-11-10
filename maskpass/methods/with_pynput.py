# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 05:18:52 2021

@author: FuturisticGoo
"""

import sys
from .cross_getch import CrossGetch


def advpass(prompt="Enter Password: ", mask="*", ide=False, suppress=True):
    """
    Description
    ----------
    An advanced version of the askpass which works in Spyder/Qtconsole and
    has a revealing feature

    Parameters
    ----------
    prompt : The prompt shown for asking password, optional
        DESCRIPTION. The default is "Enter Password: ".
    mask : The masking character, use "" for max security, optional
        DESCRIPTION. The default is "*".
    ide : Pass True if getch or linux getch not supported like in Spyder
        DESCRIPTION. Default is False
    suppress : Pass True to stop QTConsole from jumping when Spacebar is pressed
        DESCRIPTION. Default is True
    Raises
    ------
    KeyboardInterrupt
        When CTRL+C pressed while typing the password

    Returns
    -------
    Password
        Returns the entered password as string type
        Returns empty string "" if Escape pressed

    """
    from pynput import keyboard

    print(prompt, end="", flush=True)

    to_reveal = False
    count = 0
    mask_length = len(mask)
    password_input = ""
    try:
        # Checking if we're running in IPython/QtConsole/Spyder
        __IPYTHON__
        import IPython
        if(type(get_ipython())==IPython.terminal.interactiveshell.TerminalInteractiveShell):
            # Means its IPython but in terminal, so tty_check is set to True
            tty_check = True and not ide
        else:
            tty_check = False

    except NameError:
        tty_check = True and not ide
    ctrl_hold = False

    def on_press(key):

        nonlocal password_input, count, to_reveal, ctrl_hold

        try:
            if key.char in ["\x03"]:
                # CTRL+C character
                raise KeyboardInterrupt

            elif ctrl_hold and key.char.lower() == "c":
                # When using suppressed, CTRL+C doesn't get caught, so
                # this is a hacky way to detect that. Also raising error in
                # suppressed mode doesn't work, so it's raised later by
                # setting password_input as None
                password_input = None
                return False

            else:
                password_input += key.char
                # If to_reveal is True, it means the character which is
                # entered is printed, else, the masking character is printed
                char = key.char if to_reveal else mask
                print(char, end="", flush=True)
                if char != "":
                    count += 1

        except AttributeError:
            if key in [keyboard.Key.ctrl_r, keyboard.Key.ctrl_l] :
                # ctrl_hold stays True until it's released
                ctrl_hold = True


            if key == keyboard.Key.enter:
                # End listening
                return False

            elif key == keyboard.Key.space:
                char = " " if to_reveal else mask
                print(char, end="", flush=True)
                password_input += " "
                count += 1

            elif key == keyboard.Key.backspace:
                password_input = password_input[:-1]
                if count != 0:
                    # In Spyder IDE, backspace character doesn't
                    # work as expected for this, but a combination
                    # of backspace and \u200c works. So
                    # sys.stdout.isatty() is used to check whether
                    # it's the IDE console or not.
                    if tty_check:
                        if to_reveal:
                            print("\b \b", end="", flush=True)
                        else:
                            # Handling different length masking character
                            print("\b \b"*mask_length, end="", flush=True)
                    else:
                        if to_reveal:
                            print("\b\u200c", end="", flush=True)
                        else:
                            # Handling different length masking character
                            print(("\b"*mask_length)+("\u200c"*mask_length),
                                  end="", flush=True)
                    count -= 1

            elif key == keyboard.Key.ctrl_l:
                # Fancy way of revealing/unrevealing the characters
                # entered by pressing CTRL key
                to_reveal = not to_reveal

                if mask == "":
                    # If mask is "", then that means nothing has been
                    # printed while typing. So no need to remove characters
                    # from screen. Just straight up print the stuff
                    # typed before
                    if to_reveal:
                        print(password_input, end="", flush=True)
                        count = len(password_input)
                    else:
                        # Usual checking whether it's IDE/console
                        if tty_check:
                            print("\b \b"*len(password_input),
                                  end="", flush=True)
                        else:
                            print(("\b"*len(password_input)) +
                                  ("\u200c"*len(password_input)),
                                  end="", flush=True)
                        count = 0
                else:
                    # If the mask isn't "", then something has been
                    # printed on the screen and we need to remove it
                    # before printing the previously entered text
                    if to_reveal:
                        # The masking character could be multilength.
                        # So we print destructive backspace character
                        # times the length of previously entered
                        # text times the length of masking character
                        # to remove it completely
                        if tty_check:
                            print(("\b \b"*len(password_input)*mask_length) +
                                  password_input, end="", flush=True)
                        else:
                            print(("\b"*len(password_input)*mask_length) +
                                  ("\u200c"*len(password_input)*mask_length) +
                                  password_input, end="", flush=True)
                    else:
                        # Just removing the printed text and printing
                        # the mask character to unreveal the text.
                        print(("\b"*len(password_input)) +
                              (mask*len(password_input)), end="", flush=True)


            elif key == keyboard.Key.esc:
                password_input = ""
                return False

            else:
                # We don't need anything else as input, so just-
                pass


    def on_release(key):
        """
        Function only for detecting CTRL key release
        """
        nonlocal ctrl_hold
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            ctrl_hold = False

    if tty_check:
        listener = keyboard.Listener(on_press=on_press)
    else:
        # Passing suppress True prevents qtconsole from jumping on
        # pressing Spacebar
        listener = keyboard.Listener(on_press=on_press,
                                     on_release=on_release, suppress=suppress)

    listener.start()

    if tty_check:
        # You see, if you're using advpass in normal console, it's
        # actually listening to the input in background, sort of like a
        # keylogger. So while you're focussing on the console and typing
        # into that, pynput is collecting input from the background,
        # at the same time the console is keeping the input in buffer waiting
        # to put text into the console. The problem here is that, after
        # using advpass, the entered text will get put into the console
        # when it allows input afterwards. So, if you call advpass first
        # and then input(), we will get the password_input return from
        # advpass, but the entered text will also get into the input()
        # But things work differently in Spyder. It doesn't keep it in
        # in buffer. So, to work in both the environments, we use a
        # dummy getch/posix_getch just to capture the input in console
        # which will run simultaneously with the background input
        # listening so as to remove it from buffer. It will stop
        # when Enter is pressed.
        cross_getch = CrossGetch()
        while True:
            dummy_key = cross_getch.getch()
            if dummy_key in [b"\r", b"\x1b"]:
                break
            elif dummy_key == b"\x03":
                print(flush=True)  # To put a newline before the error
                raise KeyboardInterrupt
    else:
        try:
            listener.join()
        except KeyboardInterrupt as error:
            raise KeyboardInterrupt(error)

    print(flush=True)

    if password_input is None:
        raise KeyboardInterrupt

    return password_input

