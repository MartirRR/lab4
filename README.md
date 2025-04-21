# 🌳 LAB4: Árboles Binarios de Búsqueda en el Sistema de Música en Streaming

## Objetivos Generales
1. Comprender e implementar un Árbol Binario de Búsqueda (ABB) genérico en Python.  
2. Aplicar principios de responsabilidad única separando la lógica genérica de estructuras de datos de la lógica de dominio.  
3. Integrar el ABB en el sistema de streaming para acelerar búsquedas y mantener las canciones ordenadas.  
4. Practicar la definición de clases y subclases, uso de métodos mágicos y modularidad.

## Archivos Proporcionados
- arbol_binario.py
- arbol_binario_busqueda.py  
- Tú código del LAB3 con Catalogo, Usuario, etc.

## Actividades

### 0. Lógica Genérica del ABB
- Revisa las clases proporcionadas de AB y ABB y completa las funciones que faltan.  
- Todas las funciones de búsqueda, agregar o eliminar deben trabajar a nivel de objeto, en nuestro caso `valor = Cancion`.

### 1. Clase Cancion con Métodos "Mágicos"
- Asegurar que la clase Cancion implemente `__lt__` y `__eq__` basados en el título y artista.  
- Garantizar que las comparaciones entre objetos Cancion funcionen de manera consistente.

### 2. Crea una subclase de ABB para un ABB de Canciones
- Crea ArbolCancion, subclase de ArbolBinarioBusqueda, con métodos de nuestro programa, como por ejemplo funciones para buscar por título y artista.
- Ejemplo de código para buscar por título y artista usando ArbolCancion
```python
def busca_cancion(self, titulo_cancion, artista):
    raiz = self.get_raiz()
    cancion = Cancion(titulo_cancion,artista,...) # completar creando una cancion temporal para ser buscada (el resto de valores no hacen falta)
    return raiz.busca_valor(cancion)
```
### 3. Integración en el Catálogo
- Modificar la clase Catálogo para usar ArbolCancion, como un nuevo atributo donde las canciones estarán en un ABB.  
- Extiende los métodos en Catálogo de agregar y eliminar para que también añadan y eliminen del ABB.
- Implementa una nueva función de buscar por título y artista que use el ABB dentro de catálogo.

### 4. Haz pruebas de busquedas y calcula el tiempo

- En `main.py` implementa una función que:
  1. Selecciona 5 canciones al azar del catálogo.
  2. Para cada cancion, ejecuta 5 búsquedas en la **lista enlazada** y mida el tiempo total.
  3. Para cada cancion, ejecuta 5 búsquedas en el **ABB** y mida el tiempo total.
  4. Calcula y muestra (en `experiments.md`) los tiempos medios de búsqueda para cada estructura.

```python
import time

# Ejemplo de función a cronometrar
def mi_tarea():
    total = 0
    for i in range(10_000_000):
        total += i
    return total

# Medir tiempo de ejecución
start = time.perf_counter()
resultado = mi_tarea()
end = time.perf_counter()

elapsed_ms = (end - start) * 1000  # milisegundos
print(f"Tiempo de ejecución: {elapsed_ms:.2f} ms")
```

## Criterios de Entrega
- Código bien estructurado y documentado.  
- Pruebas unitarias que cubran inserción, búsqueda, eliminación y recorrido.
- Demostración de la búsqueda eficiente y del catálogo ordenado en consola.  