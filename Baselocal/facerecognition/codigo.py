from cgitb import reset
import face_recognition
import cv2
import numpy as np
import psycopg2
import pytz
from datetime import datetime
import os
import time
from math import  acos,degrees
import mediapipe as mp

conn = None
dias_semana = ("Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo")
ultimahora = datetime.strptime('23:59:59', '%H:%M:%S').time()
primerahora = datetime.strptime('00:00:00', '%H:%M:%S').time()
flaghorario = 0 #1 para dar acceso y 0 para denegarlo
directorio=os.environ.get("DIRECTORIO")
imagenes = os.listdir(directorio)
nombres = []
caras = []
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
parpado=0
parpadeos=0
d1old=0
d2old=0
video=None
vista_previargb = 0
vista_previa = 0
razon="entrada"
t1=time.perf_counter()
t2=0
xref=0
yref=0
xrefold=0
yrefold=0
x_1=0
y_1=0
etapadia=0
intento=0
total=0
resetvideo=0

# for imagen in imagenes:
#     ruta=os.path.join(directorio,imagen)
#     subir_foto = face_recognition.load_image_file(ruta)
#     decodificar = face_recognition.face_encodings(subir_foto)
#     if decodificar != []:
#         decodificar = face_recognition.face_encodings(subir_foto)[0]
#         caras.append(decodificar)
#         nombre = os.path.splitext(imagen)[0]
#         nombres.append(nombre)

#caras2 = np.array(caras)
#print(caras2.shape)

def aperturaconcedida(nombref, fechaf, horaf, razonf, contratof, cedulaf, cursorf,connf):
    cursorf.execute('''INSERT INTO web_interacciones (nombre, fecha, hora, razon, contrato, cedula_id)
    VALUES (%s, %s, %s, %s, %s, %s);''', (nombref, fechaf, horaf, razonf, contratof, cedulaf))
    cursorf.execute('''UPDATE led SET onoff=1 WHERE onoff=0;''')
    connf.commit()
    
    #cursorf.execute('SELECT * FROM led')
    #estado_led= cursorf.fetchall()
    #while estado_led[0][0]==1:
    #    cursorf.execute('SELECT * FROM led')
    #    estado_led= cursor.fetchall()

def aperturadenegada(cursorf, connf):
    cursorf.execute('''UPDATE led SET onoff=2 WHERE onoff=0;''')
    connf.commit()
    
    #cursorf.execute('SELECT * FROM led')
    #estado_led= cursorf.fetchall()
    #while estado_led[0][0]==2:
    #    cursorf.execute('SELECT * FROM led')
    #    estado_led= cursorf.fetchall()

