import os
class Commands:
    def __init__(self):
        self.home = os.getcwd()
    @staticmethod
    def pwd ():
        return os.getcwd()
    @staticmethod
    def ls ():
        ret = ''
        for entity in os.listdir():
            ret += f'{entity}\n'
        return ret
    def cd (self , dir='home'):
        if dir == 'home':
            os.chdir(self.home)
        else:
            if dir in os.listdir():
                os.chdir(dir)
            else:
                return f'no directory with the name {dir} exists!'
        return None
    @staticmethod
    def mkdir(dir , user):
        if 'touch' in user.privlages:
            if dir not in os.listdir():
                os.mkdir(dir)
            else:
                return 'directory already exists!'
        else:
            return 'only root users can create new directories!'
        return None
    @staticmethod
    def touch(file , user):
        if 'touch' in user.privlages:
            if file not in os.listdir():
                try:
                    with open(os.path.join(os.getcwd() , file) , 'x') as _ :
                        pass
                except:
                    return 'file could not be created!'
            else:
                return 'file already exists!'
        else:
            return 'only root users can create new files!'
        return None
    @staticmethod
    def rm (target , user):
        if 'rm' in user.privlages:
            if target in os.listdir():
                try:
                    os.removedirs(target)
                except:
                    os.remove(target)
            else:
                return 'target does not exist!'
        else:
            return 'only root users can delete files and folders!'
        return None
    @staticmethod
    def nano(file , user):
        if file in os.listdir():
            return True
        elif 'touch' in user.privlages:
            ret = self.touch(file,user)
            if ret == None:
                return True
            return ret
        else:
            return 'target file dose not exist!'
