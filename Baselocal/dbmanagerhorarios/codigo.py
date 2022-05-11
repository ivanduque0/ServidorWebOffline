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

            if total > 3:

                for usuario in usuarios_local:
                    cedula=usuario[0]
                    try:
                        listausuarioslocal.index(cedula)
                    except ValueError:
                        listausuarioslocal.append(cedula)
                
                for usuario in listausuarioslocal:
                    cursorweblocal.execute('SELECT entrada, salida, cedula_id, dia FROM web_horariospermitidos WHERE cedula_id=%s',(usuario,))
                    diasheroku= cursorweblocal.fetchall()
                    
                    cursorlocal.execute('SELECT * FROM web_horariospermitidos WHERE cedula_id=%s',(usuario,))
                    diaslocal= cursorlocal.fetchall()

                    if len(diasheroku) > 0 and len(diasheroku) > len(diaslocal):
                        for diasherokuiterar in diasheroku:
                            try:
                                diaslocal.index(diasherokuiterar)
                            except ValueError:
                                entrada=diasherokuiterar[0]
                                salida=diasherokuiterar[1]
                                cedula=diasherokuiterar[2]
                                dia=diasherokuiterar[3]
                                cursorlocal.execute('''INSERT INTO web_horariospermitidos (entrada, salida, cedula_id, dia)
                                VALUES (%s, %s, %s, %s);''', (entrada, salida, cedula, dia))
                                connlocal.commit()

                    if len(diaslocal) > len(diasheroku):
                        for diaslocaliterar in diaslocal:
                            try:
                                diasheroku.index(diaslocaliterar)
                            except ValueError:
                                entrada=diaslocaliterar[0]
                                salida=diaslocaliterar[1]
                                cedula=diaslocaliterar[2]
                                dia=diaslocaliterar[3]
                                cursorlocal.execute('DELETE FROM web_horariospermitidos WHERE entrada=%s AND salida=%s AND cedula_id=%s AND dia=%s',(entrada, salida, cedula, dia))
                                connlocal.commit()
                diaslocal=[]
                diasheroku=[]
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
