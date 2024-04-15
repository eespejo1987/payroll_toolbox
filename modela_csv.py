import csv
import pandas as pd
from openpyxl import load_workbook
import shutil
import funciones as f

#requiere: csv_mensualXpersona (calipso)
#aseguro: tipo de dato float(c_float) para importe y cantidad + sin guin en cuil (opcional)
def modela_mensual(mensual:list,c_float:list,cuil_guion:bool,pos_cuil:int):
    i:int=1 #dato para convertir a float(no toma la linea[0])
    aux: str
    mensual=f.str_to_float(mensual,i,c_float)
    mensual= f.rellenar_superior(mensual,1,[0,1,2])

    if cuil_guion==True:
        for x in range(i,len(mensual),1):
            aux = (mensual[x][pos_cuil]).replace('-','')
            mensual[x][pos_cuil]=aux

    return mensual


