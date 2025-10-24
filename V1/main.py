from users import User
from commands import Commands
from nano import Nano
import curses
def main(stdscr):
    howfarfromline = 21
    roles = {'root' : User('root','root','read','write','rm','touch'), 'support' : User('support','support','read','write')
    , 'guest' : User('guest','guest','read')}
    user = None
    cmd = Commands()
    running = True
    username = ''
    password = ''
    awnser =None
    phase = 'username'
    inp = ''
    while running:
        stdscr.clear()
        if phase == 'username':
            stdscr.addstr(f'username: {username}')
            key = stdscr.getkey()
            if key == '\n':
                phase = 'password'
            elif key == 'KEY_BACKSPACE':
                temp = ''
                for i in range(len(username)-1):
                    temp += username[i]
                username = temp
            elif key == ' ':
                username += ' '
            else:
                try:
                    if ord(key) in range(33,127,1):
                        username += key
                except:
                    pass
            key = ''
        elif phase == 'password':
            stdscr.addstr(f'password: {password}')
            key = stdscr.getkey()
            if key == '\n':
                phase = 'verify'
            elif key == 'KEY_BACKSPACE':
                temp = ''
                for i in range(len(password)-1):
                    temp += password[i]
                password = temp
            elif key == ' ':
                password += ' '
            else:
                try:
                    if ord(key) in range(33,127,1):
                        password += key
                except:
                    pass
            key = ''
        elif phase == 'verify':
            for role in roles:
                if username == roles[role].name and password == roles[role].password:
                    user = roles[role]
                    break
            if user == None:
                username = ''
                password = ''
                phase = 'username'
            else:
                phase = 'cmd'
        elif phase == 'cmd':
            if awnser != None and awnser != True:
                stdscr.addstr(awnser.strip() + '\n' + '$' + inp)
            else:
                stdscr.addstr('$' + inp)
            key = stdscr.getkey()
            if key == '\n':
                inp = inp.strip()
                phase = 'exec'
            elif key == 'KEY_BACKSPACE':
                temp = ''
                for i in range(len(inp)-1):
                    temp += inp[i]
                inp = temp
            elif key == ' ':
                inp += ' '
            else:
                try:
                    if ord(key) in range(33,127,1):
                        inp += key
                except:
                    pass
            key = ''
        elif phase == 'exec':
            if inp == 'logout':
                username = ''
                password = ''
                user = None
                phase = 'username'
                awnser = None
            elif inp == 'pwd':
                awnser = cmd.pwd()
            elif inp == 'ls':
                awnser = cmd.ls()
            elif inp == 'cd':
                awnser = cmd.cd()
            elif inp == 'exit':
                running = False
                awnser = None
            else:
                inp = inp.split(' ')
                if inp[0] == 'cd':
                    awnser = cmd.cd(inp[1])
                elif inp[0] == 'mkdir':
                    awnser = cmd.mkdir(inp[1],user)
                elif inp[0] == 'touch':
                    awnser = cmd.touch(inp[1],user)
                elif inp[0] == 'rm':
                    awnser = cmd.rm(inp[1],user)
                elif inp[0] == 'setline' and inp[1].isdigit() and int(inp[1]) >= 0:
                    howfarfromline = int(inp[1])
                    awnser = None
                elif inp[0] == 'nano':
                    awnser = cmd.nano(inp[1],user)
            if awnser == True:
                phase = 'nano'
            else:
                if phase != 'username':
                    phase = 'cmd'
                inp = ''
        elif phase == 'nano':
            with open(inp[1],'r') as f:
                file = f.read()
            file = file.strip() + '\n'
            if 'write' in user.privlages:
                mode = 'write'
            else:
                mode = 'read'
            target = 0
            curses.curs_set(False)
            while True:
                stdscr.clear()
                start , finish = Nano.getStartFinish(target,file,howfarfromline)
                for i in range(start,finish+1):
                    if i == target:
                            if file[i] == '\n':
                                stdscr.addstr(' \n',curses.A_STANDOUT)
                            else: 
                                stdscr.addstr(file[i],curses.A_STANDOUT)
                    else:
                        stdscr.addstr(file[i])
                stdscr.refresh()
                key = stdscr.getkey()
                if key == 'KEY_LEFT':
                    if target > 0:
                        target -= 1
                elif key == 'KEY_RIGHT':
                    if target < len(file)-1:
                        target += 1
                elif key == 'KEY_DOWN':
                    if target != len(file)-1:
                        target = Nano.down(target,file)
                elif key == 'KEY_UP':
                    if target != 0:
                        target = Nano.up(target,file)
                elif key == 'KEY_BACKSPACE':
                    if target > 0 and mode == 'write':
                        target , file = Nano.erase(target,file)
                elif ord(key) == 15:
                    with open(inp[1],'w') as filetowrite:
                        filetowrite.write(file)
                elif ord(key) == 24:
                    with open(inp[1],'r') as f:
                        lastsave = f.read()
                    lastsave = lastsave.strip() + '\n'
                    if lastsave == file:
                        break
                    else: 
                        stdscr.clear()
                        stdscr.addstr('this file contains unsaved changes do you with to close it and discard the changes ? (Y/n)')
                        stdscr.refresh()
                        while key != 'y' and key !='\n' and key !='n':
                            key = stdscr.getkey()
                        if key == 'y' or key == '\n':
                            break
                else:
                    try:
                        if (key == ' ' or key == '\n' or ord(key) in range(33,127,1)) and mode == 'write':
                            temp = ''
                            for i in range(len(file)):
                                if i == target:
                                    temp += key
                                temp += file[i]
                            file = temp
                            target += 1
                    except:
                        pass
            inp = ''
            phase = 'cmd'
            curses.curs_set(True)
        stdscr.refresh()
                                    
if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except:
        print('please increase the size of your teminal window and try again')