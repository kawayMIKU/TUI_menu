import ctypes
from ctypes import wintypes, byref, Structure, POINTER, Union
import os

# 定义 Windows API 中使用的类型
class COORD(Structure):
    _fields_ = [("X", wintypes.SHORT), ("Y", wintypes.SHORT)]

class SMALL_RECT(Structure):
    _fields_ = [("Left", wintypes.SHORT), ("Top", wintypes.SHORT),
                ("Right", wintypes.SHORT), ("Bottom", wintypes.SHORT)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [("dwSize", COORD), ("dwCursorPosition", COORD),
                ("wAttributes", wintypes.WORD),
                ("srWindow", SMALL_RECT), ("dwMaximumWindowSize", COORD)]
    
# 定义常量
class constants:
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    ENABLE_LINE_INPUT = 0x0002
    ENABLE_MOUSE_INPUT = 0x0010
    ENABLE_WINDOW_INPUT = 0x0008
    ENABLE_EXTENDED_FLAGS = 0x0080
    ENABLE_PROCESSED_INPUT = 0x0001
    ENABLE_ECHO_INPUT = 0x0004
    
    FOCUS_EVENT = 0x0010 #事件成员包含 FOCUS_EVENT_RECORD 结构。 这些事件在内部使用且应忽略。
    KEY_EVENT = 0x0001# 事件成员包含 KEY_EVENT_RECORD 结构，以及有关键盘事件的信息。
    MENU_EVENT = 0x0008 #事件成员包含 MENU_EVENT_RECORD 结构。 这些事件在内部使用且应忽略。
    MOUSE_EVENT = 0x0002 #事件成员包含 MOUSE_EVENT_RECORD 结构，以及有关鼠标移动或按下按钮事件的信息。
    WINDOW_BUFFER_SIZE_EVENT = 0x0004 #事件成员包含 WINDOW_BUFFER_SIZE_RECORD 结构，以及有关控制台屏幕缓冲区新大小的信息。

    mouse_listen_mode =  ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS
    full_listen_mode = ENABLE_WINDOW_INPUT | ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS
    normal_mode = ENABLE_LINE_INPUT | ENABLE_PROCESSED_INPUT | ENABLE_ECHO_INPUT
    none_mode = 0x0000

    FROM_LEFT_1ST_BUTTON_PRESSED = 0x0001 #最左侧的鼠标按钮。
    FROM_LEFT_2ND_BUTTON_PRESSED = 0x0004 #左侧的第二个按钮。
    FROM_LEFT_3RD_BUTTON_PRESSED = 0x0008 #左侧的第三个按钮。
    FROM_LEFT_4TH_BUTTON_PRESSED = 0x0010 #左侧的第四个按钮。
    RIGHTMOST_BUTTON_PRESSED = 0x0002 #最右侧的鼠标按钮。

    DOUBLE_CLICK = 0x0002 #所发生的双击操作的第二次单击（按钮按下）。 第一次单击将作为常规按钮按下事件返回。
    MOUSE_HWHEELED = 0x0008	#水平鼠标滚轮已移动。 如果 dwButtonState 成员的高字包含正值，则滚轮向右旋转。 否则，滚轮向左旋转。
    MOUSE_MOVED = 0x0001 #发生了鼠标位置更改。
    MOUSE_WHEELED = 0x0004 #垂直鼠标滚轮已移动。 如果 dwButtonState 成员的高字包含正值，则滚轮向前旋转，远离用户。 否则，滚轮向后旋转，接近用户。
    
    class uChar(Union): 
        _fields_ = [
        ("UnicodeChar", wintypes.WCHAR),
        ("AsciiChar", wintypes.CHAR)
        ]
    
class KEY_EVENT_RECORD(Structure):
    _fields_ = [
        
        #_KEY_EVENT_RECORD
        ("bKeyDown", wintypes.BOOL  ),
        ("wRepeatCount", wintypes.WORD  ),
        ("wVirtualKeyCode", wintypes.WORD  ),
        ("wVirtualScanCode", wintypes.WORD  ),
        ("uChar", constants.uChar),


        #公用
        ("dwControlKeyState", wintypes.DWORD), #_KEY_EVENT_RECORD, _MOUSE_EVENT_RECORD,

        ]
constants.KEY_EVENT_RECORD = KEY_EVENT_RECORD
class MOUSE_EVENT_RECORD(Structure):
    _fields_ = [

        #_MOUSE_EVENT_RECORD
        ("dwMousePosition", COORD),
        ("dwButtonState", wintypes.DWORD),
        ("dwEventFlags", wintypes.DWORD),

        #公用
        ("dwControlKeyState", wintypes.DWORD), #_KEY_EVENT_RECORD, _MOUSE_EVENT_RECORD,

        ]
constants.MOUSE_EVENT_RECORD = MOUSE_EVENT_RECORD
class MENU_EVENT_RECORD(Structure):
    _fields_ = [

        #_MENU_EVENT_RECORD
        ("dwCommandId", wintypes.UINT),

        ]
constants.MENU_EVENT_RECORD = MENU_EVENT_RECORD
class FOCUS_EVENT_RECORD(Structure):
    _fields_ = [

        #_FOCUS_EVENT_RECORD
        ("bSetFocus",wintypes.BOOL),


        ]
constants.FOCUS_EVENT_RECORD = FOCUS_EVENT_RECORD
class WINDOW_BUFFER_SIZE_RECORD(Structure):
    _fields_ = [

        #_WINDOW_BUFFER_SIZE_RECORD
        ("dwSize",COORD),

        ]
constants.WINDOW_BUFFER_SIZE_RECORD = WINDOW_BUFFER_SIZE_RECORD
class Event(Union):
    _fields_ = [

            ("KeyEvent",constants.KEY_EVENT_RECORD),
            ("MouseEvent",constants.MOUSE_EVENT_RECORD),
    ("WindowBufferSizeEvent",constants.WINDOW_BUFFER_SIZE_RECORD),
            ("MenuEvent",constants.MENU_EVENT_RECORD),
            ("FocusEvent",constants.FOCUS_EVENT_RECORD)

    ]
constants.Event = Event
class INPUT_RECORD(Structure):
    _fields_ = [
    ("EventType", wintypes.WORD),
    ("Event", constants.Event),
    ]
constants.INPUT_RECORD = INPUT_RECORD

# 加载 kernel32.dll
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

ReadConsoleInput = kernel32.ReadConsoleInputW
ReadConsoleInput.argtypes = [wintypes.HANDLE, POINTER(constants.INPUT_RECORD), wintypes.DWORD, POINTER(wintypes.DWORD)]
ReadConsoleInput.restype = wintypes.BOOL
# 函数原型
GetStdHandle = kernel32.GetStdHandle
GetStdHandle.argtypes = [wintypes.DWORD]
GetStdHandle.restype = wintypes.HANDLE

SetConsoleMode = kernel32.SetConsoleMode
SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
SetConsoleMode.restype = wintypes.BOOL



def get_console_size():
    return os.get_terminal_size()


# 设置控制台模式以启用鼠标事件
STD_INPUT_HANDLE = None
STD_OUTPUT_HANDLE = None
STD_ERROR_HANDLE = None
listen_mode = None
def init():
    global STD_INPUT_HANDLE,STD_OUTPUT_HANDLE,STD_ERROR_HANDLE
    STD_INPUT_HANDLE = GetStdHandle(constants.STD_INPUT_HANDLE)
    STD_OUTPUT_HANDLE = GetStdHandle(constants.STD_OUTPUT_HANDLE)
    STD_ERROR_HANDLE = GetStdHandle(constants.STD_ERROR_HANDLE)
def set_listen_mode(mode):
    global STD_INPUT_HANDLE,listen_mode
    if not STD_INPUT_HANDLE:
        raise ctypes.WinError(ctypes.get_last_error())

    if not SetConsoleMode(STD_INPUT_HANDLE,mode):
        raise ctypes.WinError(ctypes.get_last_error())
    listen_mode = mode
     
def get_cursor_position():
    # 获取当前控制台句柄
    console_handle = STD_OUTPUT_HANDLE

    # 定义一个CONSOLE_SCREEN_BUFFER_INFO结构体

    # 获取光标信息
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    ctypes.windll.kernel32.GetConsoleScreenBufferInfo(console_handle, ctypes.byref(csbi))

    # 返回光标的x和y坐标位置
    return csbi.dwCursorPosition.X, csbi.dwCursorPosition.Y


def input_record(nEvents=1):
        global STD_INPUT_HANDLE
        
        events = (constants.INPUT_RECORD * nEvents)()
        num_records = wintypes.DWORD()
        
        if not ReadConsoleInput(STD_INPUT_HANDLE, events, nEvents, byref(num_records)):
            raise ctypes.WinError(ctypes.get_last_error())
        '''if num_records.value > 0 and event.EventType == MOUSE_EVENT:
            mouse_event = event.Event
            print('dwMousePosition',mouse_event.dwMousePosition.X,mouse_event.dwMousePosition.Y)
            print('dwButtonState',mouse_event.dwButtonState)  # MOUSE_MOVED
            print('dwControlKeyState',mouse_event.dwControlKeyState)  # MOUSE_MOVED
            print('dwEventFlags',mouse_event.dwEventFlags)  # MOUSE_MOVED'''
        if num_records.value > 0:
            return events
        else:
            return None
            

# 调用函数以获取鼠标事件

if __name__ == '__main__': 
    # 
    # 随心画2.0!！
    # 新版特性：可以在键盘上输入字符设置画笔，可以用空格作为橡皮擦
    # 
    init()
    set_listen_mode(constants.mouse_listen_mode)
    def paint(pos,r=1,fill='%'):
        for i in range(-r,r+1):
            for j in range(-r,r+1):
                print("\033[{};{}H".format(round(pos[0]-i),round(pos[1]-j)),end='',flush=False)
                print(fill,end='',flush=False)
    char = '%'
    r = 0
    state = None
    down = False
    last = (0,0)
    while True:
        print('\033[1;0H',end='',flush=False)
        print(' '*get_console_size()[0],flush=False)
        print('\033[1;0H',end='',flush=False)
        text = '随心画 {}*{} [{}] {} {}'.format(char,r,state,get_console_size()[0],get_console_size()[1])
        print(text+'   ',end='',flush=False)
        print('\033[{};{}H'.format(0,get_console_size()[0]-2),end='',flush=False)
        print('- ×',end='',flush=False)
        print('\033[2;0H',end='',flush=False)
        print(' '*get_console_size()[0],flush=False)
        event = input_record()
        event = event[0]
        if event.EventType == constants.MOUSE_EVENT:
            
            state = event.Event.MouseEvent.dwButtonState
            if event.Event.MouseEvent.dwButtonState == 8388608:
                r += 1
            if event.Event.MouseEvent.dwButtonState == 4286578688:
                r -= 1
                if r < 0:
                    r = 0
            if event.Event.MouseEvent.dwButtonState in (0x01,0x02):
                
            
                print('\033[0;0H',end='',flush=False)
                
                
                if event.Event.MouseEvent.dwButtonState == 0x01:
                    if(event.Event.MouseEvent.dwMousePosition.Y,event.Event.MouseEvent.dwMousePosition.X) == (0,get_console_size()[0]-1):
                        break

                    pos2 = event.Event.MouseEvent.dwMousePosition.Y+1,event.Event.MouseEvent.dwMousePosition.X+1
                    if not down:
                        last  = pos2
                    down = True
                    
                    x = last[0]
                    y = last[1]
                    x2 = pos2[0]
                    y2 = pos2[1]

                    if abs(x2-x) >= abs(y2-y):
                        try:
                            dy = (y2-y)/(x2-x)
                        except:
                            dy = 0
                        if x2<x:
                            rev = -1
                        else:
                            rev = 1
                        i = 0
                        while i <= abs(x2 - x):
                            dx = i
                            paint((round(dx*rev+x),round(dx*rev*dy+y)),r=r,fill=char)
                            i += 1
                            
                    else:
                        try:
                            dx = (x2-x)/(y2-y)
                        except:
                            dx = 0
                        if y2<y:
                            rev = -1
                        else:
                            rev = 1
                        i = 0
                        while i <= abs(y2 - y):
                            dy = i
                            paint((round(dy*rev*dx+x),round(dy*rev+y)),r=r,fill=char)
                            i += 1
                    last = pos2
                else:
                    pass
            else:
                down = False
        if event.EventType == constants.KEY_EVENT:
            key = event.Event.KeyEvent.wVirtualKeyCode
            if event.Event.KeyEvent.bKeyDown:
                if not (key in 
                        (128,65408,13,37,39,67,8,46,
                        
                        8,9,12,13,16,17,18,20,
                        27,33,34,35,36,45,144,175,174,179,173,172,180,170,171,) or
                    (key>=112 and key<=123) or
                    key >= 1000
                    ):
                    try:
                        r = int(event.Event.KeyEvent.uChar.UnicodeChar)
                    except:
                        char = event.Event.KeyEvent.uChar.UnicodeChar