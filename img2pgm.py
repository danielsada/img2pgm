# -*- coding: utf-8 -*-

from PIL import Image   #(Libreria Pillow)
from azure.storage.blob import *
import urllib.request
import io
import os
import sys

#Funci+on que hace más pequeñas las imágenes (El procesador de Machine Learning pide tamaños menores o iguales a 360 heigth x 170 width)
def resizeImg():
    size = 360, 170
    img.thumbnail(size, Image.ANTIALIAS)

#La función toma una imagen de cualquier formato y la transforma a un archivo .pgm que se recibió como argumento de la consola
def transImg():
    imgrgb = img.convert("RGB")
    imgbn = imgrgb.convert("L")

    # Saca la lista de los pixeles en escala de grises y los lleva a un nuevo archivo con el formato de pgm
    pixels = list(imgbn.getdata())
    width, heigth = imgbn.size

    # Abre un archivo nuevo con extensión .pgm y escribe los primeros caracteres clave
    imgpgm = open(result, 'w')
    imgpgm.write('P2\n')
    imgpgm.write(str(width) + ' ' + str(heigth) + '\n')
    imgpgm.write('255\n')

    # Crea un ciclo en el que sube el numero 'L' que representa cantidad de gris, de acuerdo al formato pgm
    for i in range(heigth):
        for j in range(width):
            num = i * (width) + j
            imgpgm.write(ascii(pixels[num]) + ' ')
        imgpgm.write('\n')
    imgpgm.close()

if len(sys.argv) != 4:
    print('Usage: python img2pgm.py [-f|-u] input output')
    print('-f for file, -u for url');

# Crea el url de cada blob y abre la imagen de cada uno
if sys.argv[1] == '-u' :
    URL = sys.argv[2]
    with urllib.request.urlopen(URL) as url:
        f = io.BytesIO(url.read())
else:
    f = sys.argv[2]
img = Image.open(f)

# Genera el nombre de cada archivo nuevo
result = sys.argv[3]

#Manda a llamar a las funciones de resize y de transform
resizeImg()
transImg()

#Manda las imagenes .pgm al Blob Storage
block_blob_service.create_blob_from_path(img_container_edit, result, result,
                                        content_settings=ContentSettings(content_type='image/pmg'))

#Elimina las imagenes temporalmente almacenadas en la carpeta del programa
os.remove(result)