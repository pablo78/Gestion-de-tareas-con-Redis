import redis
import os

bdRedis = redis.StrictRedis(host='localhost', port=6379, db=0)

## Agregar una tarea a la lista
def agregar_tarea(tarea):
    tarea_id = bdRedis.incr('numID')  # Generar un nuevo ID para la tarea
    tarea_key = f'tarea:{tarea_id}' # Combina la palabra 'tarea' con el numID formado en la linea anterior
    bdRedis.hset(tarea_key, 'id', tarea_id)
    bdRedis.hset(tarea_key, 'descripcion', tarea)
    bdRedis.hset(tarea_key, 'completada', 'False')

## Obtener las tareas de la lista
def obtener_tareas_todas():
    keys = bdRedis.keys('tarea:*') # Se trae todas las tareas que tiene en su clave la palabra 'tarea' 
    tareas = []
    for key in keys:
        tarea = bdRedis.hgetall(key) # Obtiene todos los campos y valores del hash
        tareas.append(tarea)
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

if __name__ == "__main__":
    while True:
        os.system('cls')
        print("****GESTION DE TAREAS CON REDIS***")
        print("*********** TO DO LIST ***********")
        print("**********************************")
        print("1. Agregar tarea")
        print("2. Mostrar todas las tareas")
        print("3. Mostrar tareas pendientes")
        print("4. Mostrar tareas completadas")
        print("5. Marcar tarea como completada")
        print("6. Eliminar tarea")
        print("7. Limpiar memoria")
        print("8. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            tarea = input("Ingrese la descripción de la tarea: ")
            agregar_tarea(tarea)
        elif opcion == '2':
            os.system('cls')
            tareas_todas = obtener_tareas_todas()
            print("Todas las tareas:")
            for tarea in tareas_todas:
                print(f"ID: {tarea[b'id'].decode('utf-8')}, Descripción: {tarea[b'descripcion'].decode('utf-8')}, Completada: {tarea[b'completada'].decode('utf-8')}")
            capMenu = input("Regresar a Menu: ENTER...")    
        elif opcion == '3':
            os.system('cls')
            tareas_pendientes = obtener_tareas_no_completadas()
            print("Tareas pendientes:")
            for tarea in tareas_pendientes:
                print(f"ID: {tarea['id']}, Descripción: {tarea['descripcion']}, Completada: {tarea['completada']}")
            capMenu = input("Regresar a Menu: ENTER...")    
        elif opcion == '4':
            os.system('cls')
            tareas_completadas = obtener_tareas_completadas()
            print("Tareas completadas:")
            for tarea in tareas_completadas:
                print(f"ID: {tarea['id']}, Descripción: {tarea['descripcion']}, Completada: {tarea['completada']}")
            capMenu = input("Regresar a Menu: ENTER...")    
        elif opcion == '5':
            tarea_id = input("Ingrese el ID de la tarea que desea marcar como completada: ")
            marcar_completada(tarea_id)
        elif opcion == '6':
            tarea_id = input("Ingrese el ID de la tarea que desea eliminar: ")
            eliminar_tarea(tarea_id)
        elif opcion == '7':
            limpiar_memoria()
            print("La base de datos ha sido limpiada usando FLUSHDB.")
            capMenu = input("Regresar a Menu: ENTER...") 
        elif opcion == '8':
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
