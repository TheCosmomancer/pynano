import curses
import os
import sys
class Nano:
    @staticmethod
    def getStartFinish(target, file, howfarfromline):
        start = target
        nspassed = 0
        while True:
            if start > 0:
                start -= 1
            else:
                break
            if file[start] == "\n":
                nspassed += 1
            if nspassed > howfarfromline:
                start += 1
                break
        finish = target
        nspassed = 0
        while True:
            if file[finish] == "\n":
                nspassed += 1
            if nspassed > howfarfromline:
                finish -= 1
                break
            if finish < len(file) - 1:
                finish += 1
            else:
                break
        return (start, finish)

    @staticmethod
    def down(target, file):
        distanceFromLane = 0
        temp = target
        while True:
            if temp != 0 and file[temp - 1] != "\n":
                temp -= 1
                distanceFromLane += 1
            else:
                break
        while True:
            if target != len(file) - 1 and file[target] != "\n":
                target += 1
            else:
                break
        if file[target] == "\n" and target != len(file) - 1:
            target += 1
        for i in range(distanceFromLane):
            if target != len(file) - 1 and file[target] != "\n":
                target += 1
        return target

    @staticmethod
    def up(target, file):
        distanceFromLane = 0
        temp = target
        while True:
            if temp != 0 and file[temp - 1] != "\n":
                temp -= 1
                distanceFromLane += 1
            else:
                break
        while True:
            if target != 0 and file[target - 1] != "\n":
                target -= 1
            else:
                break
        if file[target - 1] == "\n" and target != 0:
            target -= 1
        while True:
            if target != 0 and file[target - 1] != "\n":
                target -= 1
            else:
                break
        for i in range(distanceFromLane):
            if file[target] != "\n":
                target += 1
        return target

    @staticmethod
    def erase(target, file):
        temp = ""
        i = 0
        while i < len(file):
            if i == target - 1:
                i += 1
            temp += file[i]
            i += 1
        file = temp
        target -= 1
        return (target, file)
class File:
    def __init__(self,name,content,next=None,last=None):
        self.name = name
        self.content = content
        self.next = next
        self.last = last
class Stack:
    def __init__(self,file,target,next):
        self.file = file
        self.target = target
        self.next = next
class Clipboard:
    def __init__(self,content,next=None,last=None):
        self.content = content
        self.next = next
        self.last = last
