from utils import *

class Cancion:
    def __init__(self, id, titulo:str, artista:str, album:str, duracion:int, popularidad:int, reproducciones:int = 0):
        self.__id= id
        self.__titulo= titulo
        self.__artista = artista
        self.__album = album
        self.__duracion = duracion
        self.__popularidad = popularidad
        self.__reproducciones = reproducciones if reproducciones is not None else 0
    
    
    #Getters:
    def get_id(self):
        return self.__id
    
    def get_titulo(self):
        return self.__titulo
    
    def get_artista(self):
        return self.__artista
    
    def get_album(self):
        return self.__album
    
    def get_duracion(self):
        return self.__duracion
    
    def get_popularidad(self):
        return self.__popularidad
    
    def get_reproducciones(self):
        return self.__reproducciones if self.__reproducciones is not None else 0


    #Setter:
    def set_id(self,id):
        self.__id = id

    def set_titulo(self, titulo):
        self.__titulo = titulo

    def set_artista(self,artista):
        self.__artista = artista

    def set_album(self,album):
        self.__album = album

    def set_duracion(self,duracion):
        self.__duracion = duracion

    def set_popularidad(self,popularidad):
        self.__popularidad = popularidad

    def set_reproducciones(self, reproducciones):
        self.__reproducciones = reproducciones


    #Métodos de clase:
    def duracion_formateada(self):
        duracion_entera = int(self.__duracion)
        return convertir_seg_a_min_seg(duracion_entera)
    
    def es_mas_larga(self, otra_cancion):
        if self.__duracion > otra_cancion.__duracion:
            return True
        else:
            return False
        
    def mismo_artista(self, otra_cancion):
        if self.__artista.strip().lower().replace(" ", "") == otra_cancion.__artista.strip().lower().replace(" ", ""):
            return True
        else:
            return False

    def mismo_album(self, otra_cancion):
        if self.__album.strip().lower().replace(" ", "") == otra_cancion.__album.strip().lower().replace(" ", ""):
            return True
        else:
            return False
        
    def es_mas_popular(self, otra_cancion):
        if self.__popularidad > otra_cancion.__popularidad:
            return True
        else:
            return False
    
    def reproducir_cancion(self):
        if not self.__reproducciones:
            self.__reproducciones = 1

        else:
            self.__reproducciones +=1


    def __str__(self):
        return(f'{self.__id}| {self.__titulo}| {self.__artista}| {self.__album}| {self.__duracion}| {self.__popularidad} ')
        


    def __eq__(self, otra_cancion):
        return self.get_titulo() == otra_cancion.get_titulo() and self.get_artista() == otra_cancion.get_artista() and self.get_album() == otra_cancion.get_album()
    
    
        