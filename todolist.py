import mysql.connector
import redis
import os
from colorama import Fore

bdRedis = redis.StrictRedis(host='localhost', port=6379, db=0)
connection = mysql.connector.connect(host='localhost',
                                         database='todolist',
                                         user='root',
                                         password='962994')
sqlGetAll = "SELECT id, descripcion, completada from tarea"
sqlWhereID = " WHERE id = "
sqlWhereEstado = " WHERE completada = "

## Agregar una tarea a la lista
def agregar_tarea(tarea):
    tarea_id = bdRedis.incr('numID')  # Generar un nuevo ID para la tarea
    tarea_key = f'tarea:{tarea_id}' # Combina la palabra 'tarea' con el numID formado en la linea anterior
    bdRedis.hset(tarea_key, 'id', tarea_id)
    bdRedis.hset(tarea_key, 'descripcion', tarea)
    bdRedis.hset(tarea_key, 'completada', 'False')

def agregar_tarea_id(tarea_id, tarea_descripcion, tarea_completada):
    tarea_key = f'tarea:{tarea_id}' # Combina la palabra 'tarea' con el numID formado en la linea anterior
    bdRedis.hset(tarea_key, 'id', tarea_id)
    bdRedis.hset(tarea_key, 'descripcion', tarea_descripcion)
    bdRedis.hset(tarea_key, 'completada', tarea_completada)
    bdRedis.incr('numID')
    

## Obtener las tareas de la lista
def obtener_tareas_todas():
    keys = bdRedis.keys('tarea:*') # Se trae todas las tareas que tiene en su clave la palabra 'tarea' 
    tareas = []
    for key in keys:
        tarea = bdRedis.hgetall(key) # Obtiene todos los campos y valores del hash
        tareas.append(tarea)
    if len(tareas) == 0 :
        sql = sqlGetAll
        tareas = cache_redis(sql)
    return tareas


## Obtener las tareas completadas
def obtener_tareas_completadas():
    return obtener_tareas_por_estado('True')

## Obtener las tareas no completadas
def obtener_tareas_no_completadas():
    return obtener_tareas_por_estado('False')

## Eliminar tareas por estado
def obtener_tareas_por_estado(estado):
    keys = bdRedis.keys('tarea:*')
    tareas = []
    for key in keys:
        tarea = bdRedis.hgetall(key)
        tarea = {k.decode('utf-8'): v.decode('utf-8') for k, v in tarea.items()}
        if tarea['completada'] == estado:
            tareas.append(tarea)
    return tareas

## Eliminar tareas por ID
def eliminar_tarea(tarea_id):
    tarea_key = f'tarea:{tarea_id}'
    bdRedis.delete(tarea_key)  # elimina una clave específica y su valor asociado

## Marcar tareas como COMPLETADAS por su ID
def marcar_completada(tarea_id):
    tarea_key = f'tarea:{tarea_id}'
    bdRedis.hset(tarea_key, 'completada', 'True') # permite crear o actualizar un campo y asignarle un valor en un hash existente 

## Resetear memoria
def limpiar_memoria():
    bdRedis.flushdb()  # Elimina todos los datos almacenados en la base de datos actual

## Definimos el cache con MySQL
def cache_redis(sql):
    # INPUT 1 : SQL query
    # INPUT 2 : Tiempo de expiración
    # OUTPUT  : Array de resultados
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            agregar_tarea_id(row[0], row[1], row[2])
        cursor.close()
        keys = bdRedis.keys('tarea:*') # Se trae todas las tareas que tiene en su clave la palabra 'tarea' 
        tareas = []
        for key in keys:
            tarea = bdRedis.hgetall(key) # Obtiene todos los campos y valores del hash
            tareas.append(tarea)
        return tareas
    
