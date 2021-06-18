# Maskpass

Maskpass is a Python library like getpass but with advanced features like masking and reveal/un-reveal.   
It also works in Spyder IDE

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [maskpass](https://pypi.org/project/maskpass/).

```bash
pip install maskpass
```

It is currently recommended to enforce a version if you have plans to use it in a project, since backward incompatible changes may occur.

### Usage

This module contains functions askpass() and advpass()  
askpass() uses msvcrt.getch() in windows and altenatives in *nix OS, but it doesn't work in Spyder. 

```python
import maskpass
password = maskpass.askpass()

```

The function returns the entered password in string format  
Accepts 2 optional arguments prompt and mask.

Default for prompt is `Enter password: `.  Default for mask is `*`.  
Use ` mask=""` for not echoing anything into the terminal. (Like entering sudo passwords in *nix)

### Using advpass()

advpass() uses [pynput](https://pypi.org/project/pynput/) to get the password, and it works in Spyder too!


```python
import maskpass
password = maskpass.advpass()
```
The function returns the entered password in string format.  

Accepts 4 optional arguments prompt, mask, ide and suppress.  

* prompt is the string to be printed. Default for prompt is `Enter password:` .   

* mask is the masking character to be used, can be an empty string `""`, single or multi length character. Default for mask is `*`.

* ide expects a bool, it is for overriding IDE check, and has default False. Usually there is no need to change this, since it's automatically checked whether it's running on IDE or terminal.  Default is `False`.
* suppress expects a bool, is used only in Spyder/QTConsole. Setting this to True prevents the input from being passed to the rest of the system. See [pynput documentation](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Listener) for more info. This prevents the Spyder console from jumping down when spacebar is pressed. Default is `True` .

`advpass()` also has a revealing feature which will toggle the visibility of the entered password when `Left CTRL` is pressed. Press it again to change back the visibility.  
Note: Only works with `advpass()` and needs [pynput](https://pypi.org/project/pynput/)

### Exceptions and other returns

In both askpass and advpass, pressing `Ctrl+C` raise the usual `KeyboardInterrupt`.  

Also, pressing `Escape` in both functions stops the input and returns an empty string `""`. 

### Screenshots

![Example GIF](https://raw.githubusercontent.com/FuturisticGoo/maskpass/main/images/example.gif)
>Normal askpass

![Spyder Example GIF](https://raw.githubusercontent.com/FuturisticGoo/maskpass/main/images/example2.gif)
>advpass in Spyder

![Terminal Example GIF](https://raw.githubusercontent.com/FuturisticGoo/maskpass/main/images/example3.gif)
>advpass in terminal

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Issues

There is an issue in Spyder where pressing and holding the backspace key yields unpredictable result. This only happens when the key is held down and only in Spyder. Only workaround right now is to backspace letter by letter and not hold it down. 

![Spyder Backspace Bug](https://raw.githubusercontent.com/FuturisticGoo/maskpass/main/images/backspace_bug.gif)

>Holding down backspace in advpass in Spyder

Currently I have only tested it in Windows 10, Manjaro and Parrot, so I'm not sure it works in macOS.  

This will not work in Jupyter Notebook correctly. Haven't tested it in PyCharm yet, so it might work.

### Tips

In some platforms, namely Termux in Android, maskpass does not get installed because pynput cannot install in that. In those platform (or in cases where you don't need advpass), if you would like to use only askpass, just copy both `/maskpass/input_methods/without_pynput.py ` and `/maskpass/input_methods/cross_getch` to your desired location and you can use askpass using `from without_pynput import askpass`

### License

[MIT License](https://choosealicense.com/licenses/mit/)
