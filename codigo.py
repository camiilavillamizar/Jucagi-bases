import os
import sys
import pyttsx3
import sqlite3
from datetime import datetime,timedelta
import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#PARA ABRIR LA BASE DE DATOS
con = sqlite3.connect('planeacion')

#INICIALIZANDO LA VOZ
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)
micursor = con.cursor()

tareasatiempo = ctrl.Antecedent(np.arange(0, 100, 1), 'tareasatiempo')
calidad = ctrl.Antecedent(np.arange(0,100,1), 'calidad')
command = ctrl.Consequent(np.arange(0,100,1), 'command')

tareasatiempo.automf(3)
calidad.automf(3)

command['deficiente'] = fuzz.trimf(command.universe,[0,0,49])
command['promedio'] = fuzz.trimf(command.universe,[25,50,75])
command['Excelente'] = fuzz.trimf(command.universe,[51,100,100])

r1 = ctrl.Rule(tareasatiempo['poor'] & calidad['poor'], command['deficiente'])
r2 = ctrl.Rule(tareasatiempo['poor'] & calidad['average'], command['deficiente'])
r3 = ctrl.Rule(tareasatiempo['poor'] & calidad['good'], command['promedio'])

r4 = ctrl.Rule(tareasatiempo['average'] & calidad['poor'], command['deficiente'])
r5 = ctrl.Rule(tareasatiempo['average'] & calidad['average'], command['deficiente'])
r6 = ctrl.Rule(tareasatiempo['average'] & calidad['good'], command['promedio'])

r7 = ctrl.Rule(tareasatiempo['good'] & calidad['poor'], command['deficiente'])
r8 = ctrl.Rule(tareasatiempo['good'] & calidad['average'], command['promedio'])
r9 = ctrl.Rule(tareasatiempo['good'] & calidad['good'], command['Excelente'])

command_ctrl = ctrl.ControlSystem(rules=[r1,r2,r3,r4,r5,r6,r7,r8,r9])
command_results = ctrl.ControlSystemSimulation(command_ctrl)

