# -*- coding: utf-8 -*-

"""
# Library maskpass with two functions askpass and advpass.
## askpass
     askpass uses standard library to get non blocking input and returns the password.
     askpass doesn't work in some IDLEs like Spyder.
## advpass
     advpass uses pynput to get text and returns the password.
     advpass works in both console and also in Spyder. Not sure
     if it works in other IDLEs.

"""
import sys
import platform
import threading

__all__ = ["askpass", "advpass"]

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
    print(flush=True)
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
    
    def toggle(thing):
        # Simple true/false toggler function
        if(thing):
            thing = False
        else:
            thing = True
        return thing

    print(prompt, end="", flush=True)

    to_reveal = False
    count = 0
    password_input = ""

    def on_press(key):

        nonlocal password_input, count, to_reveal

        try:
            if(key.char in ["\x03", "\x1b"]):
                # CTRL+C character
                raise KeyboardInterrupt
            else:
                password_input += key.char
                # If to_reveal is True, it means the character which is
                # entered is printed, else, the masking character is printed
                char = key.char if to_reveal else mask
                print(char, end="", flush=True)
                if(char != ""):
                    count += 1

        except AttributeError:
            if(key == keyboard.Key.enter):
                # End listening
                return False
            elif(key == keyboard.Key.space):
                char = " " if to_reveal else mask
                print(char, end="", flush=True)
                password_input += " "
                count += 1
            elif(key == keyboard.Key.backspace):
                password_input = password_input[:-1]
                if(count != 0):
                    # In Spyder IDLE, backspace character doesn't
                    # work as expected for this, but a combination
                    # of backspace and \u200c works. So 
                    # sys.stdout.isatty() is used to check whether
                    # it's the IDLE console or not.
                    if(sys.stdout.isatty() and not idle):
                        if(to_reveal):
                            print("\b \b", end="", flush=True)
                        else:
                            # Handling different length masking character
                            print("\b \b"*len(mask), end="", flush=True)
                    else:
                        if(to_reveal):
                            print("\b\u200c", end="", flush=True)
                        else:
                            # Handling different length masking character
                            print("\b\u200c"*len(mask), end="", flush=True)
                    count -= 1
            elif(key == keyboard.Key.ctrl_l):
                # Fancy way of revealing/unrevealing the characters 
                # entered by pressing CTRL key
                to_reveal = toggle(to_reveal)
                if(mask == ""):
                    # If mask is "", then that means nothing has been
                    # printed while typing. So no need to remove characters
                    # from screen. Just straight up print the stuff 
                    # typed before
                    if(to_reveal):
                        print(password_input, end="", flush=True)
                        count = len(password_input)
                    else:
                        # Usual checking whether it's IDLE/console
                        if(sys.stdout.isatty() and not idle):
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
                    if(to_reveal):
                        # The masking character could be multilength.
                        # So we print destructive backspace character
                        # times the length of previously entered 
                        # text times the length of masking character
                        # to remove it completely
                        if(sys.stdout.isatty() and not idle):
                            print(("\b \b"*len(password_input)*len(mask)) +
                                  password_input, end="", flush=True)
                        else:
                            print(("\b"*len(password_input)*len(mask)) +
                                  ("\u200c"*len(password_input)*len(mask)) +
                                  password_input, end="", flush=True)
                    else:
                        # Just removing the printed text and printing
                        # the mask character to unreveal the text.
                        print(("\b"*len(password_input)) +
                              (mask*len(password_input)), end="", flush=True)
            else:
                # We don't need anything else as input, so just-
                pass

    def start_ask():
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        # After this, password_input contains the password, so no need to
        # return anything, also, we cannot return anything since we're
        # calling this function from thread so no direct return

    thread = threading.Thread(target=start_ask)
    thread.start()

    if(sys.stdout.isatty() and not idle):
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
    print(flush=True)
    return password_input


if __name__ == "__main__":
    print(advpass(mask="*"))
    input("Press any key to exit...")
