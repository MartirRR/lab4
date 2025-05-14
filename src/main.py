import csv
from Catalogo import *
from utils import buscar_canciones_apple_music, mostrar_anuncio
from Cancion import *
from ListaReproduccion import *
from Usuario import *
from datetime import date
import random

def mostrar(lista):
    for elemento in lista:
        print(elemento)


def init_data_ficheros():
    catalogo = Catalogo()
    lista_usuarios = []
    listas_publicas = []
    
    
    
    
    with open(r".\src\canciones.csv", "r", encoding="utf-8") as f:
        lectura = csv.reader(f)
        next(lectura)  
        for campos in lectura:
            if len(campos) < 5:
                print(f"Línea mal: {campos}")
                continue
            try:
                titulo, artista, album = campos[0], campos[1], campos[2]
                duracion = int(campos[3])
                popularidad = int(campos[4])
                c = Cancion(None, titulo, artista, album, duracion, popularidad, None)
                catalogo.agregar_cancion(c)
            except ValueError as e:
                print(f"Error procesando línea: {campos} - {e}")


    f = open(r".\src\usuarios.csv")
    primera = True
    for linea in f:
        if not primera:
            campos = linea.strip().split(",")
            if len(campos) != 3:
                print(f"Error en la linea: {linea}")
                continue
            nombre, password, tipo = campos
            
            if tipo == '1':
                c = UsuarioPremium(nombre, password)
            elif tipo == "0":
                c = UsuarioFree(nombre, password)

            else:
                print(f"Tipo de usuario inválido en la linea {linea}")
                continue
            lista_usuarios.append(c)

        else:
            primera=False
    f.close()
    
    f = open(r".\src\listas.csv")
    primera = True
    for linea in f:
        if not primera :
            campos = linea.replace("\n", "").split(",")
            ids_canciones = campos[1].split("-")
            lista_canciones = []
            for id in ids_canciones:
                cancion_lista = catalogo.buscar_id(int(id))
                lista_canciones.append(cancion_lista)
            l = ListaPublica(campos[0], lista_canciones)
            listas_publicas.append(l) 

        else:
            primera = False
    f.close()
    return catalogo, lista_usuarios, listas_publicas



def guardar_canciones_enlazadas(lista_canciones):
    canciones_guardadas = []
    nodo = lista_canciones.get_cabeza() 
    while nodo is not None:
        cancion = nodo.get_dato()
        canciones_guardadas.append([
            cancion.get_titulo(),
            cancion.get_artista(),
            cancion.get_album(),
            cancion.get_duracion(),
            cancion.get_popularidad()
        ])
        nodo = nodo.get_sig()
    return canciones_guardadas



def guardado_ficheros(catalogo, listas_publicas, lista_usuarios,
                      archivo_canciones='./src/canciones.csv',
                      archivo_listas='./src/listas.csv',
                      archivo_usuarios='./src/usuarios.csv'):
    
    
    with open(archivo_canciones, mode='w', newline='', encoding='utf-8') as f_canciones:
        writer = csv.writer(f_canciones)
        writer.writerow(['titulo', 'artista', 'album', 'duracion', 'popularidad'])  
        for cancion in guardar_canciones_enlazadas(catalogo.get_actuales()):
            writer.writerow(cancion)

    
    with open(archivo_listas, mode='w', newline='', encoding='utf-8') as f_listas:
        writer = csv.writer(f_listas)
        writer.writerow(['nombre', 'ids_canciones'])  
        for lista in listas_publicas:
            ids_canciones = '-'.join([str(c.get_id()) for c in lista.get_canciones()])
            writer.writerow([lista.get_nombre(), ids_canciones])

    
    with open(archivo_usuarios, mode='w', newline='', encoding='utf-8') as f_usuarios:
        writer = csv.writer(f_usuarios)
        writer.writerow(['nombre', 'contraseña'])  
        for usuario in lista_usuarios:
            writer.writerow([usuario.get_nombre(), usuario.get_password()])

    print("Datos guardados correctamente.")


def recomendaciones(catalogo, lista_usuarios):
    contador_reproducciones = {}

    for usuario in lista_usuarios:
        for cancion in usuario.get_biblioteca():
            cancion_id = cancion["cancion"].get_id()
            if cancion_id in usuario.get_contador():
                reproducciones_usuario = usuario.get_contador()[cancion_id]
                if cancion_id in contador_reproducciones:
                    contador_reproducciones[cancion_id] += reproducciones_usuario
                else:
                    contador_reproducciones[cancion_id] = reproducciones_usuario

    canciones_ordenadas = sorted(contador_reproducciones.items(), key=lambda item: item[1], reverse=True)
    top_5 = canciones_ordenadas[:5]

    print("Top 5 canciones recomendadas:")
    for i, (id_cancion, total_repros) in enumerate(top_5, 1):
        cancion = catalogo.buscar_id(id_cancion)
        if cancion:
            print(f"{i}. {cancion.get_titulo()} - {cancion.get_artista()} ({total_repros} reproducciones)")




def busqueda_inteligente(artista, catalogo):
    canciones_artista = catalogo.buscar_artista(artista)
    return canciones_artista           

def prueba_velocidad(catalogo):
    lista = catalogo.get_actuales()
    lista_abb = catalogo.get_actualesABB()

    tamano = len(lista.to_list())
    if tamano < 5:
        print("No hay suficientes canciones para probar la velocidad")
        return
    ids = []
    nodo = catalogo.get_actuales().get_cabeza()
    while nodo is not None:
        ids.append(nodo.get_dato().get_id())
        nodo = nodo.get_sig()
    ids_random = random.sample(ids, 5)

    for id in ids_random:
        cancion = catalogo.buscar_id(id)
        if cancion is None:
            continue
        titulo = cancion.get_titulo()
        artista = cancion.get_artista()

        tiempo_lista_enlazada = []
        for i in range(5):
            inicio = time.perf_counter()
            i = catalogo.buscar_id(id)
            fin = time.perf_counter()
            tiempo_lista_enlazada.append(fin - inicio)

        tiempos_ABB = []
        for i in range(5):
            inicio = time.perf_counter()
            i = catalogo.buscar_titulo_artista_ABB(titulo, artista)
            fin = time.perf_counter()
            tiempos_ABB.append(fin - inicio)

        print(f"Canción: {id} - {titulo} - {artista}")
        print(f"Tiempo de búsqueda en lista enlazada: {sum(tiempo_lista_enlazada) / 5:.8f} segundos")
        print(f"Tiempo de búsqueda en ABB: {sum(tiempos_ABB) / 5:.8f} segundos")




