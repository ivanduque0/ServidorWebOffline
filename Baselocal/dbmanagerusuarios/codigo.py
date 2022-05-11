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
listausuariosheroku=[]
listausuarioslocal=[]
total=0

while True:
    
    t1=time.perf_counter()
    while total<=5:
        t2=time.perf_counter()
        total=t2-t1
    total=0
    try:
        
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

            nro_usu_local = len(usuarios_local)
            nro_usu_heroku = len(usuarios_heroku)


            if total>3:
            
                #cuando se va a eliminar un usuario
                if nro_usu_local > nro_usu_heroku:

                    for usuario in usuarios_heroku:
                        cedula=usuario[0]
                        try:
                            listausuariosheroku.index(cedula)
                        except ValueError:
                            listausuariosheroku.append(cedula)
                    
                    for usuario in usuarios_local:
                        cedula=usuario[0]
                        try:
                            listausuarioslocal.index(cedula)
                        except ValueError:
                            listausuarioslocal.append(cedula)

                    for usuario in listausuarioslocal:
                        try:
                            listausuariosheroku.index(usuario)
                        except ValueError:
                            cursorlocal.execute('DELETE FROM web_usuarios WHERE cedula=%s', (usuario,))
                            cursorlocal.execute('DELETE FROM web_fotos WHERE cedula_id=%s', (usuario,))
                            cursorlocal.execute('DELETE FROM web_horariospermitidos WHERE cedula_id=%s', (usuario,))
                            connlocal.commit()
                    listausuariosheroku=[]
                    listausuarioslocal=[]

                # cuando se va a agregar usuarios
                if nro_usu_heroku > nro_usu_local:

                    for usuario in usuarios_heroku:
                        cedula=usuario[0]
                        try:
                            listausuariosheroku.index(cedula)
                        except ValueError:
                            listausuariosheroku.append(cedula)
                    
                    for usuario in usuarios_local:
                        cedula=usuario[0]
                        try:
                            listausuarioslocal.index(cedula)
                        except ValueError:
                            listausuarioslocal.append(cedula)

                    for usuario in listausuariosheroku:
                        try:
                            listausuarioslocal.index(usuario)
                        except ValueError:
                            cursorweblocal.execute('SELECT * FROM web_usuarios where cedula=%s', (usuario,))
                            usuario_heroku= cursorweblocal.fetchall()
                            cedula=usuario_heroku[0][0]
                            nombre=usuario_heroku[0][1]
                            cursorlocal.execute('''INSERT INTO web_usuarios (cedula, nombre, contrato_id)
                            VALUES (%s, %s, %s)''', (cedula, nombre, CONTRATO))
                            connlocal.commit()
                    listausuariosheroku=[]
                    listausuarioslocal=[]
                total=0
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
