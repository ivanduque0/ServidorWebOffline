import psycopg2
import os
import subprocess
import time
import cloudinary
import urllib.request
import numpy as np
import cv2

CONTRATO=os.environ.get("CONTRATO")
connlocal = None
connweblocal = None
cursorweblocal=None
cursorlocal=None
listausuarioslocal=[]
listausuariosheroku=[]
total=0
DIRECTORIO=os.environ.get("DIRECTORIO", "media/personas")
if not os.path.exists(DIRECTORIO): 
    os.makedirs(DIRECTORIO)

while True:
    
    t1=time.perf_counter()
    while total<=5:
        t2=time.perf_counter()
        total=t2-t1
    total=0
    try:
        
        #con esto se apunta a la base de datos local
        connlocal = psycopg2.connect(
            database=os.environ.get("DATABASE"), 
            user=os.environ.get("USER"), 
            password=os.environ.get("PASSWORD"), 
            host=os.environ.get("HOST"), 
            port=os.environ.get("PORT")
        )
        cursorlocal = connlocal.cursor()

        connweblocal = psycopg2.connect(
            database=os.environ.get("DATABASE"), 
            user=os.environ.get("USER"), 
            password=os.environ.get("PASSWORD"), 
            host=os.environ.get("HOST2"), 
            port=os.environ.get("PORT")
        )
        cursorweblocal = connweblocal.cursor()
        
        
        t1=time.perf_counter()
        while True:
            t2=time.perf_counter()
            total=t2-t1

            cursorlocal.execute('SELECT * FROM web_usuarios where contrato_id=%s', (CONTRATO,))
            usuarios_local= cursorlocal.fetchall()

            cursorweblocal.execute('SELECT * FROM web_usuarios where contrato_id=%s', (CONTRATO,))
            usuarios_heroku= cursorweblocal.fetchall()

            if total>3:
                
                for usuario in usuarios_local:
                    cedula=usuario[0]
                    try:
                        listausuarioslocal.index(cedula)
                    except ValueError:
                        listausuarioslocal.append(cedula)

                for usuario in usuarios_heroku:
                    cedula=usuario[0]
                    try:
                        listausuariosheroku.index(cedula)
                    except ValueError:
                        listausuariosheroku.append(cedula)
                
                if len(usuarios_local) == len(usuarios_heroku):
                

                    for usuario in listausuarioslocal:
                        cursorlocal.execute('SELECT * FROM web_fotos where cedula_id=%s', (usuario,))
                        fotos_local= cursorlocal.fetchall()
                        cursorweblocal.execute('SELECT * FROM web_fotos where cedula_id=%s', (usuario,))
                        fotos_heroku= cursorweblocal.fetchall()

                        #eliminar fotos no validadas de forma local

                        for fotolocal in fotos_local:
                            estado=fotolocal[2]
                            id=fotolocal[0]
                            foto=fotolocal[1]
                            if estado==2:
                                cursorweblocal.execute('UPDATE web_fotos SET estado=2 WHERE id=%s', (id,))
                                connweblocal.commit()
                            if estado==1:
                                cursorweblocal.execute('UPDATE web_fotos SET estado=1 WHERE id=%s', (id,))
                                connweblocal.commit()
                                
                        #eliminar fotos de la base de datos local que no esten en la base de datos de heroku
                        if len(fotos_local) > len(fotos_heroku):
                            for fotolocal in fotos_local:
                                id=fotolocal[0]
                                foto=fotolocal[1]
                                try:
                                    fotos_heroku.index(fotolocal)
                                except ValueError:
                                    cursorlocal.execute('DELETE FROM web_fotos where id=%s', (id,))
                                    connlocal.commit()
                                    os.remove(f'{foto}.jpg')


                        #agregar fotos que no estan en la base de datos local pero que si estan en la de heroku
                        if len(fotos_local) < len(fotos_heroku):
                            for fotoheroku in fotos_heroku:
                                try:
                                    fotos_local.index(fotoheroku)
                                except ValueError:
                                    id=fotoheroku[0]
                                    foto=fotoheroku[1]
                                    estado=fotoheroku[2]
                                    cedula=fotoheroku[3]
                                    cursorlocal.execute('''INSERT INTO web_fotos (id, foto, estado, cedula_id)
                                    VALUES (%s, %s, %s, %s);''', (id, foto, estado, cedula))
                                    connlocal.commit()

                    

                        
                    total=0
                    listausuariosheroku=[]
                    listausuarioslocal=[]
                    t1=time.perf_counter()

    except (Exception, psycopg2.Error) as error:
        print("fallo en hacer las consultas")
        if connlocal:
            cursorlocal.close()
            connlocal.close()
        if connweblocal:
            cursorweblocal.close()
            connweblocal.close()
    finally:
        if connlocal:
            cursorlocal.close()
            connlocal.close()
        if connweblocal:
            cursorweblocal.close()
            connweblocal.close()
            print("se ha cerrado la conexion a la base de datos")