"""
micursor.execute('''
        CREATE TABLE EMPLEADO(
            ID INTEGER PRIMARY KEY,
            NOMBRE VARCHAR(50) NOT NULL,
            CORREO VARCHAR(59),
            DISPONIBILIDAD INTEGER NOT NULL,
            TAREAS INTEGER NOT NULL,
            CALIDAD INTEGER NOT NULL)
''')

micursor.execute('''
CREATE TABLE JEFE(
    ID INTEGER PRIMARY KEY,
    NOMBRE VARCHAR(50) NOT NULL,
    CORREO VARCHAR(50)
    )

''')

micursor.execute('''
CREATE TABLE ACTIVIDAD(
    ID INTEGER PRIMARY KEY,
    DESCRIPCION VARCHAR(200) NOT NULL,
    PLAZO DATETIME NOT NULL,
    PROBLEMA VARCHAR(200),
    MAYORPLAZO INTEGER,
    ENTREGA VARCHAR(200)
    )

''')

micursor.execute('''
CREATE TABLE ORGANIZACION(
    JEFE INTEGER,
    EMPLEADO INTEGER,
    FOREIGN KEY (EMPLEADO) REFERENCES EMPLEADO(ID),
    FOREIGN KEY (JEFE) REFERENCES JEFE(ID)
    )
''')

micursor.execute('''
CREATE TABLE ASIGNACION(
    ACTIVIDAD INTEGER,
    EMPLEADO INTEGER,
    FOREIGN KEY (EMPLEADO) REFERENCES EMPLEADO(ID),
    FOREIGN KEY (ACTIVIDAD) REFERENCES ACTIVIDAD(ID)
    )
''')
empleados = [
    (1,"CESAR CORRALES", "CESAR.CORRALES@GMAIL.COM",0, 90, 99),
    (2,"OLGA MARTINEZ", "OLGUILINDA2901@GMAIL.COM",1, 60, 50),
    (3,"SERGIO ORTIZ", "SERGIOORTIZ22@HOTMAIL.COM",1, 30,100),
    (4,"YOLANDA RIVERA","YOLA.RIVE11@GMAIL.COM",1, 30, 100),
    (5, "VIVIANA CALDERON", "VIVICLEON@GMAIL.COM",1, 90, 20),
    (6, "LUCILA TOUS", "LUCITOOUS@GMAIL.COM", 0, 50, 100),
    (7, "RONALD QUIROZ", "RONALDQUIROZHERNANDEZ.COM",0, 20, 90),
    (8, "ESTEPHANIE RAMIREZ", "STEPHANIERAMI28@GMAIL.COM",0, 70, 60),
    (9, "BRIAN BUSTAMANTE", "BRIANBUSTAMANTE@GMAIL.COM",1, 90, 10),
    (10, "GIOVANNY JUKOPILA", "JUKOPILA.GIOVANNY@HOTMAIL.COM", 1, 70, 20),
    (11, "JULIANA BALCERO", "JULIANA.BALCERO@GMAIL.COM", 1, 19, 80),
    (12, "CAMILA VILLAMIZAR", "CAMIILAVILLAMIZAR@GMAIL.COM",1, 80, 100)
]


micursor.executemany("INSERT INTO EMPLEADO VALUES (?,?,?,?,?,?)", empleados)

jefes =[
    (1, "RICARDO MONTANER", "RICARDO.MONTANER@GMAIL.COM"),
    (2, "LAURA ZAPATA", "LAURAZAPATACONTRERAS@GMAIL.COM"),
    (3, "KAREN GOMEZ", "KARENGOMEZQUIROZ@GMAIL.COM")
] 

micursor.executemany("INSERT INTO JEFE VALUES (?,?,?)", jefes)

actividades = [
    (1,
    "Realizar un informe del inventario",datetime(2019,7,19), "", 0, ""),
    (2,
    "Realizar presentacion en power point de la conferencia de Software", datetime(2019,3,19) ,"",0, ""),
    (3,
    "Realizar software de la conferencia de Tiendas", datetime(2019,4,23), "",0,""),
    (4,
    "Realizar busquedas necesarias para la elavoracion del software ITS983", datetime(2019,2,20) ,"",0,""),
    (5,
    "Planeacion del software T376", datetime(2019,6,29) ,"",0,""),
    (6,
    "Desarrollar Proyecto Final", datetime(2019,8,20) ,"",0,""),
    (7,
    "Desarrollar Proyecto Final", datetime(2019,8,20) ,"",0,""),
    (8,
    "Desarrollar Proyecto Final", datetime(2019,8,20) ,"",0,"")
]


micursor.executemany("INSERT INTO ACTIVIDAD VALUES (?,?,?,?,?,?)", actividades)

organizaciones = [
    (1,1),
    (1,2),
    (1,3),
    (1,4),
    (1,5),
    (2,6),
    (2,7),
    (2,8),
    (2,9),
    (3,10),
    (3,11),
    (3,12)
]

micursor.executemany("INSERT INTO ORGANIZACION VALUES (?,?)", organizaciones)

asignaciones = [
    (1,2),
    (2,3),
    (3,4),
    (4,5),
    (5,9),
    (6,10),
    (7,11),
    (8,12)
]

micursor.executemany("INSERT INTO ASIGNACION VALUES (?,?)", asignaciones)

con.commit()
con.close()
"""
#PARA LOS EMPLEADOS

peticiones = {
    "enviarA" : ["enviar"],
    "mastiempo" : ["mas tiempo", "no he logrado", "aplazar", "tiempo", "plazo"],
    "problemas" : ["problemas", "un problema"],
    "salir":["salir"]
  }
