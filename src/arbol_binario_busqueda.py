from arbol_binario import NodoAB, ArbolBinario
from Cancion import *

class NodoABB(NodoAB):
    def __init__(self, val, izq=None, der=None):
        super().__init__(val, izq, der)

    def encontrar_minimo(self, nodo):
        if nodo is None:
            return None
        while nodo.get_hijo_izq() is not None:
            nodo = nodo.get_hijo_izq()
        return nodo
    
    
    def busca_valor(self, valor_buscado):
        result = None
        if self is not None:
            valor = self.get_valor()
            if valor_buscado == valor: # OJO, para que esto funcione debemos implementar __eq__ en Cancion
                result = self
            elif valor_buscado < valor: # OJO, para que esto funcione debemos implementar __lt__ (less than) en Cancion
                if self.get_hijo_izq() is not None:
                    result = self.get_hijo_izq().busca_valor(valor_buscado)
            elif valor_buscado > valor:
                if self.get_hijo_der() is not None:
                    result = self.get_hijo_der().busca_valor(valor_buscado)
        return result

    def inserta_valor(self, nodo, nuevo_nodo):
        if nodo is None:
            return nuevo_nodo
        nuevo_valor = nuevo_nodo.get_valor()
        valor = nodo.get_valor()
        
        if nuevo_valor > valor :
            hijo_der = nodo.get_hijo_der()
            nodo.set_hijo_der(self.inserta_valor(hijo_der, nuevo_nodo))

        elif nuevo_valor < valor :
            hijo_izq = nuevo_nodo.get_hijo_izq()
            nodo.set_hijo_izqd(self.inserta_valor(hijo_izq, nuevo_nodo))
        
        return nodo
    


    def elimina_valor(self, nodo, valor):
        if nodo is None:
            return nodo
        valor_actual = nodo.get_valor()
        if valor < valor_actual:
            nodo.set_hijo_izq(self.elimina_valor(nodo.get_hijo_izq(), valor))
        elif valor > valor_actual:
            nodo.set_hijo_der(self.elimina_valor(nodo.get_hijo_der(), valor))
        else:
            if nodo.get_hijo_izq() is None and nodo.get_hijo_der() is None:
                return None
            elif nodo.get_hijo_izq() is None:
                return nodo.get_hijo_der()
            elif nodo.get_hijo_der() is None:
                return nodo.get_hijo_izq()
            else:
                
                siguiente = self.encontrar_minimo(nodo.get_hijo_der())
                nodo.set_valor(siguiente.get_valor())
                nodo.set_hijo_der(self.elimina_valor(nodo.get_hijo_der(), siguiente.get_valor()))


class ArbolBinarioBusqueda(ArbolBinario):

    def __init__(self, nodo_raiz=None):
        super().__init__(nodo_raiz)

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
    def __init__(self, nodo_raiz=None):
        super().__init__(nodo_raiz)

    def busca_cancion(self, titulo, artista):
        raiz = self.get_raiz()
        cancion_buscada = Cancion(titulo, artista)
        return raiz.busca_valor(cancion_buscada)    
    
    def introducir_cancion(self, cancion):
        raiz = self.get_raiz()
        if raiz is not None:
            raiz.inserta_valor(raiz, NodoABB(cancion))
        else:
            self.set_raiz(NodoABB(cancion))

    def eliminar_cancion(self, cancion):
        raiz = self.get_raiz()
        if raiz is not None:
            raiz_nueva = raiz.elimina_valor(raiz, cancion)
            self.set_raiz(raiz_nueva)
            
        