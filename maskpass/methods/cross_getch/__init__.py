import sys
import platform

class CrossGetch:
    """
    Cross platform getch
    """

    def __init__(self):
        if platform.system() == "Windows":
            import msvcrt
            self.getch = msvcrt.getch
        else:
            self.getch = self.posix_getch

    def posix_getch(self):
        """
        Alternative getch for posix
        Straight from stackoverflow.
        """
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