def problemas(emp):
    engine.say('\nCuenta en breves lineas cual es tu problema:\n ')
    engine.runAndWait()
    problema = input(str("Cuenta en breves lineas cual es tu problema: \n"))
    print("\nHe enviado este mensaje a tu jefe.")
    engine.say('He enviado este mensaje a tu jefe.')
    engine.runAndWait()
    micursor.execute("SELECT ACTIVIDAD FROM ASIGNACION WHERE EMPLEADO=?",emp)
    for m in micursor:
        id_act = m[0]
    micursor.execute("UPDATE ACTIVIDAD SET PROBLEMA=? WHERE ID = ?",(problema, str(id_act)))
    print("Todo bien")
    
    despedida()
    
    despedida()
def mastiempo(x):
    engine.say('¿Cuantos dias quieres aplazar tu entrega?')
    engine.runAndWait()
    tiemp = int(input("\n¿Cuantos dias quieres aplazar tu entrega?"))
    while (tiemp<0 or tiemp>150):
        if(tiemp<0):
            engine.say('jajaja los dias no pueden ser negativos. Ingrese cuantos dias quiere aplazar su entrega: ')
            tiemp = int(input("\njajaja los dias no pueden ser negativos. Ingrese cuantos dias quiere aplazar su entrega: "))
        if (tiemp>150):
            engine.say('Limite alcanzado. No puedes aplazar la actividad tantos dias. Ingrese la cantidad de dias que desea aplazar la actividad:')
            tiemp = int(input("\nLimite alcanzado. No puedes aplazar la actividad tantos dias. Ingrese la cantidad de dias que desea aplazar la actividad:"))

    engine.say('He enviado una solicitud de plazo de '+str(tiemp)+' dias a tu jefe.')
    print("He enviado una solicitud de plazo  de", tiemp, "dias a tu jefe.")
    engine.runAndWait()

    #cambia bd---coloca el numero de dias en la actividad
    micursor.execute("SELECT ACTIVIDAD FROM ASIGNACION WHERE EMPLEADO=?",x)
    for m in micursor:
        id_act = m[0]
    micursor.execute("UPDATE ACTIVIDAD SET MAYORPLAZO=? WHERE ID=?", (str(tiemp), id_act))
    despedida()
def enviarA(emp):

    conlink = "https://drive.google.com/"
    engine.say('Por favor ingrese el link de su actividad. Recuerde que debe ser un archivo en google drive.')
    engine.runAndWait()
    link = input(str("Por favor ingrese el link de su actividad. Recuerde que debe ser un archivo en google drive. Inglese link: "))
    link.capitalize()
    while (link.find(conlink)<0):
        engine.say('Recuerda que el link a enviar debe ser un documento en google drive!')
        engine.runAndWait()
        link = input(str("Recuerda que el link a enviar debe ser un documento en google drive! Ingrese link:"))
    engine.say('Lo he añadido a la entrega de la actividad')
    print("\nLo he añadido a la entrega de la actividad")
    engine.runAndWait()

  #cambios en la bd
    micursor.execute("UPDATE EMPLEADO SET DISPONIBILIDAD=0 WHERE ID=?", emp)
    micursor.execute("SELECT ACTIVIDAD FROM ASIGNACION WHERE EMPLEADO=?",emp)
    for m in micursor:
        id_act = m[0]
    micursor.execute("UPDATE ACTIVIDAD SET ENTREGA=? WHERE ID = ?",(link, str(id_act)))
    print("Todo bien")
    despedida()
def deteccion(c1, emp):
    if(c1 == "enviarA"):
        enviarA(emp)
    if (c1 == "mastiempo"):
        mastiempo(emp)
    if (c1 == "problemas"):
        problemas(emp)
    if(c1 == "salir"):
        engine.say('Ha sido un gusto! Hasta pronto')
        print("Ha sido un gusto. Hasta pronto!")
        engine.runAndWait()
        sys.exit()