def opcion_1_inicio_sesion():
    print("\n=== INICIO DE SESIÓN DE USUARIO ===")
            
    perfil = input("Introduce tu nombre de usuario: ").strip()
    contraseña = input("Introduce la contraseña: ").strip()
    
    usuario_encontrado = None

    for registro in lista_usuarios:
        if perfil == registro.get_nombre() and contraseña == registro.get_password():
            usuario_encontrado = registro
            break

    if usuario_encontrado:
        print(f"Sesión iniciada exitosamente. Bienvenido {usuario_encontrado.get_nombre()}")
        print("Accediendo al menú de usuario")
        #USUARIO FREE ##################################################################################################
        if isinstance(usuario_encontrado, UsuarioFree):
            
            while True:
                print(f"\n=== MENÚ DE USUARIO ({usuario_encontrado.get_nombre()})(Free) ===")
                print("1. Ver mi biblioteca")
                print("2. Gestionar canciones de la biblioteca")
                print("3. Gestionar listas de reproducción")
                print("4. Gestionar amigos")
                print("5. Reproducción de canciones")
                print("6. Cerrar sesión")
        
                try:
                    seleccion4 = int(input("Introduce la opción a utilizar: "))

                except ValueError:
                    print("Debe seleccionar una de las opciones del menú.")
        
                if seleccion4 == 1:
                
                    biblioteca_vacía = not usuario_encontrado.ver_biblioteca()
                    if biblioteca_vacía:
                        print("Tu biblioteca se encuentra vacía")
                    
                
                
                elif seleccion4 == 2:
                    while True:
                        print(f"\n=== BIBLIOTECA DE({usuario_encontrado.get_nombre()}) ===")
                        print("1. Ver mi biblioteca")
                        print("2. Añadir canciones a la biblioteca")
                        print("3. Eliminar canciones de la biblioteca")
                        print("4. Salir")
                        
                        try:
                            seleccion10 = int(input("Introduce la opción a utilizar: "))

                        except ValueError:
                            print("Debe seleccionar una de las opciones del menú.")

                        if seleccion10 == 1:
                            biblioteca_vacía = not usuario_encontrado.ver_biblioteca()
                            if biblioteca_vacía:
                                print("Tu biblioteca se encuentra vacía")

                        elif seleccion10 == 2:
                            print("Añadir canción a tu biblioteca:")
                            catalogo.mostrar_catalogo()
                            id_añadir_biblioteca = 0
                            ids_validos = catalogo.mapear_id()
                            
                            while id_añadir_biblioteca not in ids_validos:
                                print("El ID debe corresponder a una canción del catálogo")
                                try:
                                    id_añadir_biblioteca = int(input("Introduce el ID de la canción a añadir: "))
                                
                                except ValueError:
                                    print("ID invalido. Introduce otro ID")
                            
                            cancion_añadir_biblioteca = catalogo.buscar_id(id_añadir_biblioteca)
                            
                            if any(cancion_añadir_biblioteca.get_id() == cancion["cancion"].get_id() for cancion in usuario_encontrado.get_biblioteca()):
                                print(f"La canción '{cancion_añadir_biblioteca.get_titulo()}' ya se encuentra en la biblioteca")
                            
                            else:

                                usuario_encontrado.agregar_a_biblioteca(cancion_añadir_biblioteca)
                                if usuario_encontrado.comprobar_fecha():
                                    mostrar_anuncio("Anuncio por pringao")
                                    mostrar_anuncio("Anuncio por pringao")
                                else:
                                        mostrar_anuncio("Anuncio por pringao")
                                    
                                print(f"La cancion '{cancion_añadir_biblioteca.get_titulo()}' ha sido añadida a la biblioteca")



                        elif seleccion10 == 3:

                            print("Eliminar canción de tu biblioteca:")
                            
                            biblioteca_vacía = not usuario_encontrado.ver_biblioteca()
                            if biblioteca_vacía:
                                print("Tu biblioteca se encuentra vacía")
                            
                            else:
                                try:
                                    id_eliminar_biblioteca = int(input("Introduce el ID de la canción a eliminar: "))
                                
                                except ValueError:
                                    print("El ID debe ser un entero")
                                    continue

                                cancion_eliminar = next((cancion for cancion in usuario_encontrado.get_biblioteca() if cancion["cancion"].get_id() == id_eliminar_biblioteca), None)

                                if cancion_eliminar:
                                    usuario_encontrado.eliminar_cancion_biblioteca(cancion_eliminar)
                                    print(f"La cancion '{(catalogo.buscar_id(id_eliminar_biblioteca)).get_titulo()}' ha sido eliminada de la biblioteca")


                                else:
                                    print(f"No existe ninguna canción con el ID '{id_eliminar_biblioteca}' en la biblioteca")


                        elif seleccion10 == 4:
                            print("Saliendo de gestión de biblioteca . . .")
                            break
                        else:
                            print("Opción inválida")




                elif seleccion4 == 3:
                    while True:
                        print(f"\n=== MENÚ DE GESTIÓN DE LISTAS DE REPRODUCCIÓN ===")
                        print("1. Ver listas de reproducción")
                        print("2. Crear lista de reproducción")
                        print("3. Eliminar lista de reproducción")
                        print("4. Modificar listas de reproducción/ estadísticas")
                        print("5. Listas públicas")
                        print("6. Salir")

                        try:
                            seleccion11 = int(input("Introduce la opción a utilizar: "))

                        except ValueError:
                            print("Debe seleccionar una de las opciones del menú.")

                        if seleccion11 == 1:
                            
                            if usuario_encontrado.get_listas_reproduccion():
                            
                                for lista in usuario_encontrado.get_listas_reproduccion():
                                    print(lista)


                            else:
                                print("No tienes ninguna lista de reproducción")


                        elif seleccion11 == 2:
                            print("Creación de nueva lista de reproducción: ")
                            nombre_lista_nueva = input("Introduce el nombre para tu nueva lista de reproducción: ")

                            if any(elemento.get_nombre() == nombre_lista_nueva for elemento in usuario_encontrado.get_listas_reproduccion()):
                                print(f"Ya existe una lista con el nombre '{nombre_lista_nueva}'")
                                continue
            
                            
                            usuario_encontrado.crear_lista(nombre_lista_nueva)
                        
                            if usuario_encontrado.comprobar_fecha():
                                mostrar_anuncio("Anuncio por pringao")
                                mostrar_anuncio("Anuncio por pringao")
                            else:
                                    mostrar_anuncio("Anuncio por pringao")
                        
                            print(f"La lista {nombre_lista_nueva} ha sido creada")
                            
                

                        elif seleccion11 == 3:
                            if usuario_encontrado.get_listas_reproduccion() == []:
                                print("No hay ninguna lista de reproducción")

                            else:
                                print("Listas de reproducción:")
                                for i in usuario_encontrado.get_listas_reproduccion():
                                    print(i)


                            print("Eliminación de lista de reproducción: ")
                            nombre_lista_eliminar= input("Introduce el nombre de la lista a eliminar: ")

                            if any(elemento.get_nombre() == nombre_lista_eliminar for elemento in usuario_encontrado.get_listas_reproduccion()):
                                usuario_encontrado.eliminar_lista(nombre_lista_eliminar)
                                print(f"La lista '{nombre_lista_eliminar} ha sido eliminada")

                            else:
                                print(f"No existe ninguna lista con el nombre '{nombre_lista_eliminar}'")
                        
                        
                        elif seleccion11 == 4:
                            print("Modificación de lista de reproducción")
                            if usuario_encontrado.get_listas_reproduccion() == []:
                                print("No hay ninguna lista de reproducción")

                            else:
                                print("Listas de reproducción:")
                                for i in usuario_encontrado.get_listas_reproduccion():
                                    print(i)
                            
                            name_modificar = input("Introduce el nombre de la lista a modificar: ")
                            
                            if any(elemento.get_nombre() == name_modificar for elemento in usuario_encontrado.get_listas_reproduccion()):
                                lista_a_modificar = next((lista for lista in usuario_encontrado.get_listas_reproduccion() if lista.get_nombre() == name_modificar), None)
                                
                                if lista_a_modificar:
                                    while True:
                                        print(f"\n=== MODIFICAR LISTA DE REPRODUCCIÓN '{name_modificar}'/ ESTADÍSTICAS ===")
                                        print("1. Añadir canción")
                                        print("2. Eliminar canción")
                                        print("3. Ordenar por popularidad")
                                        print("4. Duración total")
                                        print("5. Mostrar lista")
                                        print("6. Salir")

                                        try:
                                            seleccion13 = int(input("Introduce la opción a utilizar: "))

                                        except ValueError:
                                            print("Debe seleccionar una de las opciones del menú.")

                                

                                        if seleccion13 == 1:
                                            print("Añadir canción desde el catálogo:")
                                            catalogo.mostrar_catalogo()
                                            
                                            id_añadir = 0
                                            ids_validos = catalogo.mapear_id()
                                            
                                            while id_añadir not in ids_validos:
                                                print("El ID debe corresponder a una canción del catálogo")
                                                try:
                                                    id_añadir = int(input("Introduce el ID de la canción a añadir: "))
                                                
                                                except ValueError:
                                                    print("ID invalido. Introduce otro ID")
                                            
                                            cancion_añadir = catalogo.buscar_id(id_añadir)
                                            
                                            if any(cancion_añadir.get_id() == cancion.get_id() for cancion in lista_a_modificar.get_canciones()):
                                                print(f"La canción '{cancion_añadir.get_titulo()}' ya se encuentra en la lista {name_modificar}")
                                            
                                            else:
                                                lista_a_modificar.agregar_cancion(cancion_añadir)
                                                print(f"La canción '{cancion_añadir.get_titulo()}' ha sido añadida de la lista '{name_modificar}'.")

                                        elif seleccion13 == 2:
                                        
                                            
                                            print("Eliminar canción de la lista:")
                                            for cancion in lista_a_modificar.get_canciones():
                                                print(cancion)

                                            try:
                                                id_eliminar = int(input("Introduce el id de la canción a eliminar: "))
                                        
                                            except ValueError:
                                                print("El id debe ser un entero")
                                                continue
                                            
                                            cancion_eliminar_lista = next((cancion for cancion in lista_a_modificar.get_canciones() if cancion.get_id() == id_eliminar), None)

                                            if cancion_eliminar_lista:
                                                lista_a_modificar.eliminar_cancion(cancion_eliminar_lista)

                                                print(f"La canción '{cancion_eliminar_lista.get_titulo()}' ha sido eliminada de la lista '{name_modificar}'.")
                                            else:
                                                print(f"No existe ninguna canción con el ID '{id_eliminar}' en la lista '{name_modificar}'.")
                                            


                                        elif seleccion13 == 3:
                                            lista_ordenada = lista_a_modificar.ordenar_popularidad()
                                            print(f"Lista '{lista_a_modificar.get_nombre()}' ordenada por popularidad:")
                                            for i in lista_ordenada:
                                                print(i)
                                        
                                        elif seleccion13 == 4:
                                            duracion_total = convertir_seg_a_min_seg((lista_a_modificar.duracion_total()))
                                            print(f"La duración total de la lista '{lista_a_modificar.get_nombre()}' es de {duracion_total} ")
                                        
                                        elif seleccion13 == 5:
                                            print(f"Canciones de la lista '{name_modificar}':")
                                            lista_a_modificar.mostrar_lista()

                                        elif seleccion13 == 6:
                                            print("Saliendo de la modificación listas . . .")
                                            break
                                        
                                        else:
                                            print("Opción inválida. Introduzca una opción del menú")

                                else:
                                    print("Lista de reproducción inválida")

                            else:
                                print(f"No existe ninguna lista con el nombre '{name_modificar}'")

                            
                        elif seleccion11 == 5:
                            print("Listas públicas")
                            if listas_publicas == []:
                                print("No hay listas públicas")

                            else:
                                print("Listas públicas:")
                                for i in listas_publicas:
                                    print(i)

                                
                            
                                name_publicas = input("Introduce el nombre de la lista pública a gestionar: ")
                                if any(elemento.get_nombre() == name_publicas for elemento in listas_publicas):
                                    lista_publica_gestionar = next((lista for lista in listas_publicas if lista.get_nombre() == name_publicas),None)
                                    
                                    if lista_publica_gestionar:  
                                        while True:
                                            print(f"\n=== LISTA PÚBLICA '{name_publicas}' ===")
                                            print("1. Seguir lista")
                                            print("2. Valorar")
                                            print("3. Valoracion media")
                                            print("4. Salir")
                            
                                            try:
                                                seleccion14 = int(input("Introduce la opción a utilizar: "))

                                            except ValueError:
                                                print("Debe seleccionar una de las opciones del menú.")


                                            if seleccion14 == 1:
                                                print(f"Seguir lista '{name_publicas}'")
                                                if lista_publica_gestionar.agregar_seguidor(usuario_encontrado):
                                                    print(f"Ahora sigues la lista pública '{name_publicas}'.")
                                                else:
                                                    print(f"Ya sigues la lista pública '{name_publicas}'.")
                                                
                                                    
                                        

                                            elif seleccion14 == 2:
                                                print("Valorar lista pública")
                                                try:
                                                    valoracion = int(input("Introduce la valoración para la lista (1-5): "))
                                                    if 1 <= valoracion <=5:
                                                        lista_publica_gestionar.get_valoraciones().append(valoracion)
                                                        print(f"Has valorado la lista '{name_publicas} con una nota de {valoracion}'")

                                                    else:
                                                        print("Las valoraciones deben estar entre 1 y 5")
                                                
                                                except ValueError:
                                                    print("Las valoraciones deben ser enteros.")




                                            elif seleccion14 == 4:
                                                print("Saliendo de Listas Públicas . . .")
                                                break




                                            elif seleccion14 == 3:  
                                                if lista_publica_gestionar.get_valoraciones():
                                                    media = lista_publica_gestionar.valoracion_media()
                                                    print(f"La valoración media de la lista '{name_publicas}' es: {media:.2f}")
                                                else:
                                                    print(f"La lista '{name_publicas}' no tiene valoraciones aún.")










                                            else:
                                                print("Opción inválida. Introduzca una opción del menú")

                                    else:
                                        print("Lista pública incorrecta")
                                
                                else:
                                    print(f"No existe ninguna lista pública con el nombre {name_publicas} ")

                        elif seleccion11 == 6:
                            print("Saliendo de la gestión de listas de reproducción . . .")
                            break

                        else:
                            print("Opción incorrecta. Introduzca una opción del menú")

                elif seleccion4 == 4:
                    while True:
                        print(f"\n=== MENÚ DE GESTIÓN DE AMIGOS ===")
                        print("1. Mis amigos")
                        print("2. Añadir amigos")
                        print("3. Eliminar amigos")
                        print("4. Salir")
                        
                        try:
                            seleccion9 = int(input("Introduce la opción a utilizar: "))

                        except ValueError:
                            print("Debe seleccionar una de las opciones del menú.")


                        if seleccion9 == 1:
                            
                            
                            if not usuario_encontrado.get_amigos():
                                print("No tienes amigos añadidos")
                            
                            else:
                                print("Mis amigos:")
                                mostrar(usuario_encontrado.get_amigos())
                            

                        elif seleccion9 == 2:
                            print("Añadir amigo:")
                            
                            lista_filtrada = [usuario for usuario in lista_usuarios if usuario != usuario_encontrado]
                            mostrar(lista_filtrada)
                            
                            nombre_amigo_añadir = input("Introduce el nombre del amigo a añadir: ")
                            
                            if any(nombre_amigo_añadir == usuario.get_nombre() for usuario in lista_filtrada):
                                if any(nombre_amigo_añadir == usuario.get_nombre() for usuario in usuario_encontrado.get_amigos()):
                                    print(f"El usuario {nombre_amigo_añadir} ya se encuentra en tu lista de amigos")
                                else:
                                    amigo_añadir = next(usuario for usuario in lista_filtrada if usuario.get_nombre() == nombre_amigo_añadir)
                                    usuario_encontrado.get_amigos().append(amigo_añadir)
                                    print(f"El usuario {nombre_amigo_añadir} ha sido añadido a tu lista de amigos.")
                            else:
                                print(f"No existe ningun usuario con el nombre {nombre_amigo_añadir}")
                        
                        elif seleccion9 == 3:
                            print("oPCION3")
                        
                        elif seleccion9 == 4:
                            print("Saliendo de gestión de amigos . . .")
                            break

                        else:
                            print("Opción inválida. Introduzca una opción del menú")


                elif seleccion4 == 5:
                    print("\n=== REPRODUCCIÓN DE CANCIONES ===")
                    while True:
                        print(f"\n=== MENÚ DE USUARIO ({usuario_encontrado.get_nombre()})(Premium) ===")
                        print("1. Reproducir canción desde biblioteca")
                        print("2. Reproducir canción desde lista de reproducción")
                        print("3. Reproducir canción desde la cola de espera")
                        print("4. Ver cola de espera")
                        print("5. Añadir cancion a cola")
                        print("6. Ver historial de reproducción")
                        print("7. Salir")
                
                        try:
                            seleccion15 = int(input("Introduce la opción a utilizar: "))

                        except ValueError:
                            print("Debe seleccionar una de las opciones del menú.")

                        if seleccion15 == 1:
                            if not usuario_encontrado.ver_biblioteca():
                                print("Tu biblioteca está vacía")

                            else:
                                print("Canciones en tu biblioteca:")
                                usuario_encontrado.ver_biblioteca()

                                try:
                                    id_reproducir = int(input("Introduce el id de la canción a reproducir: "))
                            
                                except ValueError:
                                    print("El id debe ser un número")
                                    continue
                                cancion_reproducir = catalogo.buscar_id(id_reproducir)
                                cancion_biblioteca = next((cancion for cancion in usuario_encontrado.get_biblioteca() if cancion["cancion"] == cancion_reproducir), None)


                                if cancion_biblioteca:
                                    cancion_biblioteca["cancion"].reproducir_cancion()
                                    print("Reproduciendo la cancion . . .")
                                else:
                                    print("No existe ninguna cancion con ese id")

                        elif seleccion15 == 2:
                            if not usuario_encontrado.get_listas_reproduccion():
                                print("No hay listas de reproducción")

                            else:
                                print("Tus listas de reproducción: ")
                                for lista in usuario_encontrado.get_listas_reproduccion():
                                    print(lista)

                                nombre_lista = input("Introduce el nombre de la lista a seleccionar: ")
                                lista_seleccionada = next((lista for lista in usuario_encontrado.get_listas_reproduccion() if lista.get_nombre() == nombre_lista), None)

                                if lista_seleccionada:
                                    if not lista_seleccionada.get_canciones():
                                        print("La lista seleccionada está vacía")
                                    else:
                                        print("Las canciones en la lista son:")
                                        lista_seleccionada.mostrar_lista()

                                    try:
                                        id_reproducir = int(input("Introduce el id de la canción a reproducir: "))
                            
                                    except ValueError:
                                        print("El id debe ser un número")
                                        continue
                                    cancion_reproducir = next((cancion for cancion in lista_seleccionada.get_canciones() if cancion.get_id() == id_reproducir), None)
                                        
                                    if cancion_reproducir:
                                        cancion_reproducir.reproducir_cancion()
                                        print("Se está reproduciendo la cancion")
                                    else:
                                        print("No existe ninguna cancion con ese id")
                                        
                                else:
                                    print("No existe ninguna lista con ese nombre")

                        elif seleccion15 == 3:
                            if usuario_encontrado.get_cola_reproduccion().vacia():
                                print("La cola de reproducción está vacía")
                            else:
                                usuario_encontrado.reproducir_siguiente()
                               
                        elif seleccion15 == 4:
                            usuario_encontrado.mostrar_lista_espera()

                        elif seleccion15 == 5:
                            print("Añadir canción desde catálogo:")
                            artista = input("Introduce el nombre del artista a buscar: ")

                            canciones_filtradas = catalogo.filtrado_inteligente(artista)
                            if canciones_filtradas:
                                print(f"Canciones disponibles del artista '{artista}'")
                                mostrar(canciones_filtradas)

                                try:
                                    id_cancion = int(input("Introduce el id de la canción para añadir a la cola: "))

                                except ValueError:
                                    print("El ID debe ser un número entero")
                                    continue

                                cancion_a_agregar = next((cancion for cancion in canciones_filtradas if cancion.get_id() == id_cancion), None)
                
                                if cancion_a_agregar:
                                    usuario_encontrado.agregar_a_espera(cancion_a_agregar)
                                    print("La canción ha sido agregada a la cola")
                                else:
                                    print("No existe ninguna canción con ese ID")
                            else:
                                print(f"No se encontraron canciones del artista {artista}")

                        elif seleccion15 == 6:
                            print("Historial de reproducción:")
                            usuario_encontrado.get_historial().imprime()
                            
                        elif seleccion15 == 7:
                            print("Saliendo del menú . . .")
                            break

                elif seleccion4 == 6:
                    print("Cerrando sesion . . .")
                    break

                


                else:
                    print("Opción inválida. Introduzca otra orden")
        #USUARIO PREMIUM#################################################################################################
        elif isinstance(usuario_encontrado, UsuarioPremium):
            while True:
                print(f"\n=== MENÚ DE USUARIO ({usuario_encontrado.get_nombre()})(Premium) ===")
                print("1. Ver mi biblioteca")
                print("2. Gestionar canciones de la biblioteca")
                print("3. Gestionar listas de reproducción")
                print("4. Gestionar amigos")
                print("5. Cerrar sesión")
        
                try:
                    seleccion4 = int(input("Introduce la opción a utilizar: "))

                except ValueError:
                    print("Debe seleccionar una de las opciones del menú.")
        
                if seleccion4 == 1:
                
                    biblioteca_vacía = not usuario_encontrado.ver_biblioteca()
                    if biblioteca_vacía:
                        print("Tu biblioteca se encuentra vacía")
                    
                
                elif seleccion4 == 2:
                    while True:
                        print(f"\n=== BIBLIOTECA DE({usuario_encontrado.get_nombre()}) ===")
                        print("1. Ver mi biblioteca")
                        print("2. Añadir canciones a la biblioteca")
                        print("3. Eliminar canciones de la biblioteca")
                        print("4. Descargar canciones")
                        print("5. Mostrar canciones descargadas")
                        print("6. Salir")
                        
                        try:
                            seleccion10 = int(input("Introduce la opción a utilizar: "))

                        except ValueError:
                            print("Debe seleccionar una de las opciones del menú.")

                        if seleccion10 == 1:
                            biblioteca_vacía = not usuario_encontrado.ver_biblioteca()
                            if biblioteca_vacía:
                                print("Tu biblioteca se encuentra vacía")

                        elif seleccion10 == 2:
                            print("Añadir canción a tu biblioteca:")
                            catalogo.mostrar_catalogo()
                            id_añadir_biblioteca = 0
                            ids_validos = catalogo.mapear_id()
                            
                            while id_añadir_biblioteca not in ids_validos:
                                print("El ID debe corresponder a una canción del catálogo")
                                try:
                                    id_añadir_biblioteca = int(input("Introduce el ID de la canción a añadir: "))
                                
                                except ValueError:
                                    print("ID invalido. Introduce otro ID")
                            
                            cancion_añadir_biblioteca = catalogo.buscar_id(id_añadir_biblioteca)
                            
                            if any(cancion_añadir_biblioteca.get_id() == cancion["cancion"].get_id() for cancion in usuario_encontrado.get_biblioteca()):
                                print(f"La canción '{cancion_añadir_biblioteca.get_titulo()}' ya se encuentra en la biblioteca")
                            
                            else:

                                usuario_encontrado.agregar_a_biblioteca(cancion_añadir_biblioteca)
                                print(f"La cancion '{cancion_añadir_biblioteca.get_titulo()}' ha sido añadida a la biblioteca")



                        elif seleccion10 == 3:

                            print("Eliminar canción de tu biblioteca:")
                            
                            biblioteca_vacía = not usuario_encontrado.ver_biblioteca()
                            if biblioteca_vacía:
                                print("Tu biblioteca se encuentra vacía")
                            
                            else:
                                try:
                                    id_eliminar_biblioteca = int(input("Introduce el ID de la canción a eliminar: "))
                                
                                except ValueError:
                                    print("El ID debe ser un entero")
                                    continue

                                cancion_eliminar = next((cancion for cancion in usuario_encontrado.get_biblioteca() if cancion["cancion"].get_id() == id_eliminar_biblioteca), None)

                                if cancion_eliminar:
                                    usuario_encontrado.eliminar_cancion_biblioteca(cancion_eliminar)
                                    print(f"La cancion '{(catalogo.buscar_id(id_eliminar_biblioteca)).get_titulo()}' ha sido eliminada de la biblioteca")


                                else:
                                    print(f"No existe ninguna canción con el ID '{id_eliminar_biblioteca}' en la biblioteca")


                        elif seleccion10 == 4:
                            print("Descargar canción desde el catálogo:")
                            catalogo.mostrar_catalogo()
                            id_descarga = 0
                            ids_validos= catalogo.mapear_id()

                            while id_descarga not in ids_validos:
                                print("El ID debe corresponder a una canción del catálogo")
                                try:
                                    id_descarga = int(input("Introduce el ID de la canción a descargar: "))

                                except ValueError:
                                    print("ID inválido. Introduce otro ID")

                            cancion_descarga = catalogo.buscar_id(id_descarga)

                            if any(cancion_descarga.get_id()==cancion["cancion"].get_id() and cancion["descargada"] for cancion in usuario_encontrado.get_biblioteca()):
                                for cancion in usuario_encontrado.get_biblioteca():
                                    if ["cancion"].get_id() == cancion_descarga.get_id():
                                        if cancion["descargada"]:
                                            print(f"La canción '{cancion_descarga.get_titulo()}' ya está descargada.")

                                        else:
                                            cancion["descargada"] = True
                                            print(f"La cancion '{cancion_descarga.get_titulo}' ya estaba en tu biblioteca")
                                        break
                                
                                    
                            else:
                                usuario_encontrado.get_biblioteca().append({"cancion":cancion_descarga, "descargada":True})
                                print(f"La canción '{cancion_descarga.get_titulo()}' ha sido descargada y añadida a tu biblioteca.")


                        elif seleccion10 == 5:
                            canciones_descargadas = usuario_encontrado.canciones_descargadas()
                            if canciones_descargadas:
                                print("Canciones descargadas:")
                                for i in canciones_descargadas:
                                    print(i)
                            else:
                                print("No tienes canciones descargadas")
                                

                        elif seleccion10 == 6:
                            print("Saliendo de gestión de biblioteca . . .")
                            break
                        else:
                            print("Opción inválida")




                elif seleccion4 == 3:
                    while True:
                        print(f"\n=== MENÚ DE GESTIÓN DE LISTAS DE REPRODUCCIÓN ===")
                        print("1. Ver listas de reproducción")
                        print("2. Crear lista de reproducción")
                        print("3. Eliminar lista de reproducción")
                        print("4. Modificar listas de reproducción/ estadísticas")
                        print("5. Listas públicas")
                        print("6. Listas de amigos")
                        print("7. Salir")

                        try:
                            seleccion11 = int(input("Introduce la opción a utilizar: "))

                        except ValueError:
                            print("Debe seleccionar una de las opciones del menú.")

                        if seleccion11 == 1:
                            
                            if usuario_encontrado.get_listas_reproduccion():
                            
                                for lista in usuario_encontrado.get_listas_reproduccion():
                                    print(lista)


                            else:
                                print("No tienes ninguna lista de reproducción")


                        elif seleccion11 == 2:
                            print("Creación de nueva lista de reproducción: ")
                            nombre_lista_nueva = input("Introduce el nombre para tu nueva lista de reproducción: ")

                            if any(elemento.get_nombre() == nombre_lista_nueva for elemento in usuario_encontrado.get_listas_reproduccion()):
                                print(f"Ya existe una lista con el nombre '{nombre_lista_nueva}'")
                                continue
            
                            
                            usuario_encontrado.crear_lista(nombre_lista_nueva)

                            
                

                        elif seleccion11 == 3:
                            if usuario_encontrado.get_listas_reproduccion() == []:
                                print("No hay ninguna lista de reproducción")

                            else:
                                print("Listas de reproducción:")
                                for i in usuario_encontrado.get_listas_reproduccion():
                                    print(i)

                                    
                            print("Eliminación de lista de reproducción: ")
                            nombre_lista_eliminar= input("Introduce el nombre de la lista a eliminar: ")

                            if any(elemento.get_nombre() == nombre_lista_eliminar for elemento in usuario_encontrado.get_listas_reproduccion()):
                                usuario_encontrado.eliminar_lista(nombre_lista_eliminar)
                                print(f"La lista '{nombre_lista_eliminar} ha sido eliminada")

                            else:
                                print(f"No existe ninguna lista con el nombre '{nombre_lista_eliminar}'")
                        
                        
                        elif seleccion11 == 4:
                            print("Modificación de lista de reproducción")
                            if usuario_encontrado.get_listas_reproduccion() == []:
                                print("No hay ninguna lista de reproducción")

                            else:
                                print("Listas de reproducción:")
                                for i in usuario_encontrado.get_listas_reproduccion():
                                    print(i)
                            
                            name_modificar = input("Introduce el nombre de la lista a modificar: ")
                            
                            if any(elemento.get_nombre() == name_modificar for elemento in usuario_encontrado.get_listas_reproduccion()):
                                lista_a_modificar = next((lista for lista in usuario_encontrado.get_listas_reproduccion() if lista.get_nombre() == name_modificar), None)
                                
                                if lista_a_modificar:
                                    while True:
                                        print(f"\n=== MODIFICAR LISTA DE REPRODUCCIÓN '{name_modificar}'/ ESTADÍSTICAS ===")
                                        print("1. Añadir canción")
                                        print("2. Eliminar canción")
                                        print("3. Ordenar por popularidad")
                                        print("4. Duración total")
                                        print("5. Mostrar lista")
                                        print("6. Salir")

                                        try:
                                            seleccion13 = int(input("Introduce la opción a utilizar: "))

                                        except ValueError:
                                            print("Debe seleccionar una de las opciones del menú.")

                                

                                        if seleccion13 == 1:
                                            print("Añadir canción desde el catálogo:")
                                            catalogo.mostrar_catalogo()
                                            
                                            id_añadir = 0
                                            ids_validos = catalogo.mapear_id()
                                            
                                            while id_añadir not in ids_validos:
                                                print("El ID debe corresponder a una canción del catálogo")
                                                try:
                                                    id_añadir = int(input("Introduce el ID de la canción a añadir: "))
                                                
                                                except ValueError:
                                                    print("ID invalido. Introduce otro ID")
                                            
                                            cancion_añadir = catalogo.buscar_id(id_añadir)
                                            
                                            if any(cancion_añadir.get_id() == cancion.get_id() for cancion in lista_a_modificar.get_canciones()):
                                                print(f"La canción '{cancion_añadir.get_titulo()}' ya se encuentra en la lista {name_modificar}")
                                            
                                            else:
                                                lista_a_modificar.agregar_cancion(cancion_añadir)
                                                print(f"La canción '{cancion_añadir.get_titulo()}' ha sido añadida de la lista '{name_modificar}'.")

                                        elif seleccion13 == 2:
                                        
                                            
                                            print("Eliminar canción de la lista:")
                                            for cancion in lista_a_modificar.get_canciones():
                                                print(cancion)

                                            try:
                                                id_eliminar = int(input("Introduce el id de la canción a eliminar: "))
                                        
                                            except ValueError:
                                                print("El id debe ser un entero")
                                                continue
                                            
                                            cancion_eliminar_lista = next((cancion for cancion in lista_a_modificar.get_canciones() if cancion.get_id() == id_eliminar), None)

                                            if cancion_eliminar_lista:
                                                lista_a_modificar.eliminar_cancion(cancion_eliminar_lista)

                                                print(f"La canción '{cancion_eliminar_lista.get_titulo()}' ha sido eliminada de la lista '{name_modificar}'.")
                                            else:
                                                print(f"No existe ninguna canción con el ID '{id_eliminar}' en la lista '{name_modificar}'.")
                                            


                                        elif seleccion13 == 3:
                                            lista_ordenada = lista_a_modificar.ordenar_popularidad()
                                            print(f"Lista '{lista_a_modificar.get_nombre()}' ordenada por popularidad:")
                                            for i in lista_ordenada:
                                                print(i)
                                        
                                        elif seleccion13 == 4:
                                            duracion_total = convertir_seg_a_min_seg((lista_a_modificar.duracion_total()))
                                            print(f"La duración total de la lista '{lista_a_modificar.get_nombre()}' es de {duracion_total} ")
                                        
                                        elif seleccion13 == 5:
                                            print(f"Canciones de la lista '{name_modificar}':")
                                            lista_a_modificar.mostrar_lista()

                                        elif seleccion13 == 6:
                                            print("Saliendo de la modificación listas . . .")
                                            break
                                        
                                        else:
                                            print("Opción inválida. Introduzca una opción del menú")

                                else:
                                    print("Lista de reproducción inválida")

                            else:
                                print(f"No existe ninguna lista con el nombre '{name_modificar}'")


                        elif seleccion11 == 5:
                            print("listas públicas")
                            if listas_publicas == []:
                                print("No hay listas públicas")

                            else:
                                print("Listas públicas:")
                                for i in listas_publicas:
                                    print(i)

                                
                            
                                name_publicas = input("Introduce el nombre de la lista pública a gestionar: ")
                                if any(elemento.get_nombre() == name_publicas for elemento in listas_publicas):
                                    lista_publica_gestionar = next((lista for lista in listas_publicas if lista.get_nombre() == name_publicas), None)
                                    
                                    if lista_publica_gestionar:  
                                        while True:
                                            print(f"\n=== LISTA PÚBLICA '{name_publicas}' ===")
                                            print("1. Seguir lista")
                                            print("2. Valorar")
                                            print("3. Valoracion media")
                                            print("4. Salir")
                            
                                            try:
                                                seleccion14 = int(input("Introduce la opción a utilizar: "))

                                            except ValueError:
                                                print("Debe seleccionar una de las opciones del menú.")


                                            if seleccion14 == 1:
                                                print(f"Seguir lista '{name_publicas}'")
                                                if lista_publica_gestionar.agregar_seguidor(usuario_encontrado):
                                                    print(f"Ahora sigues la lista '{name_publicas}'")
                                                else:
                                                    print(f"Ya sigues la lista pública '{name_publicas}'.")
                                                    
                                                    
                                                    
                                        

                                            elif seleccion14 == 2:
                                                print("Valorar lista pública")
                                                try:
                                                    valoracion = int(input("Introduce la valoración para la lista (1-5): "))
                                                    if 1 <= valoracion <=5:
                                                        lista_publica_gestionar.get_valoraciones().append(valoracion)
                                                        print(f"Has valorado la lista '{name_publicas} con una nota de {valoracion}'")

                                                    else:
                                                        print("Las valoraciones deben estar entre 1 y 5")
                                                
                                                except ValueError:
                                                    print("Las valoraciones deben ser enteros.")



                                            elif seleccion14 == 4:  
                                                
                                                if lista_publica_gestionar.get_valoraciones():
                                                    
                                                    media = lista_publica_gestionar.valoracion_media()
                                                    print(f"La valoración media de la lista '{name_publicas}' es: {media:.2f}")
                                                
                                                
                                                else:
                                                    print(f"La lista '{name_publicas}' no tiene valoraciones aún.")




                                            elif seleccion14 == 4:
                                                print("Saliendo de Listas Públicas . . .")
                                                break


                                            elif seleccion14 == 4:  
                                                if lista_publica_gestionar.get_valoraciones():
                                                    media = lista_publica_gestionar.valoracion_media()
                                                    print(f"La valoración media de la lista '{name_publicas}' es: {media:.2f}")
                                                else:
                                                    print(f"La lista '{name_publicas}' no tiene valoraciones aún.")





                                            else:
                                                print("Opción inválida. Introduzca una opción del menú")

                                    else:
                                        print("Lista pública incorrecta")
                                
                                else:
                                    print(f"No existe ninguna lista pública con el nombre {name_publicas} ")

                        elif seleccion11 == 6:
                            print("\n=== SEGUIR LISTAS DE AMIGOS ===")

                            if not usuario_encontrado.get_amigos():
                                print("No tienes amigos añadidos")

                            else:
                                print("Amigos diponibles:")
                                for amigo in usuario_encontrado.get_amigos():
                                    print(f"- {amigo.get_nombre()}")

                                nombre_amigo = input("Introduce el nombre del amigo cuyas listas quieras ver: ")
                                amigo_elegido = next((amigo for amigo in usuario_encontrado.get_amigos() if amigo.get_nombre()==nombre_amigo ), None)

                                if amigo_elegido:
                                    if not amigo_elegido.get_listas_reproduccion():
                                        print(f"El amigo '{nombre_amigo}' no tienes listas de reproducción")

                                    else:
                                        print(f"Listas de reproducción de '{nombre_amigo}':")
                                        for lista in amigo_elegido.get_listas_reproduccion():
                                            print(f"- {lista.get_nombre()}")

                                        nombre_lista = input("Introduce el nombre de la lista a seguir: ")
                                        lista_a_seguir = next((lista for lista in amigo_elegido.get_listas_reproduccion() if lista.get_nombre()==nombre_lista), None)

                                        if lista_a_seguir:
                                            if lista_a_seguir in usuario_encontrado.get_listas_reproduccion_seguidas():
                                                print(f"Ya sigues la lista '{nombre_lista}'.")
                                            else:
                                                    usuario_encontrado.seguir_lista_reproduccion(lista_a_seguir)
                                                    print(f"Ahora sigues la lista '{nombre_lista}' de tu amigo '{nombre_amigo}'.")
                                        else:
                                            print(f"No existe ninguna lista con el nombre '{nombre_lista}' en las listas de '{nombre_amigo}'.")
                                else:
                                    print(f"No existe ningún amigo con el nombre '{nombre_amigo}'.")






                        elif seleccion11 == 7:
                            print("Saliendo de la gestión de listas de reproducción . . .")
                            break

                        else:
                            print("Opción invlaida. Introduce una opción del menú")

                elif seleccion4 == 4:
                    while True:
                        print(f"\n=== MENÚ DE GESTIÓN DE AMIGOS ===")
                        print("1. Mis amigos")
                        print("2. Añadir amigos")
                        print("3. Eliminar amigos")
                        print("4. Salir")
                        
                        try:
                            seleccion9 = int(input("Introduce la opción a utilizar: "))

                        except ValueError:
                            print("Debe seleccionar una de las opciones del menú.")


                        if seleccion9 == 1:
                            
                            
                            if not usuario_encontrado.get_amigos():
                                print("No tienes amigos añadidos")
                            
                            else:
                                print("Mis amigos:")
                                mostrar(usuario_encontrado.get_amigos())
                            

                        elif seleccion9 == 2:
                            print("Añadir amigo:")
                            
                            lista_filtrada = [usuario for usuario in lista_usuarios if usuario != usuario_encontrado]
                            mostrar(lista_filtrada)
                            
                            nombre_amigo_añadir = input("Introduce el nombre del amigo a añadir: ")
                            
                            if any(nombre_amigo_añadir == usuario.get_nombre() for usuario in lista_filtrada):
                                if any(nombre_amigo_añadir == usuario.get_nombre() for usuario in usuario_encontrado.get_amigos()):
                                    print(f"El usuario {nombre_amigo_añadir} ya se encuentra en tu lista de amigos")
                                else:
                                    amigo_añadir = next(usuario for usuario in lista_filtrada if usuario.get_nombre() == nombre_amigo_añadir)
                                    usuario_encontrado.get_amigos().append(amigo_añadir)
                                    print(f"El usuario {nombre_amigo_añadir} ha sido añadido a tu lista de amigos.")
                            else:
                                print(f"No existe ningun usuario con el nombre {nombre_amigo_añadir}")
                        
                        elif seleccion9 == 3:
                            print("oPCION3")
                        
                        elif seleccion9 == 4:
                            print("Saliendo de gestión de amigos . . .")
                            break

                        else:
                            print("Opción inválida. Introduzca una opción del menú")


                elif seleccion4 == 5:
                    print("Cerrando sesion . . .")
                    break

                else:
                    print("Opción inválida. Introduzca otra orden")
            
            

    
    else:
        print("Nombre de usuario o contraseña incorrectos. Inténtelo de nuevo")


