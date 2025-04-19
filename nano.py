class Nano:
    @staticmethod
    def getStartFinish(target,file,howfarfromline):
        start = target
        nspassed = 0
        while True:
            if start > 0:
                start -= 1
            else:
                break
            if file[start] == '\n':
                nspassed += 1
            if nspassed > howfarfromline :
                start +=1
                break
        finish = target
        nspassed = 0
        while True:
            if file[finish] == '\n':
                nspassed += 1
            if nspassed > howfarfromline :
                finish -=1
                break
            if finish < len(file) - 1:
                finish += 1
            else:
                break
        return (start,finish)
    @staticmethod
    def down(target,file):
        distanceFromLane = 0
        temp = target
        while True:
            if temp!= 0 and file[temp - 1] != '\n':
                temp -= 1
                distanceFromLane += 1
            else:
                break
        while True:
            if target != len(file)-1 and file[target] != '\n':
                target += 1
            else:
                break
        if file[target] == '\n' and target != len(file)-1:
            target += 1
        for i in range(distanceFromLane):
            if target != len(file)-1 and file[target] != '\n':
                target += 1
        return target
    @staticmethod
    def up(target,file):
        distanceFromLane = 0
        temp = target
        while True:
            if temp!= 0 and file[temp - 1] != '\n':
                temp -= 1
                distanceFromLane += 1
            else:
                break
        while True:
            if target != 0 and file[target-1] != '\n':
                target -= 1
            else:
                break
        if file[target-1] == '\n' and target != 0:
            target -= 1
        while True:
            if target != 0 and file[target-1] != '\n':
                target -= 1
            else:
                break
        for i in range(distanceFromLane):
            if file[target] != '\n':
                target += 1
        return target
    @staticmethod
    def erase(target,file):
        temp = ''
        i = 0
        while i < len(file):
            if i == target-1:
                i += 1
            temp += file[i]
            i += 1
        file = temp
        target -= 1
        return (target,file)