def agregar2 (clave, agr, emp):
    print("\nLo tendre en cuenta para la proxima vez!")
    engine.say('Lo tendre en cuenta para la proxima vez!')
    engine.runAndWait()
    agre = agr.split()
    for x in agre:
        if (len(x)<=2 or x=="los" or x=="las" or x=="unos" or x=="unas" or x == "necesito" or x == "quiero" or x == "actividad"):
            a = agre.index(x)
            agre.pop(a)
    
    for c, v in peticiones.items():
        if (c == clave):
            for x in agre:
                v.append(x)
    deteccion(clave, emp) 
def agregar (arg, peticion, x):
    arg.capitalize()
    for c, v in peticiones.items():
        for va in v:
            if(arg.find(va)>=0):
                if (c == "enviarA"):
                    agregar2("enviarA",peticion, x)
                    break
                if (c == "mastiempo"):
                    agregar2("mastiempo",peticion, x)
                    break
                if (c == "problemas"):
                    agregar2("problemas",peticion, x)
                    break
                if(c == "salir"):
                    agregar2("salir",peticion, x)
                    break 
def soons (son, clave, peticion, emp):
    if(son == "si" or son == "SI" or son == "sI"):
        deteccion(clave, emp)
    else:
        nocomp(peticion, emp)
def nocomp(peticion, x):
    engine.say('No he logrado comprender tu peticion. ¿quieres enviar una tarea, pedir mayor plazo o presentas problemas con tu actividad?')  
    agr = input(str("\nNo he logrado comprender tu peticion. ¿quieres enviar una tarea, pedir mayor plazo o presentas problemas con tu actividad?\n"))
    engine.runAndWait()
    agregar(agr, peticion, x)
def peti(x,peticion):
    peticion.capitalize()
    for c,v in peticiones.items():
        for va in v:
            if(peticion.find(va)>=0):
                if (c == "enviarA"):
                    engine.say('¿Necesitas enviar tu actividad asignada?')
                    engine.runAndWait()
                    son = input(str("\n¿Necesitas enviar tu actividad asignada?"))
                    soons(son, c, peticion, x)
                    break
                if (c == "mastiempo"):
                    engine.say('¿Necesitas mas tiempo para realizar tu actividad asignada?')
                    engine.runAndWait()
                    son = input(str("\n¿Necesitas mas tiempo para realizar tu actividad asignada?"))
                    soons(son, c, peticion, x)
                    break
                if (c == "problemas"):
                    engine.say('¿Presentas problemas con tu actividad asignada?')
                    engine.runAndWait()
                    son = input(str("\n¿Presentas problemas con tu actividad asignada?"))
                    soons(son, c, peticion, x)
                    break
                if (c == "salir"):
                    engine.say('\n¿Desea salir?')
                    engine.runAndWait()
                    son = input(str("\n¿Desea salir?"))
                    soons(son, c, peticion, x) 
                    break
    nocomp(peticion, x)
def despedida():
    print("\nQue bueno haberte ayudado. Adios")
    engine.say('Que bueno haberte ayudado. Adios')
    engine.runAndWait()
    con.commit()
    con.close()
    sys.exit()
def info(x):
    micursor.execute("SELECT DISPONIBILIDAD FROM EMPLEADO WHERE ID=?",x)
    for m in micursor:
        if(m[0]==0):
            print("\nNo tiene tareas asignadas, vuelva mas tarde.")
            engine.say('No tiene tareas asignadas, vuelva mas tarde.')
            engine.runAndWait()
            despedida()
        else:
            micursor.execute("SELECT ACTIVIDAD FROM ASIGNACION WHERE EMPLEADO=?",x)
            for m in micursor:
                id_act = m[0]
            micursor.execute("SELECT DESCRIPCION,PLAZO,MAYORPLAZO FROM ACTIVIDAD WHERE ID=?",str(id_act))
            for n in micursor:
                engine.say('Tienes una actividad para la fecha en pantalla')
                print("Tienes una tarea asignada para la fecha ",n[1])
                print("Descripcion: ", n[0])
                print("Dias de plazo solicitados: ", n[2])
                engine.runAndWait()
                print("¿En que puedo ayudarte?")
                engine.say('¿En que puedo ayudarte?')
                engine.runAndWait()                             
