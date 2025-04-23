




from lista_enlazada import ListaEnlazada


class Cola(ListaEnlazada):

    def __init__(self, dato=None):
        super().__init__(dato)

    def add(self, dato):
        self.anade_elemento_final(dato)
    
    def first(self):
        return self.get_cabeza().get_dato() if not self.vacia() else None
        

    def remove(self):
        """Extrae y devuelve el primero elemento de la cola (FIFO)"""
        if not self.vacia():
            dato = self.get_cabeza().get_dato()
            self.set_cabeza(self.get_cabeza().get_sig())
            self.set_tamano(self.get_tamano() - 1)
            return dato
        else:
            return None