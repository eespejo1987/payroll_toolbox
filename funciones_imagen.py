import funciones as f
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
from pathlib import Path
import time
from pdf2image import convert_from_path
from tqdm import tqdm
from PIL import Image
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import pandas as pd


#requiere: ruta con archivos pdf + indicar si tienen que estar ordenados
#asegura: un unico pdf consolidado
def consolidar_pdf(ruta:str, lista ,destino: str,nombre:str):

    merger = PdfMerger()
    
    for ruta_pdf in lista:
        
        ruta_completa= ruta+ruta_pdf
        print(ruta_completa)
        with open(ruta_completa, 'rb') as archivo_pdf:
            merger.append(archivo_pdf)
    
    ruta_destino = Path(destino)/nombre
    merger.write(ruta_destino)
    merger.close()

#requiere: ruta con archivos PDF 
#Asegura: separa las hojas en formato PNG y los numera por orden de extracción
def pdf_a_png(ruta:str, lista_pdf:list,destino:str):
    control_i = 0
    for pdf in lista_pdf:
        ruta_i = f'{ruta}/{pdf}'
        #print(ruta_i)
        try:
            pages = convert_from_path(ruta_i, 300)
            total_pages = len(pages)
            for i, page in enumerate(tqdm(pages, desc='Procesar hojas', total=total_pages)):
                page.save(os.path.join(destino,f'{control_i + i}.png'), 'PNG')
            control_i += total_pages
        except Exception as e:
            print(f"Error al convertir el PDF {pdf}: {e}")

#requiere: ruta con archivos PNG
#Asegura: lee los png y armar lista : [cuil][hojas]
def ocr_lista_cuiles(ruta:str,ubicacion,alternativa):
    #asig_contratos = mcsv.dicc_contratos(f.lector_csv(contratos))
    lista_recibos=[]
    lista_png=(f.listar_x_extension(ruta,'.png'))


    imagenes = [Image.open(f'{ruta}/{x}.png').crop(ubicacion) for x in range(len(lista_png))]

    for x, imagen_recorte in enumerate(imagenes):
        cuil = tess.image_to_string(imagen_recorte).strip()
        #print(len(cuil))
        if len(cuil)!=13:
            #sin_espacios=(cuil).replace(',','')
            cuil=(cuil).replace(' ','')
        cuil = (cuil).replace('-','')
        
        if cuil.isdigit()==False:
            imagen_alt=Image.open(f'{ruta}/{x}.png').crop(alternativa)
            cuil=tess.image_to_string(imagen_alt).strip()
            if len(cuil)!=13:
            #sin_espacios=(cuil).replace(',','')
                cuil=(cuil).replace(' ','')
            cuil = (cuil).replace('-','')

        #print(cuil)
        lista_recibos.append([cuil,[]])
        #contrato=(asig_contratos.get(cuil, '')[0])
        lista_recibos[x][1] = x

        #print(cuil,'',x,'', len(cuil))

    return lista_recibos

#requiere: archivo.pdf + [numeros de hoja a imprimir] 
#asegura: nuevo pdf en base al archivo original
def generar_pdf_con_paginas(origen, paginas, ruta_destino, nombre_destino):
    # Abrir el archivo PDF original en modo de lectura
    with open(origen, 'rb') as file:
        pdf = PdfReader(file)
        output_pdf = PdfWriter()

        # Agregar las páginas seleccionadas al nuevo PDF
        for pagina_num in paginas:
            if int(pagina_num) < len(pdf.pages):
                pagina = pdf.pages[int(pagina_num)]
                output_pdf.add_page(pagina)
            else:
                print(f'La página {pagina_num} excede el número total de páginas en el PDF.')

        # Crear la ruta completa de destino
        ruta_completa = os.path.join(ruta_destino, nombre_destino)

        # Guardar el nuevo PDF con la ruta completa de destino
        with open(ruta_completa, 'wb') as output_file:
            output_pdf.write(output_file)



    #print(f'Tiempo de ejecución: {ejecucion} segundos')
    #generar_pdf_con_paginas('proceso_recibos/consolidado/recibos_consolidado.pdf',[0,2],
    #                        'proceso_recibos/resultados/','nuevo.pdf')
