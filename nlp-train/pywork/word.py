#codig=utf-8

class word(object):
    def __init__(self,name,bgram={},times=0):
        self.__name = name
        self.__bgram = bgram
        self.__times = times

    def get_times(self):
        return self.__times

    def update_times(self,val):
        self.__times += val

    def update_dict(self,bg):
        if bg in self.__bgram:
            self.__bgram[bg] += 1
        else:
            self.__bgram[bg] = 1
