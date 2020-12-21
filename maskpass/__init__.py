# -*- coding: utf-8 -*-

"""
Library maskpass with two functions askpass and advpass
"""
import sys
import platform
import threading

__all__ = ["askpass", "advpass"]


def toggle(thing):
    # Simple true/false toggler function
    if(thing):
        thing = False
    else:
        thing = True
    return thing


if(platform.system() == "Windows"):
    import msvcrt
    is_windows = True
else:
    # Little bit different for Linux or macOS
    def posix_getch():
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.encode()
    is_windows = False


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

    Returns
    -------
    Returns the entered password in string format.
    Returns empty string "" if CTRL+C or ESC pressed
    """

    char = b""
    password_input = b""
    count = 0

    print(prompt, end="", flush=True)

    while(True):
        if(is_windows):
            char = msvcrt.getch()
        else:
            char = posix_getch()
        if(char == b"\x03" or char == b"\x1b"):
            password_input = b""
            break
        elif(char == b"\r"):
            break
        elif(char == b"\x08" or char == b"\x7f"):
            if(count != 0):
                sys.stdout.write("\b \b"*len(mask))
                sys.stdout.flush()
                count -= 1
            password_input = password_input[:-1]
        else:
            sys.stdout.write(mask)
            sys.stdout.flush()
            if(mask != ""):
                count += 1
            password_input += char
    print()
    return password_input.decode()


def advpass(prompt="Enter Password: ", mask="*", idle=False):
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
    idle : Pass True if getch or linux getch not supported like in Spyder
        DESCRIPTION. Default is False
    Raises
    ------
    KeyboardInterrupt
        When CTRL+C pressed while typing the password

    Returns
    -------
    Password
        Returns the entered password as string type

    """
    from pynput import keyboard

    print(prompt, end="", flush=True)

    to_reveal = False
    count = 0
    password_input = ""

    def on_press(key):
        nonlocal password_input, count, to_reveal
        try:
            if(key.char in ["\x03", "\x1b"]):
                raise KeyboardInterrupt
            else:
                password_input += key.char
                char = key.char if to_reveal else mask
                print(char, end="", flush=True)
                if(char != ""):
                    count += 1
        except AttributeError:
            if(key == keyboard.Key.enter):
                return False
            elif(key == keyboard.Key.space):
                char = " " if to_reveal else mask
                print(char, end="", flush=True)
                password_input += " "
            elif(key == keyboard.Key.backspace):
                password_input = password_input[:-1]
                if(count != 0):
                    if(sys.stdout.isatty() and not idle):
                        if(to_reveal):
                            print("\b \b", end="", flush=True)
                        else:
                            print("\b \b"*len(mask), end="", flush=True)
                    else:
                        if(to_reveal):
                            print("\b\u200c", end="", flush=True)
                        else:
                            print("\b\u200c"*len(mask), end="", flush=True)
                    count -= 1
            elif(key == keyboard.Key.ctrl_l):
                to_reveal = toggle(to_reveal)
                if(mask == ""):
                    if(to_reveal):
                        print(password_input, end="", flush=True)
                        count = len(password_input)
                    else:
                        if(sys.stdout.isatty() and not idle):
                            print("\b \b"*len(password_input),
                                  end="", flush=True)
                        else:
                            print(("\b"*len(password_input)) +
                                  ("\u200c"*len(password_input)),
                                  end="", flush=True)
                        count = 0
                else:
                    if(to_reveal):
                        if(sys.stdout.isatty() and not idle):
                            print(("\b \b"*len(password_input)*len(mask)) +
                                  password_input, end="", flush=True)
                        else:
                            print(("\b"*len(password_input)*len(mask)) +
                                  ("\u200c"*len(password_input)*len(mask)) +
                                  password_input, end="", flush=True)
                    else:
                        print(("\b"*len(password_input)) +
                              (mask*len(password_input)), end="", flush=True)
            else:
                pass

    def start_ask():
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        # After this, password_input contains the password, so no need to
        # return anything, also, we cannot return anything becuase we're
        # calling this function from thread so no return

    thread = threading.Thread(target=start_ask)
    thread.start()

    if(sys.stdout.isatty() and not idle):

        if(is_windows):
            while True:
                if(msvcrt.getch() == b"\r"):
                    break
        else:
            while True:
                if(posix_getch() == b"\r"):
                    break
    else:
        thread.join()
    print()
    return password_input


if __name__ == "__main__":
    print(advpass(mask="*"))
    input("Press any key to exit...")