def main(stdscr):
    howfarfromline = 21
    running = True
    firstfile = None
    curentfile =None
    undostack = None
    redostack = None
    inp = ''
    CLIPBOARDSIZE = 5
    clipboardsizern = 0
    highlightingforcopy = False
    startofcopylight = -1
    ClipboardHead = None
    ClipboardTail = None
    curses.init_pair(1,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    if len(sys.argv) != 2:
        print('please enter a filepath or a non-empty directory as an argument')
        return
    if os.path.isfile(sys.argv[1]):
        phase = 'nano'
        with open(sys.argv[1]) as f:
            content = f.read()
        curentfile = [File(name=sys.argv[1], content=content)]
    else:
        phase = 'filepick'
        entries = os.listdir(sys.argv[1])
        for entry in entries:
            if os.path.isfile(entry):
                if firstfile == None:
                    with open(entry) as f:
                        content = f.read()
                    content = content.strip() + '\n'
                    firstfile = [File(name = entry, content = content)]
                    curentfile = firstfile
                else:
                    with open(entry) as f:
                        content = f.read()
                    content = content.strip() + '\n'
                    curentfile[0].next = [File(name = entry, content = content,last=curentfile)]
                    curentfile = curentfile[0].next
        if firstfile == None:
            print('please enter a filepath or a non-empty directory as an argument')
            return

    curentfile = firstfile
    while running:
        stdscr.clear()
        if phase == 'filepick':
            stdscr.addstr(
                f"open file: {curentfile[0].name}"
            )
            if curentfile[0].last:
                stdscr.addstr(f'\nlast file: {curentfile[0].last[0].name}')
            if curentfile[0].next:
                stdscr.addstr(f"\nnext file: {curentfile[0].next[0].name}")
            stdscr.addstr(f"\nsearch: {inp}")
            key = stdscr.getkey()
            if key == '\n':
                phase = 'nano'
            elif key =='KEY_BACKSPACE':
                inp = inp[:-1]
            elif key == 'KEY_DOWN':
                if curentfile[0].next:
                    curentfile = curentfile[0].next
            elif key == 'KEY_UP':
                if curentfile[0].last:
                    curentfile = curentfile[0].last
            else:
                try:
                    if ord(key) == 24:  # ctrl + X
                        break
                    elif(key == ' ' or key == '\n' or ord(key) in range(33,127,1)):
                        inp += key
                        while curentfile[0].next:
                            if curentfile[0].name == inp:
                                break
                            curentfile = curentfile[0].next
                        if curentfile[0].name != inp and curentfile[0].next == None:
                            curentfile = firstfile
                except:
                    pass
        elif phase == 'nano':
            target = 0
            curses.curs_set(False)
            file = curentfile[0].content
            while True:
                stdscr.clear()
                start , finish = Nano.getStartFinish(target,file,howfarfromline)
                for i in range(start,finish+1):
                    if i == target:
                            if file[i] == '\n':
                                stdscr.addstr(' \n',curses.A_STANDOUT)
                            else: 
                                stdscr.addstr(file[i],curses.A_STANDOUT)
                    elif startofcopylight != -1 and startofcopylight <= i < target:
                        stdscr.addstr(file[i],curses.color_pair(1))
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
                else:
                    try:
                        if ord(key) == 8:#ctrl + H
                            highlightingforcopy = not highlightingforcopy
                            if not highlightingforcopy:
                                if target >startofcopylight:
                                    temp = ''
                                    for i in range(len(file)):
                                            if startofcopylight <= i <= target:
                                                temp += file[i]
                                    if clipboardsizern < CLIPBOARDSIZE:
                                        if ClipboardHead:
                                            ClipboardHead = [Clipboard(temp, ClipboardHead)]
                                            ClipboardHead[0].next[0].last = ClipboardHead
                                        else:
                                            ClipboardHead = [Clipboard(temp)]
                                            ClipboardTail = ClipboardHead
                                    else:
                                        ClipboardTail[0].last[0].next = None
                                        ClipboardHead = [Clipboard(temp, ClipboardHead)]
                                        ClipboardHead[0].next[0].last = ClipboardHead
                                    clipboardsizern += 1
                                    if clipboardsizern > 5:
                                        clipboardsizern = 5
                                startofcopylight = -1
                            else:
                                startofcopylight = target
                        elif ord(key) == 2:#ctrl + B
                            openclipboard = True
                            while openclipboard:
                                stdscr.clear()
                                stdscr.addstr('ClipBoard\n')
                                temp = ClipboardHead
                                numtemp = 0
                                stdscr.addstr('Ctrl + X: Exit\n')
                                while temp:
                                    stdscr.addstr(f'{numtemp}: {temp[0].content}\n')
                                    temp = temp[0].next
                                stdscr.refresh()
                                key = stdscr.getkey()
                                if int(key) in range(clipboardsizern):
                                    item2paste = ClipboardHead
                                    for _ in range(int(key)):
                                        item2paste = item2paste[0].next
                                    if undostack:
                                        undostack = [Stack(file, target, undostack)]
                                    else:
                                        undostack = [Stack(file, target, None)]
                                    temp = ''
                                    for i in range(len(file)):
                                        if i == target:
                                            temp += item2paste[0].content
                                        temp += file[i]
                                    file = temp
                                    target += len(item2paste[0].content)
                                    openclipboard = False
                                    break
                                else:
                                    try:
                                        if ord(key) == 24:
                                            openclipboard = False
                                            break
                                    except:
                                        pass
                        elif ord(key) == 15:#ctrl + O
                            with open(curentfile[0].name, "w") as filetowrite:
                                filetowrite.write(file)
                        elif ord(key) == 24:#ctrl + X
                            with open(curentfile[0].name,'r') as f:
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
                                    running = False
                                    break
                        elif not highlightingforcopy:
                            if ord(key) == 18 and redostack:#ctrl + R
                                undostack = [Stack(file, target, undostack)]
                                file, target = redostack[0].file, redostack[0].target
                                redostack = redostack[0].next
                            elif ord(key) == 21 and undostack:#ctrl + U
                                redostack = [Stack(file, target, redostack)]
                                file , target = undostack[0].file, undostack[0].target
                                undostack =  undostack[0].next
                            elif key == 'KEY_BACKSPACE':
                                if target > 0:
                                    if undostack:
                                        undostack = [Stack(file,target, undostack)]
                                    else:
                                        undostack = [Stack(file,target, None)]
                                    target , file = Nano.erase(target,file)
                            else:
                                if (key == ' ' or key == '\n' or ord(key) in range(33,127,1)):
                                    if undostack:
                                        undostack = [Stack(file, target, undostack)]
                                    else:
                                        undostack = [Stack(file, target, None)]
                                    temp = ''
                                    for i in range(len(file)):
                                        if i == target:
                                            temp += key
                                        temp += file[i]
                                    file = temp
                                    target += 1
                    except:
                        pass
            if firstfile != None:
                phase = "filepick"
            curses.curs_set(True)
        stdscr.refresh()
                                    
if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except:
        print('please increase the size of your teminal window and try again')