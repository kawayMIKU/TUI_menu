import console_events
import time
import unicodedata
def is_full_width(char):
    return unicodedata.east_asian_width(char) in ('F', 'W')
def menu(
        menu_=['选项1','选项2','选项3'],
        ask='\033[35m[?]\033[0m选择一个项\033[0m ',
        cursor='❯ ',
        input_cursor='\033[7;32;5m',
        choice_color='\033[32m',
        enter_color='\033[33m',
        double_click=0.5,
        hide_console_cursor='\033[?25l',
        hide_console_cursor_back = '\033[?25h',
        console_mode = console_events.constants.mouse_listen_mode,
        console_mode_back = console_events.constants.normal_mode,
        ):
    console_events.init()
    console_events.set_listen_mode(console_mode)
    menu__ = []
    for i in menu_:
        menu__.append(str(i))
    m = []
    for i in range(len(menu__)):
        m.append((menu__[i],i))
    choice = 0
    l = len(m)
    c_l = len(cursor)
    s_l = [0 for i in range(l+1)]
    buffer = ''
    buffer += hide_console_cursor
    lock2 = False
    bk = False
    input = ''
    lock = False
    l_1 = l+1
    print('\n'*l_1+'\033['+str(l_1)+'A',end='')
    oy = console_events.get_cursor_position()[1]
    oy = oy+1
    tc = 0
    ctrlc = False
    lock_ = -1
    t = float('-inf')
    while not bk:
        event = console_events.input_record()
        event_ = event[0]
        if event_.EventType == console_events.constants.MOUSE_EVENT:
            ad = event_.Event.MouseEvent.dwButtonState
            ay = event_.Event.MouseEvent.dwMousePosition.Y
            af = event_.Event.MouseEvent.dwEventFlags
            if(
                (ad == console_events.constants.FROM_LEFT_1ST_BUTTON_PRESSED) and
                (ay >= oy) and
                (ay < oy+l) and
                not lock
                ):
                choice = ay-oy
                if lock_ == choice:
                    if time.time() - t <= double_click:
                        t = time.time()
                        while True:
                            event_ = console_events.input_record()[0]
                            if event_.EventType == console_events.constants.MOUSE_EVENT:
                                if event_.Event.MouseEvent.dwButtonState == 0:
                                    
                                    if time.time()-t <= double_click:
                                        bk = True
                                        break
                                    else:
                                        break
                    else:
                        t = time.time()
                else:
                    t = time.time()
                lock_ = choice
            lock = ad == console_events.constants.FROM_LEFT_1ST_BUTTON_PRESSED
            if ad == 8388608:
                choice -= 1
                if choice < 0:
                    choice = l-1
            if ad == 4286578688:
                choice += 1
                if choice > l-1:
                    choice = 0
        elif event_.EventType == console_events.constants.KEY_EVENT:
            key = event_.Event.KeyEvent.wVirtualKeyCode
            if event_.Event.KeyEvent.bKeyDown:
                if key in (ord('&'),128):
                    choice -= 1
                    if choice < 0:
                        choice = l-1
                elif key in (ord('('),65408):
                    choice += 1
                    if choice > l-1:
                        choice = 0
                elif key == 13 or bk:
                    if l != 0:
                        bk = True
                        break
                    #pass
                elif key in (ord('%'),37):
                    if tc >= 1:
                        tc -= 1
                elif key in (ord("'"),39):
                    tc += 1
                    l_ = len(input)
                    if tc > l_:
                        tc = l_
                elif key in (67,):
                    ctrlc = True
                    bk = True
                    break

                else:
                    if key == 8:
                        if tc >= 1:
                            input = input[:tc-1] + input[tc:]
                            tc -= 1
                    elif key == 46:
                        input = input[:tc] + input[tc+1:]
                    elif (key in 
                          (8,9,12,13,16,17,18,20,
                          27,32,33,34,35,36,45,144,175,174,179,173,172,180,170,171,) or
                        (key>=112 and key<=123) or
                        key >= 1000
                        ):
                        pass
                    else:
                        li_ = list(input)
                        li_.insert(tc,event_.Event.KeyEvent.uChar.UnicodeChar)
                        input = ''.join(li_)
                        tc += len(event_.Event.KeyEvent.uChar.UnicodeChar)
                    li = []
                    for i in range(len(menu__)):
                        if input in menu__[i]:
                            li.append((menu__[i],i))
                    m = li
                    l = len(li)
                    choice = 0

        li_ = list(input+' ')
        li_.insert(tc,input_cursor)
        li_.insert(tc+2,'\033[0m')
        tx = ask + ''.join(li_)
        buffer += tx + '\n'
        if lock2:
            space = '\033['+str(len(s_l))+'A'
            for i in s_l:
                space += ' '*i + '\n'
            space += '\033['+str(len(s_l))+'A'
        else:
            space = ''
            lock2 = True
        for i in range(l):
            if i == choice:
                tx = cursor + choice_color + m[i][0] + '\033[0m'
            else:
                tx = ' '*c_l + m[i][0]
            buffer += (tx) + '\n'
        buffer = buffer[:-1]
        print(space+buffer)
        s_l = []
        for i in buffer.split('\n'):
            count = 0
            for j in i:
                if is_full_width(j):
                    count += 2
                else:
                    count += 1
            s_l.append(count) 
        buffer = ''
    space = '\033['+str(len(s_l))+'A'
    for i in s_l:
        space += ' '*i + '\n'
    space += '\033['+str(len(s_l))+'A'
    if ctrlc:
        buffer = space+ask+input
    else:
        buffer = space+ask+enter_color+m[choice][0]+'\033[0m'
    buffer += hide_console_cursor_back
    print(buffer)
    console_events.set_listen_mode(console_mode_back)
    if ctrlc:
        return -1
    else:
        return m[choice][1]
if __name__ == '__main__':
    print(menu(['1','2','3']))