while True:
    
    t11=time.perf_counter()
    while total<=5:
        t22=time.perf_counter()
        total=t22-t11
    total=0

    try:

        conn = psycopg2.connect(
            database=os.environ.get("SQL_DATABASE"), 
            user=os.environ.get("SQL_USER"), 
            password=os.environ.get("SQL_PASSWORD"), 
            host=os.environ.get("SQL_HOST"), 
            port=os.environ.get("SQL_PORT")
        )

        conn.autocommit = False
        cursor = conn.cursor()
        with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75) as face_mesh:
            #camara = cv2.VideoCapture("http://192.168.21.102:81/stream")
            #camara = cv2.VideoCapture("http://192.168.20.102:8080/?action=stream")
            camara = cv2.VideoCapture(os.environ.get("HOST_STREAM"))
            while True:
                tz = pytz.timezone('America/Caracas')
                caracas_now = datetime.now(tz)
                #vista_previa = 0  
                ret,video = camara.read()
                if video is None:
                    camara = cv2.VideoCapture(os.environ.get("HOST_STREAM"))
                    ret,video = camara.read()
                    cv2.destroyAllWindows()
                #video = cv2.flip(video, 0)
                #print(video)

                cursor.execute('SELECT * FROM sensor')
                sensor_onoff = cursor.fetchall()


                if video is not None and sensor_onoff[0][0] == 1:
                    resetvideo=0
                    alto, ancho, _ = video.shape
                    K = np.float32([[1,0,100],[0,1,100]])
                    video2 = cv2.warpAffine(video, K, (ancho+200,alto+200))
                    alto2, ancho2, _ = video2.shape
                    K = cv2.getRotationMatrix2D((ancho2 // 2, alto2 // 2), 90, 1)
                    video2 = cv2.warpAffine(video2, K, (alto2,ancho2))
                    K = np.float32([[1,0,-180],[0,1,-21]])
                    video = cv2.warpAffine(video2, K, (alto, ancho))
                    video = cv2.flip(video, 0)
                    alto, ancho, _ = video.shape
                    videorgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
                    results = face_mesh.process(videorgb)

                    if results.multi_face_landmarks is not None:

                        for face_landmarks in results.multi_face_landmarks:
                            
                            #mejilla derecha
                            y_447 = int(face_landmarks.landmark[447].y * alto) 
                            x_447 = int(face_landmarks.landmark[447].x * ancho) 
                            #mejilla izquierda
                            y_227 = int(face_landmarks.landmark[227].y * alto)
                            x_227 = int(face_landmarks.landmark[227].x * ancho)
                            #frente  
                            y_10 = int(face_landmarks.landmark[10].y * alto)
                            x_10 = int(face_landmarks.landmark[10].x * ancho)
                            #barbilla
                            y_175 = int(face_landmarks.landmark[175].y * alto)
                            x_175 = int(face_landmarks.landmark[175].x * ancho)

                        #creando coordenadas de cada punto
                        p1 = np.array([x_447, y_447])
                        p2 = np.array([x_227, y_227])
                        p3 = np.array([x_227, y_447])

                        #obteniendo distancias entre los puntos
                        d1 = np.linalg.norm(p1-p2)
                        d2 = np.linalg.norm(p1-p3)

                        angulo = degrees(acos(d2/d1))
                        
                        #haciendo que el angulo sea negativo cuando se rote la cabeza
                        #a la derecha
                        if y_227 < y_447:
                            angulo= -angulo

                        #registrando la rotacion
                        m = cv2.getRotationMatrix2D((ancho // 2, alto // 2), -angulo, 1)
                        
                        #crearndo nueva ventana y dandole la rotacion a la imagen
                        alinear = cv2.warpAffine(video, m, (ancho,alto))
                        alinear_rgb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)
                            #cv2.imshow("alinear", alinear)
                            
                        results2 = face_mesh.process(alinear_rgb)
                        
                        if results2.multi_face_landmarks is not None:

                            for face_landmarks in results2.multi_face_landmarks:

                                #puntos de los parpados 
                                y_386 = int(face_landmarks.landmark[386].y * alto*10) 
                                y_374 = int(face_landmarks.landmark[374].y * alto*10) 
                                y_159 = int(face_landmarks.landmark[159].y * alto*10)
                                y_145 = int(face_landmarks.landmark[145].y * alto*10)
                                x_386 = int(face_landmarks.landmark[386].x * ancho*10) 
                                x_374 = int(face_landmarks.landmark[374].x * ancho*10) 
                                x_159 = int(face_landmarks.landmark[159].x * ancho*10)
                                x_145 = int(face_landmarks.landmark[145].x * ancho*10)

                                y_1 = int(face_landmarks.landmark[1].y * alto)
                                x_1 = int(face_landmarks.landmark[1].x * ancho)

                                #mejilla derecha
                                y_447 = int(face_landmarks.landmark[447].y * alto) 
                                x_447 = int(face_landmarks.landmark[447].x * ancho) 
                                #mejilla izquierda
                                y_227 = int(face_landmarks.landmark[227].y * alto)
                                x_227 = int(face_landmarks.landmark[227].x * ancho)
                                #frente  
                                y_10 = int(face_landmarks.landmark[10].y * alto)
                                x_10 = int(face_landmarks.landmark[10].x * ancho)
                                #barbilla
                                y_175 = int(face_landmarks.landmark[175].y * alto)
                                x_175 = int(face_landmarks.landmark[175].x * ancho)
                            

                            #if xmin < 0 or ymin < 0:
                            #    continue
                            if y_10 >=20 and x_227 >= 20:
                                vista_previa = alinear[y_10-20 : y_175 +20, x_227 - 20: x_447 +20]
                                vista_previargb = cv2.cvtColor(vista_previa, cv2.COLOR_BGR2RGB)
                                altog, anchog, _ = vista_previargb.shape
                                vista_previargb = cv2.resize(vista_previargb, (anchog+100,altog+100))
                            

                                p1 = np.array([x_386, y_386])
                                p2 = np.array([x_386, y_374])
                                p3 = np.array([x_386, y_159])
                                p4 = np.array([x_386, y_145])

                                d1 = np.linalg.norm(p1-p2)
                                d2 = np.linalg.norm(p4-p3)
                                
                                # dify1_1=
                                # dify1_2=

                                

                                if t2-t1 >= 0.7 and (x_1 >= xref+10 or x_1 <= xref-10 or y_1 >= yref+10 or y_1 <= yref-10):
                                #if x_1 >= xref+10 or x_1 <= xref-10 or y_1 >= yref+10 or y_1 <= yref-10:
                                    yref = y_1
                                    xref = x_1
                                
                                if xrefold != 0 and (xrefold != xref or yrefold != yref):
                                    xref=0
                                    yref=0
                                
                            # if cv2.waitKey(1) & 0xFF == ord('e'):
                            #     razon = "entrada"
                
                            # if cv2.waitKey(1) & 0xFF == ord('s'):
                            #     razon = "salida"

                                dif1 = (d1old*17)/100
                                dif2 = (d2old*17)/100

                                if d1>=d1old and d2>=d2old:
                                    parpado=1
                                t2=time.perf_counter()
                                if t2-t1 < 0:
                                    t2=0
                                if d1<=d1old-dif1 and d2<=d2old-dif2 and parpado==1 and x_1 <= xrefold+5 and x_1>=xrefold-5 and y_1 <= yrefold+5 and y_1 >= yrefold-5 and xref == xrefold and yref == yrefold:
                                    parpadeos=parpadeos+1         
                                    #face_locations = face_recognition.face_locations(alinear_rgb)
                                    encodingcamara = face_recognition.face_encodings(vista_previargb)          
                                    if encodingcamara != []:

                                        encodingcamaraa = face_recognition.face_encodings(vista_previargb)[0]

                                        resultado = face_recognition.compare_faces(caras, encodingcamaraa, tolerance=0.5)

                                        #nombre = "rostro no identificado. parpadee otra vez"
                                        nombrefoto = []
                                        etapadia=0
                                        etapadiaapertura=0
                                        if True in resultado:
                                            rostro_encontrado = resultado.index(True)
                                            nombrefoto = nombres[rostro_encontrado]
                                            fotoconsulta = f'{directorio}/{nombrefoto}.jpg'
                                            cursor.execute('SELECT cedula_id FROM web_fotos where foto=%s', (fotoconsulta,))
                                            cedula_id = cursor.fetchall()
                                            cedula_id = cedula_id[0][0]
                                            dia = caracas_now.weekday()
                                            diahoy = dias_semana[dia]
                                            cursor.execute('SELECT * FROM web_horariospermitidos where cedula_id=%s', (cedula_id,))
                                            horarios_permitidos = cursor.fetchall()
                                            if horarios_permitidos != []:
                                                cursor.execute('SELECT * FROM web_usuarios where cedula=%s', (cedula_id,))
                                                nombrecedula = cursor.fetchall()
                                                nombre=nombrecedula[0][1]
                                                contrato=nombrecedula[0][2]
                                                for entrada, salida, _, dia in horarios_permitidos:
                                                    if dia==diahoy:
                                                        hora=str(caracas_now)[11:19]
                                                        horahoy = datetime.strptime(hora, '%H:%M:%S').time()
                                                        fecha=str(caracas_now)[:10]
                                                        etapadia=1
                                                        if entrada<salida:
                                                            if horahoy >= entrada and horahoy <= salida:
                                                                #print('entrada concedida')
                                                                aperturaconcedida(nombre, fecha, horahoy, razon, contrato, cedula_id, cursor,conn)
                                                                etapadiaapertura=1
                                                            else:
                                                                aperturadenegada(cursor, conn)
                                                                #print('fuera de horario')
                                                        if entrada>salida:
                                                            if (horahoy>=entrada and horahoy <=ultimahora) or (horahoy>=primerahora and horahoy <= salida):
                                                                #print('entrada concedida')
                                                                aperturaconcedida(nombre, fecha, horahoy, razon, contrato, cedula_id, cursor,conn)
                                                                etapadiaapertura=1
                                                            else:
                                                                aperturadenegada(cursor, conn)
                                                                #print('fuera de horario')
                                                if etapadia==0 and etapadiaapertura==0:
                                                    aperturadenegada(cursor, conn)
                                                    #print('Dia no permitido')
                                            if horarios_permitidos == []:
                                                aperturadenegada(cursor, conn) 
                                                #print('este usuario no tiene horarios establecidos')
                                        if nombrefoto == []:
                                            aperturadenegada(cursor, conn)
                                            
                                        #print(nombre)
                                    #print(f"numero de parpadeos en esta sesion= {parpadeos}")
                                    parpado=0
                                    d1old=0
                                    d2old=0
                                    
                                if t2-t1 >= 0.9:
                                    d1old=d1
                                    d2old=d2
                                    t1=time.perf_counter()
                                
                                xrefold=xref
                                yrefold=yref
                                    
                    tecla = cv2.waitKey(1)

                    #esto es solo para simular la entrada y salida para las consultas
                    if tecla & 0xFF == 226:
                        razon = "entrada"
                    
                    if tecla & 0xFF == 225:
                        razon = "salida"

                    imagenes = os.listdir(directorio)


                    if len(nombres) > len(imagenes):
                        for img in nombres:
                            try:
                                nombreencarpeta=f'{img}.jpg'  
                                imagenes.index(nombreencarpeta)       
                            except ValueError:
                                indice = nombres.index(img)   
                                nombres.pop(indice)
                                caras.pop(indice)
                                #print(nombres)
                                #print(nombres)
                                
                        #imagenes = os.listdir(directorio)
                        
                        # print(nombres)
                        # caras2 = np.array(caras)
                        # print(caras2.shape)

                    if len(imagenes) > len(nombres):
                        for img in imagenes:
                            nombrecarpeta=os.path.splitext(img)[0]
                            fotoconsulta = f'{directorio}/{img}'
                            try:      
                                comprobar = nombres.index(nombrecarpeta)
                            except ValueError:
                                ruta=os.path.join(directorio,img)
                                subir_foto = face_recognition.load_image_file(ruta)
                                decodificar = face_recognition.face_encodings(subir_foto)
                                if decodificar != []:
                                    decodificar = face_recognition.face_encodings(subir_foto)[0]
                                    caras.append(decodificar)
                                    nombre = os.path.splitext(img)[0]
                                    nombres.append(nombre)
                                    cursor.execute('UPDATE web_fotos SET estado=1 WHERE foto=%s;', (fotoconsulta,))
                                    conn.commit()
                                else:
                                    cursor.execute('UPDATE web_fotos SET estado=2 WHERE foto=%s;', (fotoconsulta,))
                                    conn.commit()
                                    
                        for img in imagenes:
                            nombre=os.path.splitext(img)[0]
                            try:
                                comprobar = nombres.index(nombre)
                            except ValueError:
                                ruta=os.path.join(directorio,img)
                                os.remove(ruta)
                                #imagenes = os.listdir(directorio)
                                #print(f"rostro {nombre} no registrado!")
                        
                        # print(nombres)
                        # caras2 = np.array(caras)
                        # print(caras2.shape)
                        
                    #cv2.imshow('imagenp', vista_previa)
                    #cv2.imshow('imageng', vista_previargb)
                    cv2.imshow('imagenn', video)
                    

                    if tecla & 0xFF == 27:
                        break
                    
                    tecla = 0
                else:
                    if resetvideo == 0:
                        resetvideo ==1
                        cv2.destroyAllWindows()

        
        camara.release()
        cv2.destroyAllWindows()

    except (Exception, psycopg2.Error) as error:
        #print("fallo en hacer las consultas")
        camara.release()
        cv2.destroyAllWindows()
        total=0

    finally:
        if conn:
            cursor.close()
            conn.close()
            #print("se ha cerrado la conexion a la base de datos")
            camara.release()
            cv2.destroyAllWindows()
            total=0