def saludo(x, sal ):
    saludos = ["Hola", "Jucagi", "hola", "jucagi"]
    preguntas = ["¿como estas?", "¿que tal?"]
    sal.capitalize()
    for m in saludos:
        if(sal.find(m)>=0):
            micursor.execute("SELECT NOMBRE FROM EMPLEADO WHERE ID =?",x)
            for x in micursor:
                print("Hola", x[0])
                engine.say('hola '+x[0])
                engine.runAndWait()
            break
    for m in preguntas:
        if(sal.find(m)>=0):
            print('\nEstoy muy bien, ¡gracias!')
            engine.say('Estoy muy bien, ¡gracias!')
            engine.runAndWait()
            break

#PARA LOS JEFES
peticionesjef = {
  "ActsEnviadas": ["enviadas"],
  "SoldePlazo": ["solicitudes", "ampliacion", "plazo"],
  "problemas": ["problemas", "inconvenientes"],
  "nuevtarea": ["asignar", "nueva tarea"],
  "desempeno": ["desempeño", "buen empleado"],
  "salir":["salir"]
}
def desempeniof(x):
    a = micursor.execute("SELECT EMPLEADO FROM ORGANIZACION WHERE JEFE=?", str(x))    
    emps = a.fetchall()
    for i in emps:
        print("\nID: ", i[0])
        b = micursor.execute("SELECT NOMBRE, TAREAS, CALIDAD FROM EMPLEADO WHERE ID =?", i)
        noms = b.fetchall()
        for c in noms:
            print("Nombre: ", c[0])
            print("Tareas: ", c[1])
            print("Calidad: ", c[2])

            command_results.input['tareasatiempo'] = c[1]
            command_results.input['calidad'] = c[2]
            command_results.compute()
            command.view(sim=command_results)

            print("DESEMPEÑO: ", command_results.output['command'],"%")
            if(command_results.output['command']<40):
               print("Es un empleado deficiente\n")
            elif(command_results.output['command']<75):
                print("Es un empleado promedio\n")
            else:
                print("Es un empleado excelente\n")
    saludo3(x)

def error():
    print("\nPor favor, digite los datos correctamente.")
    engine.say('Por favor, digite los datos correctamente.')
    engine.runAndWait()
def nuevatarea(x):
    a = micursor.execute("SELECT EMPLEADO FROM ORGANIZACION WHERE JEFE=?", str(x))
    emps = a.fetchall()
    for i in emps:
        b = micursor.execute("SELECT DISPONIBILIDAD,NOMBRE FROM EMPLEADO WHERE ID=?", i)
        disp = b.fetchall()
        for c in disp:
            if(c[0]==0):
                print(c[1], "está disponible. Le asigare la tarea.")
                print("A continuacion por favor digite la fecha")
                dia = int(input("Dia:"))
                while (dia<0 and dia>31):
                    error()
                    dia = int(input("\nDia:"))
                mes = int(input("Mes:"))
                while(mes>12 or mes<0):
                    error()
                    mes = int(input("\nMes:"))
                anio= int(input("Año:"))
                while (anio>2020 or anio<2019):
                    error()
                    anio = int(input("\nAnio: "))
                engine.say('Haga una breve descripcion de la tarea')
                engine.runAndWait()
                desc = input(str("\nDescripcion de la tarea:"))

                a = micursor.execute("SELECT COUNT(*) FROM ACTIVIDAD")
                b = a.fetchall()
                for d in b:
                    tam = d[0]#numero de registros de la tabla actividades
                id_n = tam+1
                p = datetime(anio, mes, dia,00,00,00)
                micursor.execute("INSERT INTO ACTIVIDAD VALUES (?,?,?,?,?,?)", (id_n, desc, p, "", 0, ""))
                micursor.execute("UPDATE EMPLEADO SET DISPONIBILIDAD=1 WHERE ID=?", i)
                micursor.execute("INSERT INTO ASIGNACION VALUES (?,?)", (str(id_n), str(i[0])))
                print("\nTarea asignada")
                engine.say('la tarea ha sido asignada')
                engine.runAndWait()
                saludo3(x)
                break