def opcion_2_gestion_catalogo():
    while True:
        print("\n=== MENÚ DE GESTIÓN DE CATÁLOGO ===")
        print("1. Agregar canción")
        print("2. Eliminar canción")
        print("3. Mostrar catálogo")
        print("4. Buscar por artista")
        print("5. Top populares")
        print("6. Buscar por ID")
        print("7. Menú de gestión de canciones")
        print("8. Salir")
        try:
            seleccion2 = int(input("Introduce la seleccion a utilizar: "))

        except ValueError:
            print("Debe seleccionar una de las opciones del menú.")
            continue
        
        if seleccion2 == 1:
            titulo = input("Introduce el título de la canción: ")
            artista = input("Introduce el nombre del artista: ")
            album = input("Introduce el nombre del album: ")
            duracion = ""
            popularidad = 60
            while not isinstance(duracion, int):
                try:
                    duracion = int(input("Introduce la duración de la canción: "))
                except ValueError:
                    print("La duración debe estar en segundos.")
                    continue
            
            while popularidad > 50 or popularidad < 0 :
                print("La popularidad debe estar entre 1 y 50.")
                try:
                    popularidad = int(input("Introduce la popularidad de la canción: "))
                except ValueError:
                    print("La popularidad debe ser un número entero.")
                    continue

            nueva_cancion = Cancion(None, titulo, artista, album, duracion, popularidad, 0)

            catalogo.agregar_cancion(nueva_cancion)
            

        elif seleccion2 == 2:
            catalogo.mostrar_catalogo()
            try:
                eliminar_id = int(input("Introduce el id de la canción a eliminar: "))
            except ValueError:
                print("El ID debe ser un entero.")

            if eliminar_id in catalogo.mapear_id():

                tema = catalogo.buscar_id(eliminar_id)
                catalogo.eliminar_cancion(tema)   

            
                for usuario in lista_usuarios:
                    biblioteca = usuario.get_biblioteca()
                    canciones_a_eliminar = [cancion for cancion in biblioteca if cancion["cancion"].get_id()==eliminar_id]
                    for cancion in canciones_a_eliminar:
                        usuario.eliminar_cancion_biblioteca(cancion)
                        print(f"La canción '{tema.get_titulo()}' ha sido eliminada de la biblioteca del usuario '{usuario.get_nombre()}'.")
                        

                for lista in listas_publicas:
                    canciones_a_eliminar_listas = [cancion for cancion in lista.get_canciones() if cancion.get_id() == eliminar_id]
                    for cancion in canciones_a_eliminar_listas:
                        lista.eliminar_cancion(cancion)
                        print(f"La canción '{tema.get_titulo()}' ha sido eliminada de la lista pública '{lista.get_nombre()}'.")

                print(f"La canción '{tema.get_titulo()}' ha sido eliminada del catálogo y de todos los sitios relacionados.")


            else:
                print("No existe ninguna canción con este id")

        elif seleccion2 == 3:
            catalogo.mostrar_catalogo()
        
        elif seleccion2 == 4:
            artista_buscar = input("Introduce el nombre del artista a buscar: ")
            canciones = catalogo.buscar_artista(artista_buscar)
            
            if canciones:
                print(f"Las canciones del artista {artista_buscar} son: ")
                for i in canciones:
                    print(i)
        
            else:
                print(f"No hay canciones de {artista_buscar} en el catálogo")


        elif seleccion2 == 5:
            n = 0
            while n > catalogo.get_actuales().get_tamano() or n == 0:
                print(f"El top debe incluir como mucho {catalogo.get_actuales().get_tamano()} canciones")
                try:
                    n = int(input("Introduce la cantidad de canciones a incluir en el top: "))
                
                except ValueError:
                    print("El valor de n debe ser un entero.")
                    continue
            
            top_popular = catalogo.top_populares(n)
            print(f'Las {n} canciones más populares son:')
            for i in top_popular:
                print(i)
            

        elif seleccion2 == 6:

                try:
                    id_buscar = int(input("Introduce el id de la canción a buscar: "))
                
                except ValueError:
                    print("El ID debe ser un entero.")
                    continue
                
                cancion_buscada = catalogo.buscar_id(id_buscar)

                if cancion_buscada:
                    print(cancion_buscada)

                else:
                    print(f"No existe ninguna canción con el id {id_buscar}")
        
        elif seleccion2 == 7:
            #Submenú de gestión de canción
            while True:
                print("\n=== MENÚ DE GESTIÓN DE CANCIONES ===")
                print("1. Duración formateada")
                print("2. Canción más larga")
                print("3. Mismo artista")
                print("4. Mismo album")
                print("5. Es más popular")
                print("6. Salir")

                try:
                    seleccion3 = int(input("Introduce la opción a utilizar: "))
                except ValueError:
                    print("Opción inválida. Intrduce una opción del menú")
                    continue    

                if seleccion3 == 1:
                    
                    catalogo.mostrar_catalogo()
                    
                    id_formatear = 0

                    try:
                        id_formatear = int(input("Introduce el id de la canción cuya duración quieres formatear: "))

                    except ValueError:
                        print("El ID debe ser un entero.")
                        continue

                    cancion_formatear = catalogo.buscar_id(id_formatear)

                    if cancion_formatear:
                        tiempo = cancion_formatear.duracion_formateada()
                        print(f"La duración de la canción '{cancion_formatear.get_titulo()}' es de {tiempo}.")

                    else:
                        print(f"No hay ninguna canción con el id {id_formatear}")



                elif seleccion3 == 2:
                    catalogo.mostrar_catalogo()
                    
                    try:
                        id_cancion1 = int(input("Introduce el id de la primera canción a comparar: "))

                        id_cancion2 = int(input("Introduce el id de la segunda canción a comparar: "))
                    
                    except ValueError:
                        print("Los IDs de ambas canciones deben ser enteros")


                    cancion1 = catalogo.buscar_id(id_cancion1)
                    cancion2 = catalogo.buscar_id(id_cancion2)

                    if cancion1 and cancion2:

                        if cancion1.es_mas_larga(cancion2):
                            print(f"La canción '{cancion1.get_titulo()}' es más larga que '{cancion2.get_titulo()}'")

                        else:
                            print(f"La canción '{cancion2.get_titulo()}' es más larga que '{cancion1.get_titulo()}'")

                    elif not cancion1 and not cancion2:
                        print("Los IDs introducidos no son válidos")

                    elif not cancion1:
                        print(f"No existe ninguna canción con el id {id_cancion1}")

                    elif not cancion2:
                        print(f"No existe ninguna canción con el id {id_cancion2}")



                elif seleccion3 == 3:
                    
                    catalogo.mostrar_catalogo()
                    
                    try:
                        id_cancion1 = int(input("Introduce el de la primera canción a comparar: "))

                        id_cancion2 = int(input("Introduce el id de la segunda canción a comparar: "))
                    
                    except ValueError:
                        print("Los IDs de ambas canciones deben ser enteros")


                    cancion1 = catalogo.buscar_id(id_cancion1)
                    cancion2 = catalogo.buscar_id(id_cancion2)

                    if cancion1 and cancion2:

                        if cancion1.mismo_artista(cancion2):
                            print(f"Las canciones '{cancion1.get_titulo()}' y '{cancion2.get_titulo()}' tienen el mismo artista.")

                        else:
                            print(f"Las canciones '{cancion1.get_titulo()}' y '{cancion2.get_titulo()}' no tienen el mismo artista.")

                    elif not cancion1 and not cancion2:
                        print("Los IDs introducidos no son válidos")

                    elif not cancion1:
                        print(f"No existe ninguna canción con el id {id_cancion1}")

                    elif not cancion2:
                        print(f"No existe ninguna canción con el id {id_cancion2}")   



                elif seleccion3 == 4:
                    catalogo.mostrar_catalogo()
                    
                    try:
                        id_cancion1 = int(input("Introduce el de la primera canción a comparar: "))

                        id_cancion2 = int(input("Introduce el id de la segunda canción a comparar: "))
                    
                    except ValueError:
                        print("Los IDs de ambas canciones deben ser enteros")


                    cancion1 = catalogo.buscar_id(id_cancion1)
                    cancion2 = catalogo.buscar_id(id_cancion2)

                    if cancion1 and cancion2:

                        if cancion1.mismo_album(cancion2):
                            print(f"Las canciones '{cancion1.get_titulo()}' y '{cancion2.get_titulo()}' pertenecen al mismo album.")

                        else:
                            print(f"Las canciones '{cancion1.get_titulo()}' y '{cancion2.get_titulo()}' no pertenecen al mismo album.")

                    elif not cancion1 and not cancion2:
                        print("Los IDs introducidos no son válidos")

                    elif not cancion1:
                        print(f"No existe ninguna canción con el id {id_cancion1}")

                    elif not cancion2:
                        print(f"No existe ninguna canción con el id {id_cancion2}")

                elif seleccion3 == 5:
                    catalogo.mostrar_catalogo()
                    
                    try:
                        id_cancion1 = int(input("Introduce el de la primera canción a comparar: "))

                        id_cancion2 = int(input("Introduce el id de la segunda canción a comparar: "))
                    
                    except ValueError:
                        print("Los IDs de ambas canciones deben ser enteros")


                    cancion1 = catalogo.buscar_id(id_cancion1)
                    cancion2 = catalogo.buscar_id(id_cancion2)

                    if cancion1 and cancion2:

                        if cancion1.es_mas_popular(cancion2):
                            print(f"La canción '{cancion1.get_titulo()}' es más popular que '{cancion2.get_titulo()}'")

                        else:
                            print(f"La canción '{cancion2.get_titulo()}' es más popular que '{cancion1.get_titulo()}'")

                    elif not cancion1 and not cancion2:
                        print("Los IDs introducidos no son válidos")

                    elif not cancion1:
                        print(f"No existe ninguna canción con el id {id_cancion1}")

                    elif not cancion2:
                        print(f"No existe ninguna canción con el id {id_cancion2}")

                    
                    
                elif seleccion3 == 6:
                    print("Sliendo de la gestión de canciones...")
                    break
                    
                else:
                    print("Opción inválida. Intrduce una opción del menú")




        elif seleccion2 == 8:
            print("Saliendo de la gestión de catálogo...")
            break

        else:
            print("Opción inválida. Intrduce una opción del menú")

