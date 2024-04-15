import funciones as f
import funciones_imagen as f_img
import pandas as pd
import time

#requiere: nomina(activo+inactivo) + recibos.pdf (nombre numero+nombre_archivo)
#asegura: un pdf por contrato x orden de recibos x orden alfabetico
#_recibos: ruta_recibos
def imp_orden_alf(nomina:list,nomina_bajas:list,contratos:list,r_recibos:str,r_consolidado:str,r_img:str,
                  r_resultados:str,ubicacion_1,ubicacion_2):
    lista_impresion:list=[]
    nomina_bajas.pop(0)

    nomina_mes=nomina+nomina_bajas
    nomina_mes=f.sumar_columnas_vacias(nomina_mes,['Contrato','Afectado','Número de hoja'])
    nomina_mes=f.modifica_char_esp(nomina_mes,[('-','',2)],True)
    
    conjunto_contratos=f.conjunto_x_parametro(contratos,0,False)
    conjunto_afectados=f.conjunto_x_parametro(contratos,1,False)
    contrato_persona=f.lista_pertenencia(conjunto_contratos,contratos,0,1)

    nomina_mes=f.asignar_x_conjunto(conjunto_afectados,contrato_persona,nomina_mes,2,10,9,True)
    nomina_mes = [nomina_mes[0]] + sorted(nomina_mes[1:], key=lambda x: x[1]) #orden alfabetico

    lista_r=f.listar_x_extension(r_recibos,'pdf') #lista de recibos a procesar
    lista_r=sorted(lista_r,key=lambda x: x[0])
    print(f'Recibos a procesar: {lista_r}')
    f_img.consolidar_pdf(r_recibos,lista_r,r_consolidado,'recibos_consolidado.pdf')
    f_img.pdf_a_png(r_recibos,lista_r,r_img)

    lista_cuil_ocr=f_img.ocr_lista_cuiles(r_img,ubicacion_1,ubicacion_2)
    conjunto_cuil=f.conjunto_x_parametro(lista_cuil_ocr,0,True)
    hojas_cuil=f.lista_pertenencia(conjunto_cuil,lista_cuil_ocr,0,1)
    
    #asigna hojas a nomina calipso    
    for x in range(1,len(nomina_mes),1):
        if (nomina_mes[x][2]in conjunto_cuil) == True:
            for y in range(0,len(hojas_cuil),1):
                if nomina_mes[x][2]==hojas_cuil[y][0]:
                    nomina_mes[x][11]=hojas_cuil[y][1]
    
    #crea lista de impresion x contrato
    lista_contratos=list(conjunto_contratos)    
    
    for j in range(0,len(lista_contratos),1):
        info=[]
        info.append(lista_contratos[j])
        info.append([])
        lista_impresion.append(info)
    lista_impresion.append(['sin_contrato',[]])
    

    for x in range(1,len(nomina_mes),1):
        if (nomina_mes[x][2]in conjunto_cuil)==True:
            for y in range(0,len(lista_impresion),1):
                if nomina_mes[x][9] == lista_impresion[y][0]:
                    #hojas=[]
                    #hojas.extend(nomina_mes[x][11])
                    (lista_impresion[y][1]).extend(nomina_mes[x][11])
                elif nomina_mes[x][9] == '' and (lista_impresion[y][0])=='sin_contrato':
                    (lista_impresion[y][1]).extend(nomina_mes[x][11])
    
    
    #imprime lista impresion
    for x in range(0,len(lista_impresion),1):
        if len(lista_impresion[x][1])>0:
            nombre_pdf=lista_impresion[x][0]
            f_img.generar_pdf_con_paginas(f'{r_consolidado}/recibos_consolidado.pdf',lista_impresion[x][1],
                        r_resultados,f'{nombre_pdf}.pdf')


    #quita columna neto acordado 
    nomina_enviar=[]
    for elemento in nomina_mes:
        datos=[]
        for x in range(0,len(elemento),1):
            if x!=8:
                datos.append(elemento[x])
        nomina_enviar.append(datos)
                                        
    df_resultado=pd.DataFrame(nomina_enviar)
    df_resultado.to_excel(f'{r_resultados}nomina_impresion.xlsx', 
                          sheet_name='Resultados',index=False,header=False)
    


if __name__ == "__main__":
    inicio= time.time()
    #NQN
    '''imp_orden_alf(f.leer_csv('proceso_recibos/archivos_csv/nomina_activa.csv'),
                f.leer_csv('proceso_recibos/archivos_csv/bajas_mes.csv'),
                f.leer_csv('proceso_recibos/archivos_csv/contratos.csv'),
                'proceso_recibos/recibos/','proceso_recibos/consolidado','proceso_recibos/imagenes/',
                'proceso_recibos/resultados/',(1850, 402, 2022, 443))'''
    #daniela + lucia (tipo A4)
    imp_orden_alf(f.leer_csv('proceso_recibos/archivos_csv/nomina_activa.csv'),
                f.leer_csv('proceso_recibos/archivos_csv/bajas_mes.csv'),
                f.leer_csv('proceso_recibos/archivos_csv/contratos.csv'),
                'proceso_recibos/recibos/','proceso_recibos/consolidado','proceso_recibos/imagenes/',
                'proceso_recibos/resultados/',(1850, 439, 2021, 482),(1853,459,2022,500))
    
    #Serma: lucia (tipo A4)
    '''imp_orden_alf(f.leer_csv('proceso_recibos/archivos_csv/serma_nomina_activa.csv'),
                f.leer_csv('proceso_recibos/archivos_csv/serma_bajas_mes.csv'),
                f.leer_csv('proceso_recibos/archivos_csv/serma_contratos.csv'),
                'proceso_recibos/recibos/','proceso_recibos/consolidado','proceso_recibos/imagenes/',
                'proceso_recibos/resultados/',(1810, 222, 1974, 264),(1853,459,2022,500))'''
    


    fin= time.time()
    ejecucion=fin - inicio
    print(f'Tiempo de ejecución: {ejecucion} segundos')