def problemasjefe(x):
    a = micursor.execute("SELECT EMPLEADO FROM ORGANIZACION WHERE JEFE=?", str(x))    
    emps = a.fetchall()
    for i in emps:
        b = micursor.execute("SELECT NOMBRE, CORREO FROM EMPLEADO WHERE ID =?", i)
        noms = b.fetchall()
        for c in noms:
            d = micursor.execute("SELECT ACTIVIDAD FROM ASIGNACION WHERE EMPLEADO=?", str(i[0]))
            e = d.fetchall()
            for f in e:
                g = micursor.execute("SELECT PROBLEMA FROM ACTIVIDAD WHERE ID=?", str(f[0]))
                h = g.fetchall()
                for k in h:
                    print(k[0])
                    if(len(str(k[0]))!=0 and len(str(k[0]))!=1):
                        print(c[0], "Tiene un problema \nDescripcion:", k[0])
                        engine.say(str(c[0])+ "Tiene un problema ")
                        engine.runAndWait()
                        print("Por favor envie un correo a ", c[1], " describiendo la solucion del problema")
                        engine.say('Por favor envie un correo a la direccion en pantalla describiendo la solución del problema')
                        micursor.execute("UPDATE ACTIVIDAD SET PROBLEMA=? WHERE ID=?", ("", str(f[0])))
    print("\nNo hay empleados que tengan problemas con su actividad")
    engine.say('Ahora no hay empleados que tengan problemas con su actividad')
    engine.runAndWait()
    saludo3(x)
def SoldePlazo(x):
    a = micursor.execute("SELECT EMPLEADO FROM ORGANIZACION WHERE JEFE=?", str(x))    
    emps = a.fetchall()
    for i in emps:
        b = micursor.execute("SELECT NOMBRE FROM EMPLEADO WHERE ID =?", i)
        noms = b.fetchall()
        for c in noms:
            d = micursor.execute("SELECT ACTIVIDAD FROM ASIGNACION WHERE EMPLEADO=?", str(i[0]))
            e = d.fetchall()
            for f in e:
                g = micursor.execute("SELECT MAYORPLAZO, PLAZO FROM ACTIVIDAD WHERE ID=?", str(f[0]))
                h = g.fetchall()
                for k in h:
                    if(k[0]!=0):
                        print(c[0], "solicita una extensión de ", k[0], "dias")
                        engine.say(str(c[0])+ "solicita una extensión de "+ str(k[0]) + "dias")
                        engine.runAndWait()
                        engine.say('¿Aprueba esta solicitud?')
                        res = input(str("¿Aprueba esta solicitud?"))
                        if (res == "SI" or res == "si"):
                
                            fecha = datetime.strptime(k[1], '%Y-%m-%d %H:%M:%S') #no funciona 
                            fecha1 = fecha.date()
                            dias = timedelta(days=int(k[0]))
                            print("Tipo de dato fecha", type(fecha1))
                            print("Tipo de dato dias", type(dias))
                            fechamasdias = fecha1+dias
                            micursor.execute("UPDATE ACTIVIDAD SET PLAZO=? WHERE ID=?", (str(fechamasdias), str(f[0])))
                            micursor.execute("UPDATE ACTIVIDAD SET MAYORPLAZO=0 WHERE ID=?", str(f[0]))
                        
                  
    print("Ningun otro empleado ha solicitado plazo")
    engine.say('Ningun otro empleado ha solicitado plazo')
    saludo3(x)
