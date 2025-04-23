class Nodo:

    def __init__(self, dato, sig=None):
        self.__dato = dato
        self.__sig = sig

    def get_dato(self):
        return self.__dato

    def set_dato(self, dato):
        self.__dato = dato

    def set_sig(self, nodo):
        self.__sig = nodo

    def get_sig(self):
        return self.__sig

    def __str__(self):
        return self.__dato
