from arbol_binario import NodoAB, ArbolBinario


class NodoABB(NodoAB):
    def __init__(self, val, izq=None, der=None):
        super().__init__(val, izq, der)

    def busca_valor(self, valor_buscado):
        result = None
        if self is not None:
            valor = self.get_valor()
            if valor_buscado == valor:
                result = self
            elif valor_buscado < valor: # OJO, para que esto funcione debemos implementar __lt__ (less than) en Cancion
                if self.get_hijo_izq() is not None:
                    result = self.get_hijo_izq().busca_valor(valor_buscado)
            elif valor_buscado > valor:
                if self.get_hijo_der() is not None:
                    result = self.get_hijo_der().busca_valor(valor_buscado)
        return result

    def inserta_valor(self, nodo, nuevo_nodo):
        pass

    def elimina_valor(self, nodo, valor):
        pass


class ArbolBinarioBusqueda(ArbolBinario):

    def __init__(self, nodoRaiz=None):
        super().__init__(nodoRaiz)

    def busca_valor(self, valor_buscado):
        raiz = self.get_raiz()
        return raiz.busca_valor(valor_buscado)

    def insertar(self, valor):
        raiz = self.get_raiz()
        if raiz is not None:
            raiz.inserta_valor(raiz, NodoABB(valor))
        else:
            self.__init__(NodoABB(valor))

    def eliminar(self, valor):
        raiz = self.get_raiz()
        if raiz is not None:
            raiz.elimina_valor(raiz, valor)

class ArbolCancion(ArbolBinarioBusqueda):

    def __init__(self, nodoRaiz=None):
        super().__init__(nodoRaiz)

    def busca_cancion(self, titulo_cancion, artista):
        raiz = self.get_raiz()
        # cancion = Cancion(titulo_cancion,artista,...) # completar creando una cancion temporal para ser buscada (el resto de valores no hacen falta)
        # return raiz.busca_valor(cancion)