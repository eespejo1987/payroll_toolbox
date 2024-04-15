import funciones as f
import unicodedata
from typing import List,Tuple
import pandas as pd

#requiere: archivo csv con aportes y contribuciones sindicales
#asegura: excel con datos de pago y de registración contable x persona x convenio x concepto
def sindicatos(reporte:list,sindicatos:List[Tuple[str,list]],ruta:str)->list:
    periodo=reporte[2]
    reporte.pop(0)
    reporte.pop(1)
    #print(reporte[0])
    #borra subtotales y linea vacia
    reporte.pop(-1)
    reporte.pop(-1)
    reporte.pop(-1)
    '''print(reporte[len(reporte)-3])
    print(reporte[len(reporte)-2])
    print(reporte[len(reporte)-1])'''

    #'concepto': variables de busqueda
    for x in range(1,len(reporte),1):
        if reporte[x][6]=='':
            reporte[x][6]=reporte[x][7]
    
    #modela contribucion extraordinaria
    for x in range(1,len(reporte),1):
        if len(reporte[x][6])>=27:
            aux=(reporte[x][6])
            aux=aux.lower()
            aux=f.sin_acentos(aux)
            if aux[0:27]=='contribucion extraordinaria':
                aux='contribucion extraordinaria'
                reporte[x][6]=aux
     
    datos=['PAGA','CONVENIO','N° Cuenta Contable','CUENTA CONTABLE','CONCEPTO RECIBO','CONCEPTO BOLETA','DATOS PAGO']
    reporte=f.sumar_columnas_vacias(reporte,datos) 
    reporte=f.str_to_float(reporte,1,[10,11 ])

    #policia de trabajo
    cambio_cct={'00931','10975','10999','11024','10985'}

    #carga convenio
    for x in range(1,len(reporte),1):
        if (reporte[x][0] in cambio_cct)==True and reporte[x][6]=='Policia del trabajo':
            reporte[x][13]='Jerarquicos Austral' 
        else:
            reporte[x][13]=reporte[x][5]
    

    #asigna datos pago x sindicatos x concepto
    for elem in range(0,len(sindicatos),1):
        convenio=sindicatos[elem][0]
        datos_conv=sindicatos[elem][1]
        for x in range(1,len(reporte),1):
            if reporte[x][13]==convenio:
                for y in range(0,len(datos_conv),1):
                    if (reporte[x][6]==datos_conv[y][0]):
                        reporte[x][12]=datos_conv[y][7]
                        reporte[x][14]=datos_conv[y][2]
                        reporte[x][15]=datos_conv[y][3]
                        reporte[x][16]=datos_conv[y][4]
                        reporte[x][17]=datos_conv[y][5]
                        reporte[x][18]=datos_conv[y][6]



    '''for x in range(1,len(reporte),1):
        if reporte[x][13]=='Uocra':
            print(reporte[x])'''
    reporte.insert(0,periodo)

    df_resultado=pd.DataFrame(reporte)
    df_resultado.to_excel(f'{ruta}detalle_sindicatos.xlsx', index=False,header=False)
   
    
    return 