if __name__ == "__main__":
    while True:
        os.system('cls')
        print(Fore.RED+"****GESTION DE TAREAS CON REDIS***")
        print(Fore.RED+"*********** TO DO LIST ***********")
        print(Fore.RED+"**********************************")
        print(Fore.GREEN+"1. Agregar tarea")
        print(Fore.GREEN+"2. Mostrar todas las tareas")
        print(Fore.GREEN+"3. Mostrar tareas pendientes")
        print(Fore.GREEN+"4. Mostrar tareas completadas")
        print(Fore.GREEN+"5. Marcar tarea como completada")
        print(Fore.GREEN+"6. Eliminar tarea")
        print(Fore.GREEN+"7. Limpiar memoria")
        print(Fore.GREEN+"8. Salir")
        print(Fore.WHITE+"-------------------------")
        opcion = input(Fore.YELLOW+"Selecciona una opción XX: ")

        if opcion == '1':
            tarea = input(Fore.WHITE+"Ingrese la descripción de la tarea: ")
            agregar_tarea(tarea)
        elif opcion == '2':
            os.system('cls')
            tareas_todas = obtener_tareas_todas()
            print(Fore.GREEN+"Lista todas las tareas: Pedientes y Completadas")
            print(Fore.GREEN+"-----------------------------------------------")
            if tareas_todas is None:
                print(Fore.WHITE+" No existe tareas ")
            else:
                for tarea in tareas_todas:
                    print(Fore.WHITE+f"ID: {tarea[b'id'].decode('utf-8')}, Descripción: {tarea[b'descripcion'].decode('utf-8')}, Completada: {tarea[b'completada'].decode('utf-8')}")
            
            print(Fore.WHITE+"-----------------------------------------------")
            capMenu = input(Fore.YELLOW+"Regresar a Menu: ENTER...")    
        elif opcion == '3':
            os.system('cls')
            tareas_pendientes = obtener_tareas_no_completadas()
            print(Fore.GREEN+"Lista de las tareas: Pendientes:")
            print(Fore.GREEN+"-------------------------------")
            for tarea in tareas_pendientes:
                print(Fore.WHITE+f"ID: {tarea['id']}, Descripción: {tarea['descripcion']}, Completada: {tarea['completada']}")
            print(Fore.WHITE+"------------------------")    
            capMenu = input(Fore.YELLOW+"Regresar a Menu: ENTER...")    
        elif opcion == '4':
            os.system('cls')
            tareas_completadas = obtener_tareas_completadas()
            print(Fore.GREEN+"Lista de las tareas: Completadas:")
            print(Fore.GREEN+"---------------------------------")
            for tarea in tareas_completadas:
                print(Fore.WHITE+f"ID: {tarea['id']}, Descripción: {tarea['descripcion']}, Completada: {tarea['completada']}")
            print(Fore.WHITE+"------------------------")
            capMenu = input(Fore.YELLOW+"Regresar a Menu: ENTER...")    
        elif opcion == '5':
            tarea_id = input(Fore.WHITE+"Ingrese el ID de la tarea que desea marcar como completada: ")
            tarea_key = f'tarea:{tarea_id}'
            clave_existe = bdRedis.exists(tarea_key)
            if clave_existe:
                marcar_completada(tarea_id)
            else:
                print(Fore.RED+"No existe esta Clave")
                capMenu = input(Fore.YELLOW+"Regresar a Menu: ENTER...") 
        elif opcion == '6':
            tarea_id = input(Fore.WHITE+"Ingrese el ID de la tarea que desea eliminar: ")
            tarea_key = f'tarea:{tarea_id}'
            clave_existe = bdRedis.exists(tarea_key)
            if clave_existe:
                eliminar_tarea(tarea_id)
            else:
                print(Fore.RED+"No existe esta Clave")
                capMenu = input(Fore.YELLOW+"Regresar a Menu: ENTER...") 
        elif opcion == '7':
            limpiar_memoria()
            print(Fore.WHITE+"La base de datos ha sido limpiada usando FLUSHDB.")
            capMenu = input(Fore.YELLOW+"Regresar a Menu: ENTER...") 
        elif opcion == '8':
            if connection.is_connected():
                connection.close()
                print("MySQL connection se ha cerrado")
            break
        else:
            print(Fore.RED+"Opción no válida. Intenta de nuevo.")