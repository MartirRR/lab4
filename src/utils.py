



import pip._vendor.requests as requests, time
from datetime import date

def buscar_canciones_apple_music(query, numero_canciones=1):
    url = f"https://itunes.apple.com/search?term={query}&entity=musicTrack&limit={numero_canciones}"
    respuesta = requests.get(url)
    resultados = []
    if respuesta.status_code != 200:
        print ("Error al conectar con Apple Music.")

    datos = respuesta.json()

    if datos["resultCount"] == 0:
        print("No se encontraron canciones")

    for cancion in datos["results"]:
        nombre = cancion.get("trackName", "Desconocido")
        artista = cancion.get("artistName", "Desconocido")
        album = cancion.get("collectionName", "Desconocido")
        duracion_seg = cancion.get("trackTimeMillis", 0)/1000
        popularidad = cancion.get("trackCount", "N/A")

        resultados.append({
            "titulo": nombre,
            "artista": artista,
            "album": album,
            "duracion": duracion_seg,
            "popularidad": popularidad
            })

    return resultados


def convertir_seg_a_min_seg(s):
    return time.strftime("%M:%S", time.gmtime(s*1000 // 1000))

def mostrar_anuncio(anuncio):
    print("-------------------")
    print(anuncio)
    for i in range(3):
        print(".", end="")
        time.sleep(1)
    print("\n-------------------")