def opcion_3_listas_públcias():
    while True:
        print("\n=== MENÚ DE GESTIÓN DE LISTAS PÚBLICAS ===")
        print("1. Añadir lista pública")
        print("2. Eliminar lista pública")
        print("3. Mostrar listas públicas")
        print("4. Salir")
        try:
            seleccion5 = int(input("Introduce la seleccion a utilizar: "))

        except ValueError:
            print("El ID debe ser un entero.")
            continue

        if seleccion5 == 1:
            print("Creación de lista pública:")
            name = input("Introduce el nombre de la nueva lista: ")
            
            if any(elemento.get_nombre() == name for elemento in listas_publicas):
                print(f"Ya existe una lista con el nombre '{name}'")
                continue
            
            temas_lista_publica = []
            
            #Agregar canciones a la nueva
            while True:
                print("Añadir canciones a la nueva lista:")
                print("1. Añadir nueva canción del catálgo")
                print("2. Terminar y crear la lista")

                try:
                    seleccion6 = int(input("Introduce la opción: "))
                    
                except ValueError:
                    print("Introduce una opción del menú.")


                if seleccion6 == 1:
                    print("Añadir canción desde el catálogo:")
                    catalogo.mostrar_catalogo()
                    
                    id_añadir = 0
                    ids_validos = catalogo.mapear_id()
                    
                    while id_añadir not in ids_validos:
                        print("El ID debe corresponder a una canción del catálogo")
                        try:
                            id_añadir = int(input("Introduce el ID de la canción a añadir: "))
                        
                        except ValueError:
                            print("ID invalido. Introduce otro ID")
                    
                    cancion_añadir = catalogo.buscar_id(id_añadir)
                    
                    if any(cancion_añadir.get_id() == cancion.get_id() for cancion in temas_lista_publica):
                        print(f"La canción '{cancion_añadir.get_titulo()}' ya se encuentra en la lista {name}")
                    
                    else:
                        temas_lista_publica.append(cancion_añadir)

                elif seleccion6 == 2:
                    print("Creando lista . . .")
                    break
                
                else:
                    print("Opción inválida. Intrduce una opción del menú")


            lista_nueva = ListaPublica(name, temas_lista_publica)
            listas_publicas.append(lista_nueva)

            


        elif seleccion5 == 2:
            print("Eliminación de lista pública:")
            
            if listas_publicas == []:
                print("No hay ninguna lista pública")

            else:
                print("Listas públicas:")
                for i in listas_publicas:
                    print(i)
            
            name_eliminar = input("Introduce el nombre de la lista a eliminar: ")
            
            lista_a_eliminar = next((lista for lista in listas_publicas if lista.get_nombre() == name_eliminar), None)

            if lista_a_eliminar:
                listas_publicas.remove(lista_a_eliminar)
                print(f"Eliminado la lista '{name_eliminar}' . . .")

            else:
                print(f"No existe ninguna lista con el nombre {name_eliminar}")
                continue
        
        elif seleccion5 == 3:
            if listas_publicas == []:
                print("No hay ninguna lista pública")

            else:
                print("Listas públicas:")
                for i in listas_publicas:
                    print(i)


        elif seleccion5 == 4:
            print("Saliendo del menú de listas públicas . . .")
            break

        else:
            print("Opción inválida. Intrduce una opción del menú")

