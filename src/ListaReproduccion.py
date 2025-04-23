from Cancion import Cancion
from datetime import date
from Catalogo import Catalogo
class ListaReproduccion:


        def __init__(self, nombre, canciones=[], fecha_creacion = date.today()):
                self.__nombre = nombre
                self.__canciones = canciones
                self.__fecha_creacion = fecha_creacion
        #Getters:
        def get_nombre(self):
                return self.__nombre
        
        def get_fecha(self):
                return self.__fecha_creacion
        
        def get_canciones(self):
                return self.__canciones
        
        #Setters
        def set_nombre(self, nombre):
                self.__nombre = nombre

        def set_fecha(self, fecha):
                self.__fecha_creacion = fecha

        def set_canciones(self, canciones: list):
                self.__canciones = canciones

        #Métodos        
        def agregar_cancion(self, cancion): #En el main se hace la funcion de buscar cancion por id
                self.__canciones.append(cancion)

        def eliminar_cancion(self, cancion):
                for c in self.__canciones:
                                if c.get_id() == cancion.get_id() :
                                        self.__canciones.remove(cancion)
                                        print("La canción ha sido eliminada")


        def ordenar_popularidad(self):
                return sorted(self.__canciones, key= lambda cancion: cancion.get_popularidad(), reverse= True)
        
        def duracion_total(self):
                contador = 0
                for cancion in self.__canciones:
                        contador += int(cancion.get_duracion())
                return contador
        
        def mostrar_lista(self):
                for cancion in self.__canciones:
                        print(cancion)
        

        
        def __str__(self):
                return(f'Nombre:{self.__nombre}| NºCanciones: {len(self.__canciones)}| Fecha de Creación: {self.__fecha_creacion}')  
        
#Clase ListaPublica:

class ListaPublica(ListaReproduccion):
        def __init__(self, nombre, canciones=[], fecha_creacion=date.today(), valoraciones = [], seguidores = []):
                super().__init__(nombre, canciones, fecha_creacion)
                self.__valoraciones = valoraciones
                self.__seguidores = seguidores

        #Getters

        def get_valoraciones(self):
                return self.__valoraciones
        
        def get_seguidores(self):
                return self.__seguidores
        
        #Setters

        def set_valoraciones(self, valoraciones):
                self.__valoraciones = valoraciones

        def set_seguidores(self, seguidores):
                self.__seguidores = seguidores

        #Métodos de clase:

        def valoracion_media(self):
                total = 0
                for i in self.__valoraciones:
                        total += i
                media = (total/ len(self.__valoraciones))
                return media
        
        def agregar_seguidor(self, usuario):
                if usuario not in self.__seguidores:
                        self.__seguidores.append(usuario)
                        
                        return True
                else:
                        
                        return False

        def eliminar_seguidor(self, usuario):
                if usuario in self.__seguidores:
                        self.__seguidores.remove(usuario)
                        print(f"El usuario  {usuario.get_nombre()} ya no sigue la lista {self.get_nombre()} ")
                        return True

                else:
                        print(f"El usuario {usuario.get_nombre()} no sigue la lista {self.get_nombre}")
                        return False