import funciones as f
import unicodedata
from typing import List,Tuple
import pandas as pd


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



if __name__ == "__main__":
    prueba=f.leer_csv('SINDICATOS.csv') 
    d_camioneros=[['4054','Cuota Mutual Choferes de Camiones de Neuquen','2010700020','Sindicato Camioneros NQN a Pagar','Cuota Mutual Choferes de Camiones de Neuquen','Cuota Mutual Choferes de Camiones de RN 4055','1910093355009304416528','si'],['4075','Contribución Solidaria 8.1.1','2010700020','Sindicato Camioneros NQN a Pagar','Contribución Solidaria 8.1.1','Contribucion Solidaria 8.1.1 (4075)','1910093355009301618446','si']
,['4077','Seguro Sepelio Item 8.1.6','2010700020','Sindicato Camioneros NQN a Pagar','Seguro Sepelio Item 8.1.6','SEG. SEPELIO camioneros 4077','1910093355009301618446','si']
,['contribucion extraordinaria','contribucion extraordinaria','2010700020','Sindicato Camioneros NQN a Pagar','contribucion extraordinaria','contribucion extraordinaria','0110002020000202374165','si']
,['Item 8-1-2','Item 8-1-2','2010700020','Sindicato Camioneros NQN a Pagar',' Item 8-1-2 ','Aporte empresario 8.1.2','1910093355009301618446','si']
,['Item 8-1-4','Item 8-1-4','2010700020','Sindicato Camioneros NQN a Pagar',' Item 8-1-4 ','Aporte empresario 8.1.4 (boleta)','interbanking (BTOBE)','si']
,['Item 8-1-5','Item 8-1-5','2010700020','Sindicato Camioneros NQN a Pagar',' Item 8-1-5 ','Item 8.1.5 (boleta)','interbanking (BTOBE)','si']
]
    d_faspygp=[['4059','Cuota MUTUAL 12 de Septiembre SC','2010800033','Mutual 12 de septiembre','Cuota MUTUAL 12 de Septiembre SC','Cuota MUTUAL 12 de Septiembre SC','0860010301800031714494','si']
,['4540','Cuota Sindical Local FASPyGP','2010700043','Cuota Sindical Petroleros Local FASPyGP','Cuota Sindical Local FASPyGP','Cuota Sindical Local FASPyGP','0720477120000000044390','si']
,['4550','Cuota Sindical FASP FASPyGP','2010700046','Cuota Sindical a pagar FASyGP','Cuota Sindical FASP FASPyGP','Cuota Sindical FASP FASPyGP','0720477120000000044390','si']
,['contribucion extraordinaria','Cuota Extraordinaria','2010700033','Contrib. extraordinarias sindicales a pagar FASyGP','Contribucion Extraordinaria','Contribucion Extraordinaria','0720477120000000047672','si']
,['Cuota Solidaridad x Período','Cuota Solidaridad x Período','','','','','','no']
]
    d_j_austral=[['4045','Cuota Sindical SPJyPPGP de La Patagonia Austral','2010700014','Sindicato Jerarquicos Chubut y Sta. Cruz a pagar','Cuota Sindical SPJyPPGP de La Patagonia Austral','Cuota Sindical SPJyPPGP de La Patagonia Austral (imp s boleta)','0110208820020800380672','si']
,['4059','Cuota MUTUAL 12 de Septiembre SC','2010800033','Cuota Mutual Jerarquicos Austral','Cuota Mutual del pers Jerq.y Prof de GyP J. Austral','Cuota MUTUAL 12 de Septiembre SC','0860010301800031714494','si']
,['contribucion extraordinaria','Cuota Extraordinaria','2010700034','Contrib. extra sindicales a pagar J Austral','Contribucion Extraordinaria','Contribucion Extraordinaria','0110208840020813277426','si']
,['Jerárquicos  Austral','Jerárquicos  Austral','2010700052','Contrib. Cuota Solidaridad a pagar J Austral','Cuota Solidaridad x Período','Contrib Solidaria x Período ( importe segun boleta)','0110208840020813277426','si']
,['Policia del trabajo','Policia del trabajo','2010700009','Ley 3270 (Polic.Trabajo)','Policia del trabajo','Policia del trabajo','0830021807002000470051','si']
]
    d_j_nqn=[['4046','Cuota Sindical Pers. Jeraq. Neuquen y Río Negro','2010700015','Sindicato Jerarquicos Neuquen y Río Negro a Pagar','Cuota Sindical Pers. Jeraq. Neuquen y Río Negro','Cuota Sindical Pers. Jeraq. Neuquen y Río Negro','0440017230000003644167','si']
,['4571','Cuota Mutual del pers Jerq.y Prof de GyP J. NQN - RN','2010700050','Cuota Mutual Jerarquicos Neuquen y Río Negro a','Cuota Mutual del pers Jerq.y Prof de GyP J. NQN - RN','Cuota Mutual del pers Jerq.y Prof de GyP J. NQN - RN','0440017230000003679257','si']
,['contribucion extraordinaria','Cuota Extraordinaria','2010700035','Contrib. extra sindicales a pagar J NQN - RN','Contribucion Extraordinaria','Contribucion Extraordinaria','0440017230000003644167','si']
,['Jerarquicos NQN - RN','Jerarquicos NQN - RN','2010700042','Contrib. Social y Cultural a pagar J NQN - RN','Cuota Socio cultural','Contribucion programa socio cultural','0440017230000003644167','si']
]
    d_p_chubut=[['4541','Cuota Sindical Local Pet. Chubut','2010700044','Cuota Sindical Petroleros Local Pet. Chubut','Cuota Sindical Local Pet. Chubut','Cuota Sindical Local Pet. Chubut','0830006501002012180032','si']
,['4551','Cuota Sindical FASP Pet. Chubut','2010700047','Cuota Sindical a pagr Pet Chubut','Cuota Sindical FASP Pet. Chubut','Cuota Sindical FASP Pet. Chubut','0830006501002012180032','si']
,['contribucion extraordinaria','Cuota Extraordinaria','2010700036','Contrib. extra sindicales a pagar Pet. Chubut','Contribucion Extraordinaria','Contribucion Extraordinaria','0830006501002012180032','si']
,['Cuota Solidaridad x Período','Cuota Solidaridad x Período','2010700039','Contrib. Cuota solidaridad a pagar Pet Chubut','Cuota Solidaridad x Período','Cuota Solidaridad x Período','0830006501002012180025','si']
,['Policia del trabajo','Policia del trabajo','2010700009','Ley 3270 (Polic.Trabajo)','Policia del trabajo','Policia del trabajo','0830021807002000470051','si']
 ]
    d_p_nqn=[['4053','Devolucion Prestamo MEOPP','2010700053','Cuota Mutual Emp. Ob. P.P. del Conv Petroleros NQN','Devolucion Prestamo MEOPP','(en blanco)','0340212400730049994005','si']
,['4542','Cuota Sindical Local Pet. NQN - RN','2010700045','Cuota Sindical Petroleros Local Pet NQN - RN','Cuota Sindical Local Pet. NQN - RN','Sindicato','0970011610001092550016','si']
,['4552','Cuota Sindical FASP Pet. NQN - RN','2010700048','Cuota Sindical a pagar Pet NQN - RN','Cuota Sindical FASP Pet. NQN - RN','Aporte Solidario','0970011610001092550016','si']
,['contribucion extraordinaria','Cuota Extraordinaria','2010700037','Contrib. extra sindicales a pagar Pet NQN - RN','Contribucion Extraordinaria','Contribucion Extraordinaria','0970011610001092550016','si']
,['Cuota Solidaridad x Período','Cuota Solidaridad x Período','2010700051','Contrib. Cuota solidaridad a pagar Pet NQN - RN','Cuota Solidaridad x Período','Cuota solidaridad ART 22','0970011610001092550016','si']
,['4051','Cuota Mutual Emp. Ob. P.P.','2010700053','Cuota Mutual Emp. Ob. P.P. del Conv Petroleros NQN','Cuota Mutual Emp. Ob. P.P.','Cuota Mutual ','0970099410001096950010','si']
    ]
    d_uocra=[['4085','Seguro de Vida UOCRA','2010900014','Seguro de vida UOCRA','Seguro de vida UOCRA','Seguro de vida UOCRA','0440000430000004106941','si']
,['contribucion extraordinaria','Contribucion extraordinaria','2010900013','Contribucion Extraordinaria','Contribucion Extraordinaria','Contribucion Extraordinaria','0440000430000004106941','si']
,['FICS','FICS','2010700022','Fondo de desempleo UOCRA a pagar','FICS','Cuota Sindical UOCRA 2% (Aportes Fondos Inv. FICS 2%)','0440000430000004106941','si']
,['FODECO','FODECO','2010700022','Fondo de desempleo UOCRA a pagar','FODECO','FODECO','BtoB','si']
,['IERIC','IERIC','2010700022','Fondo de desempleo UOCRA a pagar','IERIC','IERIC','BtoB','si']
]        
    

    l_sindicatos=List[Tuple[str,List]]
    l_sindicatos=[['Camioneros',d_camioneros],['FASPyGP',d_faspygp],['Jerarquicos Austral',d_j_austral]
                  ,['Jerarquicos NQN - RN',d_j_nqn],['Petroleros Chubut',d_p_chubut],['Petroleros NQN - RN',d_p_nqn],
                  ['Uocra',d_uocra]]
  
    
    sindicatos(f.leer_csv('detalle_sindicatos/base/sindicatos.csv'),l_sindicatos,
               'detalle_sindicatos/resultados/')
    #print(len('Contribucion extraordinaria'))