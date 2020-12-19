# Maskpass

Maskpass is a Python library like getpass but with advanced features like masking and reveal/unreveal.  
It also supports Spyder IDLE

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install maskpass.

```bash
pip install maskpass
```

### Usage
This module contains functions askpass() and advpass()
askpass() uses msvcrt.getch() in windows and altenatives in *nix OS, but it doesn't work in Spyder. 

advpass() uses [pynput](https://pypi.org/project/pynput/) to get the password, and it works in Spyder too!

```python
import maskpass
password=maskpass.askpass()

```

The function returns the entered password in string format
Accepts 2 optional arguments prompt, mask and idle.  Default for prompt is `Enter password: `.  Default for mask is `*`.
Use ` mask=""` for not echoing anything into the terminal. (Like entering sudo passwords in *nix)


### Using advpass()


```python
import maskpass
password=maskpass.advpass()
```
The function returns the entered password in string format
Accepts 3 optional arguments prompt, mask and idle.  Default for prompt is `Enter password: `.  Default for mask is `*`. idle expects a bool, it is for overriding IDLE check.

`advpass()` also has a revealing feature which will toggle the visibility of the entered password when `Left CTRL` is pressed. Press it again to change back the visibility.
Note: Only works with `advpass()` and needs [pynput](https://pypi.org/project/pynput/)

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
Currently I have only tested it in Windows 10, Manjaro and Parrot, so I'm not sure it works in macOS.
The `advpass()` works well in Spyder, Windows cmd/powershell/terminal and Linux terminal.
Haven't tested it in PyCharm yet, so it might work.

### License
[MIT License](https://choosealicense.com/licenses/mit/)