def actsenviadas(x):
    a = micursor.execute("SELECT EMPLEADO FROM ORGANIZACION WHERE JEFE=?", str(x))    
    emps = a.fetchall()
    for i in emps:
        print("\nID: ", i[0])
        b = micursor.execute("SELECT NOMBRE FROM EMPLEADO WHERE ID =?", i)
        noms = b.fetchall()
        for c in noms:
            print("Nombre: ", c[0])
            d = micursor.execute("SELECT ACTIVIDAD FROM ASIGNACION WHERE EMPLEADO=?", str(i[0]))
            e = d.fetchall()
            for f in e:
                print("ID ACT: ", f[0])
                g = micursor.execute("SELECT ENTREGA FROM ACTIVIDAD WHERE ID=?", str(f[0]))
                h = g.fetchall()
                for k in h:
                    print("Engrega: ", k[0])
    saludo3(x)
def despedidajefe():
    engine.say('Supongo que eso es todo! hasta pronto')
    print("\nSupongo que eso es todo! hasta pronto")
    engine.runAndWait()
    con.commit()
    con.close()
    sys.exit()
def saludo3(x):
    engine.say('¿Desea que lo ayude en algo mas?')
    engine.runAndWait()
    print("\n¿Desea que lo ayude en algo mas?")
    res = input()
    if (res == "si" or res == "SI"):
        saludo2(x)
    else:
        despedidajefe()
def deteccionjefe(clave, x):
    print(clave)
    if(clave == "ActsEnviadas"):
        actsenviadas(x)
    if(clave == "SoldePlazo"):
        SoldePlazo(x)
    if (clave == "problemas"):
        problemasjefe(x)
    if(clave == "nuevtarea"):
        nuevatarea(x)
    if (clave == "desempeno"):
        desempeniof(x)
    if(clave == "salir"):
        despedidajefe()
def agregarjefes2(clave, agr, a):
    print("\nLo tendre en cuenta para un futuro!")
    engine.say('Lo tendre en cuenta para un futuro!')
    agre = agr.split()
    for x in agre:
        if (len(x)<=2 or x=="los" or x=="las" or x=="unos" or x=="unas" or x == "necesito" or x == "quiero" or x == "actividad"):
            a = agre.index(x)
            agre.pop(a)
    for c,v in peticionesjef.items():
        if (c == clave):
            for x in agre:
                v.append(x)
    engine.runAndWait()
    deteccionjefe(clave, a)
def agregarjefe(agr, peticion, x):
    agr.capitalize()
    for c,v in peticionesjef.items():
        for va in v:
            if (agr.find(va)>=0):
                if (c == "ActsEnviadas"):
                    agregarjefes2("ActsEnviadas", peticion, x)
                    break
                if (c == "SoldePlazo"):
                    agregarjefes2("SoldePlazo", peticion, x)
                    break
                if (c == "problemas"):
                    agregarjefes2("problemas", peticion, x)
                    break
                if (c == "nuevtarea"):
                    agregarjefes2("nuevtarea", peticion, x)
                    break
                if (c == "desempeno"):
                    agregarjefes2("desempeno", peticion, x)
                    break
                if(c == "salir"):
                    agregarjefes2("salir", peticion, x)
                    break
def nocompjefe(peticionjefe, x):
    engine.say('No he logrado comprender tu peticion. ')
    engine.runAndWait()
    agr = input(str("\nNo he logrado comprender tu peticion. ¿quieres ver las actividades enviadas, ver las solicitudes de ampliacion de plazos, ver los problemas que tienen tus empleados, asignar alguna tarea o ver el desempenio de sus empleados? \n"))
    agregarjefe(agr, peticionjefe, x)
def soons2(son2, clave, peticion, x):
    if(son2 == "si" or son2 == "SI" or son2 == "sI"):
        deteccionjefe(clave, x)
    else:
        nocompjefe(peticion, x)
