

class NodoAB:
    def __init__(self, val, izq=None, der=None):
        self.__valor = val
        self.__hijoIzq = izq
        self.__hijoDer = der

    def get_hijo_izq(self):
        return self.__hijoIzq

    def get_hijo_der(self):
        return self.__hijoDer

    def set_valor(self, val):
        self.__valor = val

    def get_valor(self):
        return self.__valor

    def set_hijo_izq(self, izq):
        self.__hijoIzq = izq

    def set_hijo_der(self, der):
        self.__hijoDer = der

    def __str__(self):
        return str(self.__valor)

    def insert_izq(self, nuevo_nodo):
        if self.__hijoIzq is None:
            self.__hijoIzq = nuevo_nodo
        else:
            nuevo_nodo.__hijoIzq = self.__hijoIzq
            self.__hijoIzq = nuevo_nodo

    def insert_der(self, nuevo_nodo):
        if self.__hijoDer is None:
            self.__hijoDer = nuevo_nodo
        else:
            nuevo_nodo.__hijoDer = self.__hijoDer
            self.__hijoDer = nuevo_nodo

    def tamano(self):
        pass

    def dibuja(self, prefijo=""):
        if self is not None:
            if self.__hijoDer is not None:
                self.__hijoDer.dibuja(prefijo + "\t")
            print(prefijo + "|-- " + str(self.__valor))
            if self.__hijoIzq is not None:
                self.__hijoIzq.dibuja(prefijo + "\t")

    def preorden(self):
        if self.__valor is not None:
            print(self, end=' ')
        if self.__hijoIzq is not None:
            self.__hijoIzq.preorden()
        if self.__hijoDer is not None:
            self.__hijoDer.preorden()

    def postorden(self):
       pass

    def inorden(self):
        pass

    def lista_preorden(self, lista_previa):
        pass

    def lista_postorden(self, lista_previa):
        pass

    def lista_inorden(self, lista_previa):
        pass

class ArbolBinario:

    def __init__(self, nodo_raiz=None):
        self.__raiz = nodo_raiz
        if nodo_raiz is None:
            self.__tamano = 0
        else:
            self.__tamano = self.__raiz.tamano()

    def get_raiz(self):
        return self.__raiz

    def get_tamano(self):
        return self.__tamano

    def dibuja_arbol(self):
        if self.__raiz is not None:
            self.__raiz.dibuja()
        else:
            print('El arbol está vacio\n')

    def preorden(self):
        raiz = self.__raiz
        raiz.preorden()

    def lista_preorden(self):
        raiz = self.__raiz
        return raiz.lista_preorden(lista_previa=[])

    def postorden(self):
        raiz = self.__raiz
        raiz.postorden()

    def lista_postorden(self):
        raiz = self.__raiz
        return raiz.lista_postorden(lista_previa=[])

    def inorden(self):
        raiz = self.__raiz
        raiz.inorden()

    def lista_inorden(self):
        raiz = self.__raiz
        return raiz.lista_inorden(lista_previa=[])