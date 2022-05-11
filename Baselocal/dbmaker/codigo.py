import psycopg2
import os
import time
connlocal = None
cursorlocal=None
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


        cursorlocal.execute('CREATE TABLE IF NOT EXISTS web_usuarios (cedula integer, nombre varchar(150), contrato_id varchar(150))')
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS web_interacciones (nombre varchar(150), fecha date, hora time without time zone, razon varchar(150), contrato varchar(150), cedula_id integer)')
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS web_horariospermitidos (entrada time without time zone, salida time without time zone, cedula_id integer, dia varchar(180))')
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS web_fotos (id integer, foto varchar(150), estado integer, cedula_id integer)')
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS led (onoff integer)')
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS sensor (onoff integer)')
        connlocal.commit()
        cursorlocal.execute('SELECT*FROM led')
        tablaled= cursorlocal.fetchall()
        cursorlocal.execute('SELECT*FROM sensor')
        tablasensor= cursorlocal.fetchall()
        if len(tablaled) < 1:
            cursorlocal.execute('INSERT INTO led values(0)')
            connlocal.commit()
        if len(tablasensor) < 1:
            cursorlocal.execute('INSERT INTO sensor values(0)')
            connlocal.commit()


    except (Exception, psycopg2.Error) as error:
        print("fallo en hacer las consultas")
        if connlocal:
            cursorlocal.close()
            connlocal.close()

    finally:
        if connlocal:
            cursorlocal.close()
            connlocal.close()
        print("se ha cerrado la conexion a la base de datos")
        break
    