def saludojefe(sal, x):
    saludos = ["Hola", "Jucagi", "hola", "jucagi"]
    preguntas = ["¿como estas?", "¿que tal?"]
    sal.capitalize()
    for m in saludos:
        if(sal.find(m)>=0):
            micursor.execute("SELECT NOMBRE FROM JEFE WHERE ID =?",str(x))
            for x in micursor:
                print("Hola", x[0])
                engine.say('hola '+x[0])
                engine.runAndWait()
            break
    for m in preguntas:
        if(sal.find(m)>=0):
            print('\nEstoy muy bien, ¡gracias!')
            engine.say('Estoy muy bien, ¡gracias!')
            engine.runAndWait()
            break
def saludo2(x):
    peticionjefe = input()
    peticionjefe.capitalize()
    for c,v in peticionesjef.items():
        for va in v:
            if (peticionjefe.find(va)>=0):
                if(c == "ActsEnviadas"):
                    engine.say('¿Desea ver las actividades enviadas de sus empleados?')
                    engine.runAndWait()
                    son2 = input(str("\n¿Desea ver las actividades enviadas de sus empleados?"))
                    soons2( son2, c, peticionesjef, x)
                    break
                if(c == "SoldePlazo"):
                    engine.say('¿Desea ver las solicitudes de ampliacion de plazos de sus empleados?')
                    engine.runAndWait()
                    son2 = input(str("\n¿Desea ver las solicitudes de ampliacion de plazos de sus empleados?"))
                    soons2( son2, c, peticionesjef, x)
                    break
                if(c == "problemas"):
                    engine.say('¿Desea ver los inconvenientes que tienen sus empleados?')
                    engine.runAndWait()
                    son2 = input(str("\n¿Desea ver los inconvenientes que tienen sus empleados?"))
                    soons2( son2, c, peticionesjef, x)
                    break
                if (c == "nuevtarea"):
                    engine.say('¿Desea asignar una nueva tarea?')
                    engine.runAndWait()
                    son2 = input(str("\n¿Desea asignar una nueva tarea?"))
                    soons2(son2, c, peticionesjef, x)
                    break
                if (c == "desempeno"):
                    engine.say('¿Desea ver el desempenio de sus empleados?')
                    engine.runAndWait()
                    son2 = input(str("\n¿Desea ver el desempenio de sus empleados?"))
                    soons2(son2, c, peticionesjef, x)
                    break
                if (c == "salir"):
                    engine.say('¿Esta seguro que desea salir?')
                    engine.runAndWait()
                    son2 = input(str("\n¿Esta seguro que desea salir?"))
                    soons2(son2, c, peticionesjef, x)
                    break
    nocompjefe(peticionjefe, x)
def saludo1jefe(x):
    engine.say('Puedo ayudarlo en estas acciones')
    print("Puedo ayudarlo en:\nVer actividades enviadas de sus empleados\nVer solicitudes de ampliacion de plazos\nVer problemas de los empleados\nAsignar nueva tarea\nVer desempenio de sus empleados\n¿En que puedo ayudarlo?")
    engine.runAndWait()
    saludo2(x)
def main():


  print("-------------------------------------------------------------------")
  print("                     HOLA, ME LLAMO JUCAGI                          ")
  print("--------------------------------------------------------------------")
  eoj = input()
  if (eoj == "902/"):
    x = input()
    sal = input()
    saludo(x, sal)
    info(x)
    peticion = input()
    peti(x, peticion)
  elif (eoj == "442/"):
      idjef = int(input(""))
      salu = input("")
      saludojefe(salu, idjef)
      saludo1jefe(idjef)
  else:
      print("No es trabajador de la empresa.")
      engine.say('No es trabajador de la empresa.')
      engine.runAndWait()
      main()
    
main()


if __name__ == "__main__":
    main()