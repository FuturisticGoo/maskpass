# -*- coding: utf-8 -*-

"""
Function askpass() and special_askpass() which accepts two optional arguments prompt and mask.
"""

import sys
import platform

__all__=["askpass","special_askpass"]

def askpass(prompt="Enter Password: ",mask="*"):
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
                     The default is "*", "" can be used for no masking - nothing gets printed. 
                     Single length string preferred, multi length string works.

    Returns
    -------
    Returns the entered password in string format. Returns empty string "" if CTRL+C or ESC pressed
    """
    
    if(platform.system()=="Windows"):
        import msvcrt
        is_windows=True
    else:   #Little bit different for Linux or macOS
        def posix_getch():
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch.encode()
        is_windows=False
    
    char=b""
    password_input=b""
    count=0
    
    print(prompt,end="",flush=True)
    
    while(True):
        
        if(is_windows):
            char=msvcrt.getch()
        else:
            char=posix_getch()    
        if(char==b"\x03" or char==b"\x1b"):
            password_input=b""
            break    
        elif(char==b"\r"):
            break
        elif(char==b"\x08" or char==b"\x7f"):
            if(count!=0):
                sys.stdout.write("\b \b"*len(mask))
                sys.stdout.flush()
                count-=1
            password_input=password_input[:-1]
        else:
            sys.stdout.write(mask)
            sys.stdout.flush()
            if(mask!=""):
                count+=1 
            password_input+=char
    print()
    return password_input.decode()

def special_askpass(prompt="Enter Password: ",mask="*"):
    """
    

    Parameters
    ----------
    prompt : The prompt shown for asking password, optional
        DESCRIPTION. The default is "Enter Password: ".
    mask : The masking character, use "" for max security, optional
        DESCRIPTION. The default is "*".

    Raises
    ------
    KeyboardInterrupt
        When CTRL+C pressed while typing the password

    Returns
    -------
    Password
        Returns the entered password as string type

    """
    
    def toggle(thing):
        if(thing):
            thing=False
        else:
            thing=True
        return thing
    
    from pynput import keyboard
    
    print(prompt,end="")
    
    reveal=False
    count=0
    password_input=""
    
    def on_press(key):
        nonlocal password_input,count,reveal
        try:
            if(key.char in ["\x03","\x1b"]):
                raise KeyboardInterrupt
            else:
                password_input+=key.char
                char=key.char if reveal else mask
                print(char,end="",flush=True)
                if(char!=""):
                    count+=1
        except AttributeError:
            if(key==keyboard.Key.enter):
                return False
            elif(key==keyboard.Key.space):
                char=" " if reveal else mask
                print(char,end="",flush=True)
                password_input+=" "
            elif(key==keyboard.Key.backspace):
                password_input=password_input[:-1]
                if(count!=0):
                    if(sys.stdout.isatty()):
                        print("\b \b"*len(mask),end="",flush=True)
                    else:
                        print("\b\u200c"*len(mask),end="",flush=True)
                    count-=1
            elif(key==keyboard.Key.ctrl_l):
                reveal=toggle(reveal)
                print("\b"*len(password_input),end="",flush=True)
                if(reveal):
                    print(password_input,end="",flush=True)
                else:
                    print(mask*len(password_input),end="",flush=True)
            else:
                pass
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()
    print()
    return password_input

if __name__=="__main__":
    print(askpass(mask=""))
    input("Press any key to exit...")
