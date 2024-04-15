import csv
import pandas as pd
from openpyxl import load_workbook
import shutil
import funciones as f
import modela_csv as m_csv
import time

#requiere: mensual + nomina contratos
#asegura: asigna 'contrato'+'afectado' la mensual
def base_control_rt(mensual:list,contratos:list):

    mensual=m_csv.modela_mensual(mensual,[12,13],True,11)
    mensual=f.sumar_columnas_vacias(mensual,['Contrato','Afectado'])

    conjunto_contratos=f.conjunto_x_parametro(contratos,0,False)
    conjunto_afectados=f.conjunto_x_parametro(contratos,1,False)
    contrato_persona=f.lista_pertenencia(conjunto_contratos,contratos,0,1)

    mensual=f.asignar_x_conjunto(conjunto_afectados,contrato_persona,mensual,11,15,14,True)

    return mensual

#requiere: nomina con contrato y afectación
#asegura: un excel con tabla pivot por CC
def control_rt(base_informe:list,cc:list,ruta:str,destino:str,nombre:str):

    enviar: list=f.copiar_filtro(base_informe,1,True,10,cc)
    f.copiar_archivo(ruta,destino,nombre)
    f.pegar_excel(destino+'/'+nombre,'BBDD',enviar)

    return







