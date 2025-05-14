from lista_enlazada import *
from Cancion import Cancion
from arbol_binario import *
from arbol_binario_busqueda import *

class Catalogo:
    def __init__(self, actuales = ListaEnlazada(), eliminadas = ListaEnlazada(), actualesABB = ArbolCancion()):
        self.__actuales = actuales
        self.__eliminadas = eliminadas
        self.__actualesABB = actualesABB

    #Getters:
    def get_actuales(self):
        return self.__actuales
    
    def get_eliminadas(self):
        return self.__eliminadas
    
    def get_actualesABB(self):
        return self.__actualesABB
    
    #Setters:
    def set_actuales(self, actuales):
        self.__actuales = actuales

    def set_actuales(self, eliminadas):
        self.__eliminadas = eliminadas
        
    def set_actualesABB(self, actualesABB):
        self.__actualesABB = actualesABB

    #Métodos:
    def agregar_cancion(self, cancion):
        repetida = False
        
        if isinstance(cancion, Cancion):
            nodo = self.__actuales.get_cabeza()
            while nodo is not None:
                if nodo.get_dato().get_titulo() == cancion.get_titulo() and nodo.get_dato().get_artista().strip().lower().replace(" ", "") == cancion.get_artista().strip().lower().replace(" ", ""):
                    repetida = True
                nodo = nodo.get_sig()


            if repetida:
                return False
            
            else:
                cancion.set_id(self.__actuales.get_tamano() + self.__eliminadas.get_tamano()+ 1)
                self.__actuales.anade_elemento_cabeza(cancion)
                self.__actualesABB.insertar(cancion)
                return True
       

    def mostrar_catalogo(self):
        self.__actuales.imprime()

    def eliminar_cancion(self, cancion):
        if self.__actuales.vacia():
            print("El catálogo está vacío. No hay canciones a eliminar")
            return False    
        else:
            if isinstance(cancion, Cancion):
                self.__actuales.elimina_elemento(cancion)
                self.__eliminadas.anade_elemento_cabeza(cancion)
                self.__actualesABB.eliminar_cancion(cancion)
                return 
            

    def buscar_artista(self, artista):
        # artista =(input("Introduce el artista: "))
        artista_nomalizado = artista.strip().lower().replace(" ", "")
        canciones_artista = []
        cancion = self.__actuales.get_cabeza()
        while cancion is not None:
            if cancion.get_dato().get_artista().strip().lower().replace(" ", "") == artista_nomalizado:
                canciones_artista.append(cancion.get_dato())
            cancion = cancion.get_sig()

        return canciones_artista
    
    def filtrado_inteligente(self, artista):
        # artista =(input("Introduce el artista: "))
        artista_nomalizado = artista.strip().lower().replace(" ", "")
        canciones_artista1 = []
        cancion = self.__actuales.get_cabeza()
        while cancion is not None:
            if cancion.get_dato().get_artista().strip().lower().replace(" ", "") == artista_nomalizado:
                canciones_artista1.append(cancion.get_dato())
            cancion = cancion.get_sig()

        return canciones_artista1



            

    def top_populares(self, n):
        # n = int(input("Introduce el número de canciones para el top: "))
        canciones = []
        nodo = self.__actuales.get_cabeza()
        while nodo is not None : 
            canciones.append(nodo.get_dato())
            nodo = nodo.get_sig()
        ordenado = sorted(canciones, key= lambda x: x.get_popularidad(), reverse= True)
        return ordenado[:n]
        
    def buscar_id(self, id_cancion):
        cancion = self.__actuales.get_cabeza()
        while cancion is not None:
            if cancion.get_dato().get_id() == id_cancion:
                return cancion.get_dato()
            else:
                cancion = cancion.get_sig()
        return None

       
    
    def mapear_id(self):
        ides = []
        nodo = self.__actuales.get_cabeza()
        while nodo is not None:
            ides.append(nodo.get_dato().get_id())
            nodo = nodo.get_sig()
        return ides
        

    def buscar_titulo_artista_ABB(self, titulo, artista):
        return self.__actualesABB.busca_cancion(titulo, artista)