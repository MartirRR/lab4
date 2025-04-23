

from lista_enlazada import ListaEnlazada

class Pila(ListaEnlazada):

    def __init__(self, dato=None):
        super().__init__(dato)

    def push(self,dato): #"Empuja" el elemento nuevo, que pasa a ser la cabeza
        self.anade_elemento_cabeza(dato)

    def top(self):
        """
        Devuelve sin extraer el elemento en la cima de la pila
        """

        return self.get_cabeza().get_dato() if not self.vacia() else None
    

    def pop(self):
        """
        Extrae y devuelve el elemento en la cima de la pila
        """
        if not self.vacia():
            dato = self.get_cabeza().get_dato()
            self.set_cabeza(self.get_cabeza().get_sig())
            self.set_tamano(self.get_tamano()-1)
            return dato
        else:
            None


