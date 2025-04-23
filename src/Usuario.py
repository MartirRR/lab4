
from Cancion import *
from ListaReproduccion import ListaReproduccion
from pila import Pila
from cola import Cola
class Usuario:
    def __init__(self, nombre:str, password:str, biblioteca = [], listas_reproduccion = [], amigos= [], historial= Pila(), cola_reproduccion= Cola()):
        self.__nombre = nombre
        self.__password = password
        self.__biblioteca = biblioteca #Lista de dicccionarios ( "cancion" "descargada")
        self.__listas_reproduccion = listas_reproduccion
        self.__amigos = amigos
        self.__historial = historial
        self.__cola_reproduccion = cola_reproduccion
        self.__contador_reproducciones = {}
   
   
   
    #Getters:
    def get_nombre(self):
        return self.__nombre
    

    def get_contador(self):
        return self.__contador_reproducciones

    def get_password(self):
        return self.__password
    
    def get_biblioteca(self):
        return self.__biblioteca
    
    def get_listas_reproduccion(self):
        return self.__listas_reproduccion
    
    def get_amigos(self):
        return self.__amigos
    
    def get_historial(self):
        return self.__historial
    
    def get_cola_reproduccion(self):
        return self.__cola_reproduccion

    #Setters

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_password(self, password):
        self.__password = password

    def set_biblioteca(self, biblioteca):
        self.__biblioteca = biblioteca

    def set_listas_reproduccion(self, listas_reproduccion):
        self.__listas_reproduccion = listas_reproduccion

    def set_amigos(self, amigpos):
        self.__amigos = amigpos


    def set_historial(self, historial):
        self.__historial = historial

    def cola_reproduccion(self, cola_reproduccion):
        self.__cola_reproduccion = cola_reproduccion

    #Métodos de clase:

    def agregar_a_biblioteca(self, cancion):
        
        for i in self.__biblioteca:
            if i["cancion"].get_id() == cancion.get_id():
                return False
            
        self.__biblioteca.append({"cancion": cancion, "descargada": False})
        return True

    def ver_biblioteca(self):
        
        if not self.__biblioteca:
            return False
        
        else:
            print("Tu biblioteca:")
            for i in self.__biblioteca:
                estado_descarga = "Descargada" if  i["descargada"] else "No descargada"
                print(f"-{i['cancion'].get_id()}|{(i['cancion']).get_titulo()}| {(i['cancion']).get_artista()}| {estado_descarga}")
            return True

    def eliminar_cancion_biblioteca(self, cancion):
        if self.__biblioteca == []:
                return False
        else:
            self.__biblioteca.remove(cancion)
            return True
        

    def crear_lista(self, nombre):
        nueva_lista = ListaReproduccion(nombre)
        self.__listas_reproduccion.append(nueva_lista)
        return nueva_lista
    
    def eliminar_lista(self, nombre):
        for lista in self.__listas_reproduccion:
            if lista.get_nombre() == nombre:
                self.__listas_reproduccion.remove(lista)
                
                return True
            
        return False

    def __str__(self):
        return(f'Nombre: {self.__nombre}| Biblioteca: {len(self.__biblioteca)} canciones| Listas de reproducción: {len(self.__listas_reproduccion)}| Amigos: {len(self.__amigos)}')


    def agregar_a_historial(self, cancion):
        self.get_historial().push(cancion)

    def deshacer_reproduccion(self):
        self.get_historial().pop()


    def mostrar_historial(self):
        self.get_historial().imprime()

    def agregar_a_espera(self, cancion):
        self.__cola_reproduccion.add(cancion)

    def reproducir_siguiente(self):
        tema = self.get_cola_reproduccion().first()
        self.__cola_reproduccion.remove()
        print(f"Se está reproduciendo la cancion '{tema.get_titulo()}'")
        self.agregar_a_historial(tema)
        tema.set_reproducciones(tema.get_reproducciones()+ 1)

    def mostrar_lista_espera(self):
        self.__cola_reproduccion.imprime()
        

    def reproducir_cancion(self, cancion):
        if cancion.get_id() in self.__contador_reproducciones:
            self.__contador_reproducciones[cancion.get_id()] += 1
        else:
            self.__contador_reproducciones[cancion.get_id()] = 1
        super().reproducir_cancion(cancion)

    








#Creación de la clase hija UsuarioPremium
class UsuarioPremium(Usuario):
    def __init__(self, nombre, password, biblioteca = [], listas_reproduccion=[], amigos = [], listas_reproduccion_seguidas = []):
        super().__init__(nombre, password, biblioteca,listas_reproduccion, amigos)
        self.__listas_reproduccion_seguidas = listas_reproduccion_seguidas

    def get_listas_reproduccion_seguidas(self):
        return self.__listas_reproduccion_seguidas
    
    def set_listas_reproduccion_seguidas(self, listas_repoduccion_seguidas):
        self.__listas_reproduccion_seguidas = listas_repoduccion_seguidas

    
    def descargar_cancion(self, cancion):
        
        cancion["descargada"] = True
        return True
       


    def canciones_descargadas(self):
        return[cancion["cancion"] for cancion in self.get_biblioteca() if cancion["descargada"]]
        
    
    def eliminar_descarga(self, cancion):
        for i in self.get_bibilioteca():
            if i["cancion"].get_id()==cancion.get_id():
                i["descargada"]=False
                print("La canción ha sido eliminada de las descargas.")
                return True
        print("La canción no está en la bibiloteca.")
        return False
    
    def seguir_lista_reproduccion(self, lista_reproduccion):
            self.__listas_reproduccion_seguidas.append(lista_reproduccion)
            return True
  

#Clase UsuarioFree:
class UsuarioFree(Usuario):
    def __init__(self, nombre, password, biblioteca = [], listas_reproduccion=[], amigos = [], fecha_registro = date.today()):
        super().__init__(nombre, password, biblioteca, listas_reproduccion, amigos)
        self.__fecha_registro = fecha_registro

    #Getters
    def get_fecha_registro(self):
        return self.__fecha_registro
    
    #Setters
    def set_fecha_registro(self, fecha_registro):
        self.__fecha_registro = fecha_registro

    #Métodos

    def ver_anuncio(self):
        mostrar_anuncio()

    def comprobar_fecha(self):
        tiempo_registrado = date.today() - self.__fecha_registro
        if tiempo_registrado.days > 730:
            return True
        else:
            return False



