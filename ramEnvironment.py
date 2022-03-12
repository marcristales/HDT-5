from curses import flash
import simpy

CPU_INST = 3
AVAILABLE_CPU = 1
PROCESOS = 50
TIEMPO = 10
UNIDAD = 1
RAM_CAPACITY = 100

def procesos(env, nombre, ramCapacidad, ramNeeded, inst_req, tiempo, velocidad):

    #NEW
    yield env.timeout(tiempo)

    tiempoInicial = env.now
    print("%p necesita %c de RAM" % (nombre, ramNeeded))
    print("Tiempo en ejecucion: %t" % (tiempo))

    #READY
    yield ramCapacidad.get(ramNeeded)
    print("%p utilizando %c de RAM" % (nombre, ramNeeded))

    next_inst = 0
    
    #RUNNING
    while inst_req > inst:
        with cpu.request() as req:
            yield req

            next_inst = inst_req - velocidad

            if (next_inst >= velocidad):

                ejecutado = velocidad
            
            else:

                ejecutado = next_inst

            print("Ejecutando %p - El CPU utiliza %i instrucciones" % (nombre, ejecutado))

            yield env.timeout(ejecutado/velocidad)

            print("Ejecutado %p - Instrucciones utilizadas: (%i/%d)" % (nombre, next_inst, inst_req))


