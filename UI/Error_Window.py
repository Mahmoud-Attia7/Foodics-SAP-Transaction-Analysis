import ctypes


class ErrWindow:
    @staticmethod
    def show_error(message):
        ctypes.windll.user32.MessageBoxW(0, message, "Error", 0x10)