def opcion_4_gestion_ususarios():
    while True:
        print("\n=== MENÚ DE REGISTRO DE USUARIOS ===")
        print("1. Añadir usuario")
        print("2. Eliminar usuario")
        print("3. Mostrar usuarios")
        print("4. Salir")
        try:
            seleccion7 = int(input("Introduce la seleccion a utilizar: "))

        except ValueError:
            print("Debe seleccionar una de las opciones del menú.")
            continue
    
        if seleccion7 == 1:
            while True:
                print("Creación de usuario:")
                print("1. Creación de usuario free")
                print("2. Creación de usuario premium")
                print("3. Salir")

                try:
                    seleccion8 = int(input("Introduce la seleccion a utilizar: "))

                except ValueError:
                    print("Debe seleccionar una de las opciones del menú.")
                    continue
            
                if seleccion8 == 1:
            
                    nombre_usuario_free = input("Introduce el nombre del usuario a registrar: ")
                    
                    if any(nombre_usuario_free == usuario.get_nombre() for usuario in lista_usuarios):
                                print(f"El usuario '{nombre_usuario_free}' ya se encuentra registrado en el sistema. Inténtelo de nuevo")
                    
                    else:
                    
                        password_usuario = input(f"Introduce la contraseña para el usuario '{nombre_usuario_free}': ")
                        nuevo_usuario_free = UsuarioFree(nombre_usuario_free, password_usuario)
                        lista_usuarios.append(nuevo_usuario_free)
                        print(f"El usuario '{nombre_usuario_free}' ha sido registrado con éxito")
                
                elif seleccion8 == 2:

                    nombre_usuario_premium = input("Introduce el nombre del usuario a registrar: ")
                    
                    if any(nombre_usuario_premium == usuario.get_nombre() for usuario in lista_usuarios):
                                print(f"El usuario '{nombre_usuario_premium}' ya se encuentra registrado en el sistema. Inténtelo de nuevo")
                    
                    else:
                    
                        password_usuario = input(f"Introduce la contraseña para el usuario '{nombre_usuario_premium}': ")
                        nuevo_usuario_premium = UsuarioPremium(nombre_usuario_premium, password_usuario)
                        lista_usuarios.append(nuevo_usuario_premium)
                        print(f"El usuario '{nombre_usuario_premium}' ha sido registrado con éxito")

                elif seleccion8 == 3:
                    print("Saliendo de la creación de usuario . . .")
                    break

                else:
                    print("Opción inválida. Intrduce una opción del menú")


        elif seleccion7 == 2:
            print("Eliminación de usuario:")

            if lista_usuarios == []:
                print("La lista de usuarios se encuentra vacía")

            else:
                nombre_usuario_eliminar = input("Introduce el nombre del ususario a eliminar: ")
                if any(nombre_usuario_eliminar == usuario.get_nombre() for usuario in lista_usuarios):
                    contraseña_usuario_eliminar = input(f"Introduce la contraseña del usuario {nombre_usuario_eliminar} para eliminarlo: ")

                    if any(contraseña_usuario_eliminar == usuario.get_password() for usuario in lista_usuarios):
                        usuario_eliminar = next((usuario for usuario in lista_usuarios if usuario.get_nombre()== nombre_usuario_eliminar and usuario.get_password() == contraseña_usuario_eliminar), None)

                        if usuario_eliminar :
                            lista_usuarios.remove(usuario_eliminar)
                            print(f"El usuario '{nombre_usuario_eliminar}' ha sido eliminado del sistema")

                        else:
                            print("El nombre de usuario y contraseña no coinciden con ningún usuario del sistema")
                    else:
                        print(f"La contraseña para el usuario '{nombre_usuario_eliminar}' no es correcta")
                else:
                    print(f"No existe ningún usuario con el nombre '{nombre_usuario_eliminar}'")

        elif seleccion7 == 3:
            print("Los usuarios registrados en el sistema son:")
            for usuario in lista_usuarios:
                print(usuario)

        elif seleccion7 == 4:
            print("Saliendo del menú de registro . . .")
            break

        else:
            print("Selección inválida. Introduce una opción del menú")













