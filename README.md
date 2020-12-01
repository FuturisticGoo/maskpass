# Maskpass

Maskpass is a Python library like getpass but with advanced features like masking and revealing

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install maskpass.

```bash
pip install maskpass
```

### Usage
This module contains functions askpass() and special_askpass(), both having two optional arguments prompt and mask. The default value for prompt is `Enter Password: ` and for mask is `*`
For most cases, `askpass()` will do, but it doesn't work for Spyder IDLE. `special_askpass()` works for Spyder but it requires [pynput](https://pypi.org/project/pynput/) to be installed. 

```python
import maskpass
password=maskpass.askpass()

```


Use ` mask=""` for not echoing anything into the terminal. (Like entering sudo passwords in *nix)

The function returns the entered password in string format

### For Spyder/QtConsole

```python
import maskpass
password=maskpass.special_askpass()
```

`special_askpass()` also has a revealing feature which will toggle the visibility of the entered password when `Left CTRL` is pressed. Press it again to change back the visibility.
Note: Only works with `special_askpass()` and in Spyder and needs [pynput](https://pypi.org/project/pynput/)

### Screenshots
Normal askpass
![Example GIF](https://raw.githubusercontent.com/FuturisticGoo/maskpass/main/images/example.gif)

Special askpass in Spyder
![Spyder Example GIF](https://raw.githubusercontent.com/FuturisticGoo/maskpass/main/images/example2.gif)

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Issues
Currently I have only tested it in Windows 10, Manjaro and Parrot, so I'm not sure it works in macOS.
The `special_askpass()` works in Spyder. It works in Jupyter Notebook but its not that nice, better to use getpass in Jupyter.
Haven't tested it in PyCharm yet, so it might work.

### License
[MIT License](https://choosealicense.com/licenses/mit/)