if __name__ == "__main__":
    
    catalogo, lista_usuarios, listas_publicas = init_data_ficheros()
    
    while True:
        print("\n=== SISTEMA DE MÚSICA EN STREAMING ===")
        print("1. Iniciar sesión como Usuario")
        print("2. Gestionar catálogo de canciones")
        print("3. Gestionar listas de reproducción públicas")
        print("4. Gestionar usuarios")
        print("5. Recomendaciones")
        print("6. Salir")
        print("7. Tiempos de ejecución")
    
        try:
            opcion = int(input("Introduce la opción a utilizar: "))
        except ValueError:
            print("Debe seleccionar una de las opciones del menú.")
            continue
        
        #Menú de inicio de sesión
        if opcion == 1:
            opcion_1_inicio_sesion()
            

        #Menú de gestión de catálogo
        elif opcion == 2:
            opcion_2_gestion_catalogo()
            
            
        #Menú de gestión de listas públicas
        elif opcion == 3:
            opcion_3_listas_públcias()


        elif opcion == 4:
            opcion_4_gestion_ususarios()

        elif opcion == 5:
            recomendaciones(catalogo, lista_usuarios)
        
        elif opcion == 6:
            print("Saliendo del programa")
            guardado_ficheros(catalogo, listas_publicas, lista_usuarios)
            break
    
        elif opcion == 8:
            prueba_velocidad()

        else:
            print("Opción inválida. Intrduce una opción del menú")

        

        

 
